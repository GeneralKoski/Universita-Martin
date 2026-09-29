#!/usr/bin/env python3
"""Riassume le misure di 2026-09-29_profilo-completo e controlla le previsioni
1-7 e la regola di scelta del README: per profilo e collezione MRR@10, atto
primo, entro dieci, a vuoto, e la mediana del tempo di ricerca dall'app. Per
ogni etichetta usa l'esito più recente. Nessun testo di query finisce nel
riassunto: solo conteggi e id.

    analizza.py
"""
import datetime, glob, json, os, statistics, subprocess, sys

QUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.environ.get("TESI_RISULTATI") or os.path.join(QUI, "..", "..")
DIR = os.path.join(BASE, "esperimenti", "2026-09-29_profilo-completo")
CONFRONTO = os.path.join(BASE, "confronto")
PROFILI = ("P0", "P1", "P2", "P3", "P4")
COLLEZIONI = ("known-item-auto", "known-item-umane", "known-item-date", "known-item-importi")


def ultimo(cartella, nome):
    trovati = sorted(glob.glob(os.path.join(cartella, f"*_{nome}.json")))
    if not trovati:
        sys.exit(f"manca {nome}")
    d = json.load(open(trovati[-1]))
    assert d["config"].get("modifiche_non_committate") in ("false", False), f"{trovati[-1]}: codice non committato"
    return os.path.basename(trovati[-1]), d


file, righe = {}, {}
for p in PROFILI:
    righe[p] = {}
    for c in COLLEZIONI:
        f, v = ultimo(os.path.join(DIR, "evaluate"), f"{c}-profilo-completo-{p}")
        etichetta = f"known-item-umane-profilo-completo-{p}" if c == "known-item-umane" else f"profilo-completo-{p}-{c}"
        fr, rap = ultimo(CONFRONTO, f"{etichetta}-koskidex")
        file[f"{p} {c}"] = {"valutazione": f, "rapporto": fr}
        qs = v["per_query"]
        n = len(qs)
        righe[p][c] = {"query": n, "mrr@10": round(v["mean_mrr@10"], 4),
                       "atto_primo": round(sum(q["mrr@10"] == 1 for q in qs) / n, 4),
                       "entro_10": round(sum(q["mrr@10"] > 0 for q in qs) / n, 4),
                       "a_vuoto": round(sum(q["retrieved"] == 0 for q in qs) / n, 4),
                       "ms_mediana": round(statistics.median(x["ms"] for x in rap["query"]), 2)}
    fi, ind = ultimo(CONFRONTO, f"profilo-completo-{p}-indicizzazione-koskidex")
    file[f"{p} indicizzazione"] = fi
    righe[p]["indicizzazione_ms"] = ind["timings"]["index_ms"]
    f24, r24 = ultimo(CONFRONTO, f"profilo-completo-{p}-confronto-24-koskidex")
    file[f"{p} confronto-24"] = f24
    righe[p]["confronto_24_risultati"] = [len(x["ids"]) for x in r24["query"]]
    n24 = righe[p]["confronto_24_risultati"]
    righe[p]["confronto_24_a_10000"] = sum(n >= 10000 for n in n24)
    righe[p]["confronto_24_massimo_sotto_10000"] = max((n for n in n24 if n < 10000), default=0)

print(f"{'':4}" + "".join(f"{c:>34}" for c in COLLEZIONI))
for p in PROFILI:
    print(f"{p:4}" + "".join(f"{righe[p][c]['mrr@10']:>9.4f} vuoto {righe[p][c]['a_vuoto']:>5.1%} {righe[p][c]['ms_mediana']:>7.2f} ms"
                             for c in COLLEZIONI) + f"   indicizzazione {righe[p]['indicizzazione_ms'] / 1000:.1f} s")

previsioni = {}


def prev(k, testo, ok, valore):
    previsioni[k] = {"previsione": testo, "valore": valore, "esito": "confermata" if ok else "smentita"}
    print(f"{k}. {previsioni[k]['esito']:10} {testo}: {valore}")


