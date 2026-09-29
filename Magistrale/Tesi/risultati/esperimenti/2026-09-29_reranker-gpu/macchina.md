# La macchina di questo esperimento

Il fisso di Martin. I tempi di questa cartella valgono solo qui. Rilevato il
29/09/2026.

| | |
|---|---|
| CPU | AMD Ryzen 5 8500G, 6 core, 12 thread |
| Memoria | 32 GB (31,1 GB visibili) |
| GPU | NVIDIA GeForce RTX 3060, 12 GB, driver 610.62 in modalità WDDM, con lo schermo attaccato |
| Sistema | Windows 11 Pro 10.0.26200, **nativo**, non WSL2 |
| Python | 3.13, in un ambiente a parte (`~/.venvs/tesi-reranker`) |
| torch | 2.14.0+cu130 (CUDA 13.0) |
| sentence-transformers | 6.1.0, transformers 5.17.0, huggingface_hub 1.33.0 |
| Go | go1.27.1 windows/amd64, solo per `scripts/evaluate` |

Sul Mac (`../../macchina.md`) il riordino gira su MPS, con torch 2.14.0 e
sentence-transformers 6.1.0: le stesse versioni.
