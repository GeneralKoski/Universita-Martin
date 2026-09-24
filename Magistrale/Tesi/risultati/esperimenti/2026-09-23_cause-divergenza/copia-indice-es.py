#!/usr/bin/env python3
"""Copia dall'Elasticsearch locale esattamente cio' che ha indicizzato, nome
troncato da pathinfo() compreso, in un JSONL da dare a esmirror.go.

L'uscita contiene gli oggetti degli atti, che possono avere nomi di persone:
va scritta fuori dal repository (per esempio nello scratchpad), mai qui.

    copia-indice-es.py /percorso/fuori/dal/repo/es-source.jsonl
"""
import json, sys, urllib.request

ES = "http://localhost:9201/search-documents-local"

def post(url, body):
    r = urllib.request.Request(url, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(r))

res = post(f"{ES}/_search?scroll=2m", {"size": 5000, "query": {"match_all": {}}})
righe, sid = [], res["_scroll_id"]
while res["hits"]["hits"]:
    for h in res["hits"]["hits"]:
        s = h["_source"]
        righe.append({"_id": "doc-" + h["_id"].zfill(4),
                      **{k: (" ".join(v) if isinstance(v, list) else (v or "")) for k, v in s.items()}})
    res = post("http://localhost:9201/_search/scroll", {"scroll": "2m", "scroll_id": sid})
with open(sys.argv[1], "w", encoding="utf8") as f:
    for r in righe:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print(len(righe), "documenti")
