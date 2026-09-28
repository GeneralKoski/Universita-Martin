# Date e importi: lo stesso valore scritto in formati diversi

**Domanda.** Nelle schede dei 10.018 atti la stessa data compare in tre formati:
`14/01/2026` (3.111 volte, in 1.470 atti), `14 gennaio 2026` (1.814, in 939),
`14.01.2026` (1.592, in 830); gli importi con i punti delle migliaia,
`1.234,56`, 499 volte, e senza, `1234,56`, in altri atti. Nessuno dei due
tokenizer li collega:

- lo **standard** (quello di Elasticsearch e del profilo di Documentale) tiene
  `14.01.2026` e `1.234,56` come un termine solo e spezza `14/01/2026`: chi
  scrive la data in un formato non trova gli atti che la scrivono in un altro;
  e `18` combacia ancora con il giorno delle date con la barra;
- quello di **Koskidex** spezza tutto: barra e punto si trovano fra loro, il
  mese in lettere no, e `18` combacia con il giorno di ogni data.

Riconoscere date e importi e indicizzarli in una forma sola chiude il difetto
senza toccare il resto?

Scritto il 28/09/2026, prima del codice e prima di generare le query. I
conteggi qui sopra vengono da una esplorazione del corpus non archiviata, fatta
per decidere se valeva la pena.

## La correzione

Due impostazioni di Koskidex, spente per default, applicate al testo degli atti
e alle query prima del tokenizer:

- `normalize_dates`: `gg/mm/aaaa` (anche `aa`), `gg.mm.aaaa`, `gg-mm-aaaa` e
  `gg <mese> aaaa` con i mesi in italiano diventano `aaaammgg`, un numero solo,
  che quindi segue le regole dei numeri (refusi e prefisso compresi). Una data
  non valida (mese 13, giorno 32, anno fuori da 1900-2099) resta com'è;
- `normalize_amounts`: in `1.234.567` e `1.234,56` si tolgono i punti delle
  migliaia, e il resto passa al tokenizer come prima.

`scripts/evaluate -date -importi`.

## Le query

Sintetiche, come le known-item automatiche, e dichiarate come tali:
`strumenti/known-item-formati.py`, con un seme fisso.

- **Date**: `<data> <comune>`. Da un atto si prende una data che, in quel
  comune, compare in quell'atto solo (in qualunque formato), e scritta
  nell'atto in un formato solo. Fino a 50 atti per formato di partenza
  (barra, punto, mese), ciascuno con tre query, una per formato: quella nel
  formato dell'atto, copiata com'è, fa da controllo, le altre due misurano il
  difetto.
- **Importi**: `<importo> <comune>`, allo stesso modo, fino a 50 atti per
  formato di partenza (con i punti, senza), due query ciascuno.
- **Guardia**: le 300 known-item automatiche, `<numero> <comune>`.

## Le configurazioni

Koskidex piatto (`scripts/evaluate`, recupero congiuntivo, punteggio
euristico, come in Documentale) con il tokenizer di Koskidex e con lo
standard, ciascuno spento e con tutte e due le impostazioni accese: quattro
configurazioni. Elasticsearch non si misura dall'app: in produzione vuole tutte
le parole nello stesso campo, e il comune non sta nel campo della data, quindi
misurerebbe il difetto del capitolo 6 e non questo. Il tokenizer standard di
Koskidex è il suo, e l'innesto ha mostrato che con le stesse impostazioni i due
motori danno gli stessi insiemi.

Si guardano l'atto primo, l'atto entro i primi dieci, le query a vuoto, per
formato di partenza e formato della query.

## Prima di misurare

1. **Il difetto, tokenizer standard, spento**: le query nel formato dell'atto
   trovano l'atto entro i primi dieci almeno nel 90% dei casi; quelle in un
   altro formato al più nel 10%.
2. **Tokenizer di Koskidex, spento**: fra barra e punto l'atto entro i primi
   dieci almeno nel 90% dei casi, come nel formato dell'atto; con il mese in
   lettere, da una parte o dall'altra, al più nel 10%.
3. **Acceso, tutti e due i tokenizer**: per ogni coppia di formati l'atto
   entro i primi dieci almeno nel 90% dei casi, e l'atto primo nelle query in
   un altro formato entro 5 punti percentuali da quello nel formato dell'atto.
4. **Importi**: spento, con e senza punti non si trovano fra loro (al più il
   10% entro i primi dieci) con nessuno dei due tokenizer; acceso, almeno il
   90%.
