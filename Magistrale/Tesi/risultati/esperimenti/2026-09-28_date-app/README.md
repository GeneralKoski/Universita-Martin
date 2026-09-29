# Date e importi dall'app

**Domanda.** `2026-09-28_date-importi` ha misurato `normalize_dates` e
`normalize_amounts` con Koskidex piatto: una data scritta in un formato diverso
da quello dell'atto passa da 0-8% a 98-100% di atti entro i primi dieci, e le
known-item automatiche non peggiorano. Documentale non le espone ancora. Dentro
l'app, con il profilo consigliato, danno la stessa cosa? E quanto costano, sulle
query che non cercano una data?

Scritto il 28/09/2026, prima di toccare il codice di Documentale.

## La modifica in Documentale

Due variabili, `KOSKIDEX_NORMALIZE_DATES` e `KOSKIDEX_NORMALIZE_AMOUNTS`,
spente per default e **fuori dal profilo consigliato**: le known-item umane
della sera del 28/09 girano con il profilo com'è. Accese, l'indice dei
documenti riceve `normalize_dates` e `normalize_amounts`; quello delle
cartelle no (cerca nei percorsi, dove le date non ci sono). Un test di
`KoskidexServiceTest`, che fallisce prima della modifica.

## Il prezzo che si cerca

