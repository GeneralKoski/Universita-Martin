# Da dove vengono i dati dei grafici

Scritti da `risultati/strumenti/dati-grafici.py`; ogni colonna è copiata da un file archiviato in `risultati/` (percorsi relativi a quella cartella).

- `carico.dat`: ricerche al secondo (campo qps) per numero di client; es = Elasticsearch come l'app, kc = Koskidex nel container, kn = Koskidex nativo; sul Mac Koskidex e' dopo le correzioni delle allocazioni. Sorgenti: `esperimenti/2026-09-28_carico/2026-09-29T074830Z_esito.json`, `esperimenti/2026-09-29_accenti/2026-09-29T080818Z_esito.json`, `esperimenti/2026-09-29_carico-fisso/2026-09-29T191821Z_esito.json`.
- `mrr-umane.dat`: MRR@10 sulle 104 known-item umane con intervallo al 95% (bootstrap accoppiato); meno e piu sono le distanze della media dagli estremi; gruppo 0 = dall'app, 1 = Koskidex piatto, 2 = Elasticsearch corretto, 3 = riordinato. Sorgenti: `esperimenti/2026-09-29_intervalli/2026-09-29T193440Z_esito.json`.
- `mrr-umane-g0.dat`: le righe del gruppo 0 di mrr-umane.dat. Sorgenti: `esperimenti/2026-09-29_intervalli/2026-09-29T193440Z_esito.json`.
- `mrr-umane-g1.dat`: le righe del gruppo 1 di mrr-umane.dat. Sorgenti: `esperimenti/2026-09-29_intervalli/2026-09-29T193440Z_esito.json`.
- `mrr-umane-g2.dat`: le righe del gruppo 2 di mrr-umane.dat. Sorgenti: `esperimenti/2026-09-29_intervalli/2026-09-29T193440Z_esito.json`.
- `mrr-umane-g3.dat`: le righe del gruppo 3 di mrr-umane.dat. Sorgenti: `esperimenti/2026-09-29_intervalli/2026-09-29T193440Z_esito.json`.
- `fusione.dat`: valore della metrica (nDCG@10 su SciFact train e NFCorpus dev, MRR@10 sulle known-item automatiche train) per costante della somma pesata. Sorgenti: `esperimenti/2026-09-25_fusione/2026-09-25T131533Z_calibrazione.json`.
- `crescita.dat`: memoria a riposo in MB (riposo_mb) e indice su disco in MB (byte_su_disco / 1e6) per numero di documenti. Sorgenti: `esperimenti/2026-09-28_carico/2026-09-29T074830Z_esito.json`, `esperimenti/2026-09-28_carico/2026-09-29T100953Z_disco-10018.json`.
- `compromesso.dat`: MRR@10 sulle known-item umane e mediana in ms della ricerca dall'app (per ES dal rapporto dell'app, che contiene testi di query e non è in git). Sorgenti: `esperimenti/2026-09-29_profilo-completo/2026-09-29T122455Z_esito.json`, `confronto/2026-09-29T093306Z_known-item-umane-elasticsearch.json`, `esperimenti/2026-09-29_intervalli/2026-09-29T193440Z_esito.json`.
