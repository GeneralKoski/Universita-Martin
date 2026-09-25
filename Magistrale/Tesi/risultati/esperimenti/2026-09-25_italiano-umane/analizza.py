#!/usr/bin/env python3
"""Stopword e stemmer italiani sulle known-item umane: per recupero (any, all)
e analisi (none, italian-stopwords, italian-stemmer, italian), MRR@10, atto
primo, entro 10, a vuoto e candidati medi. Metodo e previsioni nel README.

    analizza.py <valutazione> [...]
        (le sei di esegui.sh più LA e LT di 2026-09-25_known-item-umane)
"""
import datetime, json, os, subprocess, sys

QUI = os.path.dirname(os.path.abspath(__file__))
ANALISI = ["none", "italian-stopwords", "italian-stemmer", "italian"]

per_conf = {}
for f in sys.argv[1:]:
    v = json.load(open(f))
    c = v["config"]
    assert v["collection"] == "known-item-umane" and c.get("split", "test") == "test", f
    assert c.get("modifiche_non_committate") == "false", f"{f}: codice non committato"
    assert c["punteggio"] == "bm25" and c.get("bm25_espansioni") == "blended" and c["refusi"] == "0", f
    assert "embedder" not in c and c.get("tokenizer", "") == "" and "elisione" not in c, f
    k = (c["recupero"], c["analisi"])
    assert k[1] in ANALISI and k not in per_conf, f"{f}: {k}"
    per_conf[k] = (f, v)
assert len(per_conf) == 8, f"servono otto valutazioni, any e all per quattro analisi: {sorted(per_conf)}"
assert len({v["config"]["corpus_sha256"] for _, v in per_conf.values()}) == 1

risultati = {}
for (modo, analisi), (f, v) in sorted(per_conf.items()):
    qs = v["per_query"]
    n = len(qs)
    risultati.setdefault(modo, {})[analisi] = {
        "query": n,
        "mrr@10": round(sum(r["mrr@10"] for r in qs) / n, 4),
        "atto_primo": round(sum(r["mrr@10"] == 1 for r in qs) / n, 4),
        "entro_10": round(sum(r["mrr@10"] > 0 for r in qs) / n, 4),
        "a_vuoto": round(sum(r["retrieved"] == 0 for r in qs) / n, 4),
        "candidati_medi": round(sum(r["candidates"] for r in qs) / n, 1),
    }
    print(f"{modo:4} {analisi:18} " + "  ".join(f"{k} {x}" for k, x in risultati[modo][analisi].items()))

ora = datetime.datetime.now(datetime.timezone.utc)
git = lambda *x: subprocess.run(["git", "-C", QUI, *x], capture_output=True, text=True, check=True).stdout.strip()
esito = {"ran_at": ora.strftime("%Y-%m-%dT%H:%M:%SZ"),
         "config": {"commit": git("rev-parse", "--short", "HEAD"),
                    "modifiche_non_committate": "true" if git("status", "--porcelain", "--", QUI) else "false",
                    "valutazioni": {f"{m}/{a}": os.path.basename(f) for (m, a), (f, _) in sorted(per_conf.items())},
                    "koskidex": sorted({v["config"]["commit"][:7] for _, v in per_conf.values()})},
         "risultati": risultati}
if not os.environ.get("TESI_RISULTATI"):
    sys.exit("!!! RISULTATO NON ARCHIVIATO: TESI_RISULTATI non è impostata.")
d = os.path.join(os.environ["TESI_RISULTATI"], "esperimenti", "2026-09-25_italiano-umane")
os.makedirs(d, exist_ok=True)
o = ora.strftime("%Y-%m-%dT%H%M%SZ"); p = os.path.join(d, f"{o}_esito.json"); k = 2
while os.path.exists(p):
    p = os.path.join(d, f"{o}-{k}_esito.json"); k += 1
open(p, "x").write(json.dumps(esito, indent=2, ensure_ascii=False))
print("archiviato in", p)
