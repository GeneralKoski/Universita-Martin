#!/usr/bin/env python3
"""Known-item umane: MRR@10, atto primo, entro 10 e query a vuoto per ogni
configurazione, su tutte le query, per fonte e per query con e senza numero.
Metodo e previsioni nel README.

    analizza.py [--raccolta <raccolta.json>] <valutazione> [...]
        (le otto di esegui.sh: K0, LA, LT, A, B, V, e i due rapporti dell'app)
"""
import argparse, datetime, json, os, subprocess, sys

QUI = os.path.dirname(os.path.abspath(__file__))
CONFIGURAZIONI = ["ES", "KC", "K0", "LA", "LT", "A", "B", "V"]

p = argparse.ArgumentParser()
p.add_argument("--raccolta", default=os.path.join(QUI, "..", "..", "query", "known-item-umane", "raccolta.json"))
p.add_argument("valutazioni", nargs="+")
a = p.parse_args()


def configurazione(f, v):
    c = v["config"]
    assert v["collection"] == "known-item-umane" and c.get("split", "test") == "test", f
    assert c.get("modifiche_non_committate") == "false", f"{f}: codice non committato"
    if "motore" in c:
        if c["motore"] == "elasticsearch":
            return "ES"
        assert c["motore"] == "koskidex" and "consigliata" in c["rapporto"], f"{f}: non è Koskidex consigliata"
        return "KC"
    assert c["analisi"] == "none" and c["refusi"] == "0", f
    if "embedder" not in c:
        if c["punteggio"] == "legacy":
            assert c["recupero"] == "all", f
            return "K0"
        assert c["punteggio"] == "bm25" and c.get("bm25_espansioni") == "blended", f
        return {"any": "LA", "all": "LT"}[c["recupero"]]
    assert c["embedder"] == "ollama/bge-m3" and c.get("fusione", "somma") == "somma", f
    assert c.get("vettori_k", "100") == "100", f
    if c["ibrido"] == "vector":
        return "V"
    assert c["ibrido"] == "union" and c["punteggio"] == "bm25" and c.get("bm25_espansioni") == "blended", f
    return {("any", "160"): "A", ("all", "10"): "B"}[(c["recupero"], c.get("peso_vettore", "20"))]


per_conf = {}
for f in a.valutazioni:
    v = json.load(open(f))
    k = configurazione(f, v)
    assert k not in per_conf, f"{f}: {k} due volte"
    per_conf[k] = (f, v)
assert sorted(per_conf) == sorted(CONFIGURAZIONI), f"servono {CONFIGURAZIONI}, ci sono {sorted(per_conf)}"
corpora = {v["config"]["corpus_sha256"] for _, v in per_conf.values()}
assert len(corpora) == 1, f"corpora diversi: {corpora}"

raccolta = json.load(open(a.raccolta, encoding="utf8"))
info = {q["query"]: q for q in raccolta["query"] if not q["vuota"]}
gruppi = {
    "tutte": lambda _: True,
    "crispiano": lambda q: info[q]["fonte"] == "crispiano",
    "fvg": lambda q: info[q]["fonte"] == "fvg",
    "con numero": lambda q: info[q]["contiene_numero"],
    "senza numero": lambda q: not info[q]["contiene_numero"],
}

risultati = {}
for k in CONFIGURAZIONI:
    righe = {r["query_id"]: r for r in per_conf[k][1]["per_query"]}
    assert righe.keys() == info.keys(), f"{k}: le query valutate non sono quelle della raccolta"
    risultati[k] = {}
    for g, dentro in gruppi.items():
        qs = [righe[q] for q in sorted(righe) if dentro(q)]
        n = len(qs)
        risultati[k][g] = {"query": n} if not n else {
            "query": n,
            "mrr@10": round(sum(r["mrr@10"] for r in qs) / n, 4),
            "atto_primo": round(sum(r["mrr@10"] == 1 for r in qs) / n, 4),
            "entro_10": round(sum(r["mrr@10"] > 0 for r in qs) / n, 4),
            "a_vuoto": round(sum(r["retrieved"] == 0 for r in qs) / n, 4),
        }

print(f"{'':6}" + "".join(f"{g:>22}" for g in gruppi))
for k in CONFIGURAZIONI:
    celle = [risultati[k][g] for g in gruppi]
    print(f"{k:6}" + "".join(f"{c.get('mrr@10', 0):>10.4f} ({c.get('a_vuoto', 0):>5.1%} ⌀)" for c in celle))
print("raccolta:", json.dumps(raccolta["riassunto"], ensure_ascii=False))

ora = datetime.datetime.now(datetime.timezone.utc)
git = lambda *x: subprocess.run(["git", "-C", QUI, *x], capture_output=True, text=True, check=True).stdout.strip()
esito = {"ran_at": ora.strftime("%Y-%m-%dT%H:%M:%SZ"),
         "config": {"commit": git("rev-parse", "--short", "HEAD"),
                    "modifiche_non_committate": "true" if git("status", "--porcelain", "--", QUI) else "false",
                    "valutazioni": {k: os.path.basename(f) for k, (f, _) in sorted(per_conf.items())},
                    "koskidex": sorted({v["config"]["commit"][:7] for _, v in per_conf.values()}),
                    "corpus_sha256": corpora.pop()},
         "raccolta": raccolta["riassunto"], "risultati": risultati}
if not os.environ.get("TESI_RISULTATI"):
    sys.exit("!!! RISULTATO NON ARCHIVIATO: TESI_RISULTATI non è impostata.")
d = os.path.join(os.environ["TESI_RISULTATI"], "esperimenti", "2026-09-25_known-item-umane")
os.makedirs(d, exist_ok=True)
o = ora.strftime("%Y-%m-%dT%H%M%SZ"); p = os.path.join(d, f"{o}_esito.json"); n = 2
while os.path.exists(p):
    p = os.path.join(d, f"{o}-{n}_esito.json"); n += 1
open(p, "x").write(json.dumps(esito, indent=2, ensure_ascii=False))
print("archiviato in", p)
