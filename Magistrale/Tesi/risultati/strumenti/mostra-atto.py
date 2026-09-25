#!/usr/bin/env python3
"""Mostra un atto del corpus per intero, per giudicarlo quando l'estratto del
foglio di annotazione non basta. Non scrive niente.

    mostra-atto.py <corpus.jsonl> <doc-id> [<doc-id> ...]
"""
import json, sys, textwrap

corpus_path, *cercati = sys.argv[1:]
if not cercati:
    sys.exit(__doc__)
resto = set(cercati)
for riga in open(corpus_path, encoding="utf8"):
    d = json.loads(riga)
    if d["_id"] in resto:
        resto.discard(d["_id"])
        print(f"=== {d['_id']}\n{d.get('title', '')}\n")
        for par in d.get("text", "").split("\n"):
            print(textwrap.fill(par, 100))
        print()
        if not resto:
            break
if resto:
    sys.exit(f"non nel corpus: {', '.join(sorted(resto))}")
