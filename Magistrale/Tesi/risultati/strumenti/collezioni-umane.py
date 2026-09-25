#!/usr/bin/env python3
"""Prepara in Koskidex le collezioni delle known-item umane, per scripts/evaluate.

- known-item-umane: il corpus a schede di tutti i 10.018 atti;
- crispiano-scheda e crispiano-testo: i soli 563 atti di Crispiano, con la
  scheda o con il testo estratto dai PDF (esperimento 2026-09-25_scheda-testo).

Query e giudizi sono link a query/known-item-umane/ di questo archivio, scritti
da importa-raccolta.py: la collezione segue la raccolta senza copie. I due
corpora di Crispiano sono file veri, estratti dagli export di Documentale; come
ogni corpus, restano fuori da git (in Koskidex eval/corpora/c3-albo/ è ignorato).

    collezioni-umane.py [--corpora <cartella>] [--query <cartella>]

Senza opzioni: eval/corpora/c3-albo di Koskidex e query/known-item-umane qui.
"""
import argparse, json, os

QUI = os.path.dirname(os.path.abspath(__file__))
KOSKIDEX = os.path.expanduser("~/Desktop/Progetti-personali/Koskidex")
ALBO = os.path.join(KOSKIDEX, "eval", "corpora", "c3-albo")

p = argparse.ArgumentParser()
p.add_argument("--corpora", default=ALBO)
p.add_argument("--query", default=os.path.join(QUI, "..", "query", "known-item-umane"))
a = p.parse_args()
query = os.path.abspath(a.query)
for f in ("queries.jsonl", "qrels"):
    if not os.path.exists(os.path.join(query, f)):
        raise SystemExit(f"manca {f} in {query}: prima importa-raccolta.py")


def leggi(nome):
    return [json.loads(r) for r in open(os.path.join(ALBO, nome, "corpus.jsonl"), encoding="utf8")]


def collega(cartella, nome, destinazione):
    percorso = os.path.join(cartella, nome)
    if os.path.islink(percorso):
        os.remove(percorso)
    elif os.path.exists(percorso):
        raise SystemExit(f"{percorso} c'è già e non è un link: non lo tocco")
    os.symlink(destinazione, percorso)


scheda, testo = leggi("beir-metadata"), leggi("beir-full")
assert [d["_id"] for d in scheda] == [d["_id"] for d in testo], "i due export non hanno gli stessi atti"
crispiano = {d["_id"] for d, e in zip(scheda, testo) if d["text"] != e["text"]}
assert len(crispiano) == 563, f"attesi i 563 atti col testo intero, trovati {len(crispiano)}"

for nome, corpus in (("known-item-umane", None), ("crispiano-scheda", scheda), ("crispiano-testo", testo)):
    cartella = os.path.join(a.corpora, nome)
    os.makedirs(cartella, exist_ok=True)
    if corpus is None:
        collega(cartella, "corpus.jsonl", os.path.join(ALBO, "beir-metadata", "corpus.jsonl"))
    else:
        with open(os.path.join(cartella, "corpus.jsonl"), "w", encoding="utf8") as f:
            for d in corpus:
                if d["_id"] in crispiano:
                    f.write(json.dumps(d, ensure_ascii=False) + "\n")
    collega(cartella, "queries.jsonl", os.path.join(query, "queries.jsonl"))
    collega(cartella, "qrels", os.path.join(query, "qrels"))
    print(nome, "->", cartella)
