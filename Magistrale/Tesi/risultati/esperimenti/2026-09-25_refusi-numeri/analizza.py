#!/usr/bin/env python3
"""Niente refusi sui numeri: il quadrato due per due, campo unico o parole libere
per refusi sui numeri sì o no, dall'app.

1. Known-item: metriche e tempi delle quattro valutazioni (scripts/evaluate
   -rankings) e, per la configurazione con le parole libere e i numeri esatti,
   dove il primo classificato ha il numero quando l'atto giusto non è primo. I
   documenti si leggono dal Koskidex in ascolto; nell'esito solo id, campi e
   conteggi.
2. Le 24 query del confronto: gli insiemi con i numeri esatti contro quelli con i
   refusi sui numeri, a parità di vincolo, e le posizioni di doc-0001 per
   "ordinanza 187" e di doc-0002 per "determina 1223".

    analizza.py <queries.jsonl> <qrels.tsv> \\
        <val. unico refusi> <val. liberi refusi> <val. unico esatti> <val. liberi esatti> \\
        <conf. unico refusi> <conf. liberi refusi> <conf. unico esatti> <conf. liberi esatti> \\
        <conf. elasticsearch> [koskidex]
"""
import datetime, json, os, statistics, subprocess, sys, unicodedata, urllib.request

queries_path, qrels_path, *resto = sys.argv[1:]
val_paths, conf_paths, es_path = resto[0:4], resto[4:8], resto[8]
KX = resto[9] if len(resto) > 9 else "http://localhost:7711"
CELLE = ["campo unico, refusi sui numeri", "parole libere, refusi sui numeri",
         "campo unico, numeri esatti", "parole libere, numeri esatti"]
INDICE = "search-documents-local"
PESI = {"name": 5, "tags": 4, "summary": 3, "subjects": 3, "notes": 2, "additional_data": 1}
ATTESI = {"ordinanza 187": "doc-0001", "determina 1223": "doc-0002"}
QUI = os.path.dirname(os.path.abspath(__file__))


