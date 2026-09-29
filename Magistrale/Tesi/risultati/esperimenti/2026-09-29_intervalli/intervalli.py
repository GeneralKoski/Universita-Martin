#!/usr/bin/env python3
"""Intervalli di confidenza al 95% sull'MRR@10 delle known-item umane
(2026-09-29_intervalli): bootstrap accoppiato sulle 104 query, per la media di
ogni configurazione e per 15 differenze fissate nel README, con un test di
permutazione a segni come controllo. Legge le valutazioni per query già
archiviate (mai i testi delle query) e archivia un riassunto.

    intervalli.py
"""
import datetime, glob, json, os, subprocess, sys
import numpy as np

QUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.environ.get("TESI_RISULTATI") or os.path.join(QUI, "..", "..")
E = os.path.join(BASE, "esperimenti")
SEME, RICAMPIONAMENTI, PERMUTAZIONI = 20260929, 10000, 20000

CONFIG = {  # nome: (cartella, etichetta nel nome del file)
    "ES": ("valutazioni-albo", "known-item-umane-ku-app-elasticsearch"),
    "KC": ("valutazioni-albo", "known-item-umane-ku-app-koskidex-consigliata"),
    "K0": ("valutazioni-albo", "known-item-umane-ku-K0"),
    "LA": ("valutazioni-albo", "known-item-umane-ku-LA"),
    "LT": ("valutazioni-albo", "known-item-umane-ku-LT"),
    "A": ("valutazioni-albo", "known-item-umane-ku-A"),
    "B": ("valutazioni-albo", "known-item-umane-ku-B"),
    "V": ("valutazioni-albo", "known-item-umane-ku-V"),
    "RR-LA": ("esperimenti/2026-09-28_reranker/evaluate", "known-item-umane-rr-LA"),
    "RR-A": ("esperimenti/2026-09-28_reranker/evaluate", "known-item-umane-rr-A"),
    **{p: (f"esperimenti/2026-09-29_profilo-completo/evaluate", f"known-item-umane-profilo-completo-{p}") for p in ("P0", "P1", "P2", "P3", "P4")},
    "ESC": ("esperimenti/2026-09-29_es-corretto/evaluate", "known-item-umane-es-corretto-ESC"),
    "ESO": ("esperimenti/2026-09-29_es-corretto/evaluate", "known-item-umane-es-corretto-ESO"),
}
CONFRONTI = [  # (numero, primo, secondo)
    ("C1", "KC", "ES"), ("C2", "ESC", "ES"), ("C3", "ESC", "KC"), ("C4", "P4", "KC"), ("C5", "P4", "P2"),
    ("C6", "P2", "KC"), ("C7", "A", "LA"), ("C8", "A", "B"), ("C9", "LA", "LT"), ("C10", "RR-LA", "LA"),
    ("C11", "RR-A", "A"), ("C12", "ESO", "P2"), ("C13", "P3", "P2"), ("C14", "LA", "P2"), ("C15", "A", "P3"),
    # Aggiunti dopo aver visto il primo esito (README, "Aggiunte dopo"): non hanno previsioni.
    ("C16", "LA", "KC"), ("C17", "A", "KC"), ("C18", "P4", "ES"),
]


def carica(nome):
    cartella, etichetta = CONFIG[nome]
    trovati = sorted(glob.glob(os.path.join(BASE, cartella, f"*_{etichetta}.json")))
    if not trovati:
        sys.exit(f"manca {cartella}/{etichetta}")
    d = json.load(open(trovati[-1]))
    assert d["config"].get("modifiche_non_committate") in ("false", False), f"{trovati[-1]}: codice non committato"
    return os.path.basename(trovati[-1]), {q["query_id"]: q["mrr@10"] for q in d["per_query"]}


file, valori = {}, {}
for nome in CONFIG:
    file[nome], valori[nome] = carica(nome)
ids = sorted(valori["ES"])
assert len(ids) == 104, len(ids)
for nome, v in valori.items():
    assert sorted(v) == ids, f"{nome}: insieme di query diverso"
X = {nome: np.array([valori[nome][i] for i in ids]) for nome in CONFIG}

rng = np.random.default_rng(SEME)
indici = rng.integers(0, len(ids), size=(RICAMPIONAMENTI, len(ids)))
segni = rng.choice([-1.0, 1.0], size=(PERMUTAZIONI, len(ids)))

