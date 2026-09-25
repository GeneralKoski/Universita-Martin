#!/usr/bin/env python3
"""Configurazione consigliata contro "parole libere, numeri esatti" di
2026-09-25_refusi-numeri: known-item (valutazioni di scripts/evaluate, e
ranking query per query dai rapporti dell'app) e le 24 query del confronto
(insiemi e posizioni degli atti giusti per le due query con un numero).

    analizza.py <valutazione known-item consigliata> <valutazione di riferimento>
                <confronto-24 consigliata> <confronto-24 di riferimento>
"""
import datetime, json, os, subprocess, sys

QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.join(QUI, "..", "..")
vc, vr, cc, cr = sys.argv[1:]


def rapporto(valutazione):
    v = json.load(open(valutazione))
    return v, json.load(open(os.path.join(RADICE, "confronto", v["config"]["rapporto"])))


def known_item(v):
    pq = v["per_query"]
    return {"mrr@10": round(v["mean_mrr@10"], 4), "atto_primo": sum(q["mrr@10"] == 1 for q in pq),
            "atto_entro_10": sum(q["mrr@10"] > 0 for q in pq), "a_vuoto": v["zero_results"]}


(kc, rc), (kr, rr) = rapporto(vc), rapporto(vr)
assert kc["config"]["modifiche_non_committate"] == "false" and rc["config"]["modifiche_non_committate"] == "false"
ranking_c = {q["query"]: q["ids"] for q in rc["query"]}
ranking_r = {q["query"]: q["ids"] for q in rr["query"]}
assert ranking_c.keys() == ranking_r.keys()
diversi = sorted(q for q in ranking_c if ranking_c[q][:10] != ranking_r[q][:10])

c24, r24 = json.load(open(cc)), json.load(open(cr))
assert c24["config"]["modifiche_non_committate"] == "false"
pr = {q["query"]: q["ids"] for q in r24["query"]}
confronto = []
for q in c24["query"]:
    a, b = set(q["ids"]), set(pr[q["query"]])
    confronto.append({"query": q["query"], "consigliata": len(a), "riferimento": len(b),
                      "persi": len(b - a), "guadagnati": len(a - b), "stesso_ordine": q["ids"] == pr[q["query"]]})
posizioni = {}
for q, doc in (("ordinanza 187", "doc-0001"), ("determina 1223", "doc-0002")):
    ids = next(x["ids"] for x in c24["query"] if x["query"] == q)
    posizioni[q] = {"atto": doc, "posizione": ids.index(doc) + 1 if doc in ids else None, "risultati": len(ids)}

esito = {"known_item": {"consigliata": known_item(kc), "riferimento": known_item(kr),
                        "query_con_primi_10_diversi": len(diversi), "esempi": diversi[:10]},
         "confronto_24": {"query_che_perdono": sum(x["persi"] > 0 for x in confronto),
                          "query_che_guadagnano": sum(x["guadagnati"] > 0 for x in confronto),
                          "stesso_ordine": sum(x["stesso_ordine"] for x in confronto), "per_query": confronto},
         "posizioni_numero_atto": posizioni}
print(json.dumps({k: v for k, v in esito.items() if k != "confronto_24"}, indent=1, ensure_ascii=False))
print(json.dumps({k: v for k, v in esito["confronto_24"].items() if k != "per_query"}, ensure_ascii=False))
for x in confronto:
    if x["persi"] or x["guadagnati"]:
        print(" ", x)

ora = datetime.datetime.now(datetime.timezone.utc)
git = lambda *a: subprocess.run(["git", "-C", QUI, *a], capture_output=True, text=True, check=True).stdout.strip()
esito = {"ran_at": ora.strftime("%Y-%m-%dT%H:%M:%SZ"),
         "config": {"commit": git("rev-parse", "--short", "HEAD"),
                    "modifiche_non_committate": "true" if git("status", "--porcelain", "--", QUI) else "false",
                    "valutazioni": [os.path.basename(vc), os.path.basename(vr)],
                    "confronto": [os.path.basename(cc), os.path.basename(cr)],
                    "koskidex": [kc["config"]["commit"][:7], kr["config"]["commit"][:7]]},
         **esito}
if not os.environ.get("TESI_RISULTATI"):
    sys.exit("!!! RISULTATO NON ARCHIVIATO: TESI_RISULTATI non è impostata.")
d = os.path.join(os.environ["TESI_RISULTATI"], "esperimenti", "2026-09-25_configurazione-consigliata")
o = ora.strftime("%Y-%m-%dT%H%M%SZ"); p = os.path.join(d, f"{o}_esito.json"); n = 2
while os.path.exists(p):
    p = os.path.join(d, f"{o}-{n}_esito.json"); n += 1
open(p, "x").write(json.dumps(esito, indent=2, ensure_ascii=False))
print("archiviato in", p)
