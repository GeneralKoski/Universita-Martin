#!/usr/bin/env python3
"""Difetto 2: le quattro configurazioni (L lessicale, R re-ranking, U unione,
V solo vettori) sulle tre collezioni, dalle valutazioni di scripts/evaluate.

Per ogni collezione: metriche e tempi di ciascuna configurazione, le
differenze che le previsioni nominano, e per U contro R quante query
migliorano, peggiorano o restano uguali, e quanti documenti portati dal solo
vettore entrano fra i candidati.

    analizza.py <valutazione> [...]   (dodici file: tre collezioni per quattro configurazioni)
"""
import collections, datetime, json, os, statistics, subprocess, sys

QUI = os.path.dirname(os.path.abspath(__file__))
METRICA = {"scifact": "mean_ndcg@10", "nfcorpus": "mean_ndcg@10", "known-item-auto": "mean_mrr@10"}
PER_QUERY = {"mean_ndcg@10": "ndcg@10", "mean_mrr@10": "mrr@10"}


def git(*args):
    return subprocess.run(["git", "-C", QUI, *args], capture_output=True, text=True, check=True).stdout.strip()


def configurazione(c):
    if "embedder" not in c:
        return "L"
    return {"rerank": "R", "union": "U", "vector": "V"}[c["ibrido"]]


gruppi = collections.defaultdict(dict)
koskidex, digest = set(), set()
for p in sys.argv[1:]:
    r = json.load(open(p))
    c = r["config"]
    assert c.get("modifiche_non_committate") == "false", f"{p}: codice non committato"
    assert c["recupero"] == "any" and c["punteggio"] == "bm25" and c.get("bm25_espansioni") == "blended", p
    assert c["analisi"] == "none" and c["refusi"] == "0", p
    conf = configurazione(c)
    if conf != "L":
        assert c["embedder"] == "ollama/bge-m3", p
        digest.add(c["embedder_digest"])
        if conf in "UV":
            assert c["vettori_k"] == "100", p
    koskidex.add(c["commit"][:7])
    r["_file"] = os.path.basename(p)
    assert conf not in gruppi[c["collezione"]], f"{p}: {conf} due volte per {c['collezione']}"
    gruppi[c["collezione"]][conf] = r
assert set(gruppi) == set(METRICA), sorted(gruppi)
assert all(set(g) == set("LRUV") for g in gruppi.values()), {k: sorted(v) for k, v in gruppi.items()}
assert len(digest) == 1, digest

esito = {}
for coll, g in sorted(gruppi.items()):
    m = METRICA[coll]
    pq = PER_QUERY[m]
    righe = {}
    for conf in "LRUV":
        r = g[conf]
        ms = list(r["timings"]["per_query_ms"].values())
        righe[conf] = {"valutazione": r["_file"], "metrica": m.removeprefix("mean_"), "valore": round(r[m], 4),
                       "ndcg@10": round(r["mean_ndcg@10"], 4), "recall@100": round(r["mean_recall@100"], 4),
                       "mrr@10": round(r["mean_mrr@10"], 4), "a_vuoto": r["zero_results"],
                       "ms_mediana": round(statistics.median(ms), 3), "ms_media": round(statistics.mean(ms), 3),
                       "index_ms": round(r["timings"]["index_ms"], 1)}

    # U contro R, query per query.
    per_r = {q["query_id"]: q for q in g["R"]["per_query"]}
    meglio = peggio = uguali = 0
    for q in g["U"]["per_query"]:
        d = q[pq] - per_r[q["query_id"]][pq]
        meglio += d > 1e-12
        peggio += d < -1e-12
        uguali += abs(d) <= 1e-12

    # Quanti candidati porta il solo vettore: quelli di U meno quelli di R, che
    # sono i lessicali.
    per_r_cand = {q["query_id"]: q["candidates"] for q in g["R"]["per_query"]}
    aggiunti = [q["candidates"] - per_r_cand[q["query_id"]] for q in g["U"]["per_query"]]

    esito[coll] = {
        "configurazioni": righe,
        "R_meno_L": round(g["R"][m] - g["L"][m], 4),
        "U_meno_R": round(g["U"][m] - g["R"][m], 4),
        "U_meno_R_recall@100": round(g["U"]["mean_recall@100"] - g["R"]["mean_recall@100"], 4),
        "R_meno_L_recall@100": round(g["R"]["mean_recall@100"] - g["L"]["mean_recall@100"], 4),
        "U_contro_R_query": {"meglio": meglio, "peggio": peggio, "uguali": uguali},
        "U_meno_R_ms_mediana": round(righe["U"]["ms_mediana"] - righe["R"]["ms_mediana"], 3),
        "candidati_portati_dal_vettore": {"mediana": statistics.median(aggiunti), "minimo": min(aggiunti),
                                          "massimo": max(aggiunti)},
    }

for coll, e in esito.items():
    print(f"== {coll}")
    for conf, r in e["configurazioni"].items():
        print(f"  {conf} {r['metrica']} {r['valore']:.4f}  recall@100 {r['recall@100']:.4f}  vuote {r['a_vuoto']}  ms {r['ms_mediana']}")
    print(f"  R-L {e['R_meno_L']:+.4f}  U-R {e['U_meno_R']:+.4f}  U-R recall {e['U_meno_R_recall@100']:+.4f}  "
          f"U vs R {e['U_contro_R_query']}  U-R ms {e['U_meno_R_ms_mediana']:+.3f}")

ora = datetime.datetime.now(datetime.timezone.utc)
esito = {"ran_at": ora.strftime("%Y-%m-%dT%H:%M:%SZ"),
         "config": {"commit": git("rev-parse", "--short", "HEAD"),
                    "modifiche_non_committate": "true" if git("status", "--porcelain", "--", QUI) else "false",
                    "koskidex": sorted(koskidex), "embedder": "ollama/bge-m3", "embedder_digest": digest.pop(),
                    "valutazioni": sorted(os.path.basename(p) for p in sys.argv[1:])},
         **esito}

if not os.environ.get("TESI_RISULTATI"):
    sys.exit("!!! RISULTATO NON ARCHIVIATO: TESI_RISULTATI non è impostata.")
d = os.path.join(os.environ["TESI_RISULTATI"], "esperimenti", "2026-09-25_ibrido-unione")
o = ora.strftime("%Y-%m-%dT%H%M%SZ"); p = os.path.join(d, f"{o}_esito.json"); n = 2
while os.path.exists(p):
    p = os.path.join(d, f"{o}-{n}_esito.json"); n += 1
open(p, "x").write(json.dumps(esito, indent=2, ensure_ascii=False))
print("archiviato in", p)
