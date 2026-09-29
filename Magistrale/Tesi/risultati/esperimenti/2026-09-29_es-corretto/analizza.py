#!/usr/bin/env python3
"""Riassume 2026-09-29_es-corretto e controlla le previsioni 1-5 del README:
ESC ed ESO per collezione (MRR@10, atto primo, entro dieci, a vuoto) contro P0
e P2 dell'esito più recente di 2026-09-29_profilo-completo e contro
Elasticsearch di produzione sulle umane (2026-09-25_known-item-umane). Nessun
testo di query finisce nel riassunto.

    analizza.py
"""
import datetime, glob, json, os, subprocess, sys

QUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.environ.get("TESI_RISULTATI") or os.path.join(QUI, "..", "..")
DIR = os.path.join(BASE, "esperimenti", "2026-09-29_es-corretto")
COLLEZIONI = ("known-item-auto", "known-item-umane", "known-item-date", "known-item-importi")


def ultimo(schema):
    trovati = sorted(glob.glob(schema))
    if not trovati:
        sys.exit(f"manca {schema}")
    d = json.load(open(trovati[-1]))
    assert d["config"].get("modifiche_non_committate") in ("false", False), f"{trovati[-1]}: codice non committato"
    return os.path.basename(trovati[-1]), d


file, righe = {}, {}
for v in ("ESC", "ESO"):
    righe[v] = {}
    for c in COLLEZIONI:
        f, d = ultimo(os.path.join(DIR, "evaluate", f"*_{c}-es-corretto-{v}.json"))
        file[f"{v} {c}"] = f
        qs = d["per_query"]
        n = len(qs)
        righe[v][c] = {"query": n, "mrr@10": round(d["mean_mrr@10"], 4),
                       "atto_primo": round(sum(q["mrr@10"] == 1 for q in qs) / n, 4),
                       "entro_10": round(sum(q["mrr@10"] > 0 for q in qs) / n, 4),
                       "a_vuoto": round(sum(q["retrieved"] == 0 for q in qs) / n, 4)}
fp, pc = ultimo(os.path.join(BASE, "esperimenti", "2026-09-29_profilo-completo", "*_esito.json"))
fe, es = ultimo(os.path.join(BASE, "valutazioni-albo", "*_known-item-umane-ku-app-elasticsearch.json"))
file["profilo-completo"], file["elasticsearch di produzione, umane"] = fp, fe
riferimenti = {p: {c: pc["profili"][p][c] for c in COLLEZIONI} for p in ("P0", "P2")}
es_umane = round(es["mean_mrr@10"], 4)

for v in ("ESC", "ESO"):
    print(f"{v}  " + "  ".join(f"{c} {righe[v][c]['mrr@10']:.4f} (vuoto {righe[v][c]['a_vuoto']:.1%})" for c in COLLEZIONI))
for p in ("P0", "P2"):
    print(f"{p}   " + "  ".join(f"{c} {riferimenti[p][c]['mrr@10']:.4f}" for c in COLLEZIONI))
print(f"Elasticsearch di produzione, umane {es_umane}")

previsioni = {}


def prev(k, testo, ok, valore):
    previsioni[k] = {"previsione": testo, "valore": valore, "esito": "confermata" if ok else "smentita"}
    print(f"{k}. {previsioni[k]['esito']:10} {testo}: {valore}")


m = lambda v, c: righe[v][c]["mrr@10"]
r = lambda p, c: riferimenti[p][c]["mrr@10"]
print()
prev(1, "ESC entro 0,02 da P0 sulle automatiche", abs(m("ESC", "known-item-auto") - r("P0", "known-item-auto")) <= 0.02,
     f"{m('ESC', 'known-item-auto')} contro {r('P0', 'known-item-auto')}")
prev(2, "ESC entro 0,03 da P0 sulle umane", abs(m("ESC", "known-item-umane") - r("P0", "known-item-umane")) <= 0.03,
     f"{m('ESC', 'known-item-umane')} contro {r('P0', 'known-item-umane')}")
prev(3, "ESC almeno 0,08 sopra Elasticsearch di produzione sulle umane", m("ESC", "known-item-umane") >= es_umane + 0.08,
     f"{m('ESC', 'known-item-umane')} contro {es_umane}")
prev(4, "ESO entro 0,05 da P2 sulle umane", abs(m("ESO", "known-item-umane") - r("P2", "known-item-umane")) <= 0.05,
     f"{m('ESO', 'known-item-umane')} contro {r('P2', 'known-item-umane')}")
prev(5, "ESO almeno 0,03 sotto ESC sulle automatiche", m("ESO", "known-item-auto") <= m("ESC", "known-item-auto") - 0.03,
     f"{m('ESC', 'known-item-auto')} -> {m('ESO', 'known-item-auto')}")

ora = datetime.datetime.now(datetime.timezone.utc)
git = lambda *x: subprocess.run(["git", "-C", QUI, *x], capture_output=True, text=True, check=True).stdout.strip()
esito = {"ran_at": ora.strftime("%Y-%m-%dT%H:%M:%SZ"),
         "config": {"commit": git("rev-parse", "--short", "HEAD"),
                    "modifiche_non_committate": "true" if git("status", "--porcelain", "--untracked-files=no", "--", QUI) else "false",
                    "file": file},
         "varianti": righe, "riferimenti": riferimenti, "elasticsearch_produzione_umane": es_umane, "previsioni": previsioni}
if not os.environ.get("TESI_RISULTATI"):
    sys.exit("!!! RISULTATO NON ARCHIVIATO: TESI_RISULTATI non è impostata.")
o = ora.strftime("%Y-%m-%dT%H%M%SZ"); p = os.path.join(DIR, f"{o}_esito.json"); k = 2
while os.path.exists(p):
    p = os.path.join(DIR, f"{o}-{k}_esito.json"); k += 1
open(p, "x").write(json.dumps(esito, indent=2, ensure_ascii=False))
print("archiviato in", p)
