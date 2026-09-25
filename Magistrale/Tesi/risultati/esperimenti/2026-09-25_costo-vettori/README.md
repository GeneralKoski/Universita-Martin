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
