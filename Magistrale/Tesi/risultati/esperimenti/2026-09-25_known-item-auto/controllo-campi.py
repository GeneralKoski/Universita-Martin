#!/usr/bin/env python3
"""Controllo della causa: le stesse query, con ogni parola libera di stare in un
campo diverso.

La query di produzione (multi_match best_fields, operator and) vuole tutte le
parole nello stesso campo. Qui ogni parola diventa un multi_match best_fields a
sé, con gli stessi refusi, lo stesso prefix_length e gli stessi pesi, e tutte
sono obbligatorie: resta la congiunzione, cade solo il vincolo del campo unico.
Scrive un rapporto nel formato di app:eval-run-queries, da valutare con
scripts/evaluate -rankings come gli altri.

    TESI_RISULTATI=... controllo-campi.py <queries.txt>
"""
import datetime, json, os, subprocess, sys, time, urllib.request

ES = "http://localhost:9201"
INDICE = "search-documents-local"
PESI = ["name^5", "tags^4", "summary^3", "subjects^3", "notes^2", "additional_data^1"]
QUI = os.path.dirname(os.path.abspath(__file__))


def chiama(metodo, percorso, corpo=None):
    dati = json.dumps(corpo).encode() if corpo is not None else None
    r = urllib.request.Request(ES + percorso, data=dati, method=metodo, headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(r))


def parola(p):
    return {"multi_match": {"query": p, "type": "best_fields", "fuzziness": "AUTO", "prefix_length": 1,
                            "operator": "and", "tie_breaker": 0.3, "fields": PESI}}


query = [q.strip() for q in open(sys.argv[1], encoding="utf8") if q.strip()]
esiti = []
for q in query:
    corpo = {"query": {"bool": {"must": [parola(p) for p in q.split()]}}, "size": 10000, "_source": False}
    t0 = time.perf_counter_ns()
    hits = chiama("POST", f"/{INDICE}/_search", corpo)["hits"]["hits"]
    ms = (time.perf_counter_ns() - t0) / 1e6
    esiti.append({"query": q, "ids": ["doc-" + h["_id"].zfill(4) for h in hits], "ms": round(ms, 3)})

git = lambda *a: subprocess.run(["git", "-C", QUI, *a], capture_output=True, text=True, check=True).stdout.strip()
ora = datetime.datetime.now(datetime.timezone.utc)
rapporto = {"ran_at": ora.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "config": {"motore": "elasticsearch-parole-in-campi-diversi",
                       "variante": "bool must di un multi_match best_fields per parola, fuzziness AUTO, "
                                   "prefix_length 1, pesi di produzione",
                       "elasticsearch_versione": chiama("GET", "/")["version"]["number"], "indice": INDICE,
                       "documenti_indicizzati": chiama("GET", f"/{INDICE}/_count")["count"],
                       "query_file": sys.argv[1], "commit": git("rev-parse", "--short", "HEAD"),
                       "modifiche_non_committate": "true" if git("status", "--porcelain", "--", "*.py") else "false"},
            "query": esiti}
vuote = sum(1 for e in esiti if not e["ids"])
print(f"{len(esiti)} query, {vuote} a vuoto")
if not os.environ.get("TESI_RISULTATI"):
    sys.exit("!!! RISULTATO NON ARCHIVIATO: TESI_RISULTATI non è impostata.")
d = os.path.join(os.environ["TESI_RISULTATI"], "esperimenti", "2026-09-25_known-item-auto")
o = ora.strftime("%Y-%m-%dT%H%M%SZ"); p = os.path.join(d, f"{o}_controllo-campi.json"); n = 2
while os.path.exists(p):
    p = os.path.join(d, f"{o}-{n}_controllo-campi.json"); n += 1
open(p, "x").write(json.dumps(rapporto, indent=2, ensure_ascii=False))
print("archiviato in", p)
