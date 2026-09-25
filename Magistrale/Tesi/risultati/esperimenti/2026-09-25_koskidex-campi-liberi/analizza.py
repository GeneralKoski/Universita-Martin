#!/usr/bin/env python3
"""Koskidex innestato con le parole libere di stare in campi diversi.

1. Known-item: metriche dalla valutazione (scripts/evaluate -rankings -top) e,
   per ogni query in cui l'atto giusto non è primo, dove il primo classificato
   ha il numero: tale e quale o con un refuso, e in quale campo. I documenti si
   leggono dal Koskidex in ascolto; nell'esito vanno solo id, campi e conteggi.
2. Le 24 query del confronto: gli insiemi con i campi liberi contro quelli di
   Elasticsearch, per vedere che crescono soltanto.

    analizza.py <valutazione known-item> <queries.jsonl> <qrels.tsv> \\
        <rapporto confronto campi liberi> <rapporto confronto elasticsearch> [koskidex]
"""
import collections, datetime, json, os, subprocess, sys, unicodedata, urllib.request

val_path, queries_path, qrels_path, liberi_path, es_path, *resto = sys.argv[1:]
KX = resto[0] if resto else "http://localhost:7711"
INDICE = "search-documents-local"
PESI = {"name": 5, "tags": 4, "summary": 3, "subjects": 3, "notes": 2, "additional_data": 1}
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


def distanza(a, b):
    """Damerau-Levenshtein ristretta, come i refusi di Koskidex."""
    d = [[i + j if i * j == 0 else 0 for j in range(len(b) + 1)] for i in range(len(a) + 1)]
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + (a[i - 1] != b[j - 1]))
            if i > 1 and j > 1 and a[i - 1] == b[j - 2] and a[i - 2] == b[j - 1]:
                d[i][j] = min(d[i][j], d[i - 2][j - 2] + 1)
    return d[-1][-1]


def campi(doc_id):
    d = json.load(urllib.request.urlopen(f"{KX}/indexes/{INDICE}/documents/{doc_id.removeprefix('doc-').lstrip('0')}"))
    d = d.get("document", d)
    out = {}
    for c in PESI:
        v = d.get(c) or ""
        v = " ".join(map(str, v)) if isinstance(v, list) else str(v)
        out[c] = set(termini(v))
    return out


def dove(cs, numero, refusi):
    """I campi in cui compare il numero tale e quale, e quelli in cui compare
    solo con un refuso ammesso (uno da 3 caratteri, due da 6, prima cifra
    esatta come prefix_length 1)."""
    esatto, vicino = [], []
    for c, ts in cs.items():
        if numero in ts:
            esatto.append(c)
        elif refusi and any(t[:1] == numero[:1] and 0 < distanza(numero, t) <= refusi for t in ts):
            vicino.append(c)
    return esatto, vicino


val = json.load(open(val_path))
assert val["config"].get("modifiche_non_committate") == "false", "valutazione da codice non committato"
domande = {json.loads(r)["_id"]: json.loads(r)["text"] for r in open(queries_path, encoding="utf8")}
giusto = {r.split("\t")[0]: r.split("\t")[1] for r in open(qrels_path).read().splitlines()[1:]}

pq = val["per_query"]
motivi = collections.Counter()
righe = []
for q in pq:
    if q["mrr@10"] == 1:
        continue
    qid = q["query_id"]
    numeri = [t for t in termini(domande[qid]) if any(ch.isdigit() for ch in t)]
    numero = max(numeri, key=len)
    refusi = 0 if len(numero) < 3 else (1 if len(numero) < 6 else 2)
    primo, atto = campi(q["top"][0]), campi(giusto[qid])
    e_primo, v_primo = dove(primo, numero, refusi)
    e_atto, _ = dove(atto, numero, refusi)
    peso_primo = max([PESI[c] for c in e_primo + v_primo] or [0])
    peso_atto = max([PESI[c] for c in e_atto] or [0])
    if e_primo:
        motivo = "primo ha il numero esatto"
    elif v_primo and peso_primo > peso_atto:
        motivo = "primo ha il numero con un refuso, in un campo che pesa di più"
    elif v_primo:
        motivo = "primo ha il numero con un refuso, in un campo che non pesa di più"
    else:
        motivo = "primo non ha il numero"
    motivi[motivo] += 1
    righe.append({"query": qid, "posizione": round(1 / q["mrr@10"]) if q["mrr@10"] else None,
                  "primo": q["top"][0], "campi_numero_esatto_primo": e_primo, "campi_numero_vicino_primo": v_primo,
                  "campi_numero_atto": e_atto, "motivo": motivo})

known_item = {"valutazione": os.path.basename(val_path), "query": val["queries"],
              "mrr@10": round(val["mean_mrr@10"], 4),
              "atto_primo": sum(q["mrr@10"] == 1 for q in pq), "atto_entro_10": sum(q["mrr@10"] > 0 for q in pq),
              "recall@100": round(val["mean_recall@100"], 4), "a_vuoto": val["zero_results"],
              "non_primo_per_motivo": dict(motivi.most_common())}

liberi, es = json.load(open(liberi_path)), json.load(open(es_path))
for r in (liberi, es):
    assert r["config"].get("modifiche_non_committate") == "false", "rapporto da codice non committato"
confronto = []
for a, b in zip(liberi["query"], es["query"]):
    assert a["query"] == b["query"]
    A, B = set(a["ids"]), set(b["ids"])
    confronto.append({"query": a["query"], "campi_liberi": len(A), "elasticsearch": len(B),
                      "in_piu": len(A - B), "persi": len(B - A)})
riassunto_confronto = {"query": len(confronto), "insiemi_uguali": sum(c["in_piu"] == 0 and c["persi"] == 0 for c in confronto),
                       "query_con_documenti_persi": sum(c["persi"] > 0 for c in confronto),
                       "documenti_in_piu": sum(c["in_piu"] for c in confronto)}

print(json.dumps(known_item, indent=2, ensure_ascii=False))
print(json.dumps(riassunto_confronto, indent=2, ensure_ascii=False))

ora = datetime.datetime.now(datetime.timezone.utc)
git = lambda *a: subprocess.run(["git", "-C", QUI, *a], capture_output=True, text=True, check=True).stdout.strip()
esito = {"ran_at": ora.strftime("%Y-%m-%dT%H:%M:%SZ"),
         "config": {"commit": git("rev-parse", "--short", "HEAD"),
                    "modifiche_non_committate": "true" if git("status", "--porcelain", "--", "*.py") else "false",
                    "koskidex_versione": liberi["config"].get("koskidex_versione"),
                    "commit_documentale": liberi["config"].get("commit"),
                    "rapporto_campi_liberi": os.path.basename(liberi_path), "rapporto_elasticsearch": os.path.basename(es_path)},
         "known_item": known_item, "known_item_non_primi": righe,
         "confronto_24": {"riassunto": riassunto_confronto, "query": confronto}}
if not os.environ.get("TESI_RISULTATI"):
    sys.exit("!!! RISULTATO NON ARCHIVIATO: TESI_RISULTATI non è impostata.")
d = os.path.join(os.environ["TESI_RISULTATI"], "esperimenti", "2026-09-25_koskidex-campi-liberi")
o = ora.strftime("%Y-%m-%dT%H%M%SZ"); p = os.path.join(d, f"{o}_esito.json"); n = 2
while os.path.exists(p):
    p = os.path.join(d, f"{o}-{n}_esito.json"); n += 1
open(p, "x").write(json.dumps(esito, indent=2, ensure_ascii=False))
print("archiviato in", p)
