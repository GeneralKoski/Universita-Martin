#!/usr/bin/env python3
"""Controlla le previsioni di 2026-09-28_reranker sulle esecuzioni di esegui.sh
e archivia il riassunto: primo stadio contro riordino, recall@100 del primo
stadio come tetto, tempo del riordino, e per le known-item dove stava l'atto
nel primo stadio; per le known-item umane anche MRR@10 e ricerche a vuoto del
riordino per fonte e con o senza numero, da raccolta.json, come nella tabella
del capitolo 8. Nessun testo di query finisce nel riassunto.

    analizza.py beir|umane
"""
import datetime, glob, json, os, statistics, subprocess, sys

QUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.environ.get("TESI_RISULTATI") or os.path.join(QUI, "..", "..")
DIR = os.path.join(BASE, "esperimenti", "2026-09-28_reranker")
COSA = sys.argv[1]
KX = os.path.expanduser("~/Desktop/Progetti-personali/Koskidex/eval/corpora")
RACCOLTA = os.path.join(QUI, "..", "..", "query", "known-item-umane", "raccolta.json")


def ultimo(cartella, nome):
    trovati = sorted(glob.glob(os.path.join(DIR, cartella, f"*_{nome}.json")))
    if not trovati:
        sys.exit(f"manca {cartella}/{nome}")
    d = json.load(open(trovati[-1]))
    assert d["config"].get("modifiche_non_committate") in ("false", False), f"{trovati[-1]}: codice non committato"
    return os.path.basename(trovati[-1]), d


def qrels(corpora, collezione):
    g = {}
    for riga in list(open(os.path.join(KX, corpora, collezione, "qrels", "test.tsv")))[1:]:
        q, d, s = riga.split()
        if int(s) > 0:
            g.setdefault(q, set()).add(d)
    return g


CASI = {"beir": [("c1-public", "scifact", "LA"), ("c1-public", "nfcorpus", "LA"), ("c3-albo", "known-item-auto", "LA")],
        "umane": [("c3-albo", "known-item-umane", "LA"), ("c3-albo", "known-item-umane", "A")]}[COSA]
righe, file = {}, {}
for corpora, c, conf in CASI:
    fp, p = ultimo("primo-stadio", f"{c}-rr-primo-{conf}")
    fr, r = ultimo("evaluate", f"{c}-rr-{conf}")
    fq, rap = ultimo("riordinati", f"{c}-rr-{conf}")
    assert rap["config"]["primo_stadio"] == fp, f"{fq} riordina {rap['config']['primo_stadio']}, non {fp}"
    file[f"{c} {conf}"] = {"primo_stadio": fp, "riordino": fq, "valutazione": fr}
    riga = {"primo": {m: p[f"mean_{m}"] for m in ("ndcg@10", "mrr@10", "recall@100")},
            "riordino": {m: r[f"mean_{m}"] for m in ("ndcg@10", "mrr@10")},
            "mediana_ms": statistics.median(x["ms"] for x in rap["query"]),
            "revisione_modello": rap["config"]["revisione"]}
    if c.startswith("known-item"):
        g = qrels(corpora, c)
        rr = {q["query_id"]: q.get("top") or [] for q in r["per_query"]}
        posizioni = {"primi_10": 0, "da_11_a_100": 0, "fuori": 0, "portati_nei_10": 0}
        for q in p["per_query"]:
            top = q.get("top") or []
            pos = next((i for i, d in enumerate(top) if d in g.get(q["query_id"], ())), None)
            chiave = "fuori" if pos is None else ("primi_10" if pos < 10 else "da_11_a_100")
            posizioni[chiave] += 1
            if chiave == "da_11_a_100" and any(d in g[q["query_id"]] for d in rr[q["query_id"]][:10]):
                posizioni["portati_nei_10"] += 1
        riga["posizioni_primo_stadio"] = posizioni
    if c == "known-item-umane":
        info = {q["query"]: q for q in json.load(open(RACCOLTA, encoding="utf8"))["query"] if not q["vuota"]}
        gruppi = {"tutte": lambda q: True, "crispiano": lambda q: info[q]["fonte"] == "crispiano",
                  "fvg": lambda q: info[q]["fonte"] == "fvg", "con numero": lambda q: info[q]["contiene_numero"],
                  "senza numero": lambda q: not info[q]["contiene_numero"]}
        riga["per_gruppo"] = {}
        for g_, dentro in gruppi.items():
            qs = [x for x in r["per_query"] if dentro(x["query_id"])]
            riga["per_gruppo"][g_] = {"query": len(qs), "mrr@10": round(sum(x["mrr@10"] for x in qs) / len(qs), 4),
                                      "a_vuoto": round(sum(x["retrieved"] == 0 for x in qs) / len(qs), 4)}
        print(f"{c} {conf} riordinato per gruppo: " + json.dumps(riga["per_gruppo"]))
    righe[f"{c} {conf}"] = riga
    print(f"{c:18} {conf}  nDCG@10 {riga['primo']['ndcg@10']:.4f} -> {riga['riordino']['ndcg@10']:.4f}  "
          f"MRR@10 {riga['primo']['mrr@10']:.4f} -> {riga['riordino']['mrr@10']:.4f}  "
          f"recall@100 {riga['primo']['recall@100']:.4f}  mediana {riga['mediana_ms']:.0f} ms  {riga.get('posizioni_primo_stadio', '')}")

