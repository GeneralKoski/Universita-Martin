#!/usr/bin/env python3
"""Parità dell'innesto: le stesse query, passate dall'app, sui due motori.

Legge rapporti di app:eval-run-queries già archiviati, alcuni con
SEARCH_BACKEND=koskidex e altri con elasticsearch, e per ogni query confronta
l'insieme trovato, il top 10 e la latenza mediana delle esecuzioni.

    confronta.py <rapporto> [<rapporto> ...]
"""
import datetime, json, os, statistics, sys

rapporti = {"koskidex": [], "elasticsearch": []}
for f in sys.argv[1:]:
    r = json.load(open(f))
    if r["config"].get("modifiche_non_committate") != "false":
        sys.exit(f"{f}: prodotto da codice non committato, non vale")
    r["_file"] = os.path.basename(f)
    rapporti[r["config"]["motore"]].append(r)
kx, es = rapporti["koskidex"], rapporti["elasticsearch"]
if not kx or not es:
    sys.exit("servono rapporti di tutti e due i motori")

righe = []
for i, q in enumerate(kx[0]["query"]):
    e = es[0]["query"][i]
    assert e["query"] == q["query"], "i file di query non coincidono"
    a, b = set(q["ids"]), set(e["ids"])
    righe.append({"query": q["query"], "trovati_koskidex": len(a), "trovati_elasticsearch": len(b),
                  "solo_koskidex": len(a - b), "solo_elasticsearch": len(b - a),
                  "insieme_identico": a == b, "top10_identico": q["ids"][:10] == e["ids"][:10],
                  "ms_koskidex": statistics.median(r["query"][i]["ms"] for r in kx),
                  "ms_elasticsearch": statistics.median(r["query"][i]["ms"] for r in es)})

identici = sum(r["insieme_identico"] for r in righe)
top10 = sum(r["top10_identico"] for r in righe)
print(f"insiemi identici {identici}/{len(righe)}, top 10 identici {top10}/{len(righe)}")
print(f"ms mediana per query: koskidex {statistics.median(r['ms_koskidex'] for r in righe):.1f}, "
      f"elasticsearch {statistics.median(r['ms_elasticsearch'] for r in righe):.1f}")

ora = datetime.datetime.now(datetime.timezone.utc)
esito = {"ran_at": ora.strftime("%Y-%m-%dT%H:%M:%SZ"),
         "config": {"rapporti_koskidex": [r["_file"] for r in kx], "rapporti_elasticsearch": [r["_file"] for r in es],
                    "commit_documentale": kx[0]["config"]["commit"], "koskidex_versione": kx[0]["config"]["koskidex_versione"],
                    "elasticsearch_versione": es[0]["config"]["elasticsearch_versione"],
                    "documenti": {"koskidex": kx[0]["config"]["documenti_indicizzati"], "elasticsearch": es[0]["config"]["documenti_indicizzati"]},
                    "statistica": "insiemi dalla prima esecuzione di ciascun motore, ms mediana delle esecuzioni"},
         "insiemi_identici": identici, "top10_identici": top10, "query": righe}
if not os.environ.get("TESI_RISULTATI"):
    sys.exit("!!! RISULTATO NON ARCHIVIATO: TESI_RISULTATI non è impostata.")
d = os.path.join(os.environ["TESI_RISULTATI"], "esperimenti", "2026-09-25_innesto-parita")
o = ora.strftime("%Y-%m-%dT%H%M%SZ"); p = os.path.join(d, f"{o}_esito.json"); n = 2
while os.path.exists(p):
    p = os.path.join(d, f"{o}-{n}_esito.json"); n += 1
open(p, "x").write(json.dumps(esito, indent=2, ensure_ascii=False))
print("archiviato in", p)