medie = {}
for nome, x in X.items():
    m = x[indici].mean(axis=1)
    lo, hi = np.percentile(m, [2.5, 97.5])
    medie[nome] = {"media": round(float(x.mean()), 4), "ic95": [round(float(lo), 4), round(float(hi), 4)],
                   "semiampiezza": round(float((hi - lo) / 2), 4)}
    print(f"{nome:6} {x.mean():.4f}  [{lo:.4f}, {hi:.4f}]  semiampiezza {(hi - lo) / 2:.4f}")

print()
diff = {}
for num, a, b in CONFRONTI:
    d = X[a] - X[b]
    m = d[indici].mean(axis=1)
    lo, hi = np.percentile(m, [2.5, 97.5])
    osservata = d.mean()
    p = float((np.abs((segni * d).mean(axis=1)) >= abs(osservata) - 1e-15).mean())
    diff[num] = {"confronto": f"{a} - {b}", "differenza": round(float(osservata), 4),
                 "ic95": [round(float(lo), 4), round(float(hi), 4)], "esclude_zero": bool(lo > 0 or hi < 0),
                 "p_permutazione": round(p, 4), "query_migliori": int((d > 0).sum()), "query_peggiori": int((d < 0).sum()),
                 "query_pari": int((d == 0).sum())}
    print(f"{num:3} {a:6} - {b:6} {osservata:+.4f}  [{lo:+.4f}, {hi:+.4f}]  esclude 0: {'sì' if lo > 0 or hi < 0 else 'no':2}  p {p:.4f}  "
          f"({int((d > 0).sum())} meglio, {int((d < 0).sum())} peggio, {int((d == 0).sum())} pari)")

previsioni = {}


def prev(n, testo, ok, valore):
    previsioni[n] = {"previsione": testo, "valore": valore, "esito": "confermata" if ok else "smentita"}
    print(f"{n}. {previsioni[n]['esito']:10} {testo}: {valore}")


print()
es0 = lambda n: diff[n]["esclude_zero"]
prev(1, "C1, C2, C4, C5, C9 escludono lo zero", all(es0(n) for n in ("C1", "C2", "C4", "C5", "C9")),
     {n: es0(n) for n in ("C1", "C2", "C4", "C5", "C9")})
prev(2, "C3, C8, C11, C12 includono lo zero", not any(es0(n) for n in ("C3", "C8", "C11", "C12")),
     {n: es0(n) for n in ("C3", "C8", "C11", "C12")})
prev(3, "C10 esclude lo zero e C7 lo include", es0("C10") and not es0("C7"), {"C10": es0("C10"), "C7": es0("C7")})
semi = {n: m["semiampiezza"] for n, m in medie.items()}
prev(4, "semiampiezza di ogni media fra 0,06 e 0,10", all(0.06 <= v <= 0.10 for v in semi.values()),
     {"minima": min(semi.values()), "massima": max(semi.values())})
concordi = sum((diff[n]["p_permutazione"] < 0.05) == diff[n]["esclude_zero"] for n in [f"C{i}" for i in range(1, 16)])
prev(5, "permutazione e bootstrap concordano in almeno 13 confronti su 15", concordi >= 13, f"{concordi} su 15")

ora = datetime.datetime.now(datetime.timezone.utc)
git = lambda *x: subprocess.run(["git", "-C", QUI, *x], capture_output=True, text=True, check=True).stdout.strip()
esito = {"ran_at": ora.strftime("%Y-%m-%dT%H:%M:%SZ"),
         "config": {"commit": git("rev-parse", "--short", "HEAD"),
                    "modifiche_non_committate": "true" if git("status", "--porcelain", "--untracked-files=no", "--", QUI) else "false",
                    "seme": SEME, "ricampionamenti": RICAMPIONAMENTI, "permutazioni": PERMUTAZIONI, "query": len(ids), "file": file},
         "medie": medie, "differenze": diff, "previsioni": previsioni}
if not os.environ.get("TESI_RISULTATI"):
    sys.exit("!!! RISULTATO NON ARCHIVIATO: TESI_RISULTATI non è impostata.")
o = ora.strftime("%Y-%m-%dT%H%M%SZ"); p = os.path.join(QUI, f"{o}_esito.json"); k = 2
while os.path.exists(p):
    p = os.path.join(QUI, f"{o}-{k}_esito.json"); k += 1
open(p, "x").write(json.dumps(esito, indent=2, ensure_ascii=False))
print("archiviato in", p)
