#!/usr/bin/env python3
"""Difetto 3, calibrazione: dalle valutazioni sugli split separati (SciFact
train, NFCorpus dev, known-item train) la curva della costante della somma e
quella di α della fusione convessa, il valore migliore di ciascuna per
collezione, e quanto si perde a trasferire su NFCorpus il valore migliore di
SciFact (previsione 4).

Metrica: nDCG@10 per SciFact e NFCorpus, MRR@10 per le known-item. A parità di
metrica vince il valore più vicino al predefinito del motore (20 per la
costante, 0,5 per α): la calibrazione non deve spostarsi dal comportamento di
oggi senza un guadagno.

    calibra.py <valutazione> [...]   (57 file: tre collezioni, 8 costanti e 11 α ciascuna)
"""
import collections, datetime, json, os, subprocess, sys

QUI = os.path.dirname(os.path.abspath(__file__))
COLLEZIONI = {"scifact": ("train", "mean_ndcg@10"), "nfcorpus": ("dev", "mean_ndcg@10"),
              "known-item-auto-train": ("train", "mean_mrr@10")}
COSTANTI = [0, 5, 10, 20, 40, 80, 160, 320]
ALFA = [round(x / 10, 1) for x in range(11)]


def git(*args):
    return subprocess.run(["git", "-C", QUI, *args], capture_output=True, text=True, check=True).stdout.strip()


curve = collections.defaultdict(lambda: {"somma": {}, "convex": {}})
koskidex, digest = set(), set()
for p in sys.argv[1:]:
    r = json.load(open(p))
    c = r["config"]
    assert c.get("modifiche_non_committate") == "false", f"{p}: codice non committato"
    assert c["recupero"] == "any" and c["punteggio"] == "bm25" and c.get("bm25_espansioni") == "blended", p
    # Con -fusione evaluate non registra vettori_k (lo scrive solo con
    # -ibrido): il motore usa l'unione con VectorTopK predefinito, 100.
    assert c["embedder"] == "ollama/bge-m3" and c.get("vettori_k", "100") == "100", p
    assert c["fusione"] != "somma" or c["vettori_k"] == "100", p
    coll = c["collezione"]
    split, metrica = COLLEZIONI[coll]
    assert c.get("split", "test") == split, f"{p}: split {c.get('split', 'test')} invece di {split}"
    koskidex.add(c["commit"][:7])
    digest.add(c["embedder_digest"])
    if c["fusione"] == "somma":
        assert c["ibrido"] == "union", p
        chiave, v = "somma", float(c["peso_vettore"])
    else:
        assert c["fusione"] == "convex", p
        chiave, v = "convex", float(c["alfa"])
    assert v not in curve[coll][chiave], f"{p}: {chiave} {v} due volte"
    curve[coll][chiave][v] = {"valore": round(r[metrica], 4), "esatto": r[metrica],
                              "recall@100": round(r["mean_recall@100"], 4), "file": os.path.basename(p)}
assert set(curve) == set(COLLEZIONI), sorted(curve)
for coll, g in curve.items():
    assert sorted(g["somma"]) == COSTANTI, (coll, sorted(g["somma"]))
    assert sorted(g["convex"]) == ALFA, (coll, sorted(g["convex"]))
assert len(digest) == 1 and len(koskidex) == 1, (digest, koskidex)


def migliore(curva, predefinito):
    return max(curva, key=lambda v: (curva[v]["esatto"], -abs(v - predefinito)))


esito = {}
for coll in COLLEZIONI:
    g = curve[coll]
    c_best, a_best = migliore(g["somma"], 20), migliore(g["convex"], 0.5)
    esito[coll] = {"split": COLLEZIONI[coll][0], "metrica": COLLEZIONI[coll][1].removeprefix("mean_"),
                   "somma": {str(v): {k: x for k, x in d.items() if k != "esatto"} for v, d in sorted(g["somma"].items())},
                   "convex": {str(v): {k: x for k, x in d.items() if k != "esatto"} for v, d in sorted(g["convex"].items())},
                   "costante_migliore": c_best, "alfa_migliore": a_best,
                   "valore_costante_migliore": g["somma"][c_best]["valore"],
                   "valore_alfa_migliore": g["convex"][a_best]["valore"],
                   "valore_costante_20": g["somma"][20]["valore"]}

s, n = esito["scifact"], curve["nfcorpus"]
trasferimento = {
    "costante_di_scifact_su_nfcorpus": s["costante_migliore"],
    "perdita_costante": round(n["somma"][esito["nfcorpus"]["costante_migliore"]]["esatto"]
                              - n["somma"][s["costante_migliore"]]["esatto"], 4),
    "alfa_di_scifact_su_nfcorpus": s["alfa_migliore"],
    "perdita_alfa": round(n["convex"][esito["nfcorpus"]["alfa_migliore"]]["esatto"]
                          - n["convex"][s["alfa_migliore"]]["esatto"], 4),
}
rapporto = (max(s["costante_migliore"], esito["nfcorpus"]["costante_migliore"])
            / min(s["costante_migliore"], esito["nfcorpus"]["costante_migliore"])
            if min(s["costante_migliore"], esito["nfcorpus"]["costante_migliore"]) > 0 else None)

for coll, e in esito.items():
    print(f"== {coll} ({e['split']}, {e['metrica']})")
    print("  somma  ", "  ".join(f"{v}:{d['valore']:.4f}" for v, d in e["somma"].items()))
    print("  convex ", "  ".join(f"{v}:{d['valore']:.4f}" for v, d in e["convex"].items()))
    print(f"  costante migliore {e['costante_migliore']} ({e['valore_costante_migliore']:.4f}), "
          f"α migliore {e['alfa_migliore']} ({e['valore_alfa_migliore']:.4f})")
print("trasferimento:", trasferimento, "rapporto fra le costanti:", rapporto)

ora = datetime.datetime.now(datetime.timezone.utc)
esito = {"ran_at": ora.strftime("%Y-%m-%dT%H:%M:%SZ"),
         "config": {"commit": git("rev-parse", "--short", "HEAD"),
                    "modifiche_non_committate": "true" if git("status", "--porcelain", "--", QUI) else "false",
                    "koskidex": koskidex.pop(), "embedder_digest": digest.pop(),
                    "parita": "vince il valore più vicino al predefinito (20, 0,5)"},
         **esito, "trasferimento_su_nfcorpus": trasferimento,
         "rapporto_fra_le_costanti_migliori_scifact_nfcorpus": rapporto}

if not os.environ.get("TESI_RISULTATI"):
    sys.exit("!!! RISULTATO NON ARCHIVIATO: TESI_RISULTATI non è impostata.")
d = os.path.join(os.environ["TESI_RISULTATI"], "esperimenti", "2026-09-25_fusione")
o = ora.strftime("%Y-%m-%dT%H%M%SZ"); p = os.path.join(d, f"{o}_calibrazione.json"); k = 2
while os.path.exists(p):
    p = os.path.join(d, f"{o}-{k}_calibrazione.json"); k += 1
open(p, "x").write(json.dumps(esito, indent=2, ensure_ascii=False))
print("archiviato in", p)
