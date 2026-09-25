# Il costo dei vettori: convertirli una volta sola

**Domanda.** In Documentale la ricerca col re-ranking vettoriale passa da 8,7 a
33 ms di mediana sulle 24 query (piano, sezione 5, vettori dall'app). Una parte
è il vettore della query, che Ollama calcola a ogni ricerca. L'altra è nel
motore: i vettori arrivati via HTTP o ricaricati dallo snapshot sono
`[]interface{}`, come li decodificano JSON e gob, e `toFloat64Array` li
ricopia in un `[]float64` nuovo **per ogni documento a ogni ricerca**, due
volte con l'unione (re-ranking dei candidati lessicali e scansione dei vicini).
In `scripts/evaluate` i vettori sono già `[]float64` e il costo non si vede.

Quanto costa quella conversione, in tempo, allocazioni e memoria, e quanto se
ne recupera convertendo `_vector` una volta sola all'aggiunta del documento?

## La modifica

- `addDocumentLocked` converte `_vector` in `[]float64` e lo rimette nel
  documento. Ogni percorso passa di lì: HTTP, WAL, snapshot, `Reindex`.
- Lo snapshot gob registra `[]float64`; gli snapshot vecchi, con
  `[]interface{}`, si ricaricano e vengono convertiti all'aggiunta.
- Nessun flag: i valori sono gli stessi float64, i punteggi e l'ordine non
  cambiano. Un test lo controlla: stessi punteggi, al bit, con i vettori dati
  come `[]interface{}` e come `[]float64`, in re-ranking, unione, RRF e
  convessa. `TestBaselineRankingIsFrozen` non è toccato.

## Come si misura

Un benchmark nel motore, `BenchmarkRicercaIbrida`: 10.000 documenti con testo
breve e vettori a 1.024 dimensioni (quelle di `bge-m3`), normalizzati, da un
generatore con seme fisso, dati al motore come `[]interface{}`, cioè come
arrivano via HTTP. La query lessicale trova tutti i documenti, il caso di
SciFact con `any`. Due varianti: re-ranking (default) e unione con i 100 più
vicini. Si registrano ns/op, B/op, allocazioni per ricerca e la memoria viva
dopo il caricamento (heap dopo un GC, in MB). Si esegue sul commit prima della
modifica e su quello dopo, stessa macchina, `-count 5`, e si confrontano le
mediane.

## Prima di misurare

Scritto e committato prima del codice.

1. **Allocazioni**: per ricerca scendono di almeno il 90% in tutte e due le
   varianti. Oggi ogni ricerca alloca un `[]float64` da 8 KB per documento
   per percorso: 80 MB col re-ranking, 160 con l'unione.
2. **Tempo**: la ricerca con l'unione diventa almeno tre volte più veloce, col
   re-ranking almeno due. Il prodotto scalare su 1.024 valori costa meno della
   copia con asserzione di tipo e dell'allocazione.
3. **Memoria viva**: scende di almeno il 60%. Un `[]interface{}` di float64
   costa 24 byte a valore (16 dell'interfaccia, 8 del valore sul heap), un
   `[]float64` 8.
4. **Documentale**: non si rimisura qui. Il guadagno atteso sulle 24 query è la
   parte del motore dei 24 ms in più; il vettore della query resta.

## Esito

Prima `2026-09-25T134455Z_prima-48d714b.txt` (Koskidex `48d714b`, il benchmark
senza la modifica), dopo `2026-09-25T134620Z_dopo-8260289.txt` (`8260289`),
tutti e due su albero pulito, Apple M2, Go 1.27.1, cinque esecuzioni da 20
ricerche; mediane:

| | prima | dopo | rapporto |
|---|---|---|---|
| re-ranking, ms per ricerca | 57,6 | 24,7 | 2,33× |
| unione, ms per ricerca | 102,6 | 42,7 | 2,40× |
| re-ranking, MB allocati per ricerca | 95,1 | 13,2 | -86% |
| unione, MB allocati per ricerca | 177,3 | 13,5 | -92% |
| re-ranking, allocazioni per ricerca | 110.515 | 100.515 | -9% |
| unione, allocazioni per ricerca | 120.519 | 100.519 | -17% |
| heap vivo dopo il caricamento, MB | 270,5 | 94,7 | -65% |

**La ricerca con vettori costa meno della metà, e l'indice un terzo della
memoria.** Le 10.000 e 20.000 allocazioni che spariscono sono esattamente i
`[]float64` ricopiati, uno per documento per percorso; le altre 100.000 sono
della parte lessicale, che trova tutti i 10.000 documenti. Il profilo della
ricerca con l'unione dopo la modifica
(`2026-09-25T134651Z_profilo-union-8260289.txt`) dice dove sta il resto: il 69%
del tempo di ricerca è `cosineSimilarity`, che per ogni documento ricalcola
anche le due norme.

Preparando il benchmark è venuto fuori un difetto diverso: senza campi
dichiarati Koskidex indicizzava `_vector` come testo, un termine per valore, e
10.000 documenti non finivano di caricarsi in dieci minuti. Era una mia
regressione del 24/09 (i campi lista); corretta a parte in `d3fe995`, non
toccava nessun numero misurato, perché `scripts/evaluate` e Documentale
dichiarano i campi.

### Le previsioni

1. Allocazioni per ricerca giù di almeno il 90%: **smentita.** In numero
   scendono del 9% e del 17%, in byte dell'86% e del 92%. Contavo solo le
   copie dei vettori e dimenticavo che la parte lessicale, su una query che
   trova tutto, alloca da sola 100.000 oggetti piccoli.
2. Unione almeno tre volte più veloce, re-ranking almeno due: **smentita a
   metà**, 2,40× e 2,33×. Sottovalutavo il prodotto scalare: resta il grosso
   del tempo.
3. Memoria viva giù di almeno il 60%: **-65%, confermata.** Da 24 a 8 byte a
   valore darebbe -67% sui soli vettori; il resto è l'indice lessicale.
4. Documentale non rimisurato qui.

### Cosa vuol dire per la tesi

Per 7.4: la scansione esatta costa O(n·d), e a 10.000 documenti da 1.024
dimensioni vale circa 25 ms col re-ranking e 43 con l'unione su un M2, due
terzi dei quali nel calcolo della similarità. Il prossimo passo ovvio sono le
norme dei documenti calcolate una volta sola (`bge-m3` li dà già normalizzati,
ma il motore non può saperlo), che lascerebbe il solo prodotto scalare.

