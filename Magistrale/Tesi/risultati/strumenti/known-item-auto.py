#!/usr/bin/env python3
"""Genera le query known-item automatiche: "<numero> <comune>", una per atto.

La query nasce da un atto, e quell'atto è l'unica risposta giusta. Si tengono
solo gli atti con un numero che contiene una cifra e con la coppia (comune,
numero) unica nel corpus: la numerazione riparte ogni anno, e una query che
descrive due atti non ha una risposta sola. Metodo in
esperimenti/2026-09-25_known-item-auto/README.md.

Legge il database dell'app (doc-tesi-mysql, database albo) e scrive in
query/known-item-auto/: queries.jsonl e qrels/test.tsv in formato BEIR,
queries.txt per app:eval-run-queries, generazione.json con i conteggi.

Senza argomenti rigenera il lotto di test del 25/09/2026. Con --split train
genera un lotto di addestramento con un altro seme, in un'altra cartella, senza
gli atti di un lotto esistente (--escludi): serve a chi impara dalle query, che
non deve mai vedere quelle su cui viene valutato.

    known-item-auto.py
    known-item-auto.py --split train --seme 20260926 --nome known-item-auto-train \
        --prefisso kt --escludi known-item-auto
"""
import argparse, collections, json, os, random, re, subprocess

QUI = os.path.dirname(os.path.abspath(__file__))
arg = argparse.ArgumentParser()
arg.add_argument("--seme", type=int, default=20260925)
arg.add_argument("--quante", type=int, default=300)
arg.add_argument("--nome", default="known-item-auto")
arg.add_argument("--split", default="test")
arg.add_argument("--prefisso", default="ki")
arg.add_argument("--escludi", action="append", default=[], help="lotto i cui atti non vanno estratti")
opz = arg.parse_args()
SEME, QUANTE = opz.seme, opz.quante
USCITA = os.path.join(QUI, "..", "query", opz.nome)
if os.path.exists(os.path.join(USCITA, "generazione.json")) and opz.nome != "known-item-auto":
    raise SystemExit(f"{USCITA} esiste già: un lotto non si rigenera sopra se stesso")
esclusi = set()
for lotto in opz.escludi:
    cartella = os.path.join(QUI, "..", "query", lotto, "qrels")
    for f in os.listdir(cartella):
        for r in open(os.path.join(cartella, f)).read().splitlines()[1:]:
            esclusi.add(int(r.split("\t")[1].removeprefix("doc-")))

sql = ("select json_object('id', document_id, 'nome', name, 'subjects', subjects, "
       "'additional_data', additional_data) from document_versions order by document_id")
righe = subprocess.run(["docker", "exec", "doc-tesi-mysql", "mysql", "-uroot", "-proot", "-N", "-B", "--raw",
                        "--default-character-set=utf8mb4", "albo", "-e", sql],
                       capture_output=True, text=True, check=True).stdout.splitlines()
atti = [json.loads(r) for r in righe]


def numero(a):
    for campo in a["additional_data"] or []:
        if campo.get("name") == "numero_atto":
            return str(campo.get("value") or "").strip()
    # Crispiano non ha numero_atto: il numero sta nel nome, "Determina N. 1223 del ...".
    m = re.search(r"\bN\.?\s*(\d+)", a["nome"] or "")
    return m.group(1) if m else ""


def comune(a):
    ente = ((a["subjects"] or [{}])[0].get("name") or "").strip()
    return re.sub(r"(?i)^comune di\s+", "", ente)


conteggi = collections.Counter()
candidati = []
for a in atti:
    n, c = numero(a), comune(a)
    if not re.search(r"\d", n):
        conteggi["senza_numero_con_cifre"] += 1
        continue
    if not c:
        conteggi["senza_comune"] += 1
        continue
    candidati.append((a["id"], n, c))

coppie = collections.Counter((c.lower(), n.lower()) for _, n, c in candidati)
ammessi = [(i, n, c) for i, n, c in candidati if coppie[(c.lower(), n.lower())] == 1]
conteggi["coppia_comune_numero_ripetuta"] = len(candidati) - len(ammessi)
if esclusi:
    prima = len(ammessi)
    ammessi = [x for x in ammessi if x[0] not in esclusi]
    conteggi["gia_in_un_altro_lotto"] = prima - len(ammessi)

estratti = sorted(random.Random(SEME).sample(ammessi, QUANTE))

os.makedirs(os.path.join(USCITA, "qrels"), exist_ok=True)
with open(os.path.join(USCITA, "queries.jsonl"), "w", encoding="utf8") as q, \
     open(os.path.join(USCITA, "queries.txt"), "w", encoding="utf8") as t, \
     open(os.path.join(USCITA, "qrels", f"{opz.split}.tsv"), "w", encoding="utf8") as g:
    g.write("query-id\tcorpus-id\tscore\n")
    for k, (i, n, c) in enumerate(estratti, 1):
        qid, testo = f"{opz.prefisso}-{k:03d}", f"{n} {c}"
        q.write(json.dumps({"_id": qid, "text": testo}, ensure_ascii=False) + "\n")
        t.write(testo + "\n")
        g.write(f"{qid}\tdoc-{str(i).zfill(4)}\t2\n")

commit = subprocess.run(["git", "-C", os.path.expanduser("~/Desktop/Dieffetech/Documentale"), "rev-parse", "--short", "HEAD"],
                        capture_output=True, text=True, check=True).stdout.strip()
generazione = {"seme": SEME, "query": QUANTE, **({"split": opz.split, "lotti_esclusi": opz.escludi} if opz.split != "test" else {}), "atti": len(atti), "candidati": len(candidati), "ammessi": len(ammessi),
               "esclusi": dict(sorted(conteggi.items())),
               "estratti_da_crispiano": sum(1 for _, _, c in estratti if c.lower() == "crispiano"),
               "commit_documentale": commit}
with open(os.path.join(USCITA, "generazione.json"), "w", encoding="utf8") as f:
    f.write(json.dumps(generazione, indent=2, ensure_ascii=False) + "\n")
print(json.dumps(generazione, indent=2, ensure_ascii=False))
