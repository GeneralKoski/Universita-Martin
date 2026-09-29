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

## Esito, prima parte: SciFact, NFCorpus, known-item automatiche

Misurato il 28/09/2026 fra le 14:38 e le 16:48, Koskidex `51d4988`,
`bge-reranker-v2-m3` alla revisione `953dc6f`, MPS in fp32. Riassunto in
`2026-09-28T144809Z_esito-beir.json` (`analizza.py beir`); primi stadi in
`primo-stadio/`, rapporti riordinati in `riordinati/`, valutazioni in
`evaluate/`. La previsione 4 e la 5 aspettano le known-item umane complete.

| | primo stadio | riordino | recall@100 del primo stadio | mediana del riordino |
|---|---|---|---|---|
| SciFact, nDCG@10 | 0,6757 | **0,7233** | 0,886 | 12,0 s |
| NFCorpus, nDCG@10 | 0,3062 | **0,3306** | 0,238 | 11,3 s |
| known-item automatiche, MRR@10 | 0,8331 | **0,9528** | 1,000 | 5,1 s |

**Quattro previsioni su quattro, due di misura e una nel verso sbagliato
dello spirito.**

1. **Confermata, di poco.** SciFact da 0,6757 a 0,7233, +0,048 (soglia 0,72).
2. **Confermata, di pochissimo.** NFCorpus da 0,3062 a 0,3306 (soglia 0,33).
   Il tetto qui è basso: il primo stadio porta fra i cento solo il 24% dei
   documenti giusti, e il riordino non vede gli altri.
3. **Confermata alla lettera, smentita nello spirito.** Il riordino di LA
   resta sotto LT (0,9528 contro 0,9596), ma di 0,007, non del margine che
   avevo in mente: porta LA da 0,833 a 0,953. Delle 13 query con l'atto fra
   l'undicesimo e il centesimo posto ne porta 12 fra i primi dieci. Il
   ragionamento («un cross-encoder non pesa un numero esatto più di uno
   simile») era sbagliato: legge numero e comune nella scheda, e li riconosce.
6. **Confermata.** Mediana da 5,1 a 12,0 secondi a query, contro il
   millisecondo di Koskidex; il costo cresce con la lunghezza dei testi
   (schede corte 5 s, abstract 11-12 s).

## Esito, seconda parte: known-item umane

Misurato il 29/09/2026 fra le 11:46 e le 12:05 sulle 104 known-item umane dei
tre lotti, Koskidex `cd86102`, `bge-reranker-v2-m3` alla revisione `953dc6f`,
MPS. Riassunto in `2026-09-29T100627Z_esito-umane.json` (`analizza.py umane`);
l'esito delle 12:05 (`100554Z`) ha gli stessi numeri senza la divisione per
gruppo, aggiunta per la tabella del capitolo 8. I rapporti riordinati
contengono il testo delle query e restano fuori da git, come le risposte. Il
primo stadio dà gli stessi MRR@10 di LA e A in `2026-09-25_known-item-umane/`.

| MRR@10 | tutte | Crispiano | FVG | con numero (4) | senza numero | recall@100 del primo stadio | mediana del riordino |
|---|---|---|---|---|---|---|---|
| LA | 0,559 | 0,477 | 0,635 | 0,750 | 0,552 | 0,913 | |
| LA riordinato | **0,633** | 0,551 | 0,709 | 0,833 | 0,625 | | 5,3 s |
| A | 0,613 | 0,557 | 0,665 | 0,778 | 0,606 | 0,971 | |
| A riordinato | **0,641** | 0,565 | 0,711 | 0,833 | 0,633 | | 5,9 s |

**La 5 confermata, la 4 a metà** (`analizza.py` la segna smentita perché
controlla le due parti insieme).

4. **A metà.** Il riordino porta LA da 0,559 a 0,633, +0,074: confermata. A
   da 0,613 a 0,641, +0,028 (*nota del 30/09/2026: sui valori esatti
   0,6405 e 0,6130 è +0,027; il verdetto non cambia*), appena sotto la soglia
   di 0,03: smentita. Il
   riordino aggiunge meno dove i vettori hanno già portato l'atto in alto.
5. **Confermata.** Degli atti che il primo stadio aveva fra l'11° e il 100°
   posto, il riordino ne porta fra i primi dieci 13 su 16 con LA e 6 su 12
   con A.

La 6, il costo, tiene anche qui: 5,3 e 5,9 s di mediana a query. Il riordino
non cambia le ricerche a vuoto, perché riordina solo quello che il primo
stadio trova: LA ne lascia una, A nessuna.
