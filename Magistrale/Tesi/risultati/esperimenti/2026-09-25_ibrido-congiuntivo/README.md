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

Esito `2026-09-25T132152Z_esito.json`, da `analizza.py` al commit `b64eb0b`
(albero pulito), sulle nove valutazioni delle 13:20-13:21 UTC (Koskidex
`f16b4c9`, lo stesso codice di `d3ffe17` più il diario). Le tre known-item sono
state archiviate prima in `koskidex-beir/` per un flag `-archivio` dimenticato
e spostate in `valutazioni-albo/` senza toccarle: il file non registra la
cartella.

| recupero `all` | L | R | U | U con `any` | solo vettore |
|---|---|---|---|---|---|
| SciFact nDCG@10 | 0,0246 | 0,0246 | **0,6483** | 0,6913 | 0,6436 |
| NFCorpus nDCG@10 | 0,1939 | 0,1973 | **0,3333** | 0,3340 | 0,3149 |
| known-item MRR@10 | 0,9596 | 0,9579 | 0,9579 | 0,8464 | 0,1837 |

| | query a vuoto L / U | Recall@100 R / U | ms mediana U `all` / U `any` |
|---|---|---|---|
| SciFact | 290 / 0 | 0,024 / 0,904 | 32,3 / 40,4 |
| NFCorpus | 160 / 0 | 0,097 / 0,292 | 7,1 / 8,3 |
| known-item | 0 / 0 | 1,000 / 1,000 | 16,0 / 17,2 |

**Con il recupero congiuntivo il difetto 2 è il difetto più grande misurato
finora**: l'unione vale +0,62 di nDCG@10 su SciFact e +0,14 su NFCorpus, e
porta a zero le query a vuoto. Il re-ranking non può niente (+0,000 e +0,004):
riordina i pochi documenti che il lessicale ha trovato.

**Il risultato che non avevo previsto è la riga delle known-item.**
Con `all` più unione la stessa configurazione fa 0,9579 sulle known-item, dove
`any` più unione faceva 0,8464, e sulle collezioni pubbliche resta vicina a
`any` più unione (-0,043 su SciFact, -0,001 su NFCorpus). Il motivo per cui
`2026-09-25_scelta-per-query/` sceglieva `any` sulle query in lingua naturale
era che `all` le lasciava a vuoto; l'unione toglie quel motivo, perché i
documenti li porta il vettore. Contro `any` più unione, a parità di tutto il
resto, `all` scambia 0,04 su SciFact con 0,11 di MRR sulle known-item. Contro la
somma calibrata del difetto 3 (`any`, costante 160: 0,7067 e 0,3441 sul test)
perde 0,06 e 0,01 sulle pubbliche, ma quella costante sulle known-item non si
può usare (0,50 sul train). Ed è la configurazione più vicina a Documentale in
produzione, che cerca già con `operator and`.

### Le previsioni

1. SciFact: U almeno 0,60, R entro 0,01 da L: **0,6483 e +0,000,
   confermata.** U sta appena sopra il solo vettore (0,6436): i 10 documenti
   lessicali aggiungono poco.
2. NFCorpus: U almeno 0,30 e nessuna query a vuoto, R meno di 0,02 sopra L:
   **0,3333, zero a vuoto, +0,0035, confermata.**
3. Known-item: R entro 0,01 da L, U entro 0,01 da R: **-0,0017 e +0,000,
   confermata.** Il lessicale trova in mediana un solo candidato, quello
   giusto; i 99 portati dal vettore finiscono sotto.
4. U almeno 0,5 sopra R su SciFact: **+0,6236, confermata.**
5. U con `all` più veloce di U con `any` sulla stessa collezione:
   **confermata su tutte e tre** (8, 1,2 e 1,2 ms in meno).

### Cosa vuol dire per la tesi

Il capitolo del difetto 2 ha due metà: con il recupero disgiuntivo l'unione
conta poco, con quello congiuntivo, che è quello di Documentale, conta
moltissimo. E la scelta per query va rifatta con l'unione dentro: se `all` più
unione regge anche sulle known-item umane, il classificatore fra `any` e `all`
potrebbe non servire più, e resterebbe solo il peso del vettore del difetto 3
da scegliere per tipo di query.

