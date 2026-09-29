#!/usr/bin/env python3
"""Riassume le misure di 2026-09-29_carico-fisso, le mette accanto a quelle del
Mac (Elasticsearch da 2026-09-28_carico, Koskidex dal "dopo" di
2026-09-29_accenti) e controlla le previsioni 1-4 del README. Per ogni
etichetta usa l'esito più recente; archivia il riassunto.

    analizza.py
"""
import datetime, glob, json, os, re, subprocess, sys

QUI = os.path.dirname(os.path.abspath(__file__))
ARCHIVIO = os.path.join(os.environ.get("TESI_RISULTATI") or os.path.join(QUI, "..", ".."), "esperimenti", "2026-09-29_carico-fisso")
ESP = os.path.join(QUI, "..")
MAC = {"seq-es-app": "2026-09-28_carico/2026-09-28T091331Z_seq-es-app.json",
       "seq-es-senza-source": "2026-09-28_carico/2026-09-28T091403Z_seq-es-senza-source.json",
       "seq-koskidex-docker": "2026-09-29_accenti/dopo/2026-09-29T080100Z_seq-koskidex-docker.json",
       "seq-koskidex-nativo": "2026-09-29_accenti/dopo/2026-09-29T080102Z_seq-koskidex-nativo.json",
       "carico-es-app": "2026-09-28_carico/2026-09-28T091655Z_carico-es-app.json",
       "carico-es-senza-source": "2026-09-28_carico/2026-09-28T091925Z_carico-es-senza-source.json",
       "carico-koskidex-docker": "2026-09-29_accenti/dopo/2026-09-29T080332Z_carico-koskidex-docker.json",
       "carico-koskidex-nativo": "2026-09-29_accenti/dopo/2026-09-29T080602Z_carico-koskidex-nativo.json"}

esiti = {}
for p in sorted(glob.glob(os.path.join(ARCHIVIO, "*.json"))):
    m = re.match(r"\d{4}-\d\d-\d\dT\d{6}Z(?:-\d+)?_(.+)\.json$", os.path.basename(p))
    if m and not m.group(1).startswith("esito"):
        esiti[m.group(1)] = (os.path.basename(p), json.load(open(p, encoding="utf8")))


def e(nome):
    if nome not in esiti:
        sys.exit(f"manca l'esito {nome}")
    f, d = esiti[nome]
    assert d["config"].get("modifiche_non_committate") in ("false", False), f"{f}: codice non committato"
    return d


mac = {n: json.load(open(os.path.join(ESP, f), encoding="utf8")) for n, f in MAC.items()}
seq = lambda d, q="p50": d["sequenziale"]["riassunto"]["tutte"][q]
qps = lambda d: max(l["ricerche_al_secondo"] for l in d["carico"])

for n in ("verifica-es", "verifica-koskidex-docker"):
    print(n, json.dumps({k: v for k, v in e(n).items() if k not in ("config",)}, ensure_ascii=False)[:300])

righe = {}
print("\nUna ricerca alla volta, ms (p50 / p95 / p99): fisso | Mac")
for n in ("seq-es-app", "seq-es-senza-source", "seq-koskidex-docker", "seq-koskidex-docker-cache", "seq-koskidex-nativo"):
    r = e(n)["sequenziale"]["riassunto"]
    righe[n] = {g: {k: v[k] for k in ("n", "p50", "p95", "p99")} for g, v in r.items()}
    t = r["tutte"]
    m = f"{seq(mac[n]):.2f} / {seq(mac[n], 'p95'):.2f} / {seq(mac[n], 'p99'):.2f}" if n in mac else "-"
    print(f"  {n:28} {t['p50']:6.2f} / {t['p95']:6.2f} / {t['p99']:6.2f} | {m}")

