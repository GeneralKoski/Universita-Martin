#!/usr/bin/env python3
"""Controlla le previsioni 1-7 di 2026-09-28_date-importi sulle valutazioni di
esegui.sh e archivia il riassunto. La 8, i test, è l'esito di `go test ./...`
al commit di Koskidex delle misure, riportato nel README.

Per le date e gli importi le metriche sono per coppia (formato dell'atto,
formato della query), da query/<collezione>/formati.json; "atto primo" è
MRR@10 = 1, "entro dieci" MRR@10 > 0, "a vuoto" nessun risultato.

    analizza.py
"""
import datetime, glob, json, os, re, statistics, subprocess, sys

QUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.environ.get("TESI_RISULTATI") or os.path.join(QUI, "..", "..")
DIR = os.path.join(BASE, "esperimenti", "2026-09-28_date-importi")
QUERY = os.path.join(QUI, "..", "..", "query")

runs, commit = {}, set()
for p in sorted(glob.glob(os.path.join(DIR, "evaluate", "*.json"))):
    m = re.search(r"_(known-item-date|known-item-importi|known-item-auto)-(koskidex|standard)-(spento|acceso)-r(\d)\.json$", p)
    if not m:
        continue
    d = json.load(open(p))
    assert d["config"].get("modifiche_non_committate") in ("false", False), f"{p}: codice non committato"
    assert (m.group(3) == "acceso") == (d["config"].get("date") == "normalizzate"), f"{p}: impostazione sbagliata"
    commit.add(d["config"].get("commit"))
    runs.setdefault((m.group(1), m.group(2), m.group(3)), []).append(d)
CONFIG = [(t, n) for t in ("koskidex", "standard") for n in ("spento", "acceso")]
for c in ("known-item-date", "known-item-importi", "known-item-auto"):
    for t, n in CONFIG:
        if len(runs.get((c, t, n), [])) != 3:
            sys.exit(f"{c} {t} {n}: servono 3 ripetizioni")
        pq = [tuple(sorted((q["query_id"], q["mrr@10"], q["candidates"]) for q in r["per_query"])) for r in runs[(c, t, n)]]
        assert len(set(pq)) == 1, f"{c} {t} {n}: le ripetizioni danno metriche diverse"


def coppie(collezione, t, n):
    formati = json.load(open(os.path.join(QUERY, collezione, "formati.json")))
    out = {}
    for q in runs[(collezione, t, n)][0]["per_query"]:
        f = formati[q["query_id"]]
        k = f"{f['partenza']}>{f['query']}"
        o = out.setdefault(k, {"query": 0, "primo": 0, "entro_dieci": 0, "a_vuoto": 0})
        o["query"] += 1
        o["primo"] += q["mrr@10"] == 1
        o["entro_dieci"] += q["mrr@10"] > 0
        o["a_vuoto"] += q["retrieved"] == 0
    return out


tabelle = {}
for c in ("known-item-date", "known-item-importi"):
    for t, n in CONFIG:
        tabelle[f"{c} {t} {n}"] = coppie(c, t, n)
        print(f"{c} {t} {n}")
        for k, o in sorted(tabelle[f"{c} {t} {n}"].items()):
            print(f"   {k:14} query {o['query']:3}  primo {o['primo']:3}  entro dieci {o['entro_dieci']:3}  a vuoto {o['a_vuoto']:3}")

quota = lambda o, k: o[k] / o["query"]
previsioni = {}


def prev(k, testo, ok, valore):
    previsioni[k] = {"previsione": testo, "valore": valore, "esito": "confermata" if ok else "smentita"}
    print(f"{k}. {previsioni[k]['esito']:10} {testo}: {valore}")


print()
tab = tabelle["known-item-date standard spento"]
stesso = {k: quota(o, "entro_dieci") for k, o in tab.items() if k.split(">")[0] == k.split(">")[1]}
altro = {k: quota(o, "entro_dieci") for k, o in tab.items() if k.split(">")[0] != k.split(">")[1]}
prev(1, "standard spento: stesso formato >= 90% entro dieci, altro formato <= 10%",
     all(v >= 0.9 for v in stesso.values()) and all(v <= 0.1 for v in altro.values()),
     "; ".join(f"{k} {100 * v:.0f}%" for k, v in sorted({**stesso, **altro}.items())))
tab = tabelle["known-item-date koskidex spento"]
bp = {k: quota(o, "entro_dieci") for k, o in tab.items() if set(k.split(">")) <= {"barra", "punto"}}
me = {k: quota(o, "entro_dieci") for k, o in tab.items() if "mese" in k.split(">") and k.split(">")[0] != k.split(">")[1]}
prev(2, "tokenizer di Koskidex spento: barra e punto >= 90%, col mese in lettere <= 10%",
     all(v >= 0.9 for v in bp.values()) and all(v <= 0.1 for v in me.values()),
     "; ".join(f"{k} {100 * v:.0f}%" for k, v in sorted({**bp, **me}.items())))
