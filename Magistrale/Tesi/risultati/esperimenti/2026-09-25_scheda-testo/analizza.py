#!/usr/bin/env python3
"""Scheda contro testo intero sugli atti di Crispiano: MRR@10, atto primo,
entro 10 e a vuoto per ogni configurazione. Metodo e previsioni nel README.

    analizza.py <valutazione> [...]   (le dieci di esegui.sh)
"""
import datetime, json, os, subprocess, sys

QUI = os.path.dirname(os.path.abspath(__file__))
ATTESE = ["scheda LA", "scheda LT", "scheda A", "testo LA", "testo LT", "testo A", "testo A 8192",
          "testo LA b0.25", "testo LA b0.5", "testo LA b1"]


def nome(f, v):
    c = v["config"]
    assert v["collection"] in ("crispiano-scheda", "crispiano-testo") and c.get("split") == "crispiano", f
    assert c.get("modifiche_non_committate") == "false", f"{f}: codice non committato"
    assert c["punteggio"] == "bm25" and c.get("bm25_espansioni") == "blended", f
    assert c["analisi"] == "none" and c["refusi"] == "0" and c["documenti"] == "563", f
    corpus = v["collection"].removeprefix("crispiano-")
    if "embedder" in c:
        assert c["recupero"] == "any" and c["ibrido"] == "union" and c.get("peso_vettore") == "160", f
        assert c["bm25_b"] == "0.75", f
        return {"ollama/bge-m3": f"{corpus} A", "ollama/bge-m3@8192": f"{corpus} A 8192"}[c["embedder"]]
    base = f"{corpus} {'LA' if c['recupero'] == 'any' else 'LT'}"
    return base if c["bm25_b"] == "0.75" else f"{base} b{c['bm25_b']}"


per_conf = {}
for f in sys.argv[1:]:
    v = json.load(open(f))
    k = nome(f, v)
    assert k not in per_conf, f"{f}: {k} due volte"
    per_conf[k] = (f, v)
assert sorted(per_conf) == sorted(ATTESE), f"servono {ATTESE}: {sorted(per_conf)}"
query = {k: sorted(r["query_id"] for r in v["per_query"]) for k, (_, v) in per_conf.items()}
assert len({tuple(x) for x in query.values()}) == 1, "le configurazioni non hanno le stesse query"

risultati = {}
for k in ATTESE:
    qs = per_conf[k][1]["per_query"]
    n = len(qs)
    risultati[k] = {"query": n,
                    "mrr@10": round(sum(r["mrr@10"] for r in qs) / n, 4),
                    "atto_primo": round(sum(r["mrr@10"] == 1 for r in qs) / n, 4),
                    "entro_10": round(sum(r["mrr@10"] > 0 for r in qs) / n, 4),
                    "a_vuoto": round(sum(r["retrieved"] == 0 for r in qs) / n, 4)}
    print(f"{k:16} " + "  ".join(f"{x} {y}" for x, y in risultati[k].items()))

ora = datetime.datetime.now(datetime.timezone.utc)
git = lambda *x: subprocess.run(["git", "-C", QUI, *x], capture_output=True, text=True, check=True).stdout.strip()
esito = {"ran_at": ora.strftime("%Y-%m-%dT%H:%M:%SZ"),
         "config": {"commit": git("rev-parse", "--short", "HEAD"),
                    "modifiche_non_committate": "true" if git("status", "--porcelain", "--", QUI) else "false",
                    "valutazioni": {k: os.path.basename(f) for k, (f, _) in sorted(per_conf.items())},
                    "koskidex": sorted({v["config"]["commit"][:7] for _, v in per_conf.values()}),
                    "corpora_sha256": sorted({v["config"]["corpus_sha256"] for _, v in per_conf.values()})},
         "risultati": risultati}
if not os.environ.get("TESI_RISULTATI"):
    sys.exit("!!! RISULTATO NON ARCHIVIATO: TESI_RISULTATI non è impostata.")
d = os.path.join(os.environ["TESI_RISULTATI"], "esperimenti", "2026-09-25_scheda-testo")
os.makedirs(d, exist_ok=True)
o = ora.strftime("%Y-%m-%dT%H%M%SZ"); p = os.path.join(d, f"{o}_esito.json"); k = 2
while os.path.exists(p):
    p = os.path.join(d, f"{o}-{k}_esito.json"); k += 1
open(p, "x").write(json.dumps(esito, indent=2, ensure_ascii=False))
print("archiviato in", p)
