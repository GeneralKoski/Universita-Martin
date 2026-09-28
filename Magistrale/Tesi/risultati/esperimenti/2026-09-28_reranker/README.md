# Il tetto del riordino: un cross-encoder sui primi cento

**Domanda.** Il capitolo 7 ha mostrato che i vettori, fusi con il lessicale,
danno poco e a volte tolgono. Un cross-encoder legge query e documento insieme
ed è il modo più forte, oggi, di riordinare una lista di candidati. Riordinando
i primi cento di Koskidex, quanto si guadagna? Non è una proposta per
Documentale: è il tetto di quanto vale riordinare, con un modello che su questo
hardware costa secondi a query.

Scritto il 28/09/2026, prima del codice e prima di ogni esecuzione sulle
collezioni. L'unica prova fatta è di velocità, su testi inventati: circa 20
coppie query-documento al secondo sulla GPU del Mac (M2, MPS), in fp32 come in
fp16. Avvertenza per la previsione 4: la sera stessa, nella prova generale
della procedura delle known-item umane (`TODO.md`), ho visto le metriche dei
primi due lotti (76 query) delle configurazioni LA e A; il riordino si misura
invece sulla collezione completa.

## Il metodo

- **Modello**: `BAAI/bge-reranker-v2-m3` (568M parametri, multilingue, lo stesso
  gruppo di `bge-m3` usato per i vettori), con sentence-transformers 6.1 e
  torch 2.14, `max_length` 512, fp32, in un ambiente Python a parte: niente
  entra in Koskidex né in Documentale.
- **Primo stadio**: `scripts/evaluate` di Koskidex con `-top 100`, che salva i
  primi cento id di ogni query. BM25, recupero `any`, frequenza mescolata (LA),
  con le stopword inglesi su SciFact e NFCorpus come nel capitolo 5; sulle
  known-item umane anche A (LA più i vettori, unione, peso 160).
- **Riordino**: `strumenti/riordina.py` dà un punteggio a ogni coppia (query,
  titolo e testo del documento come nel corpus) e riordina i cento, a parità
  di punteggio nell'ordine del primo stadio; scrive un rapporto nel formato di
  `app:eval-run-queries`, con il tempo per query, e `scripts/evaluate
  -rankings -top 10` lo valuta con gli stessi giudizi.
- **Collezioni**: SciFact, NFCorpus e le known-item automatiche adesso; le
  known-item umane dopo il terzo lotto, sulla collezione completa.

Il riordino non può trovare ciò che il primo stadio non ha portato: la recall@100
del primo stadio è il tetto del tetto, e si riporta accanto.

## Prima di misurare

1. **SciFact**: nDCG@10 da 0,6757 ad almeno 0,72.
2. **NFCorpus**: nDCG@10 da 0,3062 ad almeno 0,33.
3. **Known-item automatiche** (`<numero> <comune>`): il riordino di LA
   (MRR@10 0,8331) resta sotto il recupero congiuntivo LT (0,9596). Un
   cross-encoder legge il senso, non pesa un numero esatto più di uno simile.
4. **Known-item umane** (dopo il terzo lotto): il riordino di LA fa almeno
   0,05 di MRR@10 sopra LA, quello di A almeno 0,03 sopra A.
5. **Dove il primo stadio ha l'atto fra l'undicesimo e il centesimo posto**,
   sulle known-item umane, il riordino lo porta fra i primi dieci almeno in
   metà dei casi.
6. **Il costo**: mediana del tempo di riordino almeno 2 secondi a query,
   mille volte Koskidex: il tetto non è una configurazione da usare dal vivo
   su questo hardware.