m = lambda p, c: righe[p][c]["mrr@10"]
print()
ok = (abs(m("P1", "known-item-umane") - m("P0", "known-item-umane")) <= 0.005 and m("P1", "known-item-auto") >= 0.950
      and m("P1", "known-item-date") >= 0.95 and m("P1", "known-item-importi") >= 0.95)
prev(1, "P1: umane entro 0,005 da P0, automatiche almeno 0,950, date e importi almeno 0,95", ok,
     f"umane {m('P0', 'known-item-umane')} -> {m('P1', 'known-item-umane')}; automatiche {m('P1', 'known-item-auto')}; "
     f"date {m('P1', 'known-item-date')}; importi {m('P1', 'known-item-importi')}")
prev(2, "P2, umane: MRR@10 almeno 0,50, a vuoto al più 3%",
     m("P2", "known-item-umane") >= 0.50 and righe["P2"]["known-item-umane"]["a_vuoto"] <= 0.03,
     f"{m('P2', 'known-item-umane')}, a vuoto {righe['P2']['known-item-umane']['a_vuoto']:.1%}")
prev(3, "P2, automatiche: almeno 0,03 sotto P1", m("P2", "known-item-auto") <= m("P1", "known-item-auto") - 0.03,
     f"{m('P1', 'known-item-auto')} -> {m('P2', 'known-item-auto')}")
prev(4, "P3, umane: almeno 0,03 sopra P2, entro dieci almeno 80%",
     m("P3", "known-item-umane") >= m("P2", "known-item-umane") + 0.03 and righe["P3"]["known-item-umane"]["entro_10"] >= 0.80,
     f"{m('P2', 'known-item-umane')} -> {m('P3', 'known-item-umane')}, entro dieci {righe['P3']['known-item-umane']['entro_10']:.1%}")
prev(5, "P3, automatiche: MRR@10 al più 0,80", m("P3", "known-item-auto") <= 0.80, f"{m('P3', 'known-item-auto')}")
prev(6, "P4: automatiche almeno 0,94, umane almeno 0,50",
     m("P4", "known-item-auto") >= 0.94 and m("P4", "known-item-umane") >= 0.50,
     f"automatiche {m('P4', 'known-item-auto')}, umane {m('P4', 'known-item-umane')}")
prev(7, "P4, date almeno 0,95", m("P4", "known-item-date") >= 0.95, f"{m('P4', 'known-item-date')}")

ammessi = [p for p in ("P2", "P3", "P4") if m(p, "known-item-auto") >= m("P1", "known-item-auto") - 0.01
           and m(p, "known-item-date") > 0.95 and m(p, "known-item-importi") > 0.95]
scelto = max(ammessi, key=lambda p: m(p, "known-item-umane")) if ammessi else "P1"
print(f"\nregola di scelta: ammessi {ammessi or 'nessuno'}, scelto {scelto}")

ora = datetime.datetime.now(datetime.timezone.utc)
git = lambda d, *x: subprocess.run(["git", "-C", d, *x], capture_output=True, text=True, check=True).stdout.strip()
valutazioni = [json.load(open(os.path.join(DIR, "evaluate", x["valutazione"]))) for k, x in file.items() if isinstance(x, dict)]
esito = {"ran_at": ora.strftime("%Y-%m-%dT%H:%M:%SZ"),
         "config": {"commit": git(QUI, "rev-parse", "--short", "HEAD"),
                    "modifiche_non_committate": "true" if git(QUI, "status", "--porcelain", "--untracked-files=no", "--", QUI) else "false",
                    "koskidex": sorted({v["config"].get("commit", "")[:7] for v in valutazioni}), "file": file},
         "profili": righe, "previsioni": previsioni, "regola_di_scelta": {"ammessi": ammessi, "scelto": scelto}}
if not os.environ.get("TESI_RISULTATI"):
    sys.exit("!!! RISULTATO NON ARCHIVIATO: TESI_RISULTATI non è impostata.")
o = ora.strftime("%Y-%m-%dT%H%M%SZ"); p = os.path.join(DIR, f"{o}_esito.json"); k = 2
while os.path.exists(p):
    p = os.path.join(DIR, f"{o}-{k}_esito.json"); k += 1
open(p, "x").write(json.dumps(esito, indent=2, ensure_ascii=False))
print("archiviato in", p)
