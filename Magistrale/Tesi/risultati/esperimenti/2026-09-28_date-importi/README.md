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
