#!/usr/bin/env python3
"""Un indice più grande con gli stessi atti, per la misura 3 di 2026-09-28_carico.

Crea l'indice <destinazione> con le stesse impostazioni di <sorgente> e ci copia
gli atti che il motore ha ricevuto dall'app, ripetuti fino a <n> documenti: la
copia k di un atto ha id "<id>-<k>", il testo resta uguale. Sono dati inventati,
buoni per tempi e memoria, non per la pertinenza. Ogni motore copia i propri
documenti, cioè esattamente quello che l'app gli ha dato. Archivia il tempo di
indicizzazione (a blocchi da 1.000, uguali per i due motori) e la dimensione
dell'indice su disco.

    copia.py es <url> <sorgente> <destinazione> <n>
    copia.py koskidex <url> <sorgente> <destinazione> <n> <cartella dati del container> [<url della sorgente>]

Per Koskidex la sorgente può stare in un altro server (l'ultimo argomento): la
destinazione è un container nuovo, con il solo indice copiato.
"""
import datetime, json, os, subprocess, sys, time, urllib.request

motore, url, sorgente, destinazione, n = sys.argv[1:6]
n = int(n)
url_sorgente = sys.argv[7] if len(sys.argv) > 7 else url
BLOCCO = 1000
QUI = os.path.dirname(os.path.abspath(__file__))


def chiedi(metodo, percorso, corpo=None, tipo="application/json", base=None):
    dati = None if corpo is None else (corpo if isinstance(corpo, bytes) else json.dumps(corpo).encode())
    req = urllib.request.Request((base or url) + percorso, data=dati, method=metodo, headers={"Content-Type": tipo})
    with urllib.request.urlopen(req, timeout=600) as r:
        return json.load(r)


def atti_es():
    r = chiedi("POST", f"/{sorgente}/_search?scroll=2m", {"size": 5000, "query": {"match_all": {}}, "sort": ["_doc"]})
    out = []
    while r["hits"]["hits"]:
        out += [(h["_id"], h["_source"]) for h in r["hits"]["hits"]]
        r = chiedi("POST", "/_search/scroll", {"scroll": "2m", "scroll_id": r["_scroll_id"]})
    return out


def atti_koskidex():
    out, offset = [], 0
    while True:
        r = chiedi("GET", f"/indexes/{sorgente}/documents?limit=1000&offset={offset}", base=url_sorgente)
        out += [(str(d["id"]), d) for d in r["documents"]]
        offset += len(r["documents"])
        if not r["documents"] or offset >= r["total"]:
            return out


def copie(atti):
    k = 0
    while True:
        for i, d in atti:
            yield f"{i}-{k}", d
        k += 1


if motore == "es":
    info = chiedi("GET", f"/{sorgente}")[sorgente]
    impostazioni = {k: v for k, v in info["settings"]["index"].items()
                    if k in ("analysis", "number_of_shards", "number_of_replicas", "max_result_window")}
    chiedi("PUT", f"/{destinazione}", {"settings": {"index": impostazioni}, "mappings": info["mappings"]})
    atti = atti_es()
else:
    impostazioni = chiedi("GET", f"/indexes/{sorgente}/settings", base=url_sorgente)
    chiedi("POST", "/indexes", {"name": destinazione})
    chiedi("PUT", f"/indexes/{destinazione}/settings", impostazioni)
    atti = atti_koskidex()

gen, fatti, t0 = copie(atti), 0, time.perf_counter()
while fatti < n:
    blocco = [next(gen) for _ in range(min(BLOCCO, n - fatti))]
    if motore == "es":
        righe = []
        for i, d in blocco:
            righe += [json.dumps({"index": {"_index": destinazione, "_id": i}}), json.dumps(d, ensure_ascii=False)]
        r = chiedi("POST", "/_bulk", ("\n".join(righe) + "\n").encode(), "application/x-ndjson")
        if r.get("errors"):
            sys.exit("errori nel bulk di Elasticsearch")
    else:
        chiedi("POST", f"/indexes/{destinazione}/documents", [dict(d, id=i) for i, d in blocco])
    fatti += len(blocco)
if motore == "es":
    chiedi("POST", f"/{destinazione}/_refresh")
secondi = time.perf_counter() - t0

if motore == "es":
    chiedi("POST", f"/{destinazione}/_flush")
    documenti = chiedi("GET", f"/{destinazione}/_count")["count"]
    byte = int(chiedi("GET", f"/_cat/indices/{destinazione}?format=json&bytes=b")[0]["store.size"])
else:
    documenti = chiedi("GET", f"/indexes/{destinazione}")["docs"]
    time.sleep(5)
    cartella = sys.argv[6]
    byte = sum(os.path.getsize(os.path.join(cartella, f)) for f in os.listdir(cartella)
               if f in ("koskidex.db", "operations.log"))

ora = datetime.datetime.now(datetime.timezone.utc)
git = lambda *a: subprocess.run(["git", "-C", QUI, *a], capture_output=True, text=True, check=True).stdout.strip()
esito = {"ran_at": ora.strftime("%Y-%m-%dT%H:%M:%SZ"),
         "config": {"commit": git("rev-parse", "--short", "HEAD"),
                    "modifiche_non_committate": "true" if git("status", "--porcelain", "--", QUI) else "false",
                    "motore": motore, "url": url, "url_sorgente": url_sorgente, "sorgente": sorgente,
                    "destinazione": destinazione,
                    "atti_distinti": len(atti), "blocco": BLOCCO},
         "documenti": documenti, "indicizzazione_s": round(secondi, 3), "byte_su_disco": byte}
print(json.dumps({k: v for k, v in esito.items() if k != "config"}))
if not os.environ.get("TESI_RISULTATI"):
    sys.exit("!!! RISULTATO NON ARCHIVIATO: TESI_RISULTATI non è impostata.")
d = os.path.join(os.environ["TESI_RISULTATI"], "esperimenti", "2026-09-28_carico")
os.makedirs(d, exist_ok=True)
o = ora.strftime("%Y-%m-%dT%H%M%SZ"); nome = f"copia-{motore}-{n}"
p = os.path.join(d, f"{o}_{nome}.json"); k = 2
while os.path.exists(p):
    p = os.path.join(d, f"{o}-{k}_{nome}.json"); k += 1
open(p, "x").write(json.dumps(esito, indent=2, ensure_ascii=False))
print("archiviato in", p)
