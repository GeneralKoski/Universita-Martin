#!/usr/bin/env python3
"""Trasforma i file scaricati dalla pagina di annotazione nei giudizi del pool.

Ogni file va copiato così com'è in query/confronto-24/risposte/. Per ogni ruolo
(primo, secondo annotatore) conta il file scaricato per ultimo, che contiene
anche i giudizi dei precedenti. Lo script controlla che corrisponda alle righe
della sua pagina e riscrive da zero, in modo deterministico:

- giudizi-<ruolo>.tsv: query, atto, grado, nota, secondi, se il grado è stato
  cambiato; solo id, niente testo degli atti;
- sessioni-<ruolo>.tsv: inizio, fine, prima e ultima riga, azioni (un giudizio
  cambiato conta due volte);
- qrels/test.tsv in formato BEIR, dal primo annotatore, solo a foglio completo.

Il kappa fra i due annotatori si calcola a parte, quando ci sono tutti e due.

    importa-giudizi.py
"""
import csv, glob, hashlib, json, os, sys

QUI = os.path.dirname(os.path.abspath(__file__))
CARTELLA = os.path.join(QUI, "..", "query", "confronto-24")

righe = [(r["query_id"], r["doc_id"]) for r in
         csv.DictReader(open(os.path.join(CARTELLA, "foglio", "giudizi.tsv"), encoding="utf8"), delimiter="\t")]
per_ruolo = {"primo": righe}
campione = os.path.join(CARTELLA, "campione-secondo.json")
if os.path.exists(campione):
    scelte = set(json.load(open(campione))["query"])
    per_ruolo["secondo"] = [r for r in righe if r[0] in scelte]


def impronta(rr):
    return hashlib.sha256("\n".join(f"{q}\t{d}" for q, d in rr).encode()).hexdigest()[:16]


ultimi = {}
for percorso in sorted(glob.glob(os.path.join(CARTELLA, "risposte", "*.json"))):
    nome = os.path.basename(percorso)
    r = json.load(open(percorso, encoding="utf8"))
    if r.get("strumento") != "giudizi-pool" or r.get("versione") != 1:
        sys.exit(f"{nome}: non è un file della pagina di annotazione")
    if r["ruolo"] not in per_ruolo:
        sys.exit(f"{nome}: ruolo {r['ruolo']!r} senza pagina")
    if r["impronta"] != impronta(per_ruolo[r["ruolo"]]):
        sys.exit(f"{nome}: la pagina non corrisponde al foglio di oggi; va rigenerata dallo stesso foglio")
    if r["ruolo"] not in ultimi or r["scaricato"] > ultimi[r["ruolo"]][1]["scaricato"]:
        ultimi[r["ruolo"]] = (nome, r)
if not ultimi:
    sys.exit("nessun file in risposte/")

for ruolo, (nome, r) in sorted(ultimi.items()):
    rr = per_ruolo[ruolo]
    for g in r["gradi"]:
        if (g["query"], g["atto"]) != rr[g["riga"] - 1] or g["grado"] not in (0, 1, 2):
            sys.exit(f"{nome}: la riga {g['riga']} non corrisponde al foglio")
    with open(os.path.join(CARTELLA, f"giudizi-{ruolo}.tsv"), "w", encoding="utf8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(["riga", "query_id", "doc_id", "grado", "nota", "secondi", "cambiato"])
        for g in r["gradi"]:
            w.writerow([g["riga"], g["query"], g["atto"], g["grado"], " ".join(g["nota"].split()), g["secondi"],
                        "sì" if g["cambiato"] else ""])
    with open(os.path.join(CARTELLA, f"sessioni-{ruolo}.tsv"), "w", encoding="utf8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(["inizio", "fine", "prima_riga", "ultima_riga", "azioni"])
        for s in r["sessioni"]:
            w.writerow([s["inizio"], s["fine"], s["prima"], s["ultima"], s["giudizi"]])
    completo = len(r["gradi"]) == len(rr)
    if ruolo == "primo" and completo:
        os.makedirs(os.path.join(CARTELLA, "qrels"), exist_ok=True)
        with open(os.path.join(CARTELLA, "qrels", "test.tsv"), "w", encoding="utf8") as f:
            f.write("query-id\tcorpus-id\tscore\n")
            for g in sorted(r["gradi"], key=lambda g: (g["query"], g["atto"])):
                f.write(f"{g['query']}\t{g['atto']}\t{g['grado']}\n")
    conta = {k: sum(g["grado"] == k for g in r["gradi"]) for k in (0, 1, 2)}
    secondi = sorted(g["secondi"] for g in r["gradi"])
    print(f"{ruolo}: {nome}, {len(r['gradi'])} giudizi su {len(rr)}{'' if completo else ' (incompleto)'}, "
          f"gradi {conta}, {len(r['sessioni'])} sessioni"
          + (f", mediana {secondi[len(secondi) // 2]} s a giudizio" if secondi else ""))
