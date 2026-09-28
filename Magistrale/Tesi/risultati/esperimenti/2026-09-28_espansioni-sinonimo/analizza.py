#!/usr/bin/env python3
"""Controlla le previsioni 1-6 di 2026-09-28_espansioni-sinonimo sulle
valutazioni di esegui.sh e archivia il riassunto.

    analizza.py
"""
import datetime, glob, json, os, re, statistics, subprocess, sys

QUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.environ.get("TESI_RISULTATI") or os.path.join(QUI, "..", "..")
DIR = os.path.join(BASE, "esperimenti", "2026-09-28_espansioni-sinonimo")

runs, commit = {}, set()
for p in sorted(glob.glob(os.path.join(DIR, "evaluate", "*.json"))):
    m = re.search(r"_(scifact|nfcorpus|known-item-auto)-((?:all|any)(?:-stopwords)?)-(blended|synonym|synonym-ordine)\.json$", p)
    if not m:
        continue
    d = json.load(open(p))
    assert d["config"].get("modifiche_non_committate") in ("false", False), f"{p}: codice non committato"
    commit.add(d["config"]["commit"][:7])
    runs[m.groups()] = d

CONFIG = sorted({(c, k) for c, k, _ in runs})
for c, k in CONFIG:
    for v in ("blended", "synonym", "synonym-ordine"):
        if (c, k, v) not in runs:
            sys.exit(f"manca {c} {k} {v}")
metriche = lambda d: {q["query_id"]: (q["ndcg@10"], q["recall@100"], q["mrr@10"], q["retrieved"]) for q in d["per_query"]}
candidati = lambda d: {q["query_id"]: q["candidates"] for q in d["per_query"]}
righe = {}
for c, k in CONFIG:
    b, s = runs[(c, k, "blended")], runs[(c, k, "synonym")]
    righe[f"{c} {k}"] = {x: {"ndcg@10": runs[(c, k, x)]["mean_ndcg@10"], "mrr@10": runs[(c, k, x)]["mean_mrr@10"],
                             "recall@100": runs[(c, k, x)]["mean_recall@100"],
                             "mediana_ms": statistics.median(runs[(c, k, x)]["timings"]["per_query_ms"].values())}
                         for x in ("blended", "synonym", "synonym-ordine")}
    righe[f"{c} {k}"]["query_diverse"] = sum(metriche(b)[q] != metriche(s)[q] for q in metriche(b))
    r = righe[f"{c} {k}"]
    print(f"{c:16} {k:14} nDCG@10 {r['blended']['ndcg@10']:.4f} -> {r['synonym']['ndcg@10']:.4f}   "
          f"MRR@10 {r['blended']['mrr@10']:.4f} -> {r['synonym']['mrr@10']:.4f}   query diverse {r['query_diverse']}")

previsioni = {}


def prev(k, testo, ok, valore):
    previsioni[k] = {"previsione": testo, "valore": valore, "esito": "confermata" if ok else "smentita"}
    print(f"{k}. {previsioni[k]['esito']:10} {testo}: {valore}")


print()
diverse = [f"{c} {k}" for c, k in CONFIG if metriche(runs[(c, k, "synonym")]) != metriche(runs[(c, k, "synonym-ordine")])]
prev(1, "synonym uguale con e senza -ordine-fisso", not diverse, f"{len(CONFIG) - len(diverse)} configurazioni su {len(CONFIG)}")
diverse = [f"{c} {k}" for c, k in CONFIG if candidati(runs[(c, k, "blended")]) != candidati(runs[(c, k, "synonym")])]
prev(2, "stessi candidati di blended", not diverse, f"{len(CONFIG) - len(diverse)} configurazioni su {len(CONFIG)}")
delta = lambda c, k, m: righe[f"{c} {k}"]["synonym"][m] - righe[f"{c} {k}"]["blended"][m]
v = {k: delta("scifact", k, "ndcg@10") for k in ("any", "any-stopwords")}
prev(3, "SciFact any, nDCG@10 fra -0,005 e +0,02", all(-0.005 <= x <= 0.02 for x in v.values()),
     "; ".join(f"{k} {righe['scifact ' + k]['blended']['ndcg@10']:.4f} -> {righe['scifact ' + k]['synonym']['ndcg@10']:.4f} ({x:+.4f})"
               for k, x in v.items()))
v = {k: delta("nfcorpus", k, "ndcg@10") for k in ("any", "any-stopwords")}
prev(4, "NFCorpus any, nDCG@10 entro 0,01", all(abs(x) <= 0.01 for x in v.values()),
     "; ".join(f"{k} {righe['nfcorpus ' + k]['blended']['ndcg@10']:.4f} -> {righe['nfcorpus ' + k]['synonym']['ndcg@10']:.4f} ({x:+.4f})"
               for k, x in v.items()))
v = {k: delta("known-item-auto", k, "mrr@10") for k in ("all", "any")}
prev(5, "known-item automatiche, MRR@10 entro 0,01", all(abs(x) <= 0.01 for x in v.values()),
     "; ".join(f"{k} {righe['known-item-auto ' + k]['blended']['mrr@10']:.4f} -> {righe['known-item-auto ' + k]['synonym']['mrr@10']:.4f} ({x:+.4f})"
               for k, x in v.items()))
v = {f"{c} {k}": righe[f"{c} {k}"]["synonym"]["mediana_ms"] / righe[f"{c} {k}"]["blended"]["mediana_ms"] - 1 for c, k in CONFIG}
prev(6, "mediana del tempo per query entro il 5%", all(abs(x) <= 0.05 for x in v.values()),
     "; ".join(f"{n} {100 * x:+.1f}%" for n, x in v.items()))

ora = datetime.datetime.now(datetime.timezone.utc)
git = lambda *x: subprocess.run(["git", "-C", QUI, *x], capture_output=True, text=True, check=True).stdout.strip()
esito = {"ran_at": ora.strftime("%Y-%m-%dT%H:%M:%SZ"),
         "config": {"commit": git("rev-parse", "--short", "HEAD"),
                    "modifiche_non_committate": "true" if git("status", "--porcelain", "--untracked-files=no", "--", QUI) else "false",
                    "koskidex": sorted(commit)},
         "valutazioni": righe, "previsioni": previsioni}
if not os.environ.get("TESI_RISULTATI"):
    sys.exit("!!! RISULTATO NON ARCHIVIATO: TESI_RISULTATI non è impostata.")
o = ora.strftime("%Y-%m-%dT%H%M%SZ"); p = os.path.join(DIR, f"{o}_esito.json"); k = 2
while os.path.exists(p):
    p = os.path.join(DIR, f"{o}-{k}_esito.json"); k += 1
open(p, "x").write(json.dumps(esito, indent=2, ensure_ascii=False))
print("archiviato in", p)
