#!/usr/bin/env python3
"""Confronta il "dopo" di 2026-09-28_prestazioni con il "prima", cioè le misure
di Koskidex di 2026-09-28_carico, e controlla le previsioni 1-8 del README con
le loro soglie. Per ogni etichetta usa l'esito più recente; archivia il
riassunto.

Le allocazioni per ricerca sono il totale allocato dall'avvio (profilo allocs,
alloc_space) diviso per le ricerche della misura a 8 client: il totale
comprende anche il caricamento dell'indice e i 5 s di riscaldamento, uguali
prima e dopo, quindi il valore è un po' alto in entrambi e il rapporto regge.

    analizza.py
"""
import datetime, glob, json, os, re, subprocess, sys

QUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.environ.get("TESI_RISULTATI") or os.path.join(QUI, "..", "..")
DIR_DOPO = os.path.join(BASE, "esperimenti", "2026-09-28_prestazioni")
DIR_PRIMA = os.path.join(BASE, "esperimenti", "2026-09-28_carico")


def esiti(cartella):
    out = {}
    for p in sorted(glob.glob(os.path.join(cartella, "*.json"))):
        m = re.match(r"\d{4}-\d\d-\d\dT\d{6}Z(?:-\d+)?_(.+)\.json$", os.path.basename(p))
        if m and not m.group(1).startswith("esito"):
            out[m.group(1)] = (os.path.basename(p), json.load(open(p)))
    return out


prima, dopo = esiti(DIR_PRIMA), esiti(DIR_DOPO)


def e(fase, nome):
    tutti = prima if fase == "prima" else dopo
    if nome not in tutti:
        sys.exit(f"manca l'esito {fase} {nome}")
    f, d = tutti[nome]
    assert d["config"].get("modifiche_non_committate") in ("false", False), f"{f}: codice non committato"
    return d


def seq(fase, nome, q):
    return e(fase, nome)["sequenziale"]["riassunto"]["tutte"][q]


def carichi(fase, nome):
    return e(fase, nome)["carico"]


def livello(fase, nome, client):
    return next(l for l in carichi(fase, nome) if l["client"] == client)


def mem_riposo(fase, nome):
    return e(fase, nome)["riposo"]["riassunto"]["memoria_mb"]["p50"]


def mem_carico(fase, nome):
    return max(l["risorse"]["memoria_mb"]["max"] for l in carichi(fase, nome) if l["risorse"].get("campioni"))


def mb_per_ricerca(cartella, nome_profilo, tutti):
    tops = sorted(glob.glob(os.path.join(cartella, "profilo", "*_allocs-top.txt")))
    if not tops:
        sys.exit(f"manca il profilo delle allocazioni in {cartella}")
    totale = float(re.search(r"of ([\d.]+)MB total", open(tops[-1]).read()).group(1))
    ricerche = tutti[nome_profilo][1]["carico"][0]["richieste"]
    return totale / ricerche, totale, ricerche, os.path.basename(tops[-1])


righe = {}
print("Una ricerca alla volta, ms: prima -> dopo")
for n in ["seq-koskidex-docker", "seq-koskidex-docker-cache", "seq-koskidex-nativo", "seq-koskidex-docker-100000"]:
    righe[n] = {q: [seq("prima", n, q), seq("dopo", n, q)] for q in ("p50", "p95", "p99")}
    print(f"  {n:28} " + "   ".join(f"{q} {a:7.2f} -> {b:7.2f}" for q, (a, b) in righe[n].items()))

confronto_carico = {}
print("\nSotto carico: ricerche/s, p50, p99 ms, memoria max MB, CPU media %: prima -> dopo")
for n in ["carico-koskidex-docker", "carico-koskidex-nativo"]:
    confronto_carico[n] = []
    print(" ", n)
    for la, lb in zip(carichi("prima", n), carichi("dopo", n)):
        r = {"client": la["client"]}
        for k, f in (("qps", lambda l: l["ricerche_al_secondo"]), ("p50", lambda l: l["latenza_ms"]["p50"]),
                     ("p99", lambda l: l["latenza_ms"]["p99"]),
                     ("memoria_max_mb", lambda l: l["risorse"].get("memoria_mb", {}).get("max")),
                     ("cpu_media", lambda l: l["risorse"].get("cpu_percento", {}).get("media")),
                     ("errori", lambda l: l["errori"])):
            r[k] = [f(la), f(lb)]
        confronto_carico[n].append(r)
        print(f"    {r['client']:3} client  {r['qps'][0]:7.1f} -> {r['qps'][1]:7.1f}/s  p50 {r['p50'][0]:6.2f} -> {r['p50'][1]:6.2f}"
              f"  p99 {r['p99'][0]:7.2f} -> {r['p99'][1]:7.2f}  mem {r['memoria_max_mb'][0]} -> {r['memoria_max_mb'][1]}"
              f"  cpu {r['cpu_media'][0]} -> {r['cpu_media'][1]}  errori {r['errori'][1]}")

riposi = {n: [mem_riposo("prima", n), mem_riposo("dopo", n)]
          for n in ("riposo-koskidex-docker-10018", "riposo-koskidex-docker-100000")}
print("\nA riposo, memoria MB (p50), prima -> dopo:", json.dumps(riposi))

alloc = {"prima": mb_per_ricerca(DIR_PRIMA, "profilo-carico-koskidex-nativo", prima),
         "dopo": mb_per_ricerca(DIR_DOPO, "profilo-carico-koskidex-nativo", dopo)}
for f, (x, tot, n, file) in alloc.items():
    print(f"Allocazioni {f}: {tot:.0f} MB in {n} ricerche, {x:.2f} MB a ricerca ({file})")