ok, righe = True, []
for t in ("koskidex", "standard"):
    tab = tabelle[f"known-item-date {t} acceso"]
    for k, o in sorted(tab.items()):
        a, b = k.split(">")
        controllo = quota(tab[f"{a}>{a}"], "primo")
        ok = ok and quota(o, "entro_dieci") >= 0.9 and (a == b or controllo - quota(o, "primo") <= 0.05)
        righe.append(f"{t} {k} entro dieci {100 * quota(o, 'entro_dieci'):.0f}%, primo {100 * quota(o, 'primo'):.0f}%")
prev(3, "acceso: ogni coppia >= 90% entro dieci, primo entro 5 punti dal controllo", ok, "; ".join(righe))
ok, righe = True, []
for t in ("koskidex", "standard"):
    for n in ("spento", "acceso"):
        for k, o in sorted(tabelle[f"known-item-importi {t} {n}"].items()):
            a, b = k.split(">")
            if a == b:
                continue
            v = quota(o, "entro_dieci")
            ok = ok and (v <= 0.1 if n == "spento" else v >= 0.9)
            righe.append(f"{t} {n} {k} {100 * v:.0f}% su {o['query']}")
prev(4, "importi: spento fra formati <= 10% entro dieci, acceso >= 90%", ok, "; ".join(righe))
v = {t: runs[("known-item-auto", t, "acceso")][0]["mean_mrr@10"] - runs[("known-item-auto", t, "spento")][0]["mean_mrr@10"]
     for t in ("koskidex", "standard")}
prev(5, "guardia: MRR@10 delle known-item automatiche entro 0,005", all(abs(x) < 0.005 for x in v.values()),
     "; ".join(f"{t} {runs[('known-item-auto', t, 'spento')][0]['mean_mrr@10']:.4f} -> "
               f"{runs[('known-item-auto', t, 'acceso')][0]['mean_mrr@10']:.4f}" for t in v))
testi = {json.loads(l)["_id"]: json.loads(l)["text"] for l in open(os.path.join(QUERY, "known-item-auto", "queries.jsonl"))}
piccoli = {q for q, x in testi.items() if re.fullmatch(r"\d+", x.split()[0]) and 1 <= int(x.split()[0]) <= 31}
spento = {q["query_id"]: q["candidates"] for q in runs[("known-item-auto", "koskidex", "spento")][0]["per_query"]}
acceso = {q["query_id"]: q["candidates"] for q in runs[("known-item-auto", "koskidex", "acceso")][0]["per_query"]}
su = sum(acceso[q] > spento[q] for q in piccoli); giu = sum(acceso[q] < spento[q] for q in piccoli)
prev(6, "tokenizer di Koskidex, numeri da 1 a 31: candidati mai in aumento, in calo almeno per metà",
     su == 0 and giu * 2 >= len(piccoli) and piccoli,
     f"{len(piccoli)} query: {giu} in calo, {su} in aumento; candidati {sum(spento[q] for q in piccoli)} -> "
     f"{sum(acceso[q] for q in piccoli)}")
tempi = {}
for t in ("koskidex", "standard"):
    for n in ("spento", "acceso"):
        tempi[f"{t} {n}"] = statistics.median(r["timings"]["index_ms"] for c in ("known-item-date", "known-item-importi", "known-item-auto")
                                             for r in runs[(c, t, n)])
v = {t: tempi[f"{t} acceso"] / tempi[f"{t} spento"] - 1 for t in ("koskidex", "standard")}
prev(7, "indicizzazione accesa al più il 20% più lenta", all(x <= 0.2 for x in v.values()),
     "; ".join(f"{t} {tempi[t + ' spento']:.0f} -> {tempi[t + ' acceso']:.0f} ms ({100 * x:+.0f}%)" for t, x in v.items()))

ora = datetime.datetime.now(datetime.timezone.utc)
git = lambda *x: subprocess.run(["git", "-C", QUI, *x], capture_output=True, text=True, check=True).stdout.strip()
esito = {"ran_at": ora.strftime("%Y-%m-%dT%H:%M:%SZ"),
         "config": {"commit": git("rev-parse", "--short", "HEAD"),
                    "modifiche_non_committate": "true" if git("status", "--porcelain", "--untracked-files=no", "--", QUI) else "false",
                    "koskidex": sorted(commit)},
         "coppie": tabelle, "indicizzazione_ms": tempi,
         "known_item_auto_mrr": {f"{t} {n}": runs[("known-item-auto", t, n)][0]["mean_mrr@10"] for t, n in CONFIG},
         "previsioni": previsioni}
if not os.environ.get("TESI_RISULTATI"):
    sys.exit("!!! RISULTATO NON ARCHIVIATO: TESI_RISULTATI non è impostata.")
o = ora.strftime("%Y-%m-%dT%H%M%SZ"); p = os.path.join(DIR, f"{o}_esito.json"); k = 2
while os.path.exists(p):
    p = os.path.join(DIR, f"{o}-{k}_esito.json"); k += 1
open(p, "x").write(json.dumps(esito, indent=2, ensure_ascii=False))
print("archiviato in", p)
