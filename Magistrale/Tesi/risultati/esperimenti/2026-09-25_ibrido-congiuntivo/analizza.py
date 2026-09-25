#!/usr/bin/env python3
"""Difetto 2 sul recupero congiuntivo: L, R e U con recupero all sulle tre
collezioni, le differenze che le previsioni nominano, e il tempo di U con all
contro quello di U con any già archiviato in 2026-09-25_ibrido-unione.

    analizza.py <esito di 2026-09-25_ibrido-unione> <valutazione> [...]   (nove file)
"""
import collections, datetime, json, os, statistics, subprocess, sys

QUI = os.path.dirname(os.path.abspath(__file__))
METRICA = {"scifact": "mean_ndcg@10", "nfcorpus": "mean_ndcg@10", "known-item-auto": "mean_mrr@10"}


def git(*args):
    return subprocess.run(["git", "-C", QUI, *args], capture_output=True, text=True, check=True).stdout.strip()


any_path, *valutazioni = sys.argv[1:]
unione_any = json.load(open(any_path))

gruppi = collections.defaultdict(dict)
koskidex, digest = set(), set()
for p in valutazioni:
    r = json.load(open(p))
    c = r["config"]
    assert c.get("modifiche_non_committate") == "false", f"{p}: codice non committato"
    assert c["recupero"] == "all" and c["punteggio"] == "bm25" and c.get("bm25_espansioni") == "blended", p
    assert c["analisi"] == "none" and c["refusi"] == "0" and c.get("split", "test") == "test", p
    if "embedder" not in c:
        conf = "L"
    else:
        assert c["embedder"] == "ollama/bge-m3" and c.get("fusione", "somma") == "somma", p
        assert c.get("peso_vettore", "20") == "20", p
        digest.add(c["embedder_digest"])
        conf = {"rerank": "R", "union": "U"}[c["ibrido"]]
    koskidex.add(c["commit"][:7])
    r["_file"] = os.path.basename(p)
    assert conf not in gruppi[c["collezione"]], f"{p}: {conf} due volte"
    gruppi[c["collezione"]][conf] = r
assert set(gruppi) == set(METRICA) and all(set(g) == set("LRU") for g in gruppi.values())
assert digest == {unione_any["config"]["embedder_digest"]}, digest

esito = {}
for coll, g in sorted(gruppi.items()):
    m = METRICA[coll]
    righe = {}
    for conf in "LRU":
        r = g[conf]
        righe[conf] = {"valutazione": r["_file"], "metrica": m.removeprefix("mean_"), "valore": round(r[m], 4),
                       "recall@100": round(r["mean_recall@100"], 4), "a_vuoto": r["zero_results"],
                       "ms_mediana": round(statistics.median(r["timings"]["per_query_ms"].values()), 3)}
    per_r = {q["query_id"]: q["candidates"] for q in g["R"]["per_query"]}
    aggiunti = [q["candidates"] - per_r[q["query_id"]] for q in g["U"]["per_query"]]
    u_any = unione_any[coll]["configurazioni"]["U"]
    esito[coll] = {"configurazioni": righe,
                   "R_meno_L": round(g["R"][m] - g["L"][m], 4), "U_meno_R": round(g["U"][m] - g["R"][m], 4),
                   "U_con_any": {"valore": u_any["valore"], "ms_mediana": u_any["ms_mediana"]},
                   "U_all_meno_U_any_ms": round(righe["U"]["ms_mediana"] - u_any["ms_mediana"], 3),
                   "candidati_lessicali_mediana": statistics.median(per_r.values()),
                   "candidati_portati_dal_vettore_mediana": statistics.median(aggiunti)}

for coll, e in esito.items():
    print(f"== {coll}")
    for conf, r in e["configurazioni"].items():
        print(f"  {conf} {r['metrica']} {r['valore']:.4f}  recall@100 {r['recall@100']:.4f}  vuote {r['a_vuoto']}  ms {r['ms_mediana']}")
    print(f"  R-L {e['R_meno_L']:+.4f}  U-R {e['U_meno_R']:+.4f}  U con any {e['U_con_any']}  "
          f"candidati lessicali {e['candidati_lessicali_mediana']}, dal vettore {e['candidati_portati_dal_vettore_mediana']}")

ora = datetime.datetime.now(datetime.timezone.utc)
esito = {"ran_at": ora.strftime("%Y-%m-%dT%H:%M:%SZ"),
         "config": {"commit": git("rev-parse", "--short", "HEAD"),
                    "modifiche_non_committate": "true" if git("status", "--porcelain", "--", QUI) else "false",
                    "koskidex": sorted(koskidex), "embedder_digest": digest.pop(),
                    "unione_con_any": os.path.basename(any_path),
                    "valutazioni": sorted(os.path.basename(p) for p in valutazioni)},
         **esito}

if not os.environ.get("TESI_RISULTATI"):
    sys.exit("!!! RISULTATO NON ARCHIVIATO: TESI_RISULTATI non è impostata.")
d = os.path.join(os.environ["TESI_RISULTATI"], "esperimenti", "2026-09-25_ibrido-congiuntivo")
o = ora.strftime("%Y-%m-%dT%H%M%SZ"); p = os.path.join(d, f"{o}_esito.json"); n = 2
while os.path.exists(p):
    p = os.path.join(d, f"{o}-{n}_esito.json"); n += 1
open(p, "x").write(json.dumps(esito, indent=2, ensure_ascii=False))
print("archiviato in", p)
