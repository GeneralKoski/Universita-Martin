#!/usr/bin/env python3
"""Riassume le misure di 2026-09-28_carico e controlla le previsioni 1-9 del
README con le loro soglie (la 10, sul profilo, si legge nei file di profilo/).
Per ogni etichetta usa l'esito più recente; archivia il riassunto.

I quattro esiti di copia.py del 28/09 (commit 427cc96) dicono "modifiche non
committate" perché copia.py contava anche i file di risultato non tracciati
della sua cartella, non il codice: al commit 427cc96 nessun file tracciato era
modificato, e da lì copia.py conta solo i file tracciati. Sono accettati.

    analizza.py
"""
import datetime, glob, json, os, re, subprocess, sys

QUI = os.path.dirname(os.path.abspath(__file__))
ARCHIVIO = os.path.join(os.environ.get("TESI_RISULTATI") or os.path.join(QUI, "..", ".."), "esperimenti", "2026-09-28_carico")

esiti = {}
for p in sorted(glob.glob(os.path.join(ARCHIVIO, "*.json"))):
    m = re.match(r"\d{4}-\d\d-\d\dT\d{6}Z(?:-\d+)?_(.+)\.json$", os.path.basename(p))
    if m and not m.group(1).startswith("esito"):
        esiti[m.group(1)] = (os.path.basename(p), json.load(open(p)))

def e(nome):
    if nome not in esiti:
        sys.exit(f"manca l'esito {nome}")
    f, d = esiti[nome]
    pulito = d["config"].get("modifiche_non_committate") in ("false", False)
    pulito = pulito or (nome.startswith("copia-") and d["config"].get("commit") == "427cc96")
    assert pulito, f"{f}: codice non committato"
    return d

def seq(nome, gruppo="tutte", q="p50"):
    return e(nome)["sequenziale"]["riassunto"].get(gruppo, {}).get(q)

def massimo_qps(nome):
    return max(l["ricerche_al_secondo"] for l in e(nome)["carico"])

def livello(nome, client):
    return next(l for l in e(nome)["carico"] if l["client"] == client)

def mem_carico(nome):
    return max(l["risorse"]["memoria_mb"]["max"] for l in e(nome)["carico"] if l["risorse"].get("campioni"))

def mem_riposo(nome):
    return e(nome)["riposo"]["riassunto"]["memoria_mb"]["p50"]

righe = {}
print("Una ricerca alla volta, ms (p50 / p95 / p99), tutte le 400 query per 5 passate")
for n in ["seq-es-app", "seq-es-senza-source", "seq-koskidex-docker", "seq-koskidex-docker-cache", "seq-koskidex-nativo",
          "seq-es-app-50000", "seq-koskidex-docker-50000", "seq-es-app-100000", "seq-koskidex-docker-100000"]:
    if n in esiti:
        r = e(n)["sequenziale"]["riassunto"]
        righe[n] = {g: {k: v[k] for k in ("n", "p50", "p95", "p99")} | {"byte_p50": v["byte"]["p50"]} for g, v in r.items()}
        t, pp, ps = r["tutte"], r.get("prima passata", {}), r.get("passate successive", {})
        print(f"  {n:28} {t['p50']:7.2f} {t['p95']:7.2f} {t['p99']:7.2f}   prima passata p50 {pp.get('p50')}, "
              f"successive p50 {ps.get('p50')}, byte p50 {t['byte']['p50']:.0f}")

carichi = {}
print("\nSotto carico: ricerche al secondo, p50 e p99 in ms, memoria massima MB, CPU media %")
for n in ["carico-es-app", "carico-es-senza-source", "carico-koskidex-docker", "carico-koskidex-nativo"]:
    if n in esiti:
        carichi[n] = []
        print(" ", n)
        for l in e(n)["carico"]:
            ris = l["risorse"]
            riga = {"client": l["client"], "qps": l["ricerche_al_secondo"], "p50": l["latenza_ms"]["p50"],
                    "p99": l["latenza_ms"]["p99"], "errori": l["errori"],
                    "memoria_max_mb": ris.get("memoria_mb", {}).get("max"), "cpu_media": ris.get("cpu_percento", {}).get("media")}
            carichi[n].append(riga)
            print(f"    {riga['client']:3} client {riga['qps']:8.1f}/s  p50 {riga['p50']:7.2f}  p99 {riga['p99']:7.2f}  "
                  f"mem {riga['memoria_max_mb']}  cpu {riga['cpu_media']}  errori {riga['errori']}")

riposi = {n: mem_riposo(n) for n in esiti if n.startswith("riposo-")}
print("\nA riposo, memoria MB (p50):", json.dumps(riposi, ensure_ascii=False))

copie = {n: {k: e(n)[k] for k in ("documenti", "indicizzazione_s", "byte_su_disco")} for n in esiti if n.startswith("copia-")}
print("Copie:", json.dumps(copie, ensure_ascii=False))

