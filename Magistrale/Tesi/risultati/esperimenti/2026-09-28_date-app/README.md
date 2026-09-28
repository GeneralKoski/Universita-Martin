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
