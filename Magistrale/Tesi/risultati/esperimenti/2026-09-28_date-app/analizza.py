#!/usr/bin/env python3
"""Controlla le previsioni 1-7 di 2026-09-28_date-app sulle misure di esegui.sh
e archivia il riassunto. L'ottava, i test di Documentale, è riportata nel
README. Nessun testo di query finisce nel riassunto: solo conteggi e id.

    analizza.py
"""
import collections, datetime, glob, json, os, re, statistics, subprocess, sys

QUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.environ.get("TESI_RISULTATI") or os.path.join(QUI, "..", "..")
DIR = os.path.join(BASE, "esperimenti", "2026-09-28_date-app")
CONFRONTO = os.path.join(BASE, "confronto")
FASI = ("spento", "acceso")


def ultimo(cartella, nome):
    trovati = sorted(glob.glob(os.path.join(cartella, f"*_{nome}.json")))
    if not trovati:
        sys.exit(f"manca {nome}")
    d = json.load(open(trovati[-1]))
    assert d["config"].get("modifiche_non_committate") in ("false", False), f"{trovati[-1]}: codice non committato"
    return os.path.basename(trovati[-1]), d


valutazioni, file = {}, {}
for f in FASI:
    for c in ("known-item-auto", "known-item-date", "known-item-importi", "known-item-umane"):
        file[f"{c} {f}"], valutazioni[(c, f)] = ultimo(os.path.join(DIR, "evaluate"), f"{c}-date-app-{f}")
per_query = lambda c, f: {q["query_id"]: q for q in valutazioni[(c, f)]["per_query"]}

righe = {}
for c in ("known-item-auto", "known-item-date", "known-item-importi", "known-item-umane"):
    righe[c] = {f: {"mrr@10": valutazioni[(c, f)]["mean_mrr@10"], "query": valutazioni[(c, f)]["queries"],
                    "a_vuoto": valutazioni[(c, f)]["zero_results"]} for f in FASI}
    print(f"{c:20} MRR@10 {righe[c]['spento']['mrr@10']:.4f} -> {righe[c]['acceso']['mrr@10']:.4f}  "
          f"query {righe[c]['spento']['query']}")


def coppie(c):
    formati = json.load(open(os.path.join(BASE, "query", c, "formati.json")))
    out = {}
    for f in FASI:
        pq = per_query(c, f)
        g = collections.defaultdict(lambda: [0, 0, 0])
        for qid, fm in formati.items():
            k = f"{fm['partenza']} > {fm['query']}"
            g[k][0] += 1
            if qid in pq:
                g[k][1] += pq[qid]["mrr@10"] > 0
                g[k][2] += pq[qid]["mrr@10"] == 1
        out[f] = {k: {"query": n, "entro_dieci": d, "primo": p} for k, (n, d, p) in sorted(g.items())}
    return out


date, importi = coppie("known-item-date"), coppie("known-item-importi")
print("\nentro i primi dieci, spento -> acceso")
for nome, t in (("date", date), ("importi", importi)):
    for k in t["spento"]:
        a, b = t["spento"][k], t["acceso"][k]
        print(f"  {nome:8} {k:16} {a['entro_dieci']:3}/{a['query']} -> {b['entro_dieci']:3}/{b['query']}")

quota = lambda x: x["entro_dieci"] / x["query"]
previsioni = {}


def prev(k, testo, ok, valore):
    previsioni[k] = {"previsione": testo, "valore": valore, "esito": "confermata" if ok else "smentita"}
    print(f"{k}. {previsioni[k]['esito']:10} {testo}: {valore}")


print()
stesso = {k: quota(v) for k, v in date["spento"].items() if k.split(" > ")[0] == k.split(" > ")[1]}
altro = {k: quota(v) for k, v in date["spento"].items() if k.split(" > ")[0] != k.split(" > ")[1]}
prev(1, "spento, date nel formato dell'atto almeno 90%, in un altro al più 10%",
     min(stesso.values()) >= 0.9 and max(altro.values()) <= 0.1,
     f"stesso formato {min(stesso.values()):.0%}-{max(stesso.values()):.0%}, altro {min(altro.values()):.0%}-{max(altro.values()):.0%}")
v = {k: quota(x) for k, x in date["acceso"].items()}
prev(2, "acceso, date: ogni coppia almeno 90% entro i primi dieci", min(v.values()) >= 0.9,
     f"da {min(v.values()):.0%} a {max(v.values()):.0%}")
fra = lambda t: {k: x for k, x in t.items() if k.split(" > ")[0] != k.split(" > ")[1]}
a, s = fra(importi["acceso"]), fra(importi["spento"])
prev(3, "importi fra formati: acceso almeno 90%, spento al più 10%",
     all(quota(x) >= 0.9 for x in a.values()) and all(quota(x) <= 0.1 for x in s.values()),
     "; ".join(f"{k} {s[k]['entro_dieci']}/{s[k]['query']} -> {a[k]['entro_dieci']}/{a[k]['query']}" for k in a))
