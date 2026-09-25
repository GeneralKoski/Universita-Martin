#!/usr/bin/env python3
"""Scrive una pagina HTML per ogni lotto del campione delle known-item umane.

La pagina si apre nel browser senza rete. Mostra un atto alla volta, lo nasconde
quando la persona ha letto, chiede la ricerca che farebbe per ritrovarlo e
registra i tempi; alla fine scarica un file da rimandare indietro, che
importa-raccolta.py trasforma nella collezione. Regole in
../../istruzioni-annotazione.md, parte 1.

Il testo degli atti viene dal database dell'app (doc-tesi-mysql, database albo):
per Crispiano titolo e testo integrale, per il Friuli Venezia Giulia la scheda.
Le pagine contengono il corpus e non si committano: vanno in
query/known-item-umane/pagine/, che git ignora.

    prepara-raccolta.py
"""
import hashlib, json, os, subprocess

QUI = os.path.dirname(os.path.abspath(__file__))
CARTELLA = os.path.join(QUI, "..", "query", "known-item-umane")
USCITA = os.path.join(CARTELLA, "pagine")

campione = json.load(open(os.path.join(CARTELLA, "campione.json"), encoding="utf8"))
tutti = sorted({d for docs in campione["lotti"].values() for d in docs})
sql = ("select json_object('id', document_id, 'nome', name, 'sommario', summary, 'testo', full_text, "
       "'data', document_date, 'subjects', subjects, 'additional_data', additional_data) from document_versions "
       f"where document_id in ({','.join(str(int(d[4:])) for d in tutti)})")
righe = subprocess.run(["docker", "exec", "doc-tesi-mysql", "mysql", "-uroot", "-proot", "-N", "-B", "--raw",
                        "--default-character-set=utf8mb4", "albo", "-e", sql],
                       capture_output=True, text=True, check=True).stdout.splitlines()
dal_db = {f"doc-{str(a['id']).zfill(4)}": a for a in map(json.loads, righe)}
assert len(dal_db) == len(tutti), "atti del campione mancanti nel database"


def data_italiana(d):
    return "/".join(reversed(d.split("-"))) if d else ""


def atto(doc):
    a = dal_db[doc]
    ente = ((a["subjects"] or [{}])[0].get("name") or "").strip()
    if campione["atti"][doc]["fonte"] == "crispiano":
        assert a["testo"], f"{doc}: Crispiano senza testo integrale"
        return {"id": doc, "titolo": a["nome"], "righe": [["Ente", ente], ["Data", data_italiana(a["data"])]],
                "testo": a["testo"]}
    extra = {x["name"]: x.get("value") for x in (a["additional_data"] or [])}
    righe = [["Ente", ente], ["Tipologia", extra.get("tipologia_atto")], ["Ufficio", extra.get("ufficio_competente")],
             ["Numero", extra.get("numero_atto")], ["Data", data_italiana(a["data"])]]
    if a["sommario"] and a["sommario"].strip() != (a["nome"] or "").strip():
        righe.insert(0, ["Oggetto", a["sommario"]])
    return {"id": doc, "titolo": a["nome"], "righe": [r for r in righe if r[1]], "testo": ""}


modello = open(os.path.join(QUI, "raccolta.html"), encoding="utf8").read()
os.makedirs(USCITA, exist_ok=True)
for nome, docs in campione["lotti"].items():
    impronta = hashlib.sha256("\n".join(docs).encode()).hexdigest()[:16]
    dati = {"lotto": nome, "impronta": impronta, "atti": [atto(d) for d in docs]}
    # "</" dentro un <script> chiuderebbe il blocco: si spezza.
    js = json.dumps(dati, ensure_ascii=False).replace("</", "<\\/")
    percorso = os.path.join(USCITA, f"raccolta-{nome}.html")
    with open(percorso, "w", encoding="utf8") as f:
        f.write(modello.replace("/*DATI*/null", js))
    print(percorso, len(docs), "atti, impronta", impronta)
