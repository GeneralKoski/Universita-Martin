#!/usr/bin/env python3
"""Scrive la pagina HTML per giudicare il pool delle 24 query del confronto.

La pagina si apre nel browser senza rete. Mostra il bisogno della query e un
atto alla volta, nell'ordine del foglio (per id del documento, mai per
ranking), chiede il grado 0, 1 o 2, registra i tempi e le sessioni, e scarica
un file da mettere in query/confronto-24/risposte/, che importa-giudizi.py
trasforma nei giudizi. Regole in ../../istruzioni-annotazione.md, parti 2 e 3.

Il foglio viene da scripts/pool di Koskidex (query/confronto-24/foglio/
giudizi.tsv), il testo degli atti dal database dell'app (doc-tesi-mysql,
database albo). Le pagine contengono il corpus e non si committano.

Si rifiuta di partire finché bisogni.md non è completo e committato: il
bisogno si scrive prima di vedere un solo risultato.

    prepara-giudizi.py             la pagina del primo annotatore, tutto il foglio
    prepara-giudizi.py --secondo   quella del secondo: query intere estratte a caso,
                                   almeno 150 righe (parte 3)
"""
import csv, hashlib, json, os, random, re, subprocess, sys

QUI = os.path.dirname(os.path.abspath(__file__))
CARTELLA = os.path.join(QUI, "..", "query", "confronto-24")
SEME_SECONDO, RIGHE_SECONDO = 20260928, 150
secondo = "--secondo" in sys.argv[1:]


def git(*args):
    return subprocess.run(["git", "-C", CARTELLA, *args], capture_output=True, text=True, check=True).stdout


# I bisogni: completi, e committati così come sono.
percorso_bisogni = os.path.join(CARTELLA, "bisogni.md")
testo = open(percorso_bisogni, encoding="utf8").read()
bisogni = {}
for blocco in re.split(r"^## ", testo, flags=re.M)[1:]:
    intestazione, _, corpo = blocco.partition("\n")
    qid = intestazione.split(" · ")[0].strip()
    b = corpo.split("Bisogno:", 1)[1].strip() if "Bisogno:" in corpo else ""
    bisogni[qid] = " ".join(b.split())
domande = [json.loads(r) for r in open(os.path.join(CARTELLA, "queries.jsonl"), encoding="utf8")]
mancanti = [q["_id"] for q in domande if not bisogni.get(q["_id"])]
if mancanti:
    sys.exit(f"bisogni.md: manca il bisogno di {', '.join(mancanti)}")
if not git("ls-files", "bisogni.md").strip() or git("status", "--porcelain", "--", "bisogni.md").strip():
    sys.exit("bisogni.md va committato prima di preparare le pagine")

righe = list(csv.DictReader(open(os.path.join(CARTELLA, "foglio", "giudizi.tsv"), encoding="utf8"), delimiter="\t"))
if secondo:
    ordine = sorted({r["query_id"] for r in righe})
    random.Random(SEME_SECONDO).shuffle(ordine)
    scelte, n = [], 0
    for qid in ordine:
        if n >= RIGHE_SECONDO:
            break
        scelte.append(qid)
        n += sum(r["query_id"] == qid for r in righe)
    righe = [r for r in righe if r["query_id"] in scelte]
    with open(os.path.join(CARTELLA, "campione-secondo.json"), "w", encoding="utf8") as f:
        f.write(json.dumps({"seme": SEME_SECONDO, "righe_minime": RIGHE_SECONDO, "query": sorted(scelte),
                            "righe": len(righe)}, indent=2) + "\n")
ruolo = "secondo" if secondo else "primo"
impronta = hashlib.sha256("\n".join(f"{r['query_id']}\t{r['doc_id']}" for r in righe).encode()).hexdigest()[:16]

docs = sorted({r["doc_id"] for r in righe})
sql = ("select json_object('id', document_id, 'nome', name, 'sommario', summary, 'testo', full_text, "
       "'data', document_date, 'subjects', subjects, 'additional_data', additional_data) from document_versions "
       f"where document_id in ({','.join(str(int(d[4:])) for d in docs)})")
dal_db = {f"doc-{str(a['id']).zfill(4)}": a for a in map(json.loads, subprocess.run(
    ["docker", "exec", "doc-tesi-mysql", "mysql", "-uroot", "-proot", "-N", "-B", "--raw",
     "--default-character-set=utf8mb4", "albo", "-e", sql], capture_output=True, text=True, check=True).stdout.splitlines())}
assert len(dal_db) == len(docs), "atti del pool mancanti nel database"


def data_italiana(d):
    return "/".join(reversed(d.split("-"))) if d else ""


def atto(doc):
    a = dal_db[doc]
    extra = {x["name"]: x.get("value") for x in (a["additional_data"] or [])}
    campi = [["Ente", ((a["subjects"] or [{}])[0].get("name") or "").strip()], ["Tipologia", extra.get("tipologia_atto")],
             ["Ufficio", extra.get("ufficio_competente")], ["Numero", extra.get("numero_atto")],
             ["Data", data_italiana(a["data"])]]
    if a["sommario"] and a["sommario"].strip() != (a["nome"] or "").strip():
        campi.insert(0, ["Oggetto", a["sommario"]])
    return {"titolo": a["nome"], "righe": [c for c in campi if c[1]], "testo": a["testo"] or ""}


dati = {"ruolo": ruolo, "impronta": impronta,
        "query": [{"id": q["_id"], "testo": q["text"], "bisogno": bisogni[q["_id"]]} for q in domande
                  if any(r["query_id"] == q["_id"] for r in righe)],
        "righe": [[r["query_id"], r["doc_id"]] for r in righe], "atti": {d: atto(d) for d in docs}}
modello = open(os.path.join(QUI, "giudizi.html"), encoding="utf8").read()
os.makedirs(os.path.join(CARTELLA, "pagine"), exist_ok=True)
percorso = os.path.join(CARTELLA, "pagine", f"giudizi-{ruolo}.html")
with open(percorso, "w", encoding="utf8") as f:
    # "</" dentro un <script> chiuderebbe il blocco: si spezza.
    f.write(modello.replace("/*DATI*/null", json.dumps(dati, ensure_ascii=False).replace("</", "<\\/")))
print(percorso, len(righe), "giudizi,", len(dati["query"]), "query,", len(docs), "atti, impronta", impronta)
