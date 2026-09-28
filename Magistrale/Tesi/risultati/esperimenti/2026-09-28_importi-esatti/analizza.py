#!/usr/bin/env python3
"""Controlla le previsioni 1-7 di 2026-09-28_importi-esatti sulle misure di
esegui.sh e archivia il riassunto. L'ottava, i test, è riportata nel README.
Nessun testo di query finisce nel riassunto: solo conteggi e id.

    analizza.py
"""
import collections, datetime, glob, json, os, re, subprocess, sys

QUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.environ.get("TESI_RISULTATI") or os.path.join(QUI, "..", "..")
DIR = os.path.join(BASE, "esperimenti", "2026-09-28_importi-esatti")
CONFRONTO = os.path.join(BASE, "confronto")
CFG = ("A", "B", "C", "D")
COLL = ("known-item-importi", "known-item-date", "known-item-auto", "known-item-umane")


def ultimo(cartella, nome):
    trovati = sorted(glob.glob(os.path.join(cartella, f"*_{nome}.json")))
    if not trovati:
        sys.exit(f"manca {nome}")
    d = json.load(open(trovati[-1]))
    assert d["config"].get("modifiche_non_committate") in ("false", False), f"{trovati[-1]}: codice non committato"
    return os.path.basename(trovati[-1]), d


val, file = {}, {}
for g in CFG:
    for c in COLL:
        file[f"{c} {g}"], val[(c, g)] = ultimo(os.path.join(DIR, "evaluate"), f"{c}-importi-esatti-{g}")
pq = lambda c, g: {q["query_id"]: q for q in val[(c, g)]["per_query"]}
righe = {c: {g: val[(c, g)]["mean_mrr@10"] for g in CFG} for c in COLL}
for c in COLL:
    print(f"{c:20} MRR@10 " + "  ".join(f"{g} {righe[c][g]:.4f}" for g in CFG))

formati = json.load(open(os.path.join(BASE, "query", "known-item-importi", "formati.json")))
coppie = {}
for g in CFG:
    p = pq("known-item-importi", g)
    t = collections.defaultdict(lambda: [0, 0])
    for qid, fm in formati.items():
        k = f"{fm['partenza']} > {fm['query']}"
        t[k][0] += 1
        t[k][1] += qid in p and p[qid]["mrr@10"] > 0
    coppie[g] = {k: {"query": n, "entro_dieci": d} for k, (n, d) in sorted(t.items())}
fra = lambda g: [v for k, v in coppie[g].items() if k.split(" > ")[0] != k.split(" > ")[1]]
print("\nimporti fra formati entro i primi dieci: " + "  ".join(
    f"{g} {sum(v['entro_dieci'] for v in fra(g))}/{sum(v['query'] for v in fra(g))}" for g in CFG))

rapporti = {g: ultimo(CONFRONTO, f"importi-esatti-{g}-known-item-importi-koskidex") for g in CFG}
risultati_importi = {g: sum(len(x["ids"]) for x in rapporti[g][1]["query"]) for g in CFG}
print("risultati sulle query degli importi:", risultati_importi)

previsioni = {}


def prev(k, testo, ok, valore):
    previsioni[k] = {"previsione": testo, "valore": valore, "esito": "confermata" if ok else "smentita"}
    print(f"{k}. {previsioni[k]['esito']:10} {testo}: {valore}")


print()
quota = lambda g: sum(v["entro_dieci"] for v in fra(g)) / sum(v["query"] for v in fra(g))
prev(1, "C: importi fra formati al più 10% entro i primi dieci", quota("C") <= 0.1, f"A {quota('A'):.0%}, C {quota('C'):.0%}")
prev(2, "D: importi fra formati almeno 90%, MRR@10 importi almeno 0,95",
     quota("D") >= 0.9 and righe["known-item-importi"]["D"] >= 0.95,
     f"{quota('D'):.0%}, MRR@10 {righe['known-item-importi']['D']:.4f} (A {righe['known-item-importi']['A']:.4f}, "
     f"B {righe['known-item-importi']['B']:.4f}, C {righe['known-item-importi']['C']:.4f})")
a, d = risultati_importi["A"], risultati_importi["D"]
prev(3, "D: risultati sulle query degli importi almeno -20% rispetto ad A", d <= 0.8 * a, f"{a} -> {d} ({100 * (d / a - 1):+.0f}%)")
x = righe["known-item-date"]["C"] - righe["known-item-date"]["A"]
prev(4, "C: MRR@10 delle date entro 0,01 da A", abs(x) <= 0.01,
     f"{righe['known-item-date']['A']:.4f} -> {righe['known-item-date']['C']:.4f} ({x:+.4f})")
uguali = lambda c, g: sum(pq(c, "A")[q].get("top") == pq(c, g)[q].get("top") for q in pq(c, "A"))
n = len(pq("known-item-auto", "A"))
prev(5, "C: known-item automatiche identiche ad A query per query", uguali("known-item-auto", "C") == n,
     f"{uguali('known-item-auto', 'C')} su {n}")
n = len(pq("known-item-umane", "A"))
prev(6, "C e D: known-item umane identiche ad A query per query",
     uguali("known-item-umane", "C") == n and uguali("known-item-umane", "D") == n,
     f"C {uguali('known-item-umane', 'C')} e D {uguali('known-item-umane', 'D')} su {n}")
c24 = {g: ultimo(CONFRONTO, f"importi-esatti-{g}-confronto-24-koskidex") for g in CFG}
file["confronto-24"] = {g: c24[g][0] for g in CFG}
base = c24["A"][1]["query"]
senza = [i for i, x in enumerate(base) if not re.search(r"\d", x["query"])]
stessi = {g: sum(c24[g][1]["query"][i]["ids"] == base[i]["ids"] for i in senza) for g in CFG}
con_cifre = {g: [len(c24[g][1]["query"][i]["ids"]) for i, x in enumerate(base) if re.search(r"\d", x["query"])] for g in CFG}
prev(7, "le 24: le senza cifre identiche in tutte e quattro", all(v == len(senza) for v in stessi.values()),
     f"{len(senza)} senza cifre; uguali ad A: {stessi}; risultati di quelle con cifre {con_cifre}")

ora = datetime.datetime.now(datetime.timezone.utc)
git = lambda *x: subprocess.run(["git", "-C", QUI, *x], capture_output=True, text=True, check=True).stdout.strip()
esito = {"ran_at": ora.strftime("%Y-%m-%dT%H:%M:%SZ"),
         "config": {"commit": git("rev-parse", "--short", "HEAD"),
                    "modifiche_non_committate": "true" if git("status", "--porcelain", "--untracked-files=no", "--", QUI) else "false",
                    "koskidex": sorted({v["config"].get("commit", "")[:7] for v in val.values()}), "file": file,
                    "rapporti_importi": {g: rapporti[g][0] for g in CFG}},
         "mrr@10": righe, "importi_per_coppia": coppie, "risultati_importi": risultati_importi,
         "confronto_24": {"senza_cifre": len(senza), "uguali_ad_A": stessi, "risultati_con_cifre": con_cifre},
         "previsioni": previsioni}
if not os.environ.get("TESI_RISULTATI"):
    sys.exit("!!! RISULTATO NON ARCHIVIATO: TESI_RISULTATI non è impostata.")
o = ora.strftime("%Y-%m-%dT%H%M%SZ"); p = os.path.join(DIR, f"{o}_esito.json"); k = 2
while os.path.exists(p):
    p = os.path.join(DIR, f"{o}-{k}_esito.json"); k += 1
open(p, "x").write(json.dumps(esito, indent=2, ensure_ascii=False))
print("archiviato in", p)
