# Il riordino su una GPU consumer

**Domanda.** In `2026-09-28_reranker` il cross-encoder costa 12,0 s a query su
SciFact e 11,3 s su NFCorpus, misurati sul Mac (M2, MPS, fp32). Quanto di quel
costo è della macchina? Sulla GPU del fisso di Martin, in fp32 e in fp16, quanto
scende? Solo tempi: le metriche servono a controllare che il riordino sia lo
stesso, non sono un risultato nuovo.

Scritto il 29/09/2026 sul fisso, prima dello script e prima di ogni misura. Le
previsioni di partenza sono state stimate sul Mac lo stesso giorno
(`ISTRUZIONI-FISSO.md`); qui sotto le ho affinate, prima di misurare, perché la
GPU è una **RTX 3060 da 12 GB**, non la 3060 Ti che le istruzioni davano per
scontata (circa il 20% di unità di calcolo in meno). Nessuna prova di velocità
fatta prima di scrivere.

## La macchina

In `macchina.md`. Windows 11 nativo, **non WSL2**: torch per CUDA gira
direttamente su Windows, con il driver in modalità WDDM e lo schermo attaccato
alla stessa GPU.

## Il metodo

- **Stessi primi stadi**: i file di `2026-09-28_reranker/primo-stadio/` per
  SciFact e NFCorpus (LA, `-top 100`), estratti da git in LF perché la loro
  impronta sha256 sia quella registrata nei rapporti del Mac (con
  `core.autocrlf` il checkout su Windows li ha in CRLF).
- **Stesse collezioni**: scaricate con `eval/corpora/fetch.sh` di Koskidex, che
  controlla l'md5 degli zip; lo sha256 di `corpus.jsonl` coincide con il
  `corpus_sha256` dei primi stadi del Mac.
- **Stesso modello e stessi parametri**: `BAAI/bge-reranker-v2-m3` alla
  revisione `953dc6f`, `max_length` 512, batch 32, primi 100 candidati.
- **Due esecuzioni per collezione** con `strumenti/riordina.py --dispositivo
  cuda`: `--dtype float32` (come sul Mac) e `--dtype float16` (opzione nuova,
  default `float32`, che non cambia il comportamento di prima). Il campo `ms`
  di ogni query è il tempo del riordino.
- **Valutazione** con `scripts/evaluate -rankings -top 10` di Koskidex, gli
  stessi giudizi. Per confrontare le metriche col Mac valuto con lo stesso
  binario anche i rapporti riordinati del Mac.
- **Coincidenza degli ordini**: per ogni query confronto i primi dieci id
  riordinati con quelli del Mac.

`analizza.py` riporta per ogni collezione e dtype mediana, p90 e p99 del tempo
per query, nDCG@10 e MRR@10 accanto a quelli del Mac, e la quota di query con i
primi dieci identici a quelli del Mac.

## Prima di misurare

1. **fp32, SciFact**: mediana fra 2,5 e 5 s a query (Mac 12,0 s).
2. **fp32, NFCorpus**: mediana entro il 20% di quella di SciFact, come sul Mac
   (11,3 contro 12,0).
3. **fp16**: mediana su SciFact fra 0,7 e 2,5 s, e almeno due volte più veloce
   di fp32 su entrambe le collezioni.
4. **fp32, ordini**: nDCG@10 e MRR@10 entro 0,001 da quelli del Mac su
   entrambe le collezioni, e almeno il 95% delle query con i primi dieci
   identici.
5. **fp16, ordini**: nDCG@10 e MRR@10 entro 0,005 da quelli del Mac su
   entrambe le collezioni.

## Esito

Misurato il 29/09/2026 fra le 19:58 e le 20:51 (ora italiana) sul fisso, in
Windows 11 nativo, Koskidex `0e914f5` per la valutazione,
`bge-reranker-v2-m3` alla revisione `953dc6f`, CUDA su RTX 3060 12 GB. Riassunto in
`2026-09-29T185136Z_esito.json` (`analizza.py`); rapporti in `riordinati/`,
valutazioni in `evaluate/` (le `rr-LA-mac` sono i rapporti del Mac valutati
con lo stesso binario: danno gli stessi 0,7233 e 0,3306 di
`2026-09-28_reranker`). Dichiarato: dopo aver committato le previsioni e prima
della misura ho fatto una prova di sviluppo dell'opzione `--dtype` su 3 query
di SciFact, archiviata altrove e non usata (circa 4,7 s in fp32 e 1,4 s in
fp16).

| | Mac, MPS fp32 | fisso, CUDA fp32 | fisso, CUDA fp16 |
|---|---|---|---|
| SciFact, mediana / p90 / p99 per query | 12,0 s | **4,75** / 5,12 / 5,31 s | **1,39** / 1,49 / 1,55 s |
| NFCorpus, mediana / p90 / p99 per query | 11,3 s | **4,51** / 4,89 / 5,13 s | **1,33** / 1,44 / 1,50 s |
| SciFact, nDCG@10 / MRR@10 | 0,7233 / 0,6985 | 0,7233 / 0,6985 | 0,7233 / 0,6985 |
| NFCorpus, nDCG@10 / MRR@10 | 0,3306 / 0,5389 | 0,3306 / 0,5389 | 0,3302 / 0,5373 |
| query con i primi dieci identici al Mac | | 100% / 100% | 95,3% / 95,4% |

**Cinque previsioni su cinque.**

1. **Confermata, vicino al bordo.** fp32 su SciFact: 4,75 s di mediana
   (soglia 2,5-5), contro 12,0 sul Mac.
2. **Confermata.** NFCorpus 4,51 s contro 4,75 di SciFact (sul Mac 11,3
   contro 12,0).
3. **Confermata.** fp16: 1,39 s su SciFact e 1,33 su NFCorpus, 3,42 e 3,38
   volte meno di fp32.
4. **Confermata.** fp32: metriche identiche al Mac alla quarta cifra e i primi
   dieci identici in tutte le query delle due collezioni. MPS e CUDA danno lo
   stesso riordino.
5. **Confermata.** fp16: SciFact identica; NFCorpus 0,3302 contro 0,3306 di
   nDCG@10 e 0,5373 contro 0,5389 di MRR@10, scarto massimo 0,0015 (soglia
   0,005). I primi dieci cambiano in circa una query su venti; non ho
   guardato quali documenti si scambiano.

**Cosa dice.** Il costo di 11-12 s a query era in buona parte della macchina:
una GPU consumer lo porta a 4,5-4,8 s nella stessa precisione e a 1,3-1,4 s in
fp16, con le stesse metriche in fp32 e quasi le stesse in fp16. Resta comunque
un costo da secondi, contro il millisecondo di Koskidex: la conclusione di
`2026-09-28_reranker` (il tetto non è una configurazione da usare dal vivo)
regge anche su questa macchina.
