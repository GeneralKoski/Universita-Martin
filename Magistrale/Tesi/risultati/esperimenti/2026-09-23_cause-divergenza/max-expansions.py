#!/usr/bin/env python3
"""Il limite di espansioni dei refusi spiega le differenze che restavano dopo il
quarto passo? Interroga l'Elasticsearch locale con la query di produzione di
Documentale (ElasticsearchService::cerca: best_fields, fuzziness AUTO,
prefix_length 1, operator and, tie_breaker 0.3, stessi pesi, size 10000) sulle
24 query del confronto, una volta con max_expansions di default (50) e una con
10.000, e confronta gli insiemi. Confronta anche gli insiemi di default con un
rapporto dell'app già archiviato, per dire che l'indice è quello delle misure.
Il controllo del 24/09 era stato fatto a mano, senza archiviarlo; questo lo
rifà sugli stessi dati.

    max-expansions.py <rapporto elasticsearch dell'app archiviato>
"""
import datetime, json, os, subprocess, sys, urllib.request

ES = "http://localhost:9201"
INDICE = "search-documents-local"
QUI = os.path.dirname(os.path.abspath(__file__))
CAMPI = ["name^5", "tags^4", "summary^3", "subjects^3", "notes^2", "additional_data^1"]
QUERY = os.path.join(QUI, "..", "..", "query", "confronto-24.txt")
git = lambda *a: subprocess.run(["git", *a], capture_output=True, text=True, check=True).stdout.strip()


def cerca(q, extra):
    corpo = {"query": {"multi_match": {"query": q, "type": "best_fields", "fuzziness": "AUTO", "prefix_length": 1,
                                       "operator": "and", "tie_breaker": 0.3, "fields": CAMPI, **extra}},
             "size": 10000, "_source": False}
    r = urllib.request.Request(f"{ES}/{INDICE}/_search", data=json.dumps(corpo).encode(),
                               headers={"Content-Type": "application/json"})
    return [h["_id"] for h in json.load(urllib.request.urlopen(r))["hits"]["hits"]]


rapporto = json.load(open(sys.argv[1]))
archiviati = {v["query"]: v["ids"] for v in rapporto["query"]} if isinstance(rapporto["query"], list) else \
             {q: v["ids"] for q, v in rapporto["query"].items()}
righe = []
for q in [r.strip() for r in open(QUERY, encoding="utf8") if r.strip() and not r.startswith("#")]:
    base, largo = cerca(q, {}), cerca(q, {"max_expansions": 10000})
    arch = [str(i).removeprefix("doc-").lstrip("0") for i in archiviati.get(q, [])]
    righe.append({"query": q, "default": len(base), "max_expansions_10000": len(largo),
                  "stesso_insieme": set(base) == set(largo),
                  "default_uguale_al_rapporto": set(base) == set(arch)})
esito = {"query": len(righe), "stessi_insiemi": sum(r["stesso_insieme"] for r in righe),
         "uguali_al_rapporto_archiviato": sum(r["default_uguale_al_rapporto"] for r in righe), "per_query": righe}
for r in righe:
    print(f"{r['query']!r:62s} {r['default']:5d} {r['max_expansions_10000']:5d} {r['stesso_insieme']} {r['default_uguale_al_rapporto']}")
print({k: v for k, v in esito.items() if k != "per_query"})

ora = datetime.datetime.now(datetime.timezone.utc)
esito = {"ran_at": ora.strftime("%Y-%m-%dT%H:%M:%SZ"),
         "config": {"elasticsearch_versione": json.load(urllib.request.urlopen(ES))["version"]["number"],
                    "indice": INDICE, "rapporto_archiviato": os.path.relpath(sys.argv[1], os.path.join(QUI, "..", "..")),
                    "commit": git("-C", QUI, "rev-parse", "--short", "HEAD"),
                    "modifiche_non_committate": "true" if git("-C", QUI, "status", "--porcelain", "--", os.path.abspath(__file__)) else "false",
                    "commit_documentale": git("-C", os.path.expanduser("~/Desktop/Dieffetech/Documentale"), "rev-parse", "--short", "HEAD")},
         **esito}
if not os.environ.get("TESI_RISULTATI"):
    sys.exit("!!! RISULTATO NON ARCHIVIATO: TESI_RISULTATI non è impostata.")
d = os.path.join(os.environ["TESI_RISULTATI"], "esperimenti", "2026-09-23_cause-divergenza")
o = ora.strftime("%Y-%m-%dT%H%M%SZ"); p = os.path.join(d, f"{o}_max-expansions.json"); n = 2
while os.path.exists(p):
    p = os.path.join(d, f"{o}-{n}_max-expansions.json"); n += 1
open(p, "x").write(json.dumps(esito, indent=2, ensure_ascii=False))
print("archiviato in", p)
