#!/usr/bin/env python3
"""Difetto 3 sul test: per ogni collezione l'unione con la somma di oggi (U,
dal difetto 2), la somma con la costante calibrata (S*), RRF, la convessa con
α 0,5 (C) e con α calibrato (C*), con le differenze da U che le previsioni 5-7
nominano. I valori calibrati si leggono dall'esito di calibra.py e si
controllano contro la configurazione registrata in ogni valutazione.

Quando il valore calibrato coincide col predefinito (20, 0,5) S* è U e C* è
C: non si esegue due volte la stessa configurazione.

    analizza.py <esito di calibra.py> <valutazione> [...]
"""
import collections, datetime, json, os, statistics, subprocess, sys

QUI = os.path.dirname(os.path.abspath(__file__))
METRICA = {"scifact": "mean_ndcg@10", "nfcorpus": "mean_ndcg@10", "known-item-auto": "mean_mrr@10"}
CALIBRATA_SU = {"scifact": "scifact", "nfcorpus": "nfcorpus", "known-item-auto": "known-item-auto-train"}


def git(*args):
    return subprocess.run(["git", "-C", QUI, *args], capture_output=True, text=True, check=True).stdout.strip()


cal_path, *valutazioni = sys.argv[1:]
cal = json.load(open(cal_path))
assert cal["config"]["modifiche_non_committate"] == "false"

gruppi = collections.defaultdict(dict)
koskidex = set()
for p in valutazioni:
    r = json.load(open(p))
    c = r["config"]
    assert c.get("modifiche_non_committate") == "false", f"{p}: codice non committato"
    assert c["recupero"] == "any" and c["punteggio"] == "bm25" and c.get("bm25_espansioni") == "blended", p
    assert c["embedder"] == "ollama/bge-m3" and c["embedder_digest"] == cal["config"]["embedder_digest"], p
    assert c.get("split", "test") == "test", p
    coll = c["collezione"]
    cc = cal[CALIBRATA_SU[coll]]
    fusione = c.get("fusione", "somma")
    if fusione == "somma":
        assert c["ibrido"] == "union", p
        peso = float(c.get("peso_vettore", "20"))
        conf = "U" if peso == 20 else "S*"
        assert conf == "U" or peso == cc["costante_migliore"], f"{p}: costante {peso}, calibrata {cc['costante_migliore']}"
    elif fusione == "rrf":
        conf = "RRF"
    else:
        alfa = float(c["alfa"])
        conf = "C" if alfa == 0.5 else "C*"
        assert conf == "C" or alfa == cc["alfa_migliore"], f"{p}: α {alfa}, calibrato {cc['alfa_migliore']}"
    koskidex.add(c["commit"][:7])
    r["_file"] = os.path.basename(p)
    assert conf not in gruppi[coll], f"{p}: {conf} due volte per {coll}"
    gruppi[coll][conf] = r

esito = {}
for coll, g in sorted(gruppi.items()):
    cc = cal[CALIBRATA_SU[coll]]
    if cc["costante_migliore"] == 20:
        g["S*"] = g["U"]
    if cc["alfa_migliore"] == 0.5:
        g["C*"] = g["C"]
    assert set(g) == {"U", "S*", "RRF", "C", "C*"}, (coll, sorted(g))
    m = METRICA[coll]
    righe = {}
    for conf in ("U", "S*", "RRF", "C", "C*"):
        r = g[conf]
        ms = list(r["timings"]["per_query_ms"].values())
        righe[conf] = {"valutazione": r["_file"], "metrica": m.removeprefix("mean_"), "valore": round(r[m], 4),
                       "recall@100": round(r["mean_recall@100"], 4), "a_vuoto": r["zero_results"],
                       "ms_mediana": round(statistics.median(ms), 3)}
    esito[coll] = {"costante_calibrata": cc["costante_migliore"], "alfa_calibrato": cc["alfa_migliore"],
                   "configurazioni": righe,
                   "differenze_da_U": {k: round(g[k][m] - g["U"][m], 4) for k in ("S*", "RRF", "C", "C*")},
                   "C*_meno_RRF": round(g["C*"][m] - g["RRF"][m], 4),
                   "ms_mediana_meno_U": {k: round(righe[k]["ms_mediana"] - righe["U"]["ms_mediana"], 3)
                                         for k in ("RRF", "C", "C*")}}

for coll, e in esito.items():
    print(f"== {coll} (costante {e['costante_calibrata']}, α {e['alfa_calibrato']})")
    for conf, r in e["configurazioni"].items():
        print(f"  {conf:4} {r['metrica']} {r['valore']:.4f}  recall@100 {r['recall@100']:.4f}  ms {r['ms_mediana']}")
    print("  da U:", e["differenze_da_U"], " C*-RRF:", e["C*_meno_RRF"], " ms:", e["ms_mediana_meno_U"])

ora = datetime.datetime.now(datetime.timezone.utc)
esito = {"ran_at": ora.strftime("%Y-%m-%dT%H:%M:%SZ"),
         "config": {"commit": git("rev-parse", "--short", "HEAD"),
                    "modifiche_non_committate": "true" if git("status", "--porcelain", "--", QUI) else "false",
                    "koskidex": sorted(koskidex), "calibrazione": os.path.basename(cal_path),
                    "valutazioni": sorted(os.path.basename(p) for p in valutazioni)},
         **esito}

if not os.environ.get("TESI_RISULTATI"):
    sys.exit("!!! RISULTATO NON ARCHIVIATO: TESI_RISULTATI non è impostata.")
d = os.path.join(os.environ["TESI_RISULTATI"], "esperimenti", "2026-09-25_fusione")
o = ora.strftime("%Y-%m-%dT%H%M%SZ"); p = os.path.join(d, f"{o}_esito.json"); n = 2
while os.path.exists(p):
    p = os.path.join(d, f"{o}-{n}_esito.json"); n += 1
open(p, "x").write(json.dumps(esito, indent=2, ensure_ascii=False))
print("archiviato in", p)
