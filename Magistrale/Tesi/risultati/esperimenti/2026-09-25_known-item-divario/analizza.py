#!/usr/bin/env python3
"""Chi passa davanti all'atto giusto con BM25 corretto: per ogni valutazione
con i primi dieci id, il primo classificato di ogni query sbagliata ha il
numero esatto, solo per prefisso, o non ce l'ha? Corpus letto in locale,
nell'esito solo id e conteggi.

    analizza.py <corpus.jsonl> <queries.jsonl> <qrels.tsv> <valutazione con -top> [...]
"""
import collections, datetime, json, os, statistics, subprocess, sys, unicodedata

corpus_path, queries_path, qrels_path, *valutazioni = sys.argv[1:]
QUI = os.path.dirname(os.path.abspath(__file__))


def termini(testo):
    """La tokenizzazione predefinita di Koskidex, come in 2026-09-25_bm25-numeri."""
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
lunghezza = {k: sum(c.values()) for k, c in docs.items()}
domande = {json.loads(r)["_id"]: json.loads(r)["text"] for r in open(queries_path, encoding="utf8")}
giusto = {r.split("\t")[0]: r.split("\t")[1] for r in open(qrels_path).read().splitlines()[1:]}


def classe(doc, numeri):
    if all(doc[n] > 0 for n in numeri):
        return "numero esatto"
    if all(doc[n] > 0 or any(t.startswith(n) and len(t) > len(n) for t in doc) for n in numeri):
        return "numero solo per prefisso"
    return "senza numero"


esiti = {}
for f in valutazioni:
    v = json.load(open(f))
    assert v["config"].get("modifiche_non_committate") == "false", f"{f}: codice non committato"
    assert v["config"].get("top"), f"{f}: serve una valutazione con -top"
    righe, controllo = [], 0
    for q in v["per_query"]:
        if q["mrr@10"] == 1:
            continue
        qid, atto = q["query_id"], giusto[q["query_id"]]
        qt = termini(domande[qid])
        numeri = [t for t in qt if any(c.isdigit() for c in t)]
        comune = [t for t in qt if t not in numeri]
        if any(docs[atto][t] == 0 for t in qt):
            controllo += 1
        primo = q["top"][0]
        righe.append({"query": qid, "posizione": round(1 / q["mrr@10"]) if q["mrr@10"] else None, "primo": primo,
                      "classe": classe(docs[primo], numeri),
                      "tf_comune_primo": sum(docs[primo][t] for t in comune), "tf_comune_atto": sum(docs[atto][t] for t in comune),
                      "lunghezza_primo": lunghezza[primo], "lunghezza_atto": lunghezza[atto]})
    per_classe = collections.Counter(r["classe"] for r in righe)
    senza = [r for r in righe if r["classe"] == "senza numero"]
    esiti[v["run"]] = {"file": os.path.basename(f), "koskidex": v["config"]["commit"][:7],
                       "bm25_espansioni": v["config"].get("bm25_espansioni", ""),
                       "ricerca_per_prefisso": v["config"].get("ricerca_per_prefisso", "accesa"),
                       "mrr@10": round(v["mean_mrr@10"], 4), "falliti": len(righe),
                       "controllo_tokenizzazione_fallito": controllo, "per_classe": dict(per_classe.most_common()),
                       "senza_numero_primo_ripete_il_comune_di_piu": sum(r["tf_comune_primo"] > r["tf_comune_atto"] for r in senza),
                       "senza_numero_primo_piu_corto": sum(r["lunghezza_primo"] < r["lunghezza_atto"] for r in senza),
                       "per_query": righe}
    print(json.dumps({k: x for k, x in esiti[v["run"]].items() if k != "per_query"}, indent=1, ensure_ascii=False))

ora = datetime.datetime.now(datetime.timezone.utc)
git = lambda *a: subprocess.run(["git", "-C", QUI, *a], capture_output=True, text=True, check=True).stdout.strip()
esito = {"ran_at": ora.strftime("%Y-%m-%dT%H:%M:%SZ"),
         "config": {"commit": git("rev-parse", "--short", "HEAD"),
                    "modifiche_non_committate": "true" if git("status", "--porcelain", "--", "*.py") else "false"},
         "valutazioni": esiti}
if not os.environ.get("TESI_RISULTATI"):
    sys.exit("!!! RISULTATO NON ARCHIVIATO: TESI_RISULTATI non è impostata.")
d = os.path.join(os.environ["TESI_RISULTATI"], "esperimenti", "2026-09-25_known-item-divario")
o = ora.strftime("%Y-%m-%dT%H%M%SZ"); p = os.path.join(d, f"{o}_esito.json"); n = 2
while os.path.exists(p):
    p = os.path.join(d, f"{o}-{n}_esito.json"); n += 1
open(p, "x").write(json.dumps(esito, indent=2, ensure_ascii=False))
print("archiviato in", p)
