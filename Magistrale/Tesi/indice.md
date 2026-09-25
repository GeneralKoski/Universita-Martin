# Indice della tesi

Proposta del 25/09/2026, da portare al relatore prima di scrivere. È lo stesso
indice dei capitoli in `latex/capitoli/`, che compilano già un sommario vero.
Accanto a ogni sezione: a che punto è e dove sta il materiale.

**Stato:** ✅ misurato, il materiale c'è · 🔶 in corso o in parte · ⬜ da fare

## Titolo, tre proposte

1. *Ritrovare un atto: difetti di recupero di un motore di ricerca leggero,
   misurati in un sistema documentale*
2. *Dal motore alla produzione: valutazione e correzione del recupero di un
   motore di ricerca senza dipendenze in un documentale*
3. *Koskidex in Documentale: cosa costa, in pertinenza, un motore di ricerca
   piccolo*

## La tesi in una frase

Un motore di ricerca piccolo e senza dipendenze (Koskidex), messo al posto di
Elasticsearch in un sistema documentale (Documentale), ha difetti di recupero
precisi: la tesi li trova misurando, li corregge uno alla volta dietro un
interruttore, e dice con numeri riproducibili quanto costava ciascuno, contro il
codice di partenza e contro Elasticsearch di produzione.

## Capitoli

### 1. Introduzione ⬜
1.1 Ritrovare un atto in un documentale
1.2 Koskidex e Documentale
1.3 La domanda di ricerca
1.4 Contributi
1.5 Il metodo: ipotesi prima della misura
1.6 Struttura della tesi

*Contributi da elencare:* un impianto di valutazione riproducibile; quattro
difetti del motore e tre della ricerca in produzione, ciascuno misurato; un
corpus pubblico di dominio con query known-item; la scelta della configurazione
per tipo di query.

### 2. Fondamenti e lavori correlati ⬜
2.1 Indice invertito e recupero booleano, congiuntivo e disgiuntivo
2.2 Modelli di punteggio: dall'euristico a BM25
2.3 Espansioni: prefisso, refusi e frequenza mescolata
2.4 Analisi lessicale: tokenizzazione, stopword, stemming, elisioni
2.5 Recupero denso e ibrido, fusione dei punteggi
2.6 Valutazione: paradigma di Cranfield, pooling, metriche, known-item, accordo fra annotatori
2.7 Lavori correlati: BEIR, Lucene ed Elasticsearch, Meilisearch, predizione e scelta per query

### 3. I sistemi e l'innesto ✅
3.1 Koskidex: com'era il 23/09/2026
3.2 Documentale: come cerca in produzione
3.3 L'innesto: un contratto, due motori, gli stessi risultati
3.4 Le differenze di matching trovate per arrivarci
3.5 Prestazioni dell'innesto

*Materiale:* `risultati/esperimenti/2026-09-23_cause-divergenza/`,
`2026-09-25_innesto-parita/` (24/24 e 300/300 insiemi uguali, ricerca 2,7 ms
contro 22, il `fsync` per documento).

### 4. L'impianto di valutazione 🔶
4.1 Principi: ipotesi prima, interruttori, baseline congelato, archivio con provenienza
4.2 Le collezioni pubbliche: SciFact e NFCorpus
4.3 Il corpus di dominio: gli albi pretori
4.4 Le query: known-item automatiche, known-item umane, bisogni aperti
4.5 Giudizi e accordo fra annotatori
4.6 Gli strumenti

*Materiale:* `risultati/README.md`, `istruzioni-annotazione.md`,
`eval/corpora/c3-albo/SOURCE.md` di Koskidex. *Manca:* le known-item umane, i
giudizi del pool e il kappa (`da-fare-a-mano.md`).

### 5. Il recupero lessicale 🔶
5.1 Difetto 0: il recupero congiuntivo ✅
5.2 Difetto 1: niente IDF, e BM25 ✅
5.3 Le espansioni pesate con il termine trovato ✅
5.4 Le stopword: un guadagno che veniva da altrove ✅
5.5 Identificativi e lingua naturale: nessuna impostazione unica ✅
5.6 Analisi lessicale italiana ⬜
5.7 Scheda contro testo intero, e la lunghezza dei documenti ⬜

*Materiale:* `eval/DIARIO.md` di Koskidex; `risultati/esperimenti/`
`2026-09-25_bm25-numeri/`, `_stopword-espansioni/`, `_known-item-divario/`,
`_recupero-intermedio/`. *Manca:* 5.6 e 5.7 aspettano le known-item umane.

### 6. La ricerca in produzione: tre difetti di Documentale ✅
6.1 Il numero d'atto
6.2 Le elisioni
6.3 Numero e comune: il campo unico e i refusi sui numeri
6.4 Cosa cambia per chi cerca

*Materiale:* `2026-09-23_numero-atto/` (`ordinanza 187` al 12° posto),
`2026-09-25_elisioni/` (40,3% degli atti), `_known-item-auto/`,
`_koskidex-campi-liberi/`, `_refusi-numeri/` (dal 2% entro dieci al 92% primo).

### 7. Recupero ibrido e fusione ⬜
7.1 Gli embedding e la suddivisione dei documenti lunghi
7.2 Difetto 2: dal re-ranking al recupero ibrido
7.3 Difetto 3: fondere scale incomparabili
7.4 Il costo: scansione dei vettori, latenza, memoria
7.5 Scegliere la configurazione per tipo di query 🔶

*Materiale:* 7.5 ha già `2026-09-25_scelta-per-query/` (il classificatore a
0,0006 dall'oracolo, e una regola a due condizioni che fa lo stesso). *Manca:*
la decisione sugli embedding (`da-fare-a-mano.md`), poi tutto il resto.

### 8. Il confronto finale con Elasticsearch ⬜
8.1 Le configurazioni a confronto
8.2 Pertinenza, per famiglia di query e per fonte
8.3 Latenza, memoria, dimensione dell'indice
8.4 Dove un motore piccolo è competitivo, e dove no

### 9. Conclusioni ⬜
9.1 Le risposte alla domanda
9.2 Limiti
9.3 Sviluppi futuri

*Limiti già noti da scrivere:* query fabbricate, un solo corpus di dominio, pochi
annotatori, tipi di query separati per collezione, recall del pool come limite
superiore.

### Appendici
A. Come rifare ogni numero: comandi, commit, archivio ✅
B. Istruzioni di annotazione ✅
C. Registro delle ipotesi: ogni previsione scritta prima della misura, con l'esito 🔶
D. Le impostazioni aggiunte a Koskidex ✅

L'appendice C è il punto di forza da mostrare al relatore: al 25/09/2026 ogni
esperimento ha le sue previsioni committate prima dei numeri, e molte sono
state smentite. È la risposta alla domanda che arriva sempre in discussione,
"le metriche le hai scelte dopo aver visto i risultati?".