5. **La guardia**: sulle known-item automatiche l'MRR@10 acceso differisce da
   quello spento di meno di 0,005, con tutti e due i tokenizer.
6. **Meno falsi positivi**: con il tokenizer di Koskidex, sulle known-item
   automatiche con un numero da 1 a 31, acceso i candidati non aumentano per
   nessuna query e diminuiscono almeno per metà.
7. **Il costo**: l'indicizzazione accesa al più il 20% più lenta di quella
   spenta.
8. **I test** passano, `TestBaselineRankingIsFrozen` senza toccarlo.

## Esito

Da `2026-09-28T110657Z_esito.json` (`analizza.py`), Koskidex `c059664`, 36
valutazioni in `evaluate/` (tre ripetizioni identiche nelle metriche). Le
query: 707, 770 e 653 atti candidati per le date con la barra, il punto e il
mese; 50 estratti per formato, 450 query. Per gli importi 191 candidati con i
punti e **solo 2 senza**: 52 atti e 104 query, e la misura degli importi va di
fatto in un verso solo, dagli atti con i punti alle query senza.

**Date, atto entro i primi dieci**, su 50 query per coppia (formato dell'atto
> formato della query):

| coppia | standard, spento | Koskidex, spento | acceso (tutti e due) |
|---|---|---|---|
| barra > barra | 98% | 98% | 100% |
| barra > punto | **0%** | 94% | 100% |
| barra > mese | **6%** | **6%** | 100% |
| punto > punto | 98% | 98% | 98% |
| punto > barra | **0%** | 94% | 98% |
| punto > mese | **0%** | **0%** | 98% |
| mese > mese | 100% | 100% | 100% |
| mese > barra | **8%** | **8%** | 100% |
| mese > punto | **0%** | **8%** | 100% |

1. **Confermata.** Con il tokenizer standard, quello di Elasticsearch, la data
   nel formato dell'atto trova l'atto nel 98-100% dei casi, in un altro
   formato nello 0-8%: quasi sempre a vuoto (fino a 50 query su 50).
2. **Confermata.** Il tokenizer di Koskidex collega barra e punto (94%), non il
   mese in lettere (0-8%).
3. **Confermata.** Acceso, ogni coppia sta fra il 98% e il 100% entro i primi
   dieci, con tutti e due i tokenizer, e l'atto primo nelle query in un altro
   formato è lo stesso del controllo (100%, 96%, 92% per barra, mese e punto
   di partenza). Due query con il punto perdono il primo posto rispetto allo
   spento: accese, trovano anche un secondo atto che contiene davvero quella
   data (scritta con i trattini) e le parole del comune, pur essendo di un
   altro ente. L'unicità delle query è per ente, non per parole: è un limite
   della famiglia sintetica, non della normalizzazione.
4. **Confermata.** Importi: spento, con e senza punti non si trovano mai (0%
   su 50 e su 2), con nessuno dei due tokenizer; acceso, 100%.
5. **Confermata.** Le known-item automatiche non peggiorano, anzi: MRR@10 da
   0,9750 a 0,9767 con il tokenizer di Koskidex, a 0,9772 con lo standard.
6. **Smentita.** Sulle 12 known-item automatiche con un numero da 1 a 31 i
   candidati non aumentano mai, ma calano solo per 4 (da 76 a 67 in tutto),
   non per metà: il comune nella query restringe già a pochi atti, e fra
   quelli pochi hanno una data con quel giorno.
7. **Smentita.** L'indicizzazione accesa è più lenta del 41-46% (mediana da
   924 a 1.345 ms con il tokenizer di Koskidex, da 998 a 1.411 con lo
   standard), non al più del 20%: le cinque espressioni regolari passano su
   tutto il testo di ogni campo. Si può ridurre senza cambiare un risultato,
   saltando i testi senza cifre e cercando i mesi solo dove compare il nome
   di un mese.
8. **Confermata** (`go test ./...` a `c059664`).

**Cosa ne segue.** Per Documentale è un difetto di produzione nuovo: con il
tokenizer standard di Elasticsearch una data scritta in un formato diverso da
quello dell'atto non trova quasi mai l'atto, e nel corpus i formati sono tre,
tutti frequenti. Le due impostazioni lo chiudono con tutti e due i tokenizer,
senza toccare le ricerche per numero. Le query sono sintetiche: dicono che il
motore trova la data in qualunque formato, non quanto spesso una persona
cerca per data (nelle known-item umane raccolte finora, quasi mai).
