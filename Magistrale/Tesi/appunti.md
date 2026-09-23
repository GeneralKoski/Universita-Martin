# Tesi magistrale - appunti

Raccolta di appunti sulla scelta dell'argomento di tesi. Non è ancora un
progetto: è il diario delle idee valutate e del perché sono state tenute o
scartate.

## Criterio di scelta

Una tesi magistrale non ha bisogno di software che funziona, ha bisogno di:

1. una **domanda** precisa,
2. un **metodo** per rispondere,
3. una **valutazione misurabile** del risultato.

Un progetto grande e ben fatto ma senza domanda resta una tesi progettuale.
Ogni candidato qui sotto è giudicato con questo metro.

## Contesto voto

Dal `CLAUDE.md` del repo: partenza ~102,66 + 3 (in corso) = 105,66. Servono
**4 punti tesi per il 110**, 7 per la lode. Quindi la tesi pesa, e una tesi con
misure e un contributo difendibile vale più di una tesi applicativa.

## Candidati valutati (15 settembre 2026)

Passati in rassegna tutti i repo personali sull'account GitHub `GeneralKoski`.

### Traccia aperta: Koskidex

Motore di ricerca full-text self-hosted scritto in Go (2.850 righe di codice
più 2.060 di test), binario
singolo senza dipendenze a runtime. Ha già tolleranza ai refusi, faccette e
ricerca vettoriale.

L'ingegneria c'è. Manca tutta la parte che lo rende una tesi:

- valutazione IR su dataset standard (BEIR, MS MARCO)
- curve **recall@k contro latenza**, non solo "è veloce"
- confronto con Meilisearch / Tantivy / Elasticsearch
- studio della **fusione lessicale + densa**: RRF contro pesatura, dove il
  vettoriale aiuta davvero e dove peggiora i risultati

Quest'ultimo punto è il candidato più forte a diventare *la* domanda di tesi.

### Parcheggiato: gpu-quant-bench

Benchmark di formati e quantizzazioni di un modello 7B su una RTX 3060 (12 GB):
FP16, GGUF Q8_0/Q5_K_M/Q4_K_M, GPTQ 4-bit, AWQ 4-bit, su contesti da 512, 2048
e 8192 token.

È l'unico repo nato già in forma di studio sperimentale, con domanda, variabili
controllate e metriche definite (throughput, TTFT, prefill, VRAM di picco,
perplexity). Il contributo metodologico interessante è riportare **varianza** e
**throttling termico**, che i benchmark pubblicati quasi sempre omettono.

**Non è la tesi.** È lo step 1 di un percorso di studio ML più lungo, descritto
nel repo `ml-notes`. Se in futuro dovesse servire come base di tesi, le
direzioni per irrobustirlo sono: più modelli, una seconda GPU per generalizzare,
valutazione di qualità oltre la perplexity (task downstream, non solo control
prompt letti a mano) e analisi energetica (J/token), che oggi manca ed è
l'angolo più facile da difendere.

### Scartati

| Progetto | Motivo |
|---|---|
| sudoku-instance-generation / Constraint_Programming | Esame del primo anno, già valutato. Fuori discussione. |
| MelaGolfo | Scartato. |
| KalTrack, unidesk, unidesk-mobile, Hydran, PiacenzAdvisor, PizzaGigante, Klipski, Chesso, Automarket, metin, Personal-website | Scartati: product engineering, integrazione o esercizi, nessuna domanda di ricerca. |

## Decisione presa (15 settembre 2026), confermata il 23 settembre

**Tesi su Koskidex innestato in Documentale.** Il piano operativo sta in
[piano-implementazione.md](piano-implementazione.md).

La domanda non è "integro il mio motore nel gestionale", che sarebbe lavoro di
integrazione senza contributo. È che il recupero di Koskidex ha quattro difetti
precisi, verificati leggendo il codice e poi **misurati** (23/09/2026):

0. **Il recupero è congiuntivo.** `ParseQuery` in `ranker.go:33` mette ogni
   parola in `MustTerms`: un documento deve contenere **tutti** i termini della
   query. Lucene è disgiuntivo con punteggio, e un documento che ne prende 8 su
   12 si piazza bene. Misurato sulla collezione pubblica SciFact: **290 query su
   300 tornano completamente vuote**, nDCG@10 a 0,0246 contro un riferimento
   BM25 di 0,6789. Non è un bug: l'AND è ragionevole per la barra di ricerca di
   un e-commerce, per cui Koskidex era nato. Ma è il difetto che **viene prima
   degli altri tre**, perché su query vuote nessun miglioramento del punteggio
   può fare niente, ed è il più rilevante per un documentale, dove le query sono
   in lingua naturale e sempre più spesso riscritte da un LLM. Dettagli e prove
   in `Koskidex/eval/DIARIO.md`.
1. **Nessun IDF.** Il punteggio è `(10 - refusi + 2*esatti) * peso_campo`. Il
   campo `Posting.TF` esiste in `internal/engine/inverted.go:12` con scritto
   `// term frequency (calculated later)` e non è usato da nessuna parte. Un
   termine rarissimo e uno comunissimo pesano identico.
2. **L'ibrido non è ibrido.** In `ranker.go:203-222` il punteggio vettoriale si
   somma solo ai documenti già trovati dal lessicale: è re-ranking. Un documento
   semanticamente pertinente che il lessicale non pesca non entra mai.
