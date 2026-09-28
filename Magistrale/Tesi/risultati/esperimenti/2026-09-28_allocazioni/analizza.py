#!/usr/bin/env python3
"""Confronta il "dopo" di 2026-09-28_allocazioni con il "prima" (misura.sh e
identita.sh delle due fasi) e controlla le previsioni 1-7 del README. Per
ogni etichetta usa l'esito più recente; archivia il riassunto.

Le allocazioni per ricerca si calcolano come in 2026-09-28_prestazioni: il
totale allocato dall'avvio diviso per le ricerche della misura a 8 client.

    analizza.py
"""
import datetime, glob, json, os, re, subprocess, sys

QUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.environ.get("TESI_RISULTATI") or os.path.join(QUI, "..", "..")
DIR = os.path.join(BASE, "esperimenti", "2026-09-28_allocazioni")


def esiti(cartella):
    out = {}
    for p in sorted(glob.glob(os.path.join(cartella, "*.json"))):
        m = re.match(r"\d{4}-\d\d-\d\dT\d{6}Z(?:-\d+)?_(.+)\.json$", os.path.basename(p))
        if m:
            d = json.load(open(p))
            assert d["config"].get("modifiche_non_committate") in ("false", False), f"{p}: codice non committato"
            out[m.group(1)] = (os.path.basename(p), d)
    return out


fasi = {f: esiti(os.path.join(DIR, f)) for f in ("prima", "dopo")}
for f in fasi:
    for n in ("seq-koskidex-docker", "seq-koskidex-nativo", "carico-koskidex-docker", "carico-koskidex-nativo",
              "seq-koskidex-docker-100000", "profilo-carico-koskidex-nativo"):
        if n not in fasi[f]:
            sys.exit(f"manca l'esito {f} {n}")
e = lambda f, n: fasi[f][n][1]
seq = lambda f, n, q: e(f, n)["sequenziale"]["riassunto"]["tutte"][q]
qps_max = lambda f, n: max(l["ricerche_al_secondo"] for l in e(f, n)["carico"])

righe = {}
print("Una ricerca alla volta, ms: prima -> dopo")
for n in ("seq-koskidex-docker", "seq-koskidex-nativo", "seq-koskidex-docker-100000"):
    righe[n] = {q: [seq("prima", n, q), seq("dopo", n, q)] for q in ("p50", "p95", "p99")}
    print(f"  {n:28} " + "   ".join(f"{q} {a:7.2f} -> {b:7.2f}" for q, (a, b) in righe[n].items()))

carico = {}
print("\nSotto carico: ricerche/s, p99 ms, memoria max MB: prima -> dopo")
for n in ("carico-koskidex-docker", "carico-koskidex-nativo"):
    carico[n] = []
    for la, lb in zip(e("prima", n)["carico"], e("dopo", n)["carico"]):
        r = {"client": la["client"], "qps": [la["ricerche_al_secondo"], lb["ricerche_al_secondo"]],
             "p99": [la["latenza_ms"]["p99"], lb["latenza_ms"]["p99"]],
             "memoria_max_mb": [la["risorse"].get("memoria_mb", {}).get("max"), lb["risorse"].get("memoria_mb", {}).get("max")],
             "errori": [la["errori"], lb["errori"]]}
        carico[n].append(r)
        print(f"  {n:24} {r['client']:3} client  {r['qps'][0]:7.1f} -> {r['qps'][1]:7.1f}/s  "
              f"p99 {r['p99'][0]:6.2f} -> {r['p99'][1]:6.2f}  mem {r['memoria_max_mb'][0]} -> {r['memoria_max_mb'][1]}")


def profilo(f):
    tops = sorted(glob.glob(os.path.join(DIR, f, "profilo", "*_allocs-top.txt")))
    if not tops:
        sys.exit(f"manca il profilo delle allocazioni {f}")
    testo = open(tops[-1]).read()
    totale = float(re.search(r"of ([\d.]+)MB total", testo).group(1))
    m = re.search(r"^\s*[\d.]+[kMG]?B\s+([\d.]+)%.*\.fuzzyCandidates$", testo, re.M)
    ricerche = e(f, "profilo-carico-koskidex-nativo")["carico"][0]["richieste"]
    return {"mb_per_ricerca": round(totale / ricerche, 4), "mb_totali": totale, "ricerche": ricerche,
            "quota_fuzzycandidates": float(m.group(1)) if m else 0.0, "profilo": os.path.basename(tops[-1])}


alloc = {f: profilo(f) for f in fasi}
for f, a in alloc.items():
    print(f"Allocazioni {f}: {a['mb_totali']:.0f} MB in {a['ricerche']} ricerche, {a['mb_per_ricerca']:.3f} MB a ricerca, "
          f"fuzzyCandidates {a['quota_fuzzycandidates']}%")

impronte = {}
for n in ("10018", "100000"):
    a = json.load(open(sorted(glob.glob(os.path.join(DIR, f"*_risposte-prima-{n}.json")))[-1]))["risposte"]
    b = json.load(open(sorted(glob.glob(os.path.join(DIR, f"*_risposte-dopo-{n}.json")))[-1]))["risposte"]
    impronte[n] = {"query": len(a["query"]), "diverse": sum(a["query"][k] != b["query"].get(k) for k in a["query"]),
                   "errori": [a["errori"], b["errori"]]}