def termini(testo):
    t = unicodedata.normalize("NFD", str(testo).lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    out, p = [], []
    for c in t:
        if c.isalnum():
            p.append(c)
        elif p:
            out.append("".join(p)); p = []
    return out + (["".join(p)] if p else [])


def campi(doc_id):
    d = json.load(urllib.request.urlopen(f"{KX}/indexes/{INDICE}/documents/{doc_id.removeprefix('doc-').lstrip('0')}"))
    d = d.get("document", d)
    out = {}
    for c in PESI:
        v = d.get(c) or ""
        v = " ".join(map(str, v)) if isinstance(v, list) else str(v)
        out[c] = set(termini(v))
    return out


def carica(p):
    r = json.load(open(p))
    assert r["config"].get("modifiche_non_committate") == "false", f"{p}: codice non committato"
    return r


domande = {json.loads(r)["_id"]: json.loads(r)["text"] for r in open(queries_path, encoding="utf8")}
giusto = {r.split("\t")[0]: r.split("\t")[1] for r in open(qrels_path).read().splitlines()[1:]}

vals = [carica(p) for p in val_paths]
known_item = {}
for cella, p, v in zip(CELLE, val_paths, vals):
    pq, ms = v["per_query"], list(v["timings"]["per_query_ms"].values())
    known_item[cella] = {"valutazione": os.path.basename(p), "koskidex": v["config"]["commit"][:7],
                         "mrr@10": round(v["mean_mrr@10"], 4), "atto_primo": sum(q["mrr@10"] == 1 for q in pq),
                         "atto_entro_10": sum(q["mrr@10"] > 0 for q in pq), "recall@100": round(v["mean_recall@100"], 4),
                         "a_vuoto": v["zero_results"], "ms_mediana": round(statistics.median(ms), 2),
                         "ms_media": round(statistics.mean(ms), 2)}

# Chi resta davanti con le parole libere e i numeri esatti.
motivi, righe = {}, []
for q in vals[3]["per_query"]:
    if q["mrr@10"] == 1:
        continue
    qid = q["query_id"]
    numeri = [t for t in termini(domande[qid]) if any(ch.isdigit() for ch in t)]
    numero = max(numeri, key=len)
    primo, atto = campi(q["top"][0]), campi(giusto[qid])
    c_primo = [c for c, ts in primo.items() if numero in ts]
    c_atto = [c for c, ts in atto.items() if numero in ts]
    if not c_primo:
        motivo = "primo senza il numero esatto"
    elif max(PESI[c] for c in c_primo) > max([PESI[c] for c in c_atto] or [0]):
        motivo = "primo ha il numero esatto, in un campo che pesa di più"
    else:
        motivo = "primo ha il numero esatto, in un campo che non pesa di più"
    motivi[motivo] = motivi.get(motivo, 0) + 1
    righe.append({"query": qid, "numero_solo_cifre": numero.isdigit(),
                  "posizione": round(1 / q["mrr@10"]) if q["mrr@10"] else None, "primo": q["top"][0],
                  "campi_numero_primo": c_primo, "campi_numero_atto": c_atto, "motivo": motivo})

confs = [carica(p) for p in conf_paths]
es = carica(es_path)


def insiemi(prima, dopo):
    out = []
    for a, b in zip(prima["query"], dopo["query"]):
        assert a["query"] == b["query"]
        A, B = set(a["ids"]), set(b["ids"])
        if A != B:
            out.append({"query": a["query"], "prima": len(A), "dopo": len(B), "persi": len(A - B), "nuovi": len(B - A)})
    return {"query": len(prima["query"]), "insiemi_cambiati": out}


confronto = {"campo unico": insiemi(confs[0], confs[2]), "parole libere": insiemi(confs[1], confs[3])}
posizioni = {}
for q, doc in ATTESI.items():
    posizioni[q] = {}
    for nome, r in [("elasticsearch, produzione", es)] + list(zip(CELLE, confs)):
        ids = next(x["ids"] for x in r["query"] if x["query"] == q)
        posizioni[q][nome] = {"posizione": ids.index(doc) + 1 if doc in ids else None, "risultati": len(ids)}

print(json.dumps(known_item, indent=1, ensure_ascii=False))
print(json.dumps(motivi, indent=1, ensure_ascii=False))
print(json.dumps(confronto, indent=1, ensure_ascii=False))
print(json.dumps(posizioni, indent=1, ensure_ascii=False))

ora = datetime.datetime.now(datetime.timezone.utc)
git = lambda *a: subprocess.run(["git", "-C", QUI, *a], capture_output=True, text=True, check=True).stdout.strip()
esito = {"ran_at": ora.strftime("%Y-%m-%dT%H:%M:%SZ"),
         "config": {"commit": git("rev-parse", "--short", "HEAD"),
                    "modifiche_non_committate": "true" if git("status", "--porcelain", "--", "*.py") else "false",
                    "rapporti_confronto": [os.path.basename(p) for p in conf_paths],
                    "rapporto_elasticsearch": os.path.basename(es_path)},
         "known_item": known_item, "parole_libere_numeri_esatti_non_primi": {"per_motivo": motivi, "query": righe},
         "confronto_24": confronto, "posizioni_numero_atto": posizioni}
if not os.environ.get("TESI_RISULTATI"):
    sys.exit("!!! RISULTATO NON ARCHIVIATO: TESI_RISULTATI non è impostata.")
d = os.path.join(os.environ["TESI_RISULTATI"], "esperimenti", "2026-09-25_refusi-numeri")
o = ora.strftime("%Y-%m-%dT%H%M%SZ"); p = os.path.join(d, f"{o}_esito.json"); n = 2
while os.path.exists(p):
    p = os.path.join(d, f"{o}-{n}_esito.json"); n += 1
open(p, "x").write(json.dumps(esito, indent=2, ensure_ascii=False))
print("archiviato in", p)
