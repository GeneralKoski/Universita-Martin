#!/usr/bin/env python3
"""Quanto costa la ricerca per sottostringa di Koskidex (Task F6).

Legge rapporti di scripts/compare -sottostringa gia' archiviati e confronta,
query per query, la configurazione "or + euristico" con la stessa piu' la
sottostringa: stesso indice, stesse impostazioni, l'unica differenza e' la
scansione del vocabolario. Per ogni corpus prende la mediana delle esecuzioni.

    costo.py <rapporto> [<rapporto> ...]
"""
import datetime, json, os, statistics, sys

BASE, SOTTO = "or + euristico", "or + euristico + sottostringa"

per_corpus = {}
for f in sys.argv[1:]:
    r = json.load(open(f))
    if r["config"].get("modifiche_non_committate") != "false":
        sys.exit(f"{f}: prodotto da codice non committato, non vale")
    termini = {c["etichetta"]: c["termini"] for c in r["configurazioni"]}
    voce = per_corpus.setdefault(r["config"]["corpus"], {"rapporti": [], "termini": termini[SOTTO],
                                                         "commit": r["config"]["commit"], "query": {}})
    voce["rapporti"].append(os.path.basename(f))
    for q in r["query"]:
        b, s = q["esiti"][BASE], q["esiti"][SOTTO]
        riga = voce["query"].setdefault(q["query"], {"ms_base": [], "ms_sottostringa": [],
                                                     "trovati_base": b["trovati"], "trovati_sottostringa": s["trovati"]})
        riga["ms_base"].append(b["ms"])
        riga["ms_sottostringa"].append(s["ms"])

corpora = []
for corpus, v in per_corpus.items():
    righe = []
    for q, r in v["query"].items():
        mb, ms = statistics.median(r["ms_base"]), statistics.median(r["ms_sottostringa"])
        righe.append({"query": q, "ms_base": mb, "ms_sottostringa": ms, "ms_in_piu": ms - mb,
                      "trovati_base": r["trovati_base"], "trovati_sottostringa": r["trovati_sottostringa"],
                      "trovati_in_piu": r["trovati_sottostringa"] - r["trovati_base"]})
    in_piu = [r["ms_in_piu"] for r in righe]
    corpora.append({"corpus": corpus, "commit": v["commit"], "termini": v["termini"], "esecuzioni": len(v["rapporti"]),
                    "rapporti": v["rapporti"],
                    "ms_in_piu_mediana": statistics.median(in_piu), "ms_in_piu_min": min(in_piu), "ms_in_piu_max": max(in_piu),
                    "query": righe})
    print(f"\n{corpus}\n  {v['termini']} termini, {len(v['rapporti'])} esecuzioni, mediana per query")
    for r in righe:
        print(f"  {r['query']:10s} {r['ms_base']:6.2f} -> {r['ms_sottostringa']:6.2f} ms  (+{r['ms_in_piu']:5.2f})"
              f"   trovati {r['trovati_base']:5d} -> {r['trovati_sottostringa']:5d}")
    print(f"  ms in più: mediana {statistics.median(in_piu):.2f}, da {min(in_piu):.2f} a {max(in_piu):.2f}")

ora = datetime.datetime.now(datetime.timezone.utc)
esito = {"ran_at": ora.strftime("%Y-%m-%dT%H:%M:%SZ"), "config": {"confronto": f"{BASE} contro {SOTTO}",
         "statistica": "mediana delle esecuzioni per query"}, "corpora": corpora}
d = os.path.join(os.environ["TESI_RISULTATI"], "esperimenti", "2026-09-24_costo-sottostringa") if os.environ.get("TESI_RISULTATI") else None
if not d:
    print("\n!!! RISULTATO NON ARCHIVIATO: TESI_RISULTATI non è impostata.")
    sys.exit()
o = ora.strftime("%Y-%m-%dT%H%M%SZ"); p = os.path.join(d, f"{o}_esito.json"); n = 2
while os.path.exists(p):
    p = os.path.join(d, f"{o}-{n}_esito.json"); n += 1
open(p, "x").write(json.dumps(esito, indent=2, ensure_ascii=False))
print("\narchiviato in", p)
