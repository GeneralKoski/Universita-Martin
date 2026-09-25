#!/usr/bin/env python3
"""Riassume le valutazioni known-item e controlla le previsioni del README.

Legge le valutazioni archiviate da scripts/evaluate (una per run) e i due
rapporti di app:eval-run-queries, e scrive un esito con: per ogni run MRR@10,
quota di query con l'atto al primo posto e nei primi 10, Recall@100, query a
vuoto; la parità degli insiemi fra Elasticsearch e Koskidex innestato; dove
finisce l'atto giusto quando un run non lo mette primo.

    analizza.py <valutazione> [...] --rapporti <rapporto elasticsearch> <rapporto koskidex>
"""
import collections, datetime, json, os, subprocess, sys

argomenti = sys.argv[1:]
i = argomenti.index("--rapporti")
valutazioni, (rap_es, rap_kx) = argomenti[:i], argomenti[i + 1:]
QUI = os.path.dirname(os.path.abspath(__file__))

run = {}
for f in valutazioni:
    v = json.load(open(f))
    if v["config"].get("modifiche_non_committate") != "false":
        sys.exit(f"{f}: prodotto da codice non committato, non vale")
    pq = v["per_query"]
    # Un solo atto giusto per query: MRR@10 = 1/posizione, zero se oltre il 10°.
    posizioni = collections.Counter(round(1 / q["mrr@10"]) if q["mrr@10"] > 0 else "oltre 10" for q in pq)
    run[v["run"]] = {"file": os.path.basename(f), "query": v["queries"],
                     "mrr@10": round(v["mean_mrr@10"], 4),
                     "primo_posto": round(sum(q["mrr@10"] == 1 for q in pq) / len(pq), 4),
                     "entro_10": round(sum(q["mrr@10"] > 0 for q in pq) / len(pq), 4),
                     "recall@100": round(v["mean_recall@100"], 4),
                     "a_vuoto": v["zero_results"],
                     "posizione_dell_atto": {str(k): n for k, n in sorted(posizioni.items(), key=lambda x: (isinstance(x[0], str), x[0]))}}

es, kx = json.load(open(rap_es)), json.load(open(rap_kx))
for r in (es, kx):
    if r["config"].get("modifiche_non_committate") != "false":
        sys.exit("un rapporto dell'app viene da codice non committato")
coppie = list(zip(es["query"], kx["query"]))
assert all(a["query"] == b["query"] for a, b in coppie), "i due rapporti non hanno le stesse query"
identici = sum(set(a["ids"]) == set(b["ids"]) for a, b in coppie)
diverse = [{"query": a["query"], "solo_elasticsearch": len(set(a["ids"]) - set(b["ids"])),
            "solo_koskidex": len(set(b["ids"]) - set(a["ids"]))}
           for a, b in coppie if set(a["ids"]) != set(b["ids"])]

for nome, r in run.items():
    print(f"{nome:18s} MRR@10 {r['mrr@10']:.4f}  primo {r['primo_posto']:.1%}  entro 10 {r['entro_10']:.1%}  "
          f"R@100 {r['recall@100']:.4f}  a vuoto {r['a_vuoto']}")
print(f"insiemi identici Elasticsearch/Koskidex innestato: {identici}/{len(coppie)}")

ora = datetime.datetime.now(datetime.timezone.utc)
git = lambda *a: subprocess.run(["git", "-C", QUI, *a], capture_output=True, text=True, check=True).stdout.strip()
esito = {"ran_at": ora.strftime("%Y-%m-%dT%H:%M:%SZ"),
         "config": {"commit": git("rev-parse", "--short", "HEAD"),
                    "modifiche_non_committate": "true" if git("status", "--porcelain", "--", "*.py") else "false",
                    "rapporto_elasticsearch": os.path.basename(rap_es), "rapporto_koskidex": os.path.basename(rap_kx),
                    "elasticsearch_versione": es["config"].get("elasticsearch_versione"),
                    "koskidex_versione": kx["config"].get("koskidex_versione"),
                    "commit_documentale": es["config"].get("commit")},
         "run": run,
         "parita_app": {"insiemi_identici": identici, "query": len(coppie), "diverse": diverse}}
if not os.environ.get("TESI_RISULTATI"):
    sys.exit("!!! RISULTATO NON ARCHIVIATO: TESI_RISULTATI non è impostata.")
d = os.path.join(os.environ["TESI_RISULTATI"], "esperimenti", "2026-09-25_known-item-auto")
o = ora.strftime("%Y-%m-%dT%H%M%SZ"); p = os.path.join(d, f"{o}_esito.json"); n = 2
while os.path.exists(p):
    p = os.path.join(d, f"{o}-{n}_esito.json"); n += 1
open(p, "x").write(json.dumps(esito, indent=2, ensure_ascii=False))
print("archiviato in", p)