previsioni = {}
def prev(k, testo, ok, valore):
    previsioni[k] = {"previsione": testo, "valore": valore, "esito": "confermata" if ok else "smentita"}
    print(f"{k}. {previsioni[k]['esito']:10} {testo}: {valore}")

print()
a, b = seq("seq-koskidex-docker"), seq("seq-es-app")
prev(1, "p50 Koskidex nel container < p50 Elasticsearch come l'app", a < b, f"{a} contro {b} ms")
a, b = seq("seq-es-app", "risultati da 1000"), seq("seq-es-senza-source", "risultati da 1000")
n1000 = e("seq-es-app")["sequenziale"]["riassunto"].get("risultati da 1000", {}).get("n", 0)
prev(2, "da 1.000 risultati, p50 ES come l'app >= 2 x senza _source", a is not None and b is not None and a >= 2 * b,
     f"{a} contro {b} ms su {n1000} richieste")
a, b = seq("seq-es-senza-source"), seq("seq-koskidex-docker")
prev(3, "p50 ES senza _source e Koskidex entro un fattore 2", 0.5 <= a / b <= 2, f"{a} e {b} ms, rapporto {a / b:.2f}")
a = seq("seq-koskidex-docker-cache", "passate successive")
prev(4, "con la cache, p50 Koskidex < 1 ms a richieste ripetute", a < 1, f"{a} ms")
a, b = massimo_qps("carico-koskidex-docker"), massimo_qps("carico-es-app")
prev(5, "massimo ricerche/s Koskidex nel container >= 1,5 x ES come l'app", a >= 1.5 * b, f"{a} contro {b}, rapporto {a / b:.2f}")
a, b = mem_carico("carico-es-app"), mem_carico("carico-koskidex-docker")
prev(6, "sotto carico ES fra 1.300 e 1.800 MB, Koskidex nel container <= 400 MB", 1300 <= a <= 1800 and b <= 400,
     f"ES {a} MB, Koskidex {b} MB")
a = livello("carico-koskidex-docker", 16)["latenza_ms"]["p99"]
prev(7, "a 16 client p99 Koskidex nel container < 100 ms", a < 100, f"{a} ms")
a, b = seq("seq-koskidex-nativo"), seq("seq-koskidex-docker")
prev(8, "p50 nativo al più il 30% sotto quello nel container", a >= 0.7 * b, f"{a} contro {b} ms, {100 * (1 - a / b):.0f}% sotto")
if all(n in esiti for n in ("riposo-es-10018", "riposo-es-100000", "riposo-koskidex-docker-10018",
                            "riposo-koskidex-docker-100000", "seq-es-app-100000", "seq-koskidex-docker-100000")):
    km, em = mem_riposo("riposo-koskidex-docker-100000") / mem_riposo("riposo-koskidex-docker-10018"), \
        mem_riposo("riposo-es-100000") / mem_riposo("riposo-es-10018")
    kt, et = seq("seq-koskidex-docker-100000") / seq("seq-koskidex-docker"), seq("seq-es-app-100000") / seq("seq-es-app")
    prev(9, "a 100.000 documenti memoria Koskidex >= 5x, ES < 1,5x; p50 Koskidex >= 3x, ES < 3x",
         km >= 5 and em < 1.5 and kt >= 3 and et < 3,
         f"memoria Koskidex x{km:.2f}, ES x{em:.2f}; p50 Koskidex x{kt:.2f}, ES x{et:.2f}")

ora = datetime.datetime.now(datetime.timezone.utc)
git = lambda *x: subprocess.run(["git", "-C", QUI, *x], capture_output=True, text=True, check=True).stdout.strip()
esito = {"ran_at": ora.strftime("%Y-%m-%dT%H:%M:%SZ"),
         "config": {"commit": git("rev-parse", "--short", "HEAD"),
                    "modifiche_non_committate": "true" if git("status", "--porcelain", "--untracked-files=no", "--", QUI) else "false",
                    "esiti": {n: f for n, (f, _) in sorted(esiti.items())}},
         "sequenziale": righe, "carico": carichi, "riposo_mb": riposi, "copie": copie, "previsioni": previsioni}
if not os.environ.get("TESI_RISULTATI"):
    sys.exit("!!! RISULTATO NON ARCHIVIATO: TESI_RISULTATI non è impostata.")
o = ora.strftime("%Y-%m-%dT%H%M%SZ"); p = os.path.join(ARCHIVIO, f"{o}_esito.json"); k = 2
while os.path.exists(p):
    p = os.path.join(ARCHIVIO, f"{o}-{k}_esito.json"); k += 1
open(p, "x").write(json.dumps(esito, indent=2, ensure_ascii=False))
print("archiviato in", p)
