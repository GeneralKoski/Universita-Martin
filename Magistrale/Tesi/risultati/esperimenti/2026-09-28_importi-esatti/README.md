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

## Esito

Misurato il 28/09/2026 con Koskidex `98701ad` e Documentale `dad69da`.
Riassunto in `2026-09-28T115249Z_esito.json` (`analizza.py`); valutazioni in
`evaluate/`, rapporti dell'app e tempi di indicizzazione in `confronto/`
(`*importi-esatti*`; quelli delle known-item umane fuori da git). Le
impostazioni lette dall'indice dopo ogni riempimento corrispondono alle
quattro configurazioni. Una prima esecuzione di `analizza.py` si è fermata
su un errore (le query senza risultati non hanno la lista `top`) prima di
archiviare; corretto e committato, poi rieseguito sulle stesse misure.

**Sette previsioni su otto**, e la smentita è nel verso buono.

| | A profilo | B + importi normalizzati | C + importi esatti | D + tutti e due |
|---|---|---|---|---|
| importi fra formati, entro i primi dieci | 52/52 | 52/52 | 0/52 | **52/52** |
| MRR@10 importi | 0,917 | 0,891 | 0,495 | **0,990** |
| risultati sulle 104 query degli importi | 175 | 218 | 53 | 106 |
| MRR@10 date | 0,315 | 0,315 | 0,333 | 0,333 |
| MRR@10 known-item automatiche | 0,950 | 0,950 | 0,950 | 0,950 |
| MRR@10 known-item umane (76) | 0,499 | 0,499 | 0,499 | 0,499 |

1. **Confermata.** In C gli importi fra formati non si trovano più (0 su 52,
   in A 52): il ponte era il refuso.
2. **Confermata.** In D fra formati 52 su 52 e MRR@10 degli importi 0,990,
   da 0,917.
3. **Confermata.** Risultati sulle query degli importi da 175 a 106, -39%:
   sono gli atti con un importo diverso di una o due cifre.
4. **Smentita, nel verso buono.** MRR@10 delle date da 0,315 a 0,333, +0,018,
   fuori dalla soglia di 0,01. Cambiano 14 query, tutte date col punto cercate
   col punto, tutte in meglio: `14.01.2026` è un termine con i punti, e prima
   ammetteva refusi, quindi trovava anche `14.01.2025` o `04.01.2026`. I
   risultati sulle 450 query delle date scendono da 594 a 241.
5. **Confermata.** Known-item automatiche identiche ad A in 300 query su 300.
6. **Confermata.** Known-item umane identiche ad A in C e in D, 76 su 76.
   *Aggiunto il 29/09/2026:* la ragione scritta nella previsione era
   sbagliata. Tre query su 76 hanno una cifra
   (`corpus/2026-09-28T124257Z_conteggi.json`, `con_una_cifra`); nessuna ha
   un importo o una data (`con_importo` e `con_data` a 0), ed è per questo che
   C e D non le toccano.
7. **Confermata.** Le 21 del confronto senza cifre identiche in tutte e
   quattro; le tre con cifre danno 0, 1 e 1 risultati in tutte e quattro.
8. **Confermata.** I test di Koskidex passano (`go test ./...` a `98701ad`,
   `TestBaselineRankingIsFrozen` senza toccarlo); il test nuovo di
   `KoskidexServiceTest` fallisce prima della modifica e passa dopo, e la
   suite di Documentale passa tranne il 404 di `ExampleTest`, che c'era già.

**Cosa ne segue.** Il difetto è quello del numero d'atto su un'altra forma di
numero, e la correzione è la stessa: niente refusi su ciò che è un numero. Da
sola toglie il ponte fra formati che il refuso dava per caso; insieme alla
normalizzazione degli importi dà l'importo giusto in qualunque formato e solo
quello. Dove la normalizzazione degli importi, da sola, peggiorava (B), con
gli importi esatti migliora. Per il profilo consigliato la coppia
`KOSKIDEX_TYPOS_ON_AMOUNTS=false` e `KOSKIDEX_NORMALIZE_AMOUNTS=true` non
tocca le known-item automatiche, le umane raccolte finora e le 24 senza
cifre; entrerà nel profilo insieme alla decisione sulle date, dopo le
known-item umane complete, con la misura del profilo come un tutto.
