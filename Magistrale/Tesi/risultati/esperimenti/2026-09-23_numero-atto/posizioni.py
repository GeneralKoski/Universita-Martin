#!/usr/bin/env python3
"""Dove finisce l'atto cercato quando lo si cerca per numero.

Interroga l'Elasticsearch locale con la query di produzione di Documentale
(ElasticsearchService::fuzzySearch: best_fields, fuzziness AUTO,
prefix_length 1, operator and, stessi pesi) e con due varianti che isolano le
cause: refusi spenti, e campo name tolto. Per Koskidex legge le posizioni da un
rapporto di scripts/compare gia' archiviato.

    posizioni.py <rapporto koskidex archiviato>

Gli atti giusti sono doc-0001 (Ordinanza N. 187) e doc-0002 (Determina N. 1223),
verificati sul corpus: sono i due atti di Crispiano con quel numero.
"""
import datetime, json, os, sys, time, urllib.request

ES = "http://localhost:9201/search-documents-local"
CASI = {"ordinanza 187": "1", "determina 1223": "2"}
CAMPI = ["name^5", "tags^4", "summary^3", "subjects^3", "notes^2", "additional_data^1"]
VARIANTI = {
    "produzione": {"fuzziness": "AUTO", "fields": CAMPI},
    "senza_refusi": {"fuzziness": 0, "fields": CAMPI},
    "senza_campo_name": {"fuzziness": "AUTO", "fields": CAMPI[1:]},
}

def post(url, body):
    r = urllib.request.Request(url, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(r))

righe = []
for variante, extra in VARIANTI.items():
    for q, giusto in CASI.items():
        corpo = {"query": {"multi_match": {"query": q, "type": "best_fields", "prefix_length": 1,
                                           "operator": "and", "tie_breaker": 0.3, **extra}},
                 "size": 10000, "_source": False}
        t0 = time.perf_counter_ns()
        hits = post(f"{ES}/_search", corpo)["hits"]["hits"]
        ms = (time.perf_counter_ns() - t0) / 1e6
        ids = [h["_id"] for h in hits]
        righe.append({"motore": "elasticsearch", "variante": variante, "query": q,
                      "atto_giusto": "doc-" + giusto.zfill(4),
                      "posizione": ids.index(giusto) + 1 if giusto in ids else None,
                      "risultati": len(ids), "ms": ms})

kx = json.load(open(sys.argv[1]))
for voce in kx["query"]:
    if voce["query"] in CASI:
        for cfg, e in voce["esiti"].items():
            giusto = "doc-" + CASI[voce["query"]].zfill(4)
            righe.append({"motore": "koskidex", "variante": cfg, "query": voce["query"],
                          "atto_giusto": giusto,
                          "posizione": e["ids"].index(giusto) + 1 if giusto in e["ids"] else None,
                          # trovati e' il totale; ids ne conserva solo la testa
                          "risultati": e.get("trovati", len(e["ids"])), "ms": e["ms"]})

for r in righe:
    print(f"{r['motore']:14s} {r['variante']:24s} {r['query']!r:18s} posizione {r['posizione']} su {r['risultati']}")

ora = datetime.datetime.now(datetime.timezone.utc)
esito = {"ran_at": ora.strftime("%Y-%m-%dT%H:%M:%SZ"),
         "config": {"elasticsearch_versione": json.load(urllib.request.urlopen("http://localhost:9201"))["version"]["number"],
                    "indice": "search-documents-local", "rapporto_koskidex": sys.argv[1]},
         "righe": righe}
d = os.path.join(os.environ["TESI_RISULTATI"], "esperimenti", "2026-09-23_numero-atto")
o = ora.strftime("%Y-%m-%dT%H%M%SZ"); p = os.path.join(d, f"{o}_esito.json"); n = 2
while os.path.exists(p):
    p = os.path.join(d, f"{o}-{n}_esito.json"); n += 1
open(p, "x").write(json.dumps(esito, indent=2, ensure_ascii=False))
print("archiviato in", p)
