# La macchina di questo esperimento

Il fisso di Martin. I tempi di questa cartella valgono solo qui. Rilevato il
29/09/2026.

| | |
|---|---|
| CPU | AMD Ryzen 5 8500G, 6 core, 12 thread |
| Memoria | 32 GB (31,1 GB visibili) |
| Sistema | Windows 11 Pro 10.0.26200, **nativo**; Docker in WSL2 |
| Go | go1.27.1 windows/amd64 (client `scripts/carico` e Koskidex nativo); il binario del container è compilato per linux/amd64 |
| PHP | 8.4.12, Composer 2.8.11 (solo per riempire i motori dall'app) |
| Docker | Docker Desktop, motore 29.7.2, VM WSL2 con 12 CPU e 23,5 GB (`.wslconfig` già presente per un altro progetto, non toccato) |
| Elasticsearch | docker.elastic.co/elasticsearch/elasticsearch:9.1.0, nodo singolo, heap `-Xms1g -Xmx1g`, sicurezza spenta, `--cpus 4` |
| Koskidex nel container | `alpine:latest`, binario linux/amd64 di Koskidex `0e914f5`, `--cpus 4`, dati montati dal disco di Windows |
| Koskidex nativo | stesso commit, `k-nativo.exe` su Windows, tutti i 12 thread divisi con il client |
| MySQL | 8.4.10 in Docker, acceso durante le misure come sul Mac |

**Le CPU.** Sul Mac la VM di Docker ha 4 CPU; qui ne ha 12, e ogni container
dei motori ha un tetto di 4 CPU (`--cpus 4`, quota di tempo, non core
dedicati). Nessun altro container acceso oltre a MySQL e ai due motori.

**L'app**, per riempire i motori, gira senza `.env` con le variabili sulla riga
di comando delle istruzioni, più tre che senza `.env` mancano: `APP_KEY`
(generata a caso, serve solo ad avviare Laravel), `APP_ENV=local` (dà il nome
dell'indice `search-documents-local`) ed `ELASTICSEARCH_API_KEY` con un valore
qualunque (il client la vuole stringa; con la sicurezza spenta Elasticsearch
la ignora). `ELASTICSEARCH_INDEX_NAME=search-type-local` come in `.env.example`.
