# La scelta per tipo di query, su query dei due tipi nella stessa collezione

**Domanda.** In `2026-09-25_scelta-ibrida/` scegliere per ogni query fra
**A** (`any`, unione, peso 160) e **B** (`all`, unione, peso 10) con la regola
*B se la query ha una cifra e il recupero lessicale congiuntivo trova
qualcosa* vale +0,023 di nDCG@10 medio, e il classificatore fa lo stesso. Ma lì
ogni tipo di query stava in una collezione diversa, e la regola poteva
riconoscere la collezione invece del tipo. Sulle known-item umane, dove una
query per contenuto e una con un numero cercano atti dello stesso corpus, la
regola regge ancora?

Scritto il 25/09/2026, prima che arrivi una sola risposta.

## Metodo

- **Le valutazioni**: A, B e LT (BM25 `all`, frequenza mescolata, senza
  vettori: dà la caratteristica "il congiuntivo trova qualcosa") sulle
  known-item umane, cioè le stesse di `2026-09-25_known-item-umane/`, senza
  esecuzioni nuove.
- **Il classificatore è congelato**: i pesi, le medie e le deviazioni
  dell'esito di `2026-09-25_scelta-ibrida/` (`2026-09-25T133033Z_esito.json`),
  applicati così come sono. Niente riaddestramento: le query umane sono il test,
  e non se ne usa nessuna per imparare.
- **Le strategie**: sempre A, sempre B, l'oracolo, la regola, il classificatore.
  Metrica nDCG@10 per query (con un atto solo, è l'MRR pesato per posizione),
  sul totale e per query con e senza cifra.

## Prima di misurare

1. **L'oracolo sta almeno 0,03 sopra la regola.** Con i due tipi nella stessa
   collezione, la cifra non basta più a dire quale configurazione vince.
2. **La regola non sta più di 0,01 sotto la migliore configurazione fissa.**
   Sbaglia meno di quanto guadagna.
3. **Il classificatore congelato non supera la regola di più di 0,01.** Ha
   imparato la stessa regola; nel motore non entra.
4. **Fra le query senza cifra, B batte A su almeno il 15%**: è lo spazio che la
   regola, che su quelle sceglie sempre A, non può prendere.

Se la 1 e la 4 tengono, la scelta per tipo di query ha un limite che una
caratteristica della query non supera, e va scritto nella sezione 7.5 come
tale.

## Esito

Misurato il 29/09/2026 sulle 104 known-item umane dei tre lotti, con A, B e
LT di `2026-09-25_known-item-umane/` (Koskidex `cd86102`) e il classificatore
di `2026-09-25_scelta-ibrida/2026-09-25T133033Z_esito.json`. Riassunto in
`2026-09-29T094348Z_esito.json` (`analizza.py`).

| nDCG@10 | tutte (104) | con cifra (4) | senza cifra (100) |
|---|---|---|---|
| sempre A | 0,6719 | 0,8253 | 0,6657 |
| sempre B | 0,6623 | 0,7544 | 0,6586 |
| regola | 0,6727 (B su 1) | 0,8467 (B su 1) | 0,6657 (B su 0) |
| classificatore | 0,6769 (B su 59) | 0,7544 (B su 3) | 0,6738 (B su 56) |
| oracolo | **0,7045** (B su 13) | 0,8467 | 0,6989 |

A e B danno lo stesso nDCG@10 su 73 query delle 104; B vince su 13, A su 18.

**Tre previsioni su quattro.**

1. **Confermata, di poco.** L'oracolo sta 0,032 sopra la regola (0,7045
   contro 0,6727).
2. **Confermata.** La regola non sta sotto la migliore configurazione fissa,
   sempre A, ma 0,0008 sopra: sceglie B su una query sola, e ci guadagna.
3. **Confermata.** Il classificatore congelato supera la regola di 0,004
   (0,6769 contro 0,6727), sotto la soglia di 0,01: sceglie B su 59 query, ma
   su quasi tutte A e B si equivalgono. Nel motore non entra.
4. **Smentita.** Fra le query senza cifra B batte A su 12 su 100, il 12%, non
   almeno il 15%.

La 1 tiene e la 4 no: il margine dell'oracolo c'è, ma sta in poche query (13
su 104 dove B vince) e non si concentra fra quelle senza cifra quanto
previsto. Sulle query scritte da persone la scelta per tipo di query vale
poco in entrambe le direzioni: la regola non perde niente rispetto a sempre A,
e non guadagna quasi niente.
