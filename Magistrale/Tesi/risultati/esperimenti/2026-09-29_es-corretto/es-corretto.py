#!/usr/bin/env python3
"""Elasticsearch con le correzioni del profilo consigliato, per
2026-09-29_es-corretto. Ricrea l'indice es-corretto con il mapping di
search-documents-local e il filtro elision di Lucene nell'analizzatore
predefinito, ci copia i documenti con _reindex, poi interroga l'indice con la
variante chiesta su un file di query e scrive un rapporto nel formato di
app:eval-run-queries in $TESI_RISULTATI/confronto, da valutare con
scripts/evaluate -rankings. Stampa solo il percorso del rapporto.

    es-corretto.py indice                          ricrea l'indice
    es-corretto.py ESC|ESO <queries.txt> <etichetta>
"""
import datetime, json, os, subprocess, sys, time, urllib.error, urllib.request

ES = "http://localhost:9201"
SORGENTE, INDICE = "search-documents-local", "es-corretto"
PESI = ["name^5", "tags^4", "summary^3", "subjects^3", "notes^2", "additional_data^1"]
# Gli articoli del filtro elision dell'analizzatore italian di Elasticsearch, come in 2026-09-25_elisioni.
ARTICOLI = ["c", "l", "all", "dall", "dell", "nell", "sull", "coll", "pell", "gl", "agl", "dagl", "degl", "negl",
            "sugl", "un", "m", "t", "s", "v", "d"]
QUI = os.path.dirname(os.path.abspath(__file__))


def chiama(metodo, percorso, corpo=None):
    dati = json.dumps(corpo).encode() if corpo is not None else None
    r = urllib.request.Request(ES + percorso, data=dati, method=metodo, headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(r, timeout=600))


def ricrea():
    try:
        chiama("DELETE", f"/{INDICE}")
    except urllib.error.HTTPError as e:
        if e.code != 404:
            raise
    mapping = chiama("GET", f"/{SORGENTE}/_mapping")[SORGENTE]["mappings"]
    chiama("PUT", f"/{INDICE}", {"settings": {"number_of_shards": 1, "number_of_replicas": 0, "analysis": {
        "filter": {"elisione_it": {"type": "elision", "articles_case": True, "articles": ARTICOLI}},
        "analyzer": {"default": {"type": "custom", "tokenizer": "standard", "filter": ["elisione_it", "lowercase"]}}}},
        "mappings": mapping})
    chiama("POST", "/_reindex?refresh=true", {"source": {"index": SORGENTE}, "dest": {"index": INDICE}})
    n, m = chiama("GET", f"/{INDICE}/_count")["count"], chiama("GET", f"/{SORGENTE}/_count")["count"]
    assert n == m, f"copiati {n} documenti su {m}"


def parola(p):
    return {"multi_match": {"query": p, "type": "best_fields", "fuzziness": 0 if p.strip(".,;:()").isdigit() else "AUTO",
                            "prefix_length": 1, "operator": "and", "tie_breaker": 0.3, "fields": PESI}}


def corpo(variante, q):
    clausole = [parola(p) for p in q.split()]
    if variante == "ESC":
        return {"bool": {"must": clausole}}
    return {"bool": {"should": clausole, "minimum_should_match": 1}}


if sys.argv[1] == "indice":
    ricrea()
    sys.exit(0)
variante, file_query, etichetta = sys.argv[1:4]
assert variante in ("ESC", "ESO"), variante
esiti = []
for q in (x.strip() for x in open(file_query, encoding="utf8")):
    if not q:
        continue
    t0 = time.perf_counter_ns()
    hits = chiama("POST", f"/{INDICE}/_search", {"query": corpo(variante, q), "size": 10000, "_source": False})["hits"]["hits"]
    esiti.append({"query": q, "ids": ["doc-" + h["_id"].zfill(4) for h in hits], "ms": round((time.perf_counter_ns() - t0) / 1e6, 3)})

git = lambda *a: subprocess.run(["git", "-C", QUI, *a], capture_output=True, text=True, check=True).stdout.strip()
ora = datetime.datetime.now(datetime.timezone.utc)
rapporto = {"ran_at": ora.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "config": {"motore": "elasticsearch-corretto", "variante": variante,
                       "descrizione": "bool di un multi_match best_fields per parola, fuzziness AUTO (0 sulle parole di sole "
                                      "cifre), prefix_length 1, tie_breaker 0.3, pesi di produzione, filtro elision; "
                                      + ("tutte le parole obbligatorie" if variante == "ESC" else "minimum_should_match 1"),
                       "elasticsearch_versione": chiama("GET", "/")["version"]["number"], "indice": INDICE,
                       "documenti_indicizzati": str(chiama("GET", f"/{INDICE}/_count")["count"]),
                       "query_file": file_query, "label": etichetta, "commit": git("rev-parse", "--short", "HEAD"),
                       "modifiche_non_committate": "true" if git("status", "--porcelain", "--untracked-files=no", "--", QUI) else "false"},
            "query": esiti}
if not os.environ.get("TESI_RISULTATI"):
    sys.exit("!!! RISULTATO NON ARCHIVIATO: TESI_RISULTATI non è impostata.")
d = os.path.join(os.environ["TESI_RISULTATI"], "confronto")
o = ora.strftime("%Y-%m-%dT%H%M%SZ"); p = os.path.join(d, f"{o}_{etichetta}-elasticsearch.json"); n = 2
while os.path.exists(p):
    p = os.path.join(d, f"{o}-{n}_{etichetta}-elasticsearch.json"); n += 1
open(p, "x").write(json.dumps(rapporto, indent=2, ensure_ascii=False))
print(p)
