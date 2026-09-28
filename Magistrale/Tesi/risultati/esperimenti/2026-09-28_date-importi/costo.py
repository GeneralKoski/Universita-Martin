#!/usr/bin/env python3
"""Il costo, dopo, di 2026-09-28_date-importi: confronta le valutazioni di
costo.sh (evaluate-costo/) con quelle dell'esito (evaluate/). Previsione 1:
metriche per query identiche; previsione 2: indicizzazione accesa al più il
15% più lenta della spenta. Archivia il riassunto.

    costo.py
"""
import datetime, glob, json, os, re, statistics, subprocess, sys

QUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.environ.get("TESI_RISULTATI") or os.path.join(QUI, "..", "..")
DIR = os.path.join(BASE, "esperimenti", "2026-09-28_date-importi")


def leggi(cartella):
    runs, commit = {}, set()
    for p in sorted(glob.glob(os.path.join(DIR, cartella, "*.json"))):
        m = re.search(r"_(known-item-date|known-item-importi|known-item-auto)-(koskidex|standard)-(spento|acceso)-r(\d)\.json$", p)
        if m:
            d = json.load(open(p))
            assert d["config"].get("modifiche_non_committate") in ("false", False), p
            commit.add(d["config"]["commit"][:7])
            runs.setdefault(m.groups()[:3], []).append(d)
    return runs, commit


prima, cp = leggi("evaluate")
dopo, cd = leggi("evaluate-costo")
assert set(prima) == set(dopo) and all(len(v) == 3 for v in dopo.values()), "valutazioni mancanti"
metrica = lambda r: sorted((q["query_id"], q["mrr@10"], q["ndcg@10"], q["retrieved"], q["candidates"]) for q in r["per_query"])
diverse = sorted(" ".join(k) for k in prima if any(metrica(r) != metrica(prima[k][0]) for r in dopo[k]))
tempi = {f: {f"{t} {n}": statistics.median(r["timings"]["index_ms"] for c in ("known-item-date", "known-item-importi", "known-item-auto")
                                            for r in runs[(c, t, n)])
             for t in ("koskidex", "standard") for n in ("spento", "acceso")} for f, runs in (("prima", prima), ("dopo", dopo))}
previsioni = {}


def prev(k, testo, ok, valore):
    previsioni[k] = {"previsione": testo, "valore": valore, "esito": "confermata" if ok else "smentita"}
    print(f"{k}. {previsioni[k]['esito']:10} {testo}: {valore}")


prev(1, "nessun risultato cambia", not diverse, f"{len(prima) - len(diverse)} configurazioni su {len(prima)} identiche")
v = {t: tempi["dopo"][f"{t} acceso"] / tempi["dopo"][f"{t} spento"] - 1 for t in ("koskidex", "standard")}
prev(2, "indicizzazione accesa al più il 15% più lenta", all(x <= 0.15 for x in v.values()),
     "; ".join(f"{t} {tempi['dopo'][t + ' spento']:.0f} -> {tempi['dopo'][t + ' acceso']:.0f} ms ({100 * x:+.0f}%), "
               f"prima {100 * (tempi['prima'][t + ' acceso'] / tempi['prima'][t + ' spento'] - 1):+.0f}%" for t, x in v.items()))
ora = datetime.datetime.now(datetime.timezone.utc)
git = lambda *x: subprocess.run(["git", "-C", QUI, *x], capture_output=True, text=True, check=True).stdout.strip()
esito = {"ran_at": ora.strftime("%Y-%m-%dT%H:%M:%SZ"),
         "config": {"commit": git("rev-parse", "--short", "HEAD"),
                    "modifiche_non_committate": "true" if git("status", "--porcelain", "--untracked-files=no", "--", QUI) else "false",
                    "koskidex_prima": sorted(cp), "koskidex_dopo": sorted(cd)},
         "indicizzazione_ms": tempi, "configurazioni_diverse": diverse, "previsioni": previsioni}
if not os.environ.get("TESI_RISULTATI"):
    sys.exit("!!! RISULTATO NON ARCHIVIATO: TESI_RISULTATI non è impostata.")
o = ora.strftime("%Y-%m-%dT%H%M%SZ"); p = os.path.join(DIR, f"{o}_esito-costo.json"); k = 2
while os.path.exists(p):
    p = os.path.join(DIR, f"{o}-{k}_esito-costo.json"); k += 1
open(p, "x").write(json.dumps(esito, indent=2, ensure_ascii=False))
print("archiviato in", p)