carichi = {}
print("\nSotto carico: ricerche al secondo, p50 e p99 ms, memoria massima MB, CPU media %")
for n in ("carico-es-app", "carico-es-senza-source", "carico-koskidex-docker", "carico-koskidex-nativo"):
    carichi[n] = []
    print(f"  {n}  (Mac: massimo {qps(mac[n]):.0f}/s)")
    for l in e(n)["carico"]:
        ris = l["risorse"]
        riga = {"client": l["client"], "qps": l["ricerche_al_secondo"], "p50": l["latenza_ms"]["p50"],
                "p99": l["latenza_ms"]["p99"], "errori": l["errori"],
                "memoria_max_mb": ris.get("memoria_mb", {}).get("max"), "cpu_media": ris.get("cpu_percento", {}).get("media")}
        carichi[n].append(riga)
        print(f"    {riga['client']:3} client {riga['qps']:8.1f}/s  p50 {riga['p50']:7.2f}  p99 {riga['p99']:7.2f}  "
              f"mem {riga['memoria_max_mb']}  cpu {riga['cpu_media']}  errori {riga['errori']}")

riposi = {n: e(n)["riposo"]["riassunto"]["memoria_mb"]["p50"] for n in esiti if n.startswith("riposo-")}
print("\nA riposo, memoria MB (p50):", json.dumps(riposi, ensure_ascii=False))

previsioni = {}


def prev(k, testo, ok, valore):
    previsioni[k] = {"previsione": testo, "valore": valore, "esito": "confermata" if ok else "smentita"}
    print(f"{k}. {previsioni[k]['esito']:10} {testo}: {valore}")


print()
kd, es = seq(e("seq-koskidex-docker")), seq(e("seq-es-app"))
prev(1, "p50 Koskidex nel container fra 0,6 e 1,3 ms, Elasticsearch come l'app fra 4,4 e 8,2 ms",
     0.6 <= kd <= 1.3 and 4.4 <= es <= 8.2, f"Koskidex {kd} ms (Mac {seq(mac['seq-koskidex-docker'])}), ES {es} ms (Mac {seq(mac['seq-es-app'])})")
a = qps(e("carico-koskidex-nativo"))
prev(2, "massimo del nativo fra 4.000 e 8.000 ricerche/s", 4000 <= a <= 8000, f"{a:.0f} (Mac {qps(mac['carico-koskidex-nativo']):.0f})")
r, rm = qps(e("carico-koskidex-docker")) / qps(e("carico-es-app")), qps(mac["carico-koskidex-docker"]) / qps(mac["carico-es-app"])
prev(3, "rapporto di capacità Koskidex nel container / ES come l'app entro il 30% del Mac", 0.7 * rm <= r <= 1.3 * rm,
     f"{qps(e('carico-koskidex-docker')):.0f} / {qps(e('carico-es-app')):.0f} = {r:.2f} (Mac {rm:.2f})")
r, rm = es / kd, seq(mac["seq-es-app"]) / seq(mac["seq-koskidex-docker"])
prev(4, "rapporto dei p50 ES come l'app / Koskidex nel container entro il 30% del Mac", 0.7 * rm <= r <= 1.3 * rm,
     f"{es} / {kd} = {r:.2f} (Mac {rm:.2f})")

ora = datetime.datetime.now(datetime.timezone.utc)
git = lambda *x: subprocess.run(["git", "-C", QUI, *x], capture_output=True, text=True, check=True).stdout.strip()
esito = {"ran_at": ora.strftime("%Y-%m-%dT%H:%M:%SZ"),
         "config": {"commit": git("rev-parse", "--short", "HEAD"),
                    "modifiche_non_committate": "true" if git("status", "--porcelain", "--untracked-files=no", "--", QUI) else "false",
                    "esiti": {n: f for n, (f, _) in sorted(esiti.items())}, "mac": MAC},
         "sequenziale": righe, "carico": carichi, "riposo_mb": riposi, "previsioni": previsioni}
if not os.environ.get("TESI_RISULTATI"):
    sys.exit("!!! RISULTATO NON ARCHIVIATO: TESI_RISULTATI non è impostata.")
o = ora.strftime("%Y-%m-%dT%H%M%SZ"); p = os.path.join(ARCHIVIO, f"{o}_esito.json"); k = 2
while os.path.exists(p):
    p = os.path.join(ARCHIVIO, f"{o}-{k}_esito.json"); k += 1
open(p, "x", encoding="utf8").write(json.dumps(esito, indent=2, ensure_ascii=False))
print("archiviato in", p)
