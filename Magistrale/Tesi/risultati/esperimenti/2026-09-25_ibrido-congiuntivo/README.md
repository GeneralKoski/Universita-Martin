# Difetto 2 sul recupero congiuntivo

**Domanda.** In `2026-09-25_ibrido-unione/` l'unione non ha cambiato niente su
SciFact, perché il lessicale disgiuntivo trova già quasi tutti i documenti, e
ha portato 0,031 di Recall@100 su NFCorpus. Il peso del difetto 2 dipende dal
recupero lessicale. Documentale in produzione cerca in modo congiuntivo
(`operator and`), come Koskidex con `RetrievalMode = all`: lì il lessicale
lascia a vuoto la maggior parte delle query lunghe. Quanto vale l'unione dove
il lessicale trova poco?

## Metodo

- Stessa impostazione del difetto 2, cambiando una cosa sola: recupero
  **`all`** al posto di `any`. BM25, frequenza mescolata, nessuna analisi,
  refusi spenti, `bge-m3` digest `790764642607` dalla cache, i 100 più
  vicini, la somma `sim * 20` di oggi.
- Tre configurazioni: **L** lessicale, **R** re-ranking (oggi), **U** unione.
  Il solo vettore non dipende dal recupero lessicale: vale quello già misurato
  (SciFact 0,6436, NFCorpus 0,3149, known-item 0,1837).
- Punti di partenza già archiviati, L con `all`: SciFact nDCG@10 0,0246 con 290
  query a vuoto su 300 (`koskidex-beir/2026-09-25T100240Z`), NFCorpus 0,1939
  con 160 su 323 (`100242Z`), known-item MRR@10 0,9596 (`valutazioni-albo/`
  `2026-09-25T094211Z`). Si rimisurano comunque, sul commit di oggi.
- Le esecuzioni si lanciano a calibrazione del difetto 3 finita, per non
  sporcare i tempi.

## Prima di misurare

Scritto e committato prima di lanciare le valutazioni.

1. **SciFact**: U fa almeno 0,60 di nDCG@10, vicino al solo vettore, perché il
   lessicale risponde a 10 query su 300; R resta entro 0,01 da L, perché non
   può riordinare risultati che non ci sono.
2. **NFCorpus**: U fa almeno 0,30 e nessuna query a vuoto; R guadagna su L meno
   di 0,02.
3. **Known-item**: R entro 0,01 da L e U entro 0,01 da R: con `all` l'atto
   giusto è quasi sempre fra i pochi candidati, e i documenti del solo
   vettore finiscono sotto.
4. **Il difetto 2 qui pesa**: U supera R di almeno 0,5 di nDCG@10 su SciFact,
   dove con `any` la differenza era zero.
5. **Costo**: la mediana del tempo per query di U con `all` è sotto quella di U
   con `any` sulla stessa collezione, perché il lessicale porta meno
   candidati.

## Esito
