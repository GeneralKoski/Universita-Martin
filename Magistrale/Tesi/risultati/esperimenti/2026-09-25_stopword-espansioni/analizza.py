#!/usr/bin/env python3
"""Le stopword o le loro espansioni: il conto sulle query di SciFact e il
guadagno delle stopword diviso fra le query con e senza una stopword
espandibile.

La lista delle stopword si legge da analyzer.go di Koskidex, così non può
divergere da quella usata in valutazione. Una stopword è espandibile se ha
almeno due byte, come in fuzzySearchTermsLocked, e se nel vocabolario c'è un
termine più lungo che comincia con lei.

    analizza.py <koskidex> <val. senza analisi> <val. con stopword> \\
        <senza prefisso, senza analisi> <senza prefisso, con stopword> \\
        [<nfcorpus senza prefisso> <nfcorpus senza prefisso, stopword>]
"""
import collections, datetime, json, os, re, statistics, subprocess, sys, unicodedata

kx, base_path, sw_path, *controfattuali = sys.argv[1:]
QUI = os.path.dirname(os.path.abspath(__file__))
SCIFACT = os.path.join(kx, "eval/corpora/c1-public/scifact")


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


sorgente = open(os.path.join(kx, "internal/engine/analyzer.go"), encoding="utf8").read()
blocco = re.search(r"func EnglishStopWords\(\).*?parole := \[\]string\{(.*?)\}", sorgente, re.S).group(1)
STOP = set(re.findall(r'"([^"]+)"', blocco))
assert len(STOP) == 33, f"attese le 33 stopword di Lucene, trovate {len(STOP)}"

df = collections.Counter()
for riga in open(os.path.join(SCIFACT, "corpus.jsonl"), encoding="utf8"):
    d = json.loads(riga)
    df.update(set(termini((d.get("title", "") + " " + d.get("text", "")).strip())))
per_prefisso = collections.defaultdict(list)
for t in df:
    for s in STOP:
        if len(s.encode()) >= 2 and len(t) > len(s) and t.startswith(s):
            per_prefisso[s].append(t)

base, sw = json.load(open(base_path)), json.load(open(sw_path))
for v in (base, sw):
    assert v["config"].get("modifiche_non_committate") == "false"
    assert v["config"].get("bm25_espansioni") in (None, ""), "servono le valutazioni con le espansioni di serie"
domande = {json.loads(r)["_id"]: json.loads(r)["text"] for r in open(os.path.join(SCIFACT, "queries.jsonl"), encoding="utf8")}
ndcg_base = {q["query_id"]: q["ndcg@10"] for q in base["per_query"]}
ndcg_sw = {q["query_id"]: q["ndcg@10"] for q in sw["per_query"]}
assert ndcg_base.keys() == ndcg_sw.keys()

righe = []
for qid in sorted(ndcg_base):
    qt = termini(domande[qid])
    espandibili = [t for t in qt if t in STOP and per_prefisso.get(t)]
    righe.append({"query": qid, "stopword": sum(t in STOP for t in qt), "stopword_espandibili": len(espandibili),
                  "espansioni": sum(len(per_prefisso[t]) for t in espandibili),
                  "guadagno_ndcg@10": round(ndcg_sw[qid] - ndcg_base[qid], 4)})

con = [r for r in righe if r["stopword_espandibili"]]
senza = [r for r in righe if not r["stopword_espandibili"]]
totale = sum(r["guadagno_ndcg@10"] for r in righe)
occorrenze = collections.Counter(t for qid in ndcg_base for t in termini(domande[qid]) if t in STOP and per_prefisso.get(t))
stopword = {s: {"occorrenze_nelle_query": n, "df": df[s], "espansioni": len(per_prefisso[s]),
                "espansioni_con_df_1": sum(df[t] == 1 for t in per_prefisso[s]),
                "df_mediana_espansioni": statistics.median(df[t] for t in per_prefisso[s])}
            for s, n in occorrenze.most_common()}
riassunto = {"query": len(righe), "stopword_nella_lista": len(STOP), "vocabolario": len(df),
             "query_con_stopword_espandibile": len(con), "query_senza": len(senza),
             "guadagno_medio_totale": round(totale / len(righe), 4),
             "quota_del_guadagno_dalle_query_senza": round(sum(r["guadagno_ndcg@10"] for r in senza) / totale, 3) if totale else None,
             "guadagno_medio_query_con": round(statistics.mean(r["guadagno_ndcg@10"] for r in con), 4) if con else None,
             "guadagno_medio_query_senza": round(statistics.mean(r["guadagno_ndcg@10"] for r in senza), 4) if senza else None,
             "query_senza_che_cambiano": sum(r["guadagno_ndcg@10"] != 0 for r in senza)}

valutazioni = {}
for f in [base_path, sw_path, *controfattuali]:
    v = json.load(open(f))
    assert v["config"].get("modifiche_non_committate") == "false", f
    valutazioni[os.path.basename(f)] = {"collezione": v["collection"], "analisi": v["config"].get("analisi"),
                                        "ricerca_per_prefisso": v["config"].get("ricerca_per_prefisso", "accesa"),
                                        "koskidex": v["config"]["commit"][:7], "ndcg@10": round(v["mean_ndcg@10"], 4),
                                        "recall@100": round(v["mean_recall@100"], 4)}

print(json.dumps(riassunto, indent=1))
print(json.dumps(stopword, indent=1))
print(json.dumps(valutazioni, indent=1))

ora = datetime.datetime.now(datetime.timezone.utc)
git = lambda *a: subprocess.run(["git", "-C", QUI, *a], capture_output=True, text=True, check=True).stdout.strip()
esito = {"ran_at": ora.strftime("%Y-%m-%dT%H:%M:%SZ"),
         "config": {"commit": git("rev-parse", "--short", "HEAD"),
                    "modifiche_non_committate": "true" if git("status", "--porcelain", "--", "*.py") else "false",
                    "koskidex": subprocess.run(["git", "-C", kx, "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()},
         "riassunto": riassunto, "stopword": stopword, "valutazioni": valutazioni, "per_query": righe}
if not os.environ.get("TESI_RISULTATI"):
    sys.exit("!!! RISULTATO NON ARCHIVIATO: TESI_RISULTATI non è impostata.")
d = os.path.join(os.environ["TESI_RISULTATI"], "esperimenti", "2026-09-25_stopword-espansioni")
o = ora.strftime("%Y-%m-%dT%H%M%SZ"); p = os.path.join(d, f"{o}_esito.json"); n = 2
while os.path.exists(p):
    p = os.path.join(d, f"{o}-{n}_esito.json"); n += 1
open(p, "x").write(json.dumps(esito, indent=2, ensure_ascii=False))
print("archiviato in", p)
