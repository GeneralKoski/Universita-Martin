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
