#!/usr/bin/env python3
"""Controlla le previsioni di 2026-09-29_riordino-corto e archivia il
riassunto: per ogni caso MRR@10 del primo stadio e del riordino con k 20, 30 e
100 (il 100 da 2026-09-28_reranker), la recall@k del primo stadio e la mediana
del tempo di riordino. Nessun testo di query finisce nel riassunto.

    analizza.py
"""
import datetime, glob, json, os, statistics, subprocess, sys

QUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.environ.get("TESI_RISULTATI") or os.path.join(QUI, "..", "..")
DIR = os.path.join(BASE, "esperimenti", "2026-09-29_riordino-corto")
RR = os.path.join(BASE, "esperimenti", "2026-09-28_reranker")
KX = os.path.expanduser("~/Desktop/Progetti-personali/Koskidex/eval/corpora/c3-albo")
CASI = (("known-item-umane", "LA"), ("known-item-umane", "A"), ("known-item-auto", "LA"))


def ultimo(cartella, nome):
    trovati = sorted(glob.glob(os.path.join(cartella, f"*_{nome}.json")))
    if not trovati:
        sys.exit(f"manca {cartella}/{nome}")
    d = json.load(open(trovati[-1]))
    assert d["config"].get("modifiche_non_committate") in ("false", False), f"{trovati[-1]}: codice non committato"
    return os.path.basename(trovati[-1]), d


righe, file = {}, {}
for c, conf in CASI:
    g = {}
    for riga in list(open(os.path.join(KX, c, "qrels", "test.tsv")))[1:]:
        q, d, s = riga.split()
        if int(s) > 0:
            g.setdefault(q, set()).add(d)
    fp, p = ultimo(os.path.join(RR, "primo-stadio"), f"{c}-rr-primo-{conf}")
    riga = {"primo": round(p["mean_mrr@10"], 4), "k": {}}
    file[f"{c} {conf}"] = {"primo_stadio": fp}
    for k in (20, 30, 100):
        cart, nome = (RR, f"{c}-rr-{conf}") if k == 100 else (DIR, f"{c}-rr{k}-{conf}")
        fv, v = ultimo(os.path.join(cart, "evaluate"), nome)
        fr, rap = ultimo(os.path.join(cart, "riordinati"), nome)
        assert rap["config"]["primo_stadio"] == fp, f"{fr} riordina {rap['config']['primo_stadio']}, non {fp}"
        assert int(rap["config"]["k"]) == k, f"{fr}: k {rap['config']['k']}"
        file[f"{c} {conf}"][str(k)] = {"riordino": fr, "valutazione": fv}
        dentro = sum(any(d in g.get(q["query_id"], ()) for d in (q.get("top") or [])[:k]) for q in p["per_query"])
        riga["k"][str(k)] = {"mrr@10": round(v["mean_mrr@10"], 4), "recall@k_primo_stadio": round(dentro / len(p["per_query"]), 4),
                             "mediana_ms": round(statistics.median(x["ms"] for x in rap["query"]), 1)}
    righe[f"{c} {conf}"] = riga
    print(f"{c:17} {conf:2}  primo {riga['primo']:.4f}  " + "  ".join(
        f"k {k}: {x['mrr@10']:.4f} (recall {x['recall@k_primo_stadio']:.3f}, {x['mediana_ms'] / 1000:.2f} s)" for k, x in riga["k"].items()))

previsioni = {}


def prev(n, testo, ok, valore):
    previsioni[n] = {"previsione": testo, "valore": valore, "esito": "confermata" if ok else "smentita"}
    print(f"{n}. {previsioni[n]['esito']:10} {testo}: {valore}")


m = lambda caso, k: righe[caso]["k"][str(k)]["mrr@10"]
t = lambda caso, k: righe[caso]["k"][str(k)]["mediana_ms"]
UL, UA, AL = "known-item-umane LA", "known-item-umane A", "known-item-auto LA"
print()
prev(1, "umane LA: k 30 almeno 0,61, k 20 almeno 0,60", m(UL, 30) >= 0.61 and m(UL, 20) >= 0.60, f"k 30 {m(UL, 30)}, k 20 {m(UL, 20)}")
prev(2, "umane A: k 20 entro 0,01 da k 100", abs(m(UA, 20) - m(UA, 100)) <= 0.01, f"{m(UA, 100)} -> {m(UA, 20)}")
prev(3, "automatiche LA: k 20 almeno 0,93", m(AL, 20) >= 0.93, f"{m(AL, 20)}")
quote = {caso: round(t(caso, 20) / t(caso, 100), 3) for caso in righe}
prev(4, "mediana con k 20 fra il 15% e il 25% di k 100 in ogni caso", all(0.15 <= x <= 0.25 for x in quote.values()), quote)
prev(5, "umane, k 20: mediana almeno 0,8 s", min(t(UL, 20), t(UA, 20)) >= 800, f"LA {t(UL, 20)} ms, A {t(UA, 20)} ms")

ora = datetime.datetime.now(datetime.timezone.utc)
git = lambda *x: subprocess.run(["git", "-C", QUI, *x], capture_output=True, text=True, check=True).stdout.strip()
esito = {"ran_at": ora.strftime("%Y-%m-%dT%H:%M:%SZ"),
         "config": {"commit": git("rev-parse", "--short", "HEAD"),
                    "modifiche_non_committate": "true" if git("status", "--porcelain", "--untracked-files=no", "--", QUI) else "false",
                    "file": file},
         "casi": righe, "previsioni": previsioni}
if not os.environ.get("TESI_RISULTATI"):
    sys.exit("!!! RISULTATO NON ARCHIVIATO: TESI_RISULTATI non è impostata.")
o = ora.strftime("%Y-%m-%dT%H%M%SZ"); p = os.path.join(DIR, f"{o}_esito.json"); n = 2
while os.path.exists(p):
    p = os.path.join(DIR, f"{o}-{n}_esito.json"); n += 1
open(p, "x").write(json.dumps(esito, indent=2, ensure_ascii=False))
print("archiviato in", p)