previsioni = {}


def prev(k, testo, ok, valore):
    previsioni[k] = {"previsione": testo, "valore": valore, "esito": "confermata" if ok else "smentita"}
    print(f"{k}. {previsioni[k]['esito']:10} {testo}: {valore}")


print()
mediane = [x["mediana_ms"] for x in righe.values()]
if COSA == "beir":
    x = righe["scifact LA"]["riordino"]["ndcg@10"]
    prev(1, "SciFact nDCG@10 almeno 0,72", x >= 0.72, f"{righe['scifact LA']['primo']['ndcg@10']:.4f} -> {x:.4f}")
    x = righe["nfcorpus LA"]["riordino"]["ndcg@10"]
    prev(2, "NFCorpus nDCG@10 almeno 0,33", x >= 0.33, f"{righe['nfcorpus LA']['primo']['ndcg@10']:.4f} -> {x:.4f}")
    _, lt = ultimo("primo-stadio", "known-item-auto-rr-primo-LT")
    file["known-item-auto LT"] = _
    x = righe["known-item-auto LA"]["riordino"]["mrr@10"]
    prev(3, "known-item automatiche: il riordino di LA sotto LT", x < lt["mean_mrr@10"],
         f"LA {righe['known-item-auto LA']['primo']['mrr@10']:.4f}, riordino {x:.4f}, LT {lt['mean_mrr@10']:.4f}")
else:
    la, a = righe["known-item-umane LA"], righe["known-item-umane A"]
    dla, da = la["riordino"]["mrr@10"] - la["primo"]["mrr@10"], a["riordino"]["mrr@10"] - a["primo"]["mrr@10"]
    prev(4, "umane: riordino di LA almeno +0,05, di A almeno +0,03", dla >= 0.05 and da >= 0.03,
         f"LA {la['primo']['mrr@10']:.4f} -> {la['riordino']['mrr@10']:.4f} ({dla:+.4f}); "
         f"A {a['primo']['mrr@10']:.4f} -> {a['riordino']['mrr@10']:.4f} ({da:+.4f})")
    q = [r["posizioni_primo_stadio"] for r in (la, a)]
    prev(5, "umane: dall'11° al 100° posto nei primi dieci almeno in metà dei casi",
         all(x["portati_nei_10"] >= x["da_11_a_100"] / 2 for x in q),
         "; ".join(f"{n} {x['portati_nei_10']} su {x['da_11_a_100']}" for n, x in zip(("LA", "A"), q)))
prev(6, "mediana del riordino almeno 2 secondi a query", min(mediane) >= 2000,
     "; ".join(f"{n} {r['mediana_ms']:.0f} ms" for n, r in righe.items()))

ora = datetime.datetime.now(datetime.timezone.utc)
git = lambda *x: subprocess.run(["git", "-C", QUI, *x], capture_output=True, text=True, check=True).stdout.strip()
esito = {"ran_at": ora.strftime("%Y-%m-%dT%H:%M:%SZ"),
         "config": {"commit": git("rev-parse", "--short", "HEAD"),
                    "modifiche_non_committate": "true" if git("status", "--porcelain", "--untracked-files=no", "--", QUI) else "false",
                    "file": file},
         "righe": righe, "previsioni": previsioni}
if not os.environ.get("TESI_RISULTATI"):
    sys.exit("!!! RISULTATO NON ARCHIVIATO: TESI_RISULTATI non è impostata.")
o = ora.strftime("%Y-%m-%dT%H%M%SZ"); p = os.path.join(DIR, f"{o}_esito-{COSA}.json"); k = 2
while os.path.exists(p):
    p = os.path.join(DIR, f"{o}-{k}_esito-{COSA}.json"); k += 1
open(p, "x").write(json.dumps(esito, indent=2, ensure_ascii=False))
print("archiviato in", p)
