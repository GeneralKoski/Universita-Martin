#!/usr/bin/env python3
"""Costruisce la collezione delle known-item umane dai file rimandati indietro.

Ogni file scaricato dalla pagina di raccolta va copiato così com'è in
query/known-item-umane/risposte/. Questo script li rilegge tutti, controlla che
ognuno corrisponda al suo lotto del campione, e riscrive da zero, in modo
deterministico: queries.jsonl e qrels/test.tsv in formato BEIR, i giudizi per
fonte (qrels/crispiano.tsv e qrels/fvg.tsv, per scripts/evaluate -split),
queries.txt per app:eval-run-queries, raccolta.json con chi, quanto e come per
ogni query.

La collezione si ricostruisce a ogni file che arriva; si misura solo a raccolta
chiusa. Le query vuote ("non saprei cosa scrivere") restano in raccolta.json e
non entrano nella collezione.

    importa-raccolta.py
"""
import glob, hashlib, json, os, re

QUI = os.path.dirname(os.path.abspath(__file__))
CARTELLA = os.path.join(QUI, "..", "query", "known-item-umane")
campione = json.load(open(os.path.join(CARTELLA, "campione.json"), encoding="utf8"))

file_risposte = sorted(glob.glob(os.path.join(CARTELLA, "risposte", "*.json")))
if not file_risposte:
    raise SystemExit("nessun file in risposte/")

righe, visti, sorgenti = [], {}, []
for percorso in file_risposte:
    nome = os.path.basename(percorso)
    grezzo = open(percorso, "rb").read()
    r = json.loads(grezzo)
    if r.get("strumento") != "raccolta-known-item" or r.get("versione") != 1:
        raise SystemExit(f"{nome}: non è un file della pagina di raccolta")
    docs = campione["lotti"].get(r["lotto"])
    if docs is None:
        raise SystemExit(f"{nome}: lotto {r['lotto']!r} non nel campione")
    if r["impronta"] != hashlib.sha256("\n".join(docs).encode()).hexdigest()[:16]:
        raise SystemExit(f"{nome}: il lotto {r['lotto']} della pagina non è quello del campione")
    if r["lotto"] in visti:
        raise SystemExit(f"{nome}: il lotto {r['lotto']} c'è già in {visti[r['lotto']]}; un atto, una query")
    visti[r["lotto"]] = nome
    if not r.get("pseudonimo", "").strip():
        raise SystemExit(f"{nome}: senza soprannome")
    for k, x in enumerate(r["risposte"]):
        if x["posizione"] != k + 1 or x["atto"] != docs[k]:
            raise SystemExit(f"{nome}: la risposta {k + 1} non corrisponde all'atto {k + 1} del lotto")
        numero_lotto = int(r["lotto"].removeprefix("lotto-"))
        query = x["query"].strip()
        righe.append({"query": f"ku-{numero_lotto}-{x['posizione']:02d}", "testo": query, "atto": x["atto"],
                      **campione["atti"][x["atto"]], "lotto": r["lotto"], "pseudonimo": r["pseudonimo"].strip(),
                      "vuota": not query, "motivo": x.get("motivo", ""),
                      "contiene_numero": bool(re.search(r"\d", query)),
                      "secondi_lettura": x["secondi_lettura"], "secondi_scrittura": x["secondi_scrittura"],
                      "ricaricato": x.get("ricaricato", False)})
    sorgenti.append({"file": nome, "sha256": hashlib.sha256(grezzo).hexdigest(), "lotto": r["lotto"],
                     "risposte": len(r["risposte"]), "completo": len(r["risposte"]) == len(docs),
                     "iniziato": r.get("iniziato"), "finito": r.get("finito")})

righe.sort(key=lambda x: (int(x["lotto"].removeprefix("lotto-")), x["query"]))
piene = [x for x in righe if not x["vuota"]]
os.makedirs(os.path.join(CARTELLA, "qrels"), exist_ok=True)
with open(os.path.join(CARTELLA, "queries.jsonl"), "w", encoding="utf8") as q, \
     open(os.path.join(CARTELLA, "queries.txt"), "w", encoding="utf8") as t, \
     open(os.path.join(CARTELLA, "qrels", "test.tsv"), "w", encoding="utf8") as g:
    g.write("query-id\tcorpus-id\tscore\n")
    for x in piene:
        q.write(json.dumps({"_id": x["query"], "text": x["testo"]}, ensure_ascii=False) + "\n")
        t.write(x["testo"] + "\n")
        g.write(f"{x['query']}\t{x['atto']}\t2\n")
for fonte in ("crispiano", "fvg"):
    with open(os.path.join(CARTELLA, "qrels", f"{fonte}.tsv"), "w", encoding="utf8") as g:
        g.write("query-id\tcorpus-id\tscore\n")
        for x in piene:
            if x["fonte"] == fonte:
                g.write(f"{x['query']}\t{x['atto']}\t2\n")

riassunto = {"file": len(sorgenti), "atti_mostrati": len(righe), "query": len(piene), "vuote": len(righe) - len(piene),
             "per_fonte": {f: sum(x["fonte"] == f for x in piene) for f in ("crispiano", "fvg")},
             "con_numero": sum(x["contiene_numero"] for x in piene),
             "persone": len({x["pseudonimo"] for x in righe})}
with open(os.path.join(CARTELLA, "raccolta.json"), "w", encoding="utf8") as f:
    f.write(json.dumps({"riassunto": riassunto, "sorgenti": sorgenti, "query": righe}, indent=2, ensure_ascii=False) + "\n")
print(json.dumps(riassunto, indent=2, ensure_ascii=False))
