# Quanto valgono le differenze: intervalli di confidenza sulle known-item umane

**Domanda.** La tesi dice più volte che una differenza «di qualche centesimo
sta nel rumore» di 104 query, ma non lo quantifica. Quali delle differenze di
MRR@10 su cui poggiano le conclusioni del capitolo 8 sono più grandi della
variabilità che 104 query lasciano?

Scritto il 29/09/2026, prima dello script e prima di qualunque calcolo. Dichiarato:
conosco già le medie di tutte le configurazioni (sono nelle tabelle della
tesi), non la variabilità per query.

## Metodo

Dalle valutazioni per query già archiviate (`scripts/evaluate`, campo
`mrr@10` di ogni query, sempre le stesse 104 query umane): per ogni
configurazione la media con un intervallo di confidenza al 95%, e per una
lista fissa di 15 confronti la differenza fra le medie con l'intervallo al 95%,
tutti con il **bootstrap accoppiato** (si ricampionano le query, non le
configurazioni: le due configurazioni vedono le stesse query, e questo tiene
conto di quanto sono correlate). 10.000 ricampionamenti, seme fisso 20260929,
percentili 2,5 e 97,5. Come controllo, un test di permutazione a segni sulla
differenza per query (20.000 permutazioni, seme fisso), p a due code.
Stesse 104 query; nessun testo di query nei file.

I 15 confronti (primo meno secondo):

| # | confronto | differenza nota |
|---|---|---|
| C1 | KC (P0) - ES di produzione | +0,106 |
| C2 | ESC - ES di produzione | +0,123 |
| C3 | ESC - KC | +0,017 |
| C4 | P4 - KC | +0,176 |
| C5 | P4 - P2 | +0,105 |
| C6 | P2 - KC | +0,071 |
| C7 | A - LA | +0,054 |
| C8 | A - B | +0,006 |
| C9 | LA - LT | +0,213 |
| C10 | RR-LA - LA | +0,074 |
| C11 | RR-A - A | +0,028 |
| C12 | ESO - P2 | +0,001 |
| C13 | P3 - P2 | +0,073 |
| C14 | LA - P2 | +0,057 |
| C15 | A - P3 | +0,037 |

Le configurazioni sono quelle del capitolo 8: ES e KC dall'app, K0, LA, LT, A,
B, V con Koskidex piatto, RR-LA e RR-A i riordini di `2026-09-28_reranker`,
P0-P4 di `2026-09-29_profilo-completo`, ESC ed ESO di `2026-09-29_es-corretto`.

## Prima di misurare

1. **L'intervallo della differenza esclude lo zero** (estremo inferiore
   positivo) in C1, C2, C4, C5 e C9: sono le differenze grandi su cui poggia il
   capitolo 8.
2. **L'intervallo include lo zero** in C3, C8, C11 e C12: sono le coppie che
   la tesi chiama «uguali» o «nel rumore».
3. **C10 esclude lo zero e C7 lo include**: il riordino di LA vale più del
   guadagno dei vettori su LA, con 104 query.
4. **L'intervallo al 95% della media di una singola configurazione ha
   un'ampiezza (metà dell'intervallo) fra 0,06 e 0,10** in tutte le
   configurazioni.
5. **Il test di permutazione concorda con il bootstrap** (p sotto 0,05 se e
   solo se l'intervallo esclude lo zero) in almeno 13 confronti su 15.

## Aggiunte dopo

Dopo il primo esito (`2026-09-29T193420Z_esito.json`, cinque previsioni su
cinque) ho aggiunto tre confronti che non avevano una previsione, perché
servono a due frasi della tesi che il primo esito metteva in dubbio: **C16**
LA - KC e **C17** A - KC (quanto sta sopra KC il recupero disgiuntivo fuori
dall'app) e **C18** P4 - ES (quanto vale, in tutto, il lavoro sul profilo
migliore dall'app rispetto alla produzione). Il calcolo è lo stesso, e le
prime quindici righe non cambiano (stessi semi).

## Esito

Calcolato il 29/09/2026, script `intervalli.py`, 104 query, 10.000
ricampionamenti, 20.000 permutazioni, semi fissi. Primo esito
`2026-09-29T193420Z_esito.json` (C1-C15, le cinque previsioni); secondo
`2026-09-29T193440Z_esito.json` (stessi numeri, più C16-C18).

**Cinque previsioni su cinque.**

1. **Confermata.** C1, C2, C4, C5 e C9 escludono lo zero. C1 di poco:
   +0,106 con intervallo da +0,035 a +0,184, p 0,006.
2. **Confermata.** C3, C8, C11 e C12 includono lo zero, e con largo margine
   (p da 0,38 a 0,97).
3. **Confermata, e C7 è un caso di confine.** RR-LA - LA esclude lo zero
   (+0,074, da +0,012 a +0,136, p 0,020). A - LA: +0,054, intervallo da
   -0,0005 a +0,111, p 0,058: l'estremo inferiore è quasi zero, e non si può
   dire che i vettori aiutino su queste 104 query con la stessa sicurezza del
   riordino.
4. **Confermata.** La semiampiezza dell'intervallo di una singola media va da
   0,075 a 0,088 di MRR@10.
5. **Confermata.** Bootstrap e permutazione concordano in tutti i 15
   confronti.

Medie con intervallo al 95%:

| | MRR@10 | intervallo | | MRR@10 | intervallo |
|---|---|---|---|---|---|
| ES | 0,326 | 0,243 - 0,410 | P0 = KC | 0,432 | 0,349 - 0,517 |
| K0 | 0,337 | 0,259 - 0,418 | P2 | 0,502 | 0,417 - 0,588 |
| LT | 0,346 | 0,264 - 0,431 | P3 | 0,576 | 0,492 - 0,657 |
| ESC | 0,449 | 0,361 - 0,537 | P4 | 0,607 | 0,528 - 0,686 |
| ESO | 0,503 | 0,419 - 0,588 | LA | 0,559 | 0,476 - 0,640 |
| V | 0,520 | 0,441 - 0,601 | A | 0,613 | 0,534 - 0,691 |
| RR-LA | 0,633 | 0,556 - 0,710 | B | 0,607 | 0,526 - 0,686 |
| RR-A | 0,641 | 0,566 - 0,715 | | | |

Cosa dicono: con 104 query due medie a meno di circa 0,15 l'una dall'altra
hanno intervalli che si sovrappongono. Ma le differenze accoppiate sono più
strette, perché le due configurazioni vedono le stesse query. Le differenze
grandi (KC e ES, P4 e KC, LA e LT, ESC e ES) reggono. Non reggono: A su LA, P2
su KC, LA su P2 (recupero disgiuntivo dall'app contro piatto), A su P3 e il
riordino di A. Sono i confronti che la tesi chiama «nel rumore» o dà per
suggeriti, ed è giusto che sia così.

**Aggiunte, senza previsione.** C16 LA - KC +0,128 (da +0,048 a +0,208),
C17 A - KC +0,181 (da +0,093 a +0,269), C18 P4 - ES +0,282 (da +0,195 a
+0,372): il recupero disgiuntivo fuori dall'app, i vettori, e il profilo
migliore dall'app sopra la produzione sono tutti oltre l'intervallo.
