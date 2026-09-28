# Gli importi che ammettono refusi

**Domanda.** `2026-09-28_date-app` ha trovato che nell'app, con la tolleranza
AUTO, `5056,03` combacia con `5.056,03`: il tokenizer standard tiene l'importo
come un termine solo, un carattere di differenza è un refuso ammesso, e
`disable_on_numbers` non lo ferma perché un termine con la virgola non è fatto
di sole cifre. Così gli importi si trovano fra formati, ma combaciano anche
importi diversi di una o due cifre, e togliere i punti peggiora le cose (MRR@10
degli importi da 0,917 a 0,891). È lo stesso difetto del numero d'atto
(sezione 6.1) su un'altra forma di numero. Negare i refusi anche agli importi,
e insieme toglierne i punti, dà solo l'importo giusto?

Scritto il 28/09/2026, prima del codice.

## La correzione

Un campo nuovo di `TypoSettings` in Koskidex, `disable_on_amounts`, spento per
default: nega i refusi a un termine della query fatto solo di cifre, punti e
virgole, che comincia e finisce con una cifra e contiene almeno un punto o una
virgola (`1.234,56`, `5056,03`, `3,5`, e anche la data `14.01.2026`). Le sole
cifre restano a `disable_on_numbers`. In Documentale una variabile,
`KOSKIDEX_TYPOS_ON_AMOUNTS`, accesa per default come in produzione e fuori dal
profilo: spenta, l'indice dei documenti riceve `disable_on_amounts`.

## Come si misura

Come `2026-09-28_date-app`, dall'app con `KOSKIDEX_PROFILO=consigliata`, in
quattro configurazioni: **A** il profilo; **B** più `normalize_amounts`; **C**
più `disable_on_amounts`; **D** più tutti e due. Per ciascuna, un indice vuoto
riempito dall'app, poi le known-item degli importi, delle date e automatiche,
le known-item umane raccolte fin qui e le 24 del confronto; `scripts/evaluate
-rankings -top 10` sulle quattro con i giudizi. Koskidex piatto non serve:
`scripts/evaluate` cerca senza refusi, e lì il difetto non c'è.

## Prima di misurare

1. **Il ponte era il refuso**: in C gli importi fra formati trovano l'atto
   entro i primi dieci al più nel 10% dei casi (in A il 100%).
2. **Tutti e due**: in D gli importi fra formati almeno nel 90%, e l'MRR@10
   degli importi almeno 0,95 (A 0,917, B 0,891).
3. **Meno importi sbagliati**: sulle query degli importi, il totale dei
   risultati in D almeno il 20% sotto quello di A.
4. **Le date**, senza normalizzazione come nel profilo: in C l'MRR@10 delle
   known-item delle date entro 0,01 da A (le date col punto perdono i refusi).
5. **Known-item automatiche**: C identica ad A query per query (i numeri di
   quelle query sono sole cifre, già esatti nel profilo).
6. **Known-item umane raccolte finora**: C e D identiche ad A query per query
   (nessuna contiene cifre).
7. **Le 24 del confronto**: le 21 senza cifre danno gli stessi risultati,
   nello stesso ordine, in tutte e quattro.
8. **I test** di Koskidex, `TestBaselineRankingIsFrozen` senza toccarlo, e di
   Documentale passano.
