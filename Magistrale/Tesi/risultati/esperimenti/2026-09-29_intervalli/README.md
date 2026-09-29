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