d = righe["known-item-auto"]["acceso"]["mrr@10"] - righe["known-item-auto"]["spento"]["mrr@10"]
prev(4, "known-item automatiche, MRR@10 entro 0,005", abs(d) < 0.005,
     f"{righe['known-item-auto']['spento']['mrr@10']:.4f} -> {righe['known-item-auto']['acceso']['mrr@10']:.4f} ({d:+.4f})")
ps, pa = per_query("known-item-umane", "spento"), per_query("known-item-umane", "acceso")
cambiano = sum((ps[q]["mrr@10"] > 0) != (pa[q]["mrr@10"] > 0) for q in ps)
spostate = sum(ps[q]["mrr@10"] != pa[q]["mrr@10"] for q in ps)
d = righe["known-item-umane"]["acceso"]["mrr@10"] - righe["known-item-umane"]["spento"]["mrr@10"]
prev(5, "known-item umane: nessuna entra o esce dai primi dieci, MRR@10 entro 0,01", cambiano == 0 and abs(d) < 0.01,
     f"{len(ps)} query, {cambiano} entrano o escono, {spostate} cambiano posizione, MRR@10 {d:+.4f}")

rap = {f: ultimo(CONFRONTO, f"date-app-{f}-confronto-24-koskidex") for f in FASI}
file["confronto-24"] = {f: rap[f][0] for f in FASI}
qs, qa = rap["spento"][1]["query"], rap["acceso"][1]["query"]
assert [x["query"] for x in qs] == [x["query"] for x in qa]
anno = lambda t: re.search(r"(?<!\d)(19|20)\d\d(?!\d)", t)
senza = [(x, y) for x, y in zip(qs, qa) if not re.search(r"\d", x["query"])]
con_anno = [(x, y) for x, y in zip(qs, qa) if anno(x["query"])]
altre = [(x, y) for x, y in zip(qs, qa) if re.search(r"\d", x["query"]) and not anno(x["query"])]
stessi = sum(set(x["ids"]) == set(y["ids"]) for x, y in senza)
stesso_ordine = sum(x["ids"] == y["ids"] for x, y in senza)
ok = stessi == len(senza) and all(len(y["ids"]) <= len(x["ids"]) and set(y["ids"]) <= set(x["ids"]) for x, y in con_anno)
confronto = {"senza_cifre": len(senza), "stessi_atti": stessi, "stesso_ordine": stesso_ordine,
             "con_anno": [[len(x["ids"]), len(y["ids"])] for x, y in con_anno],
             "altre_con_cifre": [[len(x["ids"]), len(y["ids"]), set(x["ids"]) == set(y["ids"])] for x, y in altre]}
prev(6, "le 24: senza cifre stessi atti; con l'anno i risultati solo diminuiscono", ok,
     f"senza cifre {stessi} su {len(senza)} stessi atti ({stesso_ordine} stesso ordine); "
     f"con l'anno risultati {confronto['con_anno']}")

tempi = {}
for f in FASI:
    rs = sorted(glob.glob(os.path.join(CONFRONTO, f"*_date-app-{f}-indicizzazione-koskidex.json")))[-3:]
    if len(rs) < 3:
        sys.exit(f"mancano le tre indicizzazioni {f}")
    tempi[f] = [json.load(open(p))["timings"]["index_ms"] for p in rs]
    file[f"indicizzazione {f}"] = [os.path.basename(p) for p in rs]
ms, ma = statistics.median(tempi["spento"]), statistics.median(tempi["acceso"])
prev(7, "indicizzazione dall'app accesa al più il 10% più lenta", ma <= 1.10 * ms,
     f"mediana {ms:.0f} -> {ma:.0f} ms ({100 * (ma / ms - 1):+.1f}%)")

ora = datetime.datetime.now(datetime.timezone.utc)
git = lambda *x: subprocess.run(["git", "-C", QUI, *x], capture_output=True, text=True, check=True).stdout.strip()
esito = {"ran_at": ora.strftime("%Y-%m-%dT%H:%M:%SZ"),
         "config": {"commit": git("rev-parse", "--short", "HEAD"),
                    "modifiche_non_committate": "true" if git("status", "--porcelain", "--untracked-files=no", "--", QUI) else "false",
                    "koskidex": sorted({v["config"].get("commit", "")[:7] for v in valutazioni.values()}), "file": file},
         "valutazioni": righe, "date": date, "importi": importi, "confronto_24": confronto,
         "indicizzazione_ms": tempi, "previsioni": previsioni}
if not os.environ.get("TESI_RISULTATI"):
    sys.exit("!!! RISULTATO NON ARCHIVIATO: TESI_RISULTATI non è impostata.")
o = ora.strftime("%Y-%m-%dT%H%M%SZ"); p = os.path.join(DIR, f"{o}_esito.json"); k = 2
while os.path.exists(p):
    p = os.path.join(DIR, f"{o}-{k}_esito.json"); k += 1
open(p, "x").write(json.dumps(esito, indent=2, ensure_ascii=False))
print("archiviato in", p)