CHIAVI = ("mean_mrr@10", "mean_ndcg@10", "mean_recall@100", "per_query", "queries", "skipped_no_relevant", "zero_results")
senza_ora = lambda p: re.sub(r"^\d{4}-\d\d-\d\dT\d{6}Z_", "", os.path.basename(p))
valutazioni = {senza_ora(p): p for p in sorted(glob.glob(os.path.join(DIR, "evaluate", "*.json")))}
metriche = {}
for nome, p in sorted(valutazioni.items()):
    if "-prima-" in nome:
        a, b = json.load(open(p)), json.load(open(valutazioni[nome.replace("-prima-", "-dopo-")]))
        assert b["config"].get("modifiche_non_committate") in ("false", False)
        metriche[nome.replace("-prima-", "-")[:-5]] = all(a[k] == b[k] for k in CHIAVI)
print("Impronte:", json.dumps(impronte), "\nMetriche di evaluate uguali:", json.dumps(metriche))

previsioni = {}


def prev(k, testo, ok, valore):
    previsioni[k] = {"previsione": testo, "valore": valore, "esito": "confermata" if ok else "smentita"}
    print(f"{k}. {previsioni[k]['esito']:10} {testo}: {valore}")


print()
ok = all(v["diverse"] == 0 and v["query"] == 429 for v in impronte.values()) and len(metriche) == 9 and all(metriche.values())
prev(1, "nessun risultato cambia (impronte a 10.018 e 100.000, metriche di evaluate)", ok,
     f"impronte diverse {impronte['10018']['diverse']} e {impronte['100000']['diverse']} su 429; "
     f"evaluate uguali {sum(metriche.values())} su {len(metriche)}")
a, b = alloc["prima"]["mb_per_ricerca"], alloc["dopo"]["mb_per_ricerca"]
prev(2, "allocazioni per ricerca almeno -60% nel profilo a 8 client", b <= 0.4 * a,
     f"{a:.3f} -> {b:.3f} MB, {100 * (1 - b / a):.0f}% in meno")
a, b = alloc["prima"]["quota_fuzzycandidates"], alloc["dopo"]["quota_fuzzycandidates"]
prev(3, "fuzzyCandidates sotto il 10% dei byte allocati", b < 10, f"{a}% -> {b}%")
for k, n, dove in ((4, "carico-koskidex-nativo", "nativa"), (5, "carico-koskidex-docker", "nel container")):
    a, b = qps_max("prima", n), qps_max("dopo", n)
    prev(k, f"capacità {dove}, massimo almeno +5%", b >= 1.05 * a, f"{a} -> {b} ricerche/s ({100 * (b / a - 1):+.1f}%)")
(a95, b95), (a99, b99) = righe["seq-koskidex-docker-100000"]["p95"], righe["seq-koskidex-docker-100000"]["p99"]
prev(6, "a 100.000 documenti p95 e p99 almeno -15%", b95 <= 0.85 * a95 and b99 <= 0.85 * a99,
     f"p95 {a95} -> {b95} ms ({100 * (b95 / a95 - 1):+.1f}%), p99 {a99} -> {b99} ms ({100 * (b99 / a99 - 1):+.1f}%)")
a, b = righe["seq-koskidex-docker"]["p50"]
prev(7, "una alla volta nel container, p50 non peggiora di più del 5%", b <= 1.05 * a,
     f"{a} -> {b} ms ({100 * (b / a - 1):+.1f}%)")

ora = datetime.datetime.now(datetime.timezone.utc)
git = lambda *x: subprocess.run(["git", "-C", QUI, *x], capture_output=True, text=True, check=True).stdout.strip()
esito = {"ran_at": ora.strftime("%Y-%m-%dT%H:%M:%SZ"),
         "config": {"commit": git("rev-parse", "--short", "HEAD"),
                    "modifiche_non_committate": "true" if git("status", "--porcelain", "--untracked-files=no", "--", QUI) else "false",
                    "koskidex": {f: sorted({d["config"].get("commit", "")[:7] for _, d in fasi[f].values()}) for f in fasi},
                    "esiti": {f: {n: x for n, (x, _) in sorted(fasi[f].items())} for f in fasi}},
         "sequenziale": righe, "carico": carico, "allocazioni": alloc,
         "impronte": impronte, "evaluate_uguali": metriche, "previsioni": previsioni}
if not os.environ.get("TESI_RISULTATI"):
    sys.exit("!!! RISULTATO NON ARCHIVIATO: TESI_RISULTATI non è impostata.")
o = ora.strftime("%Y-%m-%dT%H%M%SZ"); p = os.path.join(DIR, f"{o}_esito.json"); k = 2
while os.path.exists(p):
    p = os.path.join(DIR, f"{o}-{k}_esito.json"); k += 1
open(p, "x").write(json.dumps(esito, indent=2, ensure_ascii=False))
print("archiviato in", p)
