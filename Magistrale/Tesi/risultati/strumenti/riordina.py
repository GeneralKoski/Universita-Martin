#!/usr/bin/env python3
"""Riordina con un cross-encoder i primi k candidati di una valutazione di
scripts/evaluate salvata con -top k, e scrive un rapporto nel formato di
app:eval-run-queries, che scripts/evaluate -rankings valuta con gli stessi
giudizi (esperimento 2026-09-28_reranker).

Il punteggio è quello del modello sulla coppia (testo della query, titolo e
testo del documento come nel corpus); a parità di punteggio vale l'ordine del
primo stadio. Il campo ms di ogni query è il tempo del riordino.

Gira nell'ambiente a parte con torch e sentence-transformers
(~/.venvs/tesi-reranker), non nel Python di sistema.

    riordina.py --valutazione <json> --collezione <cartella BEIR> --uscita <json> [--dtype float16]
"""
import argparse, datetime, hashlib, json, os, platform, subprocess, time

QUI = os.path.dirname(os.path.abspath(__file__))
p = argparse.ArgumentParser()
p.add_argument("--valutazione", required=True, help="scripts/evaluate con -top k: il primo stadio")
p.add_argument("--collezione", required=True, help="cartella con corpus.jsonl e queries.jsonl")
p.add_argument("--uscita", required=True, help="il rapporto da scrivere; non si sovrascrive")
p.add_argument("--modello", default="BAAI/bge-reranker-v2-m3")
p.add_argument("--k", type=int, default=100)
p.add_argument("--max-length", type=int, default=512)
p.add_argument("--batch", type=int, default=32)
p.add_argument("--dispositivo", default="mps")
p.add_argument("--dtype", default="float32", choices=["float32", "float16"])
a = p.parse_args()

import sentence_transformers, torch
from huggingface_hub import snapshot_download
from sentence_transformers import CrossEncoder

primo = json.load(open(a.valutazione))
assert primo["config"].get("modifiche_non_committate") in ("false", False), f"{a.valutazione}: codice non committato"
assert int(primo["config"].get("top", 0)) >= a.k, f"{a.valutazione}: il primo stadio ha salvato meno di {a.k} id"
testi = {}
for riga in open(os.path.join(a.collezione, "corpus.jsonl"), encoding="utf8"):
    d = json.loads(riga)
    testi[d["_id"]] = ((d.get("title") or "") + " " + (d.get("text") or "")).strip()
domande = {}
for riga in open(os.path.join(a.collezione, "queries.jsonl"), encoding="utf8"):
    q = json.loads(riga)
    domande[q["_id"]] = q["text"]

modello = CrossEncoder(a.modello, max_length=a.max_length, device=a.dispositivo,
                       model_kwargs={"dtype": getattr(torch, a.dtype)})
esiti = []
for q in primo["per_query"]:
    candidati = (q.get("top") or [])[: a.k]
    inizio = time.perf_counter()
    if candidati:
        punteggi = modello.predict([(domande[q["query_id"]], testi[c]) for c in candidati], batch_size=a.batch)
        ordine = sorted(range(len(candidati)), key=lambda i: (-float(punteggi[i]), i))
        ids = [candidati[i] for i in ordine]
    else:
        ids = []
    esiti.append({"query": domande[q["query_id"]], "ids": ids, "ms": round((time.perf_counter() - inizio) * 1000, 3)})
    print(f"  {q['query_id']:>16} {len(ids):4d} candidati {esiti[-1]['ms']:9.1f} ms", flush=True)

git = lambda *x: subprocess.run(["git", "-C", QUI, *x], capture_output=True, text=True).stdout.strip()
rapporto = {
    "ran_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "config": {
        "motore": "reranker-" + a.modello.split("/")[-1], "modello": a.modello,
        "revisione": os.path.basename(snapshot_download(a.modello, local_files_only=True)),
        "k": a.k, "max_length": a.max_length, "batch": a.batch, "dispositivo": a.dispositivo,
        "dtype": str(next(modello.parameters()).dtype).removeprefix("torch."),
        "torch": torch.__version__, "sentence_transformers": sentence_transformers.__version__,
        "python": platform.python_version(),
        "primo_stadio": os.path.basename(a.valutazione),
        "primo_stadio_sha256": hashlib.sha256(open(a.valutazione, "rb").read()).hexdigest(),
        "collezione": primo["collection"],
        "commit": git("rev-parse", "HEAD"),
        "modifiche_non_committate": "true" if git("status", "--porcelain", "--", os.path.abspath(__file__)) else "false",
    },
    "query": esiti,
}
os.makedirs(os.path.dirname(os.path.abspath(a.uscita)), exist_ok=True)
open(a.uscita, "x").write(json.dumps(rapporto, indent=2, ensure_ascii=False))
print("scritto in", a.uscita)
