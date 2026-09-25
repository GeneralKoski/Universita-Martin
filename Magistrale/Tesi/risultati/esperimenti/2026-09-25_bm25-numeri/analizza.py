#!/usr/bin/env python3
"""Chi passa davanti all'atto giusto quando BM25 sbaglia una ricerca per numero.

Legge la valutazione di BM25 con la testa dei ranking (scripts/evaluate -top),
le valutazioni dei controfattuali, e il corpus in locale. Per ogni query in cui
l'atto giusto non è primo confronta il primo classificato con l'atto giusto:
contiene il numero? quante volte ripete le parole del comune? quanto è lungo?
Nell'esito finiscono solo id e conteggi, mai testi.

    analizza.py <corpus.jsonl> <queries.jsonl> <qrels.tsv> <bm25 con -top> [<controfattuale> ...]
"""
import collections, datetime, json, os, statistics, subprocess, sys, unicodedata

corpus_path, queries_path, qrels_path, base_path, *altri = sys.argv[1:]
QUI = os.path.dirname(os.path.abspath(__file__))


def termini(testo):
    """La tokenizzazione predefinita di Koskidex: minuscolo, via gli accenti,
    si spezza su tutto ciò che non è lettera o cifra."""
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
    # Come KoskidexSearcher: titolo e testo in un campo solo.
    docs[d["_id"]] = collections.Counter(termini((d.get("title", "") + " " + d.get("text", "")).strip()))
df = collections.Counter(t for c in docs.values() for t in c)
lunghezza = {k: sum(c.values()) for k, c in docs.items()}
media = statistics.mean(lunghezza.values())

domande = {json.loads(r)["_id"]: json.loads(r)["text"] for r in open(queries_path, encoding="utf8")}
giusto = {r.split("\t")[0]: r.split("\t")[1] for r in open(qrels_path).read().splitlines()[1:]}

base = json.load(open(base_path))
assert base["config"].get("modifiche_non_committate") == "false", "valutazione da codice non committato"
assert base["config"].get("top"), "serve una valutazione con -top"

righe, controllo_fallito = [], 0
for q in base["per_query"]:
    qid, atto = q["query_id"], giusto[q["query_id"]]
    qt = termini(domande[qid])
    numero = [t for t in qt if any(c.isdigit() for c in t)]
    comune = [t for t in qt if t not in numero]
    if any(docs[atto][t] == 0 for t in qt):
        controllo_fallito += 1
    posizione = round(1 / q["mrr@10"]) if q["mrr@10"] > 0 else None
    riga = {"query": qid, "posizione": posizione, "df_numero": min(df[t] for t in numero),
            "tf_comune_atto": sum(docs[atto][t] for t in comune), "lunghezza_atto": lunghezza[atto]}
    if posizione != 1:
        primo = q["top"][0]
        # Nessun termine della query tale e quale: il primo combacia solo per
        # prefisso (190 con 1900129), che è l'unico altro modo con i refusi spenti.
        esatti = [t for t in qt if docs[primo][t] > 0]
        riga.update({"primo": primo, "primo_ha_il_numero": all(docs[primo][t] > 0 for t in numero),
                     "primo_solo_per_prefisso": not esatti,
                     "tf_comune_primo": sum(docs[primo][t] for t in comune), "lunghezza_primo": lunghezza[primo]})
    righe.append(riga)

falliti = [r for r in righe if r["posizione"] != 1]
riusciti = [r for r in righe if r["posizione"] == 1]
senza_numero = [r for r in falliti if not r["primo_ha_il_numero"]]
riassunto = {
    "query": len(righe), "atto_primo": len(riusciti), "falliti": len(falliti),
    "controllo_tokenizzazione_fallito": controllo_fallito,
    "falliti_primo_senza_numero": len(senza_numero),
    "falliti_primo_con_il_numero": len(falliti) - len(senza_numero),
    "falliti_primo_solo_per_prefisso": sum(r["primo_solo_per_prefisso"] for r in falliti),
    "mediana_df_numero_falliti": statistics.median(r["df_numero"] for r in falliti),
    "mediana_df_numero_riusciti": statistics.median(r["df_numero"] for r in riusciti),
    "mediana_tf_comune_primo_nei_falliti": statistics.median(r["tf_comune_primo"] for r in falliti),
    "mediana_tf_comune_atto_nei_falliti": statistics.median(r["tf_comune_atto"] for r in falliti),
    "falliti_primo_ripete_il_comune_piu_dell_atto": sum(r["tf_comune_primo"] > r["tf_comune_atto"] for r in falliti),
    "falliti_primo_piu_corto_dell_atto": sum(r["lunghezza_primo"] < r["lunghezza_atto"] for r in falliti),
    "lunghezza_media_corpus": round(media, 1),
}
controfattuali = {}
for f in [base_path, *altri]:
    v = json.load(open(f))
    assert v["config"].get("modifiche_non_committate") == "false", f"{f}: codice non committato"
    pq = v["per_query"]
    controfattuali[v["run"]] = {"file": os.path.basename(f), "bm25_k1": v["config"].get("bm25_k1"),
                                "ricerca_per_prefisso": v["config"].get("ricerca_per_prefisso", "accesa"),
                                "bm25_b": v["config"].get("bm25_b"), "punteggio": v["config"].get("punteggio"),
                                "mrr@10": round(v["mean_mrr@10"], 4),
                                "atto_primo": sum(q["mrr@10"] == 1 for q in pq),
                                "oltre_10": sum(q["mrr@10"] == 0 for q in pq)}

for k, v in riassunto.items():
    print(f"{k}: {v}")
for k, v in controfattuali.items():
    print(f"{k:14s} k1={v['bm25_k1']} b={v['bm25_b']}  MRR@10 {v['mrr@10']:.4f}  primo {v['atto_primo']}/300  oltre 10 {v['oltre_10']}")

ora = datetime.datetime.now(datetime.timezone.utc)
git = lambda *a: subprocess.run(["git", "-C", QUI, *a], capture_output=True, text=True, check=True).stdout.strip()
esito = {"ran_at": ora.strftime("%Y-%m-%dT%H:%M:%SZ"),
         "config": {"commit": git("rev-parse", "--short", "HEAD"),
                    "modifiche_non_committate": "true" if git("status", "--porcelain", "--", "*.py") else "false",
                    "valutazione_base": os.path.basename(base_path), "commit_koskidex": base["config"].get("commit"),
                    "corpus_sha256": base["config"].get("corpus_sha256")},
         "riassunto": riassunto, "controfattuali": controfattuali, "per_query": righe}
if not os.environ.get("TESI_RISULTATI"):
    sys.exit("!!! RISULTATO NON ARCHIVIATO: TESI_RISULTATI non è impostata.")
d = os.path.join(os.environ["TESI_RISULTATI"], "esperimenti", "2026-09-25_bm25-numeri")
o = ora.strftime("%Y-%m-%dT%H%M%SZ"); p = os.path.join(d, f"{o}_esito.json"); n = 2
while os.path.exists(p):
    p = os.path.join(d, f"{o}-{n}_esito.json"); n += 1
open(p, "x").write(json.dumps(esito, indent=2, ensure_ascii=False))
print("archiviato in", p)