impronte = {}
for n in ("10018", "100000"):
    a = json.load(open(glob.glob(os.path.join(DIR_DOPO, f"*_risposte-prima-{n}.json"))[-1]))["risposte"]
    b = json.load(open(glob.glob(os.path.join(DIR_DOPO, f"*_risposte-dopo-{n}.json"))[-1]))["risposte"]
    impronte[n] = {"query": len(a["query"]), "diverse": sum(a["query"][k] != b["query"].get(k) for k in a["query"]),
                   "errori": [a["errori"], b["errori"]]}
metriche = {}
CHIAVI = ("mean_mrr@10", "mean_ndcg@10", "mean_recall@100", "per_query", "queries", "skipped_no_relevant", "zero_results")
senza_ora = lambda p: re.sub(r"^\d{4}-\d\d-\d\dT\d{6}Z_", "", os.path.basename(p))
valutazioni = {senza_ora(p): p for p in sorted(glob.glob(os.path.join(DIR_DOPO, "evaluate", "*.json")))}
for nome, p in sorted(valutazioni.items()):
    if "-prima-" in nome:
        a, b = json.load(open(p)), json.load(open(valutazioni[nome.replace("-prima-", "-dopo-")]))
        metriche[nome.replace("-prima-", "-")[:-5]] = all(a[k] == b[k] for k in CHIAVI)
print("Impronte:", json.dumps(impronte), "\nMetriche di evaluate uguali:", json.dumps(metriche))

previsioni = {}


def prev(k, testo, ok, valore):
    previsioni[k] = {"previsione": testo, "valore": valore, "esito": "confermata" if ok else "smentita"}
    print(f"{k}. {previsioni[k]['esito']:10} {testo}: {valore}")


print()
ok = all(v["diverse"] == 0 for v in impronte.values()) and len(metriche) == 9 and all(metriche.values())
prev(1, "nessun risultato cambia (impronte a 10.018 e 100.000, metriche di evaluate)", ok,
     f"impronte diverse {impronte['10018']['diverse']} e {impronte['100000']['diverse']} su 429; "
     f"evaluate uguali {sum(metriche.values())} su {len(metriche)}")
a, b = alloc["prima"][0], alloc["dopo"][0]
prev(2, "allocazioni per ricerca almeno -60% nel profilo a 8 client", b <= 0.4 * a,
     f"{a:.2f} -> {b:.2f} MB, {100 * (1 - b / a):.0f}% in meno")
a, b = seq("dopo", "seq-koskidex-docker", "p50"), seq("dopo", "seq-koskidex-docker", "p95")
prev(3, "una alla volta nel container p50 <= 1,5 ms e p95 <= 6", a <= 1.5 and b <= 6, f"p50 {a}, p95 {b} ms")
a = max(l["ricerche_al_secondo"] for l in carichi("dopo", "carico-koskidex-docker"))
prev(4, "massimo ricerche/s nel container >= 900", a >= 900, f"{a}")
a = livello("dopo", "carico-koskidex-docker", 32)["latenza_ms"]["p99"]
prev(5, "a 32 client p99 nel container <= 110 ms", a <= 110, f"{a} ms")
a, b = seq("dopo", "seq-koskidex-docker-100000", "p95"), seq("dopo", "seq-koskidex-docker-100000", "p99")
prev(6, "a 100.000 documenti p95 <= 40 ms e p99 <= 60", a <= 40 and b <= 60, f"p95 {a}, p99 {b} ms")
r0, r1 = riposi["riposo-koskidex-docker-10018"]
m = mem_carico("dopo", "carico-koskidex-docker")
prev(7, "a riposo entro il 10% di prima, sotto carico massimo <= 300 MB", abs(r1 / r0 - 1) <= 0.10 and m <= 300,
     f"riposo {r0} -> {r1} MB ({100 * (r1 / r0 - 1):+.1f}%), carico massimo {m} MB")
a = livello("dopo", "carico-koskidex-docker", 1)["risorse"]["cpu_percento"]["media"]
prev(8, "con un client la CPU nel container <= 100%", a <= 100, f"{a}%")

ora = datetime.datetime.now(datetime.timezone.utc)
git = lambda *x: subprocess.run(["git", "-C", QUI, *x], capture_output=True, text=True, check=True).stdout.strip()
esito = {"ran_at": ora.strftime("%Y-%m-%dT%H:%M:%SZ"),
         "config": {"commit": git("rev-parse", "--short", "HEAD"),
                    "modifiche_non_committate": "true" if git("status", "--porcelain", "--untracked-files=no", "--", QUI) else "false",
                    "prima": {n: f for n, (f, _) in sorted(prima.items()) if "koskidex" in n},
                    "dopo": {n: f for n, (f, _) in sorted(dopo.items())}},
         "sequenziale": righe, "carico": confronto_carico, "riposo_mb": riposi,
         "allocazioni": {f: {"mb_per_ricerca": round(x, 3), "mb_totali": tot, "ricerche": n, "profilo": file}
                         for f, (x, tot, n, file) in alloc.items()},
         "impronte": impronte, "evaluate_uguali": metriche, "previsioni": previsioni}
if not os.environ.get("TESI_RISULTATI"):
    sys.exit("!!! RISULTATO NON ARCHIVIATO: TESI_RISULTATI non è impostata.")
o = ora.strftime("%Y-%m-%dT%H%M%SZ"); p = os.path.join(DIR_DOPO, f"{o}_esito.json"); k = 2
while os.path.exists(p):
    p = os.path.join(DIR_DOPO, f"{o}-{k}_esito.json"); k += 1
open(p, "x").write(json.dumps(esito, indent=2, ensure_ascii=False))
print("archiviato in", p)