Con le date normalizzate l'anno di una data non è più un termine a sé:
`14/01/2026` diventa `20260114`, e `2026` da solo non ci combacia (nel profilo
i numeri combaciano esattamente e il prefisso è spento). Una query come
"bilancio 2026", con il recupero congiuntivo, perde gli atti in cui l'anno
compare solo dentro una data. Quanto pesa si vede solo sulle query vere: delle
76 known-item umane raccolte finora nessuna contiene un anno, una data o un
importo (conteggio con un'espressione regolare, non archiviato); delle 24 del
confronto una sola contiene un anno; delle 300 known-item automatiche 30
contengono un numero fra 1900 e 2099, che lì è un numero di registro.

## Come si misura

Koskidex del commit corrente, un indice vuoto riempito dall'app due volte con
`KOSKIDEX_PROFILO=consigliata`: una senza altre variabili, una con le due
accese. Ogni volta si registra il tempo di indicizzazione
(`strumenti/indicizza-koskidex.sh`) e si eseguono dall'app
(`app:eval-run-queries`) le known-item automatiche, le date e gli importi
sintetici di `2026-09-28_date-importi`, le known-item umane raccolte fin qui e
le 24 del confronto; le prime quattro si valutano con `scripts/evaluate
-rankings -top 10`, delle 24 si confrontano i risultati.

## Prima di misurare

1. **Il difetto, spento**: le date in un formato diverso da quello dell'atto
   trovano l'atto entro i primi dieci al più nel 10% dei casi, come il
   tokenizer standard piatto; nel formato dell'atto almeno nel 90%.
2. **Accese, date**: per ogni coppia di formati l'atto entro i primi dieci
   almeno nel 90% dei casi.
3. **Accese, importi**: dagli atti con i punti alle query senza, e
   viceversa, almeno il 90% entro i primi dieci; spente al più il 10%.
4. **Known-item automatiche**: MRR@10 acceso entro 0,005 da spento.
5. **Known-item umane raccolte finora**: nessuna contiene cifre, quindi
   nessuna perde o guadagna l'atto cercato entro i primi dieci; l'ordine può
   spostarsi di poco, perché le date normalizzate cambiano la lunghezza dei
   campi (`14/01/2026` da tre termini a uno), e l'MRR@10 cambia di meno di
   0,01.
6. **Le 24 del confronto**: le 21 senza cifre trovano gli stessi atti (il
   numero di risultati non cambia; l'ordine può, per le lunghezze); di quella
   con l'anno i risultati possono solo diminuire (l'anno dentro le date non
   combacia più), non aumentare.
7. **Il costo dall'app**: l'indicizzazione accesa al più il 10% più lenta
   (il +29% di Koskidex piatto pesa poco dentro un'indicizzazione dominata
   dall'app e dal database).
8. **I test di Documentale** passano.

## Esito

Misurato il 28/09/2026 con Koskidex `3bff7ca` e Documentale `f921ef7`.
Riassunto in `2026-09-28T114447Z_esito.json` (`analizza.py`); le valutazioni
in `evaluate/`, i rapporti dell'app e i tempi di indicizzazione in
`confronto/` (`*date-app*`; quello delle known-item umane resta fuori da git
perché contiene le query). Le impostazioni lette dall'indice: spento senza
`normalize_*`, acceso con tutte e due, il resto uguale.

**Sei previsioni su otto** (le prime sette in `analizza.py`, l'ottava a mano). Le due smentite dicono una cosa che Koskidex
piatto non poteva mostrare, perché `scripts/evaluate` cerca senza refusi e
l'app con i refusi AUTO.

1. **Confermata.** Spento, la data nel formato dell'atto trova l'atto entro i
   primi dieci nel 98-100% dei casi, in un altro formato nello 0-8%: come
   Koskidex piatto con il tokenizer standard.
2. **Confermata.** Acceso, ogni coppia di formati fra il 98% e il 100%. MRR@10
   delle date da 0,315 a 0,979.
3. **Smentita, per metà.** Acceso gli importi si trovano fra formati nel 100%
   dei casi, ma anche spento: 50 su 50 e 2 su 2. Nell'app `5056,03` trova
   `5.056,03` per i refusi: il tokenizer standard tiene l'importo come un
   termine solo, un carattere di differenza è un refuso ammesso, e
   `disable_on_numbers` non lo ferma perché un termine con la virgola non è
   fatto di sole cifre (verificato a mano su un indice di prova: con
   `fuzziness=AUTO` combacia, con `0` no). Lo stesso refuso fa combaciare
   importi diversi. E accesa, la normalizzazione peggiora: MRR@10 degli
   importi da 0,917 a 0,891, 12 query su 104 cambiano, 10 in peggio. Senza i
   punti gli importi sono più corti e quindi più vicini per i refusi:
   `6.999,14` e `69.199,10` distano tre modifiche, `6999,14` e `69199,10`
   due, e il secondo atto entra fra i risultati sopra quello cercato.
4. **Smentita, nel verso buono.** Known-item automatiche, MRR@10 da 0,9498 a
   0,9551, +0,0053: fuori di poco dalla soglia di 0,005, in meglio, come in
   Koskidex piatto (+0,002).
5. **Confermata.** Known-item umane (76 query): nessuna cambia, né l'atto
   entro i primi dieci né la posizione; MRR@10 identico.
6. **Confermata.** Delle 24 del confronto, le 21 senza cifre trovano gli
   stessi atti nello stesso ordine: le lunghezze dei campi cambiano, ma il
   punteggio euristico dell'app non le usa. La query con l'anno non trova
   niente né spenta né accesa, quindi non misura il prezzo dell'anno da solo.
7. **Confermata.** Indicizzazione dall'app, mediana di tre, da 1.897 a
   2.018 ms, +6,4%.
8. **Confermata.** Il test nuovo di `KoskidexServiceTest` fallisce prima
   della modifica e passa dopo; la suite passa tranne `ExampleTest` (la home
   risponde 404), che fallisce allo stesso modo senza la modifica.

**Cosa ne segue.** Nell'app le date vanno normalizzate e gli importi no. Le
date sono il difetto misurato in `2026-09-28_date-importi`, chiuso anche
dall'app, al prezzo del 6% di indicizzazione e di nessuna query vera cambiata
fra quelle raccolte finora. Gli importi non hanno il difetto nell'app, perché
lo coprono i refusi; ne hanno un altro, più grave: due importi che
differiscono di una o due cifre combaciano, e la normalizzazione lo
peggiora. La correzione giusta sarebbe trattare gli importi come numeri
anche per `disable_on_numbers`, che cambia i risultati del profilo e va
quindi dietro un'impostazione, con la sua misura. Il profilo resta com'è
finché non girano le known-item umane complete, che sono il posto dove
l'anno da solo può pesare.

## Rilancio sulle known-item umane complete

*Scritto il 29/09/2026, prima del rilancio.* La raccolta si è chiusa con tre
lotti e 104 query (`query/known-item-umane/riassunto.json`); 4 contengono una
cifra. La previsione 5 sopra diceva «nessuna contiene cifre» delle 76 dei primi
due lotti, ed era sbagliata nella premessa: 3 su 76 ne hanno una (lo ha
trovato il terzo controllo della tesi il 29/09); l'esito, nessuna query
cambiata, resta quello misurato. Il rilancio è lo stesso `esegui.sh`, con
Koskidex `cd86102` (le correzioni fra `3bff7ca` e questo non cambiano i
risultati: `2026-09-28_allocazioni` e `2026-09-29_accenti`) e Documentale al
commit corrente, e lo stesso `analizza.py`, che rilegge l'esito più recente di
ogni etichetta. Cosa mi aspetto:

- **R1.** Le previsioni 1-4 e 6 danno gli stessi numeri del 28/09: date,
  importi, known-item automatiche e le 24 non dipendono dalla raccolta.
- **R2.** Known-item umane, 104 query: nessuna entra o esce dai primi dieci
  e l'MRR@10 cambia di meno di 0,01, cioè la previsione 5 tiene anche sulla
  raccolta completa. Se una query cambia, è fra le 4 con una cifra.
- **R3.** Indicizzazione accesa di nuovo al più il 10% più lenta.

Se R2 tiene, l'anno da solo non costa niente sulle query vere raccolte, e
`normalize_dates` può entrare nel profilo consigliato, con una misura del
profilo come un tutto.
