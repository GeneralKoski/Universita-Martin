#!/usr/bin/env python3
"""Estrae dagli esiti archiviati in risultati/ i dati dei grafici della tesi e
li scrive in latex/dati/*.dat (tabelle di testo per pgfplots) con
latex/dati/PROVENIENZA.md, che dice da quale file viene ogni colonna. Non
calcola niente di nuovo: solo copia numeri già archiviati (a parte la mediana
dei tempi di un rapporto dell'app, che è una mediana di ms già scritti).
Nessun testo di query finisce nei dati.

    dati-grafici.py
"""
import glob, json, os, statistics

QUI = os.path.dirname(os.path.abspath(__file__))
R = os.path.abspath(os.path.join(QUI, ".."))
OUT = os.path.abspath(os.path.join(R, "..", "latex", "dati"))
os.makedirs(OUT, exist_ok=True)
prov = []


def ultimo(percorso):
    trovati = sorted(glob.glob(os.path.join(R, percorso)))
    if not trovati:
        raise SystemExit(f"manca {percorso}")
    return trovati[-1]


def carica(percorso):
    f = ultimo(percorso)
    return os.path.relpath(f, R), json.load(open(f))


def scrivi(nome, intestazione, righe, sorgenti, nota):
    with open(os.path.join(OUT, nome), "w") as fh:
        fh.write(" ".join(intestazione) + "\n")
        for r in righe:
            fh.write(" ".join(str(x) for x in r) + "\n")
    prov.append((nome, nota, sorgenti))
    print(f"{nome}: {len(righe)} righe")


# 1. Ricerche al secondo per numero di client: Mac e fisso. Sul Mac Elasticsearch
# viene da 2026-09-28_carico e Koskidex (dopo le correzioni, secondo valore di
# ogni coppia [prima, dopo]) da 2026-09-29_accenti; sul fisso tutto da carico-fisso.
fm, mac = carica("esperimenti/2026-09-28_carico/*_esito.json")
fa, acc = carica("esperimenti/2026-09-29_accenti/*_esito.json")
ff, fisso = carica("esperimenti/2026-09-29_carico-fisso/*_esito.json")
righe = []
for c in (1, 2, 4, 8, 16, 32):
    riga = [c,
            next(x["qps"] for x in mac["carico"]["carico-es-app"] if x["client"] == c),
            next(x["qps"][1] for x in acc["carico"]["carico-koskidex-docker"] if x["client"] == c),
            next(x["qps"][1] for x in acc["carico"]["carico-koskidex-nativo"] if x["client"] == c)]
    for k in ("carico-es-app", "carico-koskidex-docker", "carico-koskidex-nativo"):
        riga.append(next(x["qps"] for x in fisso["carico"][k] if x["client"] == c))
    righe.append(riga)
scrivi("carico.dat", ["client", "mac_es", "mac_kc", "mac_kn", "fisso_es", "fisso_kc", "fisso_kn"], righe, [fm, fa, ff],
       "ricerche al secondo (campo qps) per numero di client; es = Elasticsearch come l'app, kc = Koskidex nel container, kn = Koskidex nativo; sul Mac Koskidex e' dopo le correzioni delle allocazioni")

# 2. MRR@10 delle known-item umane con intervallo al 95%.
fi, iv = carica("esperimenti/2026-09-29_intervalli/*_esito.json")
ordine = [("ES", 0), ("K0", 1), ("LT", 1), ("ESC", 2), ("KC", 0), ("P2", 0), ("ESO", 2), ("P3", 0), ("P4", 0),
          ("LA", 1), ("V", 1), ("B", 1), ("A", 1), ("RR-LA", 3), ("RR-A", 3)]
righe = []
for i, (n, g) in enumerate(ordine):
    m = iv["medie"][n]
    righe.append([i, n, g, m["media"], m["ic95"][0], m["ic95"][1]])
