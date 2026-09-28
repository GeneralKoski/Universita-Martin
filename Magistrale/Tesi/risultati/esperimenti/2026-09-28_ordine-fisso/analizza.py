#!/usr/bin/env python3
"""Controlla le previsioni 1-6 di 2026-09-28_ordine-fisso sulle misure di
esegui.sh e archivia il riassunto. La 7, i test, non ha un file di misura: è
l'esito di `go test ./...` al commit di Koskidex delle misure, riportato nel
README.

    analizza.py
"""
import datetime, glob, json, os, re, statistics, subprocess, sys

QUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.environ.get("TESI_RISULTATI") or os.path.join(QUI, "..", "..")
DIR = os.path.join(BASE, "esperimenti", "2026-09-28_ordine-fisso")
DIR_PRESTAZIONI = os.path.join(BASE, "esperimenti", "2026-09-28_prestazioni")
COLLEZIONI = ("scifact", "nfcorpus", "known-item-auto")
CONFIG = ("baseline", "bm25-all", "bm25-any")
METRICHE = ("ndcg@10", "recall@100", "mrr@10", "retrieved", "candidates")

runs = {}
commit = set()
for p in sorted(glob.glob(os.path.join(DIR, "evaluate", "*.json"))):
    m = re.search(r"_(scifact|nfcorpus|known-item-auto)-(spento|acceso)-(baseline|bm25-all|bm25-any)-r(\d)\.json$", p)
    if not m:
        continue
    d = json.load(open(p))
    assert d["config"].get("modifiche_non_committate") in ("false", False), f"{p}: codice non committato"
    assert (m.group(2) == "acceso") == (d["config"].get("ordine_fisso") == "acceso"), f"{p}: impostazione sbagliata"
    commit.add(d["config"].get("commit"))
    runs.setdefault((m.group(1), m.group(3), m.group(2)), []).append(d)

righe = {}
for c in COLLEZIONI:
    for k in CONFIG:
        for o in ("spento", "acceso"):
            rip = runs.get((c, k, o), [])
            if len(rip) != 5:
                sys.exit(f"{c} {k} {o}: {len(rip)} ripetizioni invece di 5")
            per_query = [{q["query_id"]: tuple(q[x] for x in METRICHE) for q in r["per_query"]} for r in rip]
            variano = sum(len({pq[qid] for pq in per_query}) > 1 for qid in per_query[0])
            medie = [r["mean_ndcg@10"] for r in rip]
            tempi = [t for r in rip for t in r["timings"]["per_query_ms"].values()]
            righe[f"{c} {k} {o}"] = {"query": len(per_query[0]), "query_che_variano": variano,
                                    "ndcg@10": medie, "mediana_ms": round(statistics.median(tempi), 4)}
            print(f"{c:16} {k:9} {o:7} variano {variano:3} su {len(per_query[0])}  nDCG@10 {sorted(set(medie))}  "
                  f"mediana {statistics.median(tempi):.3f} ms")

previsioni = {}


def prev(k, testo, ok, valore):
    previsioni[k] = {"previsione": testo, "valore": valore, "esito": "confermata" if ok else "smentita"}
    print(f"{k}. {previsioni[k]['esito']:10} {testo}: {valore}")


print()
v = {c: righe[f"{c} baseline spento"]["query_che_variano"] for c in COLLEZIONI}
prev(1, "spento, il baseline non varia fra le ripetizioni", all(x == 0 for x in v.values()), json.dumps(v))
v = {f"{c} {k}": (righe[f"{c} {k} spento"]["query_che_variano"],
                  len({round(x, 4) for x in righe[f"{c} {k} spento"]["ndcg@10"]}))
     for c in COLLEZIONI for k in ("bm25-all", "bm25-any")}
prev(2, "spento, con BM25 al più 5 query variano e le medie coincidono alla quarta cifra",
     all(a <= 5 and b == 1 for a, b in v.values()),
     "; ".join(f"{n}: {a} query, {b} medie distinte" for n, (a, b) in v.items()))
v = {f"{c} {k}": righe[f"{c} {k} acceso"]["query_che_variano"] for c in COLLEZIONI for k in CONFIG}
prev(3, "acceso, nessuna query varia fra le ripetizioni", all(x == 0 for x in v.values()),
     f"query che variano in tutto: {sum(v.values())}")
v = {f"{c} {k}": righe[f"{c} {k} acceso"]["ndcg@10"][0] - righe[f"{c} {k} spento"]["ndcg@10"][0]
     for c in COLLEZIONI for k in CONFIG}
ok = all(abs(x) < 0.001 for x in v.values()) and all(v[f"{c} baseline"] == 0 for c in COLLEZIONI)
prev(4, "acceso contro spento, nDCG@10 entro 0,001, baseline uguale", ok,
     "; ".join(f"{n} {x:+.5f}" for n, x in v.items()))

a = glob.glob(os.path.join(DIR, "*_risposte-acceso-10018.json"))
b = glob.glob(os.path.join(DIR_PRESTAZIONI, "*_risposte-dopo-10018.json"))
if not a or not b:
    sys.exit("mancano le impronte")
ia, ib = json.load(open(sorted(a)[-1])), json.load(open(sorted(b)[-1]))
assert ia["config"].get("modifiche_non_committate") in ("false", False)
qa, qb = ia["risposte"]["query"], ib["risposte"]["query"]
diverse = sorted(k for k in qb if qa.get(k) != qb[k])
prev(5, "Documentale, impronte con l'impostazione accesa uguali a quelle dopo di prestazioni",
     not diverse and len(qa) == len(qb), f"{len(qb) - len(diverse)} su {len(qb)} uguali")

v = {f"{c} {k}": righe[f"{c} {k} acceso"]["mediana_ms"] / righe[f"{c} {k} spento"]["mediana_ms"] - 1
     for c in COLLEZIONI for k in CONFIG}
prev(6, "mediana del tempo per query, acceso entro il 5% di spento", all(abs(x) <= 0.05 for x in v.values()),
     "; ".join(f"{n} {100 * x:+.1f}%" for n, x in v.items()))

ora = datetime.datetime.now(datetime.timezone.utc)
git = lambda *x: subprocess.run(["git", "-C", QUI, *x], capture_output=True, text=True, check=True).stdout.strip()
esito = {"ran_at": ora.strftime("%Y-%m-%dT%H:%M:%SZ"),
         "config": {"commit": git("rev-parse", "--short", "HEAD"),
                    "modifiche_non_committate": "true" if git("status", "--porcelain", "--untracked-files=no", "--", QUI) else "false",
                    "koskidex": sorted(commit), "impronte": [os.path.basename(sorted(a)[-1]), os.path.basename(sorted(b)[-1])]},
         "valutazioni": righe, "impronte_diverse": diverse, "previsioni": previsioni}
if not os.environ.get("TESI_RISULTATI"):
    sys.exit("!!! RISULTATO NON ARCHIVIATO: TESI_RISULTATI non è impostata.")
o = ora.strftime("%Y-%m-%dT%H%M%SZ"); p = os.path.join(DIR, f"{o}_esito.json"); k = 2
while os.path.exists(p):
    p = os.path.join(DIR, f"{o}-{k}_esito.json"); k += 1
open(p, "x").write(json.dumps(esito, indent=2, ensure_ascii=False))
print("archiviato in", p)