3. **La fusione somma scale incomparabili.** `m.Score += sim * 20.0`, dove il
   lessicale cresce senza limite con la lunghezza della query e il vettoriale è
   fisso a 20. Su una parola il vettore domina, su cinque è rumore.

Ognuno è un capitolo con un risultato numerico, e il baseline è il codice di
oggi, congelato in un test e misurato: SciFact 0,0246 e NFCorpus 0,1659 di
nDCG@10. Documentale fornisce il corpus e il carico di query reale.

**Il difetto 0 è stato trovato misurando, non leggendo il codice**, ed è la
dimostrazione che costruire l'impianto di valutazione prima di toccare il
ranking era la scelta giusta: la tesi stava per essere scritta su tre capitoli
di ottimizzazione del punteggio, su un motore che nel 97% dei casi non
restituiva niente da ottimizzare.

Tre cose in una tesi sola: progetto personale (Koskidex), progetto aziendale
(Documentale), e il contributo di Martin documentato dai commit.

**Fuori dal perimetro:** `rustann` e gli indici approssimati. La forza bruta
regge il volume di un documentale aziendale, quindi sarebbe una domanda di
ricerca senza un bisogno reale.

**Il vincolo che decide tutto:** non esistono dati di produzione, solo uno
staging. Quindi i giudizi di rilevanza si scrivono a mano *prima* di guardare
cosa risponde il motore. Seedare va bene per misurare latenza e memoria, mai
per misurare la rilevanza: sarebbe circolare.

## Relatore: stato e tempi

Il 21 settembre 2026 ho agganciato entrambi i potenziali relatori a fine
lezione, come da [lunedi-21-settembre.md](lunedi-21-settembre.md): **Dal Palù**
(Programmazione Dichiarativa) e **Bonnici** (Algoritmi per l'IA e Laboratorio
di IA). Nessuno dei due discorsi ha chiuso l'argomento, ed era previsto così:
l'obiettivo di quel giorno era aprire un canale, non ottenere un sì.

**La riproposta vera va a dicembre 2026**, per due motivi che si incastrano:

1. **A dicembre ho i progetti dei loro esami.** Laboratorio di IA si esamina con
   un progetto da presentare, Programmazione Dichiarativa con un progetto più
   orale. Arrivare con un lavoro consegnato e valutato da loro vale molto più di
   un discorso in corridoio: è la differenza fra dire "so fare questa cosa" e
   averla già fatta sotto il loro giudizio.
2. **Le tracce di tesi escono verso gennaio.** Presentarsi a dicembre significa
   essere già nella loro testa quando decidono a chi assegnare cosa, invece di
   arrivare quando la lista è già distribuita.

**La leva da non sprecare:** il progetto di Laboratorio di IA deve applicare i
concetti del laboratorio più qualcosa dalla teoria di Algoritmi. Se lo si sceglie
su un terreno vicino al recupero dell'informazione e alla valutazione del
ranking, diventa allo stesso tempo l'esame e la dimostrazione da portare a
Bonnici. Un progetto solo, due scopi. Da valutare quando Bonnici assegna i temi,
senza forzare: se il tema è lontano, si fa il progetto e basta.

Nel frattempo la tesi non parte comunque. Il vincolo resta quello scritto nel
foglio del 21: sette esami da chiudere, la tesi entra nel vivo da febbraio o
marzo 2027 per arrivare a settembre 2027.

## Prossimi passi

Il lavoro tecnico di questi mesi sta in [piano-autunno-2026.md](piano-autunno-2026.md).
**Le correzioni al ranking si fanno prima della tesi** (deciso il 23/09/2026), a tre
condizioni: baseline congelato in un test, ogni modifica dietro un flag di `Settings`
con default sul comportamento attuale, e ogni modifica annotata in `eval/DIARIO.md`
con l'ipotesi scritta *prima* di misurare. Il motivo è il tempo: da febbraio a luglio
2027 ci sono cinque mesi di sere, e arrivarci con il codice già scritto lascia liberi
misurazione e scrittura, che sono le parti che non si comprimono.

**Entro dicembre 2026**

- [ ] Scegliere il progetto di Laboratorio di IA guardando anche se può fare da
      dimostrazione per Bonnici
- [ ] Riproporre la tesi a Bonnici e Dal Palù a progetti consegnati
- [ ] Chiedere all'azienda cosa è pubblicabile di Documentale (non dipende dai
      professori, si può fare prima)

**Da gennaio 2027, quando escono le tracce**

- [ ] Verificare se fra le tracce ufficiali c'è qualcosa che assorbe o sostituisce
      la proposta su Koskidex
- [ ] Chiudere sul relatore

**Prima di annotare qualsiasi cosa**

- [ ] Scegliere la collezione pubblica per validare BM25
- [ ] Sentire il relatore prima di iniziare ad annotare il corpus di dominio
- [ ] Chiedere se si può usare in gran parte una collezione pubblica e costruire
      a mano solo una piccola parte di dominio: è il costo nascosto del piano
      Koskidex, settimane di sere che non sono codice

## Nota organizzativa

La tesi sta **tutta qui dentro**, in `Magistrale/Tesi/`: appunti ora, e più
avanti anche il codice e la scrittura. Niente repo separata e niente repo
annidata (git non gestisce le repo dentro le repo). `Universita-Martin` è il
percorso universitario nella sua interezza, e la tesi ne fa parte.
