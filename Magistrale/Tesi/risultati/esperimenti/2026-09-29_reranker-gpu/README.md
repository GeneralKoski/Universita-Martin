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
