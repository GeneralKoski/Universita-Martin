# La macchina delle misure

Tutti i tempi di questa cartella sono stati misurati qui, e valgono solo qui.
Rilevato il 24/09/2026.

| | |
|---|---|
| Modello | Mac14,7, Apple M2 |
| Core | 8 |
| Memoria | 16 GB |
| Sistema | macOS 26.6.2 (25G83) |
| Go | go1.27.1 |
| PHP | 8.5.5 |
| Docker | 27.4.0, macchina virtuale con 4 CPU e 7 GB |
| Elasticsearch | docker.elastic.co/elasticsearch/elasticsearch:9.1.0, nodo singolo, heap `-Xms1g -Xmx1g`, sicurezza spenta, licenza basic |
| MySQL | 8.4.10 in Docker |

**Koskidex** gira nativo, fuori da Docker, su tutti i core.
**Elasticsearch e MySQL** girano dentro la macchina virtuale di Docker, con le
risorse qui sopra: è una delle ragioni per cui i tempi dei due motori non si
confrontano alla pari (vedi il README).
