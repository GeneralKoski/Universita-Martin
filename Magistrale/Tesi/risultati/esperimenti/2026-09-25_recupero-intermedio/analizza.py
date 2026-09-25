#!/usr/bin/env python3
"""Recupero intermedio e coordinazione: metriche delle varianti contro la base
sulle tre collezioni, e per le known-item i fallimenti divisi per numero di
termini della query e per classe del primo classificato (numero esatto, solo
per prefisso, senza numero), come in 2026-09-25_known-item-divario.

    analizza.py <corpus known-item> <queries known-item> <qrels known-item> <valutazione> [...]
"""
import collections, datetime, json, os, subprocess, sys, unicodedata

corpus_path, queries_path, qrels_path, *valutazioni = sys.argv[1:]
QUI = os.path.dirname(os.path.abspath(__file__))


def termini(testo):
    t = unicodedata.normalize("NFD", testo.lower())
    t = unicodedata.normalize("NFC", "".join(c for c in t if unicodedata.category(c) != "Mn"))
    out, parola = [], []
    for c in t:
        if c.isalpha() or c.isnumeric():
            parola.append(c)
        elif parola:
            out.append("".join(parola)); parola = []
    if parola:
        out.append("".join(parola))
    return out


docs = {}
for riga in open(corpus_path, encoding="utf8"):
    d = json.loads(riga)
    docs[d["_id"]] = collections.Counter(termini((d.get("title", "") + " " + d.get("text", "")).strip()))
domande = {json.loads(r)["_id"]: json.loads(r)["text"] for r in open(queries_path, encoding="utf8")}


def classe(doc, numeri):
    if all(doc[n] > 0 for n in numeri):
        return "numero esatto"
    if all(doc[n] > 0 or any(t.startswith(n) and len(t) > len(n) for t in doc) for n in numeri):
        return "numero solo per prefisso"
    return "senza numero"


def lunghezza(n):
    return "2 termini" if n <= 2 else ("3-4 termini" if n <= 4 else "5 o più")


righe = {}
for f in valutazioni:
    v = json.load(open(f))
    c = v["config"]
    assert c.get("modifiche_non_committate") == "false", f"{f}: codice non committato"
    pq = v["per_query"]
    r = {"file": os.path.basename(f), "collezione": v["collection"], "koskidex": c["commit"][:7],
         "recupero": c.get("recupero"), "bm25_espansioni": c.get("bm25_espansioni", ""),
         "minimum_should_match": c.get("minimum_should_match", ""), "coordinazione": c.get("coordinazione", "spenta"),
         "ndcg@10": round(v["mean_ndcg@10"], 4), "mrr@10": round(v["mean_mrr@10"], 4),
         "recall@100": round(v["mean_recall@100"], 4), "a_vuoto": v["zero_results"]}
    if v["collection"] == "known-item-auto":
        r["atto_primo"] = sum(q["mrr@10"] == 1 for q in pq)
        per_lunghezza = collections.defaultdict(lambda: {"query": 0, "primo": 0})
        per_classe = collections.Counter()
        for q in pq:
            qt = termini(domande[q["query_id"]])
            g = per_lunghezza[lunghezza(len(qt))]
            g["query"] += 1
            g["primo"] += q["mrr@10"] == 1
            if q["mrr@10"] != 1 and c.get("top"):
                per_classe[classe(docs[q["top"][0]], [t for t in qt if any(ch.isdigit() for ch in t)])] += 1
        r["atto_primo_per_lunghezza"] = dict(sorted(per_lunghezza.items()))
        if c.get("top"):
            r["falliti_per_classe"] = dict(per_classe.most_common())
    righe[v["run"] + "@" + v["collection"]] = r
    print(json.dumps(r, ensure_ascii=False))

ora = datetime.datetime.now(datetime.timezone.utc)
git = lambda *a: subprocess.run(["git", "-C", QUI, *a], capture_output=True, text=True, check=True).stdout.strip()
esito = {"ran_at": ora.strftime("%Y-%m-%dT%H:%M:%SZ"),
         "config": {"commit": git("rev-parse", "--short", "HEAD"),
                    "modifiche_non_committate": "true" if git("status", "--porcelain", "--", "*.py") else "false"},
         "valutazioni": righe}
if not os.environ.get("TESI_RISULTATI"):
    sys.exit("!!! RISULTATO NON ARCHIVIATO: TESI_RISULTATI non è impostata.")
d = os.path.join(os.environ["TESI_RISULTATI"], "esperimenti", "2026-09-25_recupero-intermedio")
o = ora.strftime("%Y-%m-%dT%H%M%SZ"); p = os.path.join(d, f"{o}_esito.json"); n = 2
while os.path.exists(p):
    p = os.path.join(d, f"{o}-{n}_esito.json"); n += 1
open(p, "x").write(json.dumps(esito, indent=2, ensure_ascii=False))
print("archiviato in", p)