scrivi("mrr-umane.dat", ["posizione", "nome", "gruppo", "media", "basso", "alto", "meno", "piu"],
       [r + [round(r[3] - r[4], 4), round(r[5] - r[3], 4)] for r in righe], [fi],
       "MRR@10 sulle 104 known-item umane con intervallo al 95% (bootstrap accoppiato); meno e piu sono le distanze della media dagli estremi; gruppo 0 = dall'app, 1 = Koskidex piatto, 2 = Elasticsearch corretto, 3 = riordinato")
for g in range(4):
    scrivi(f"mrr-umane-g{g}.dat", ["posizione", "nome", "gruppo", "media", "basso", "alto", "meno", "piu"],
           [r + [round(r[3] - r[4], 4), round(r[5] - r[3], 4)] for r in righe if r[2] == g], [fi],
           f"le righe del gruppo {g} di mrr-umane.dat")

# 3. Costante della fusione (somma pesata), per collezione.
fc, cal = carica("esperimenti/2026-09-25_fusione/*calibrazione.json")
costanti = ["0.0", "5.0", "10.0", "20.0", "40.0", "80.0", "160.0", "320.0"]
righe = []
for i, c in enumerate(costanti):
    righe.append([i, int(float(c))] + [cal[k]["somma"][c]["valore"] for k in ("scifact", "nfcorpus", "known-item-auto-train")])
scrivi("fusione.dat", ["posizione", "costante", "scifact", "nfcorpus", "known"], righe, [fc],
       "valore della metrica (nDCG@10 su SciFact train e NFCorpus dev, MRR@10 sulle known-item automatiche train) per costante della somma pesata")

# 4. Crescita con il numero di documenti: memoria a riposo e indice su disco.
fd, disco = carica("esperimenti/2026-09-28_carico/*disco-10018.json")
r = mac["riposo_mb"]; cp = mac["copie"]
righe = [[10018, r["riposo-es-10018"], r["riposo-koskidex-docker-10018"],
          round(disco["elasticsearch"]["byte_su_disco"] / 1e6, 2), round(disco["koskidex"]["byte_su_disco"] / 1e6, 2)]]
for n in (50000, 100000):
    righe.append([n, r[f"riposo-es-{n}"], r[f"riposo-koskidex-docker-{n}"],
                  round(cp[f"copia-es-{n}"]["byte_su_disco"] / 1e6, 2), round(cp[f"copia-koskidex-{n}"]["byte_su_disco"] / 1e6, 2)])
scrivi("crescita.dat", ["documenti", "mem_es", "mem_k", "disco_es", "disco_k"], righe, [fm, fd],
       "memoria a riposo in MB (riposo_mb) e indice su disco in MB (byte_su_disco / 1e6) per numero di documenti")

# 5. Pertinenza contro costo, dall'app: MRR@10 delle umane e mediana della ricerca.
fp, pc = carica("esperimenti/2026-09-29_profilo-completo/*_esito.json")
fr, rap = carica("confronto/*T093306Z_known-item-umane-elasticsearch.json")
ms_es = round(statistics.median(x["ms"] for x in rap["query"]), 2)
righe = [["ES", ms_es, iv["medie"]["ES"]["media"]]]
for p in ("P0", "P2", "P3", "P4"):  # P1 ha le stesse umane di P0: un punto solo, P0 (README di profilo-completo)
    righe.append(["P0=P1" if p == "P0" else p, pc["profili"][p]["known-item-umane"]["ms_mediana"], pc["profili"][p]["known-item-umane"]["mrr@10"]])
scrivi("compromesso.dat", ["nome", "ms", "mrr"], righe, [fp, fr, fi],
       "MRR@10 sulle known-item umane e mediana in ms della ricerca dall'app (per ES dal rapporto dell'app, che contiene testi di query e non è in git)")

with open(os.path.join(OUT, "PROVENIENZA.md"), "w") as fh:
    fh.write("# Da dove vengono i dati dei grafici\n\nScritti da `risultati/strumenti/dati-grafici.py`; ogni colonna è copiata da un file archiviato in `risultati/` (percorsi relativi a quella cartella).\n\n")
    for nome, nota, sorg in prov:
        fh.write(f"- `{nome}`: {nota}. Sorgenti: " + ", ".join(f"`{s}`" for s in sorg) + ".\n")
print("scritto", OUT)
