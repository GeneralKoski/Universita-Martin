#!/usr/bin/env python3
"""Le elisioni con Koskidex innestato: quattro motori sulle stesse parole, e cosa
cambia per le altre query. Metodo e ipotesi nel README.

1. Le coppie (atto, parola solo elisa) dai termini veri dell'indice di
   Elasticsearch, come conta.py di 2026-09-25_elisioni.
2. Ogni parola cercata da sola su Elasticsearch di produzione, sull'indice di
   controllo col filtro elision (creato e cancellato qui), su Koskidex elis0 ed
   elis1 con la richiesta di KoskidexClient::searchIds.
3. Le 24 query del confronto su elis0 ed elis1 e le 300 known-item su lib0 e
   lib1, dai rapporti di app:eval-run-queries e dalle loro valutazioni.

Nell'esito solo conteggi, id e le parole presenti in almeno 20 atti.

    TESI_RISULTATI=... analizza.py <conf. elis0> <conf. elis1> <known-item lib0> <known-item lib1> \\
        <val. lib0> <val. lib1> <queries.txt delle known-item> [koskidex]
"""
import collections, datetime, json, os, re, statistics, subprocess, sys, time, urllib.error, urllib.parse, urllib.request

ES = "http://localhost:9201"
INDICE = "search-documents-local"
CONTROLLO = "elisioni-controllo"
CAMPI = ["name", "tags", "summary", "subjects", "notes", "additional_data"]
PESI = ["name^5", "tags^4", "summary^3", "subjects^3", "notes^2", "additional_data^1"]
# Gli articoli del filtro italian_elision dell'analizzatore italian di Elasticsearch.
ARTICOLI = ["c", "l", "all", "dall", "dell", "nell", "sull", "coll", "pell", "gl", "agl",
            "dagl", "degl", "negl", "sugl", "un", "m", "t", "s", "v", "d"]
ELISO = re.compile(r"^([^\W\d_]+)['’]([^\W\d_]+)$")  # quella di conta.py
MIN_LETTERE = 3
MIN_ATTI_PAROLA = 20
QUI = os.path.dirname(os.path.abspath(__file__))

conf0_p, conf1_p, ki0_p, ki1_p, val0_p, val1_p, ki_queries_p, *resto = sys.argv[1:]
KX = resto[0] if resto else "http://localhost:7711"
INDICI_KX = {k: f"search-documents-{k}" for k in ("elis0", "elis1", "lib0", "lib1")}


def chiama(metodo, percorso, corpo=None):
    dati = json.dumps(corpo).encode() if corpo is not None else None
    r = urllib.request.Request(ES + percorso, data=dati, method=metodo,
                               headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(r))


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout.strip()


def eliso(t):
    m = ELISO.match(t)
    return (m.group(1), m.group(2)) if m else None


def cerca_es(indice, parola):
    corpo = {"query": {"multi_match": {"query": parola, "type": "best_fields", "fuzziness": "AUTO",
                                       "prefix_length": 1, "operator": "and", "tie_breaker": 0.3,
                                       "fields": PESI}},
             "size": 10000, "_source": False}
    return {h["_id"] for h in chiama("POST", f"/{indice}/_search", corpo)["hits"]["hits"]}


def cerca_kx(indice, parola):
    # La richiesta di KoskidexClient::searchIds di Documentale.
    q = urllib.parse.urlencode({"q": parola, "limit": 10000, "ids_only": "true", "fuzziness": "AUTO"})
    r = json.load(urllib.request.urlopen(f"{KX}/indexes/{indice}/search?{q}"))
    return {str(h["id"]) for h in r.get("hits") or []}


def carica(p):
    r = json.load(open(p))
    assert r["config"].get("modifiche_non_committate") == "false", f"{p}: codice non committato"
    return r


if not os.environ.get("TESI_RISULTATI"):
    print("!!! RISULTATO NON ARCHIVIATO: TESI_RISULTATI non è impostata.")

inizio = time.perf_counter_ns()

# Le impostazioni dei quattro indici, rilette da Koskidex.
impostazioni = {}
for k, i in INDICI_KX.items():
    s = json.load(urllib.request.urlopen(f"{KX}/indexes/{i}/settings"))
    s = s.get("settings", s)
    impostazioni[k] = {"elision_articles": len(s.get("elision_articles") or []),
                       "all_terms_in_one_field": s.get("all_terms_in_one_field"),
                       "disable_on_numbers": s["typo_tolerance"].get("disable_on_numbers"),
                       "tokenizer": s.get("tokenizer"), "retrieval_mode": s.get("retrieval_mode"),
                       "documenti": json.load(urllib.request.urlopen(f"{KX}/indexes/{i}"))["docs"]}
assert impostazioni["elis0"]["elision_articles"] == 0 and impostazioni["elis1"]["elision_articles"] == 21
assert impostazioni["lib0"]["elision_articles"] == 0 and impostazioni["lib1"]["elision_articles"] == 21
assert impostazioni["elis0"]["all_terms_in_one_field"] and not impostazioni["lib0"]["all_terms_in_one_field"]

# 1. Gli id, poi i termini veri di ogni atto.
res = chiama("POST", f"/{INDICE}/_search?scroll=2m", {"size": 5000, "_source": False, "query": {"match_all": {}}})
ids, sid = [], res["_scroll_id"]
while res["hits"]["hits"]:
    ids += [h["_id"] for h in res["hits"]["hits"]]
    res = chiama("POST", "/_search/scroll", {"scroll": "2m", "scroll_id": sid})
chiama("DELETE", "/_search/scroll", {"scroll_id": sid})

termini = {}
for i in range(0, len(ids), 500):
    blocco = chiama("POST", f"/{INDICE}/_mtermvectors",
                    {"ids": ids[i:i + 500], "parameters": {"fields": CAMPI, "positions": False, "offsets": False,
                                                          "term_statistics": False, "field_statistics": False}})
    for d in blocco["docs"]:
        termini[d["_id"]] = set().union(*(set(v["terms"]) for v in d.get("term_vectors", {}).values()))
assert len(termini) == len(ids), "mancano i termini di qualche atto"
assert all(v["documenti"] == len(ids) for v in impostazioni.values()), "un indice Koskidex ha un altro numero di atti"

a_rischio = collections.defaultdict(set)
prefissi_di = collections.defaultdict(set)  # (atto, parola) -> prefissi con cui la parola vi compare elisa
presente = collections.Counter()
for doc, ts in termini.items():
    for t in ts:
        m = eliso(t)
        if not m:
            continue
        p, w = m
        if len(w) >= MIN_LETTERE and w not in ts:
            a_rischio[w].add(doc)
            prefissi_di[(doc, w)].add(p)
for w in a_rischio:
    presente[w] = sum(1 for ts in termini.values() if w in ts)

# 2. Quattro motori per ogni parola.
mapping = chiama("GET", f"/{INDICE}/_mapping")[INDICE]["mappings"]
try:
    chiama("DELETE", f"/{CONTROLLO}")
except urllib.error.HTTPError:
    pass
chiama("PUT", f"/{CONTROLLO}", {
    "settings": {"number_of_shards": 1, "number_of_replicas": 0, "analysis": {
        "filter": {"elisione_it": {"type": "elision", "articles_case": True, "articles": ARTICOLI}},
        "analyzer": {"default": {"type": "custom", "tokenizer": "standard", "filter": ["elisione_it", "lowercase"]}}}},
    "mappings": mapping})
insiemi = {}
ms = collections.defaultdict(list)
try:
    chiama("POST", "/_reindex?refresh=true&wait_for_completion=true", {"source": {"index": INDICE}, "dest": {"index": CONTROLLO}})
    assert chiama("GET", f"/{CONTROLLO}/_count")["count"] == len(ids)
    prova = chiama("POST", f"/{CONTROLLO}/_analyze", {"field": "summary", "text": "dell'illuminazione"})
    assert [t["token"] for t in prova["tokens"]] == ["illuminazione"], prova
    motori = {"produzione": lambda w: cerca_es(INDICE, w), "controllo": lambda w: cerca_es(CONTROLLO, w),
              "elis0": lambda w: cerca_kx(INDICI_KX["elis0"], w), "elis1": lambda w: cerca_kx(INDICI_KX["elis1"], w)}
    for w in sorted(a_rischio):
        insiemi[w] = {}
        for nome, f in motori.items():
            t0 = time.perf_counter_ns()
            insiemi[w][nome] = f(w)
            ms[nome].append((time.perf_counter_ns() - t0) / 1e6)
finally:
    chiama("DELETE", f"/{CONTROLLO}")

parole = sorted(a_rischio)
coppie = {(d, w) for w in parole for d in a_rischio[w]}


def perse(motore):
    return {(d, w) for (d, w) in coppie if d not in insiemi[w][motore]}


def in_piu(motore, rispetto):
    return sum(len(insiemi[w][motore] - insiemi[w][rispetto] - a_rischio[w]) for w in parole)


def diverse(a, b):
    return [w for w in parole if insiemi[w][a] != insiemi[w][b]]


def elencabile(w):
    return presente[w] + len(a_rischio[w]) >= MIN_ATTI_PAROLA


perse_prod, perse_ctrl, perse_k0, perse_k1 = perse("produzione"), perse("controllo"), perse("elis0"), perse("elis1")
rec_ctrl = perse_prod - perse_ctrl
rec_k1 = perse_k0 - perse_k1


def prefissi_residui(residue):
    c = collections.Counter()
    for coppia in residue:
        for p in prefissi_di[coppia]:
            c[(p, p.lower() in ARTICOLI)] += 1
    return [{"prefisso": p, "coppie": n, "nell_elenco": dentro} for (p, dentro), n in c.most_common()]


def confronto_parole(a, b):
    dw = diverse(a, b)
    return {"parole_con_lo_stesso_insieme": len(parole) - len(dw), "parole_diverse": len(dw),
            "documenti_solo_" + a: sum(len(insiemi[w][a] - insiemi[w][b]) for w in dw),
            "documenti_solo_" + b: sum(len(insiemi[w][b] - insiemi[w][a]) for w in dw),
            # Aggiunti dopo la prova di sviluppo, vedi il README: le due cause
            # delle differenze. Col tetto entrambi restituiscono 10.000 atti di
            # più di 10.000 trovati, e l'ordine decide quali.
            "parole_col_tetto_dei_10000": sum(len(insiemi[w][a]) == len(insiemi[w][b]) == 10000 for w in dw),
            "parole_dove_" + a + "_trova_solo_di_piu": sum(insiemi[w][b] < insiemi[w][a] for w in dw),
            "parole_dove_" + b + "_trova_solo_di_piu": sum(insiemi[w][a] < insiemi[w][b] for w in dw),
            "parole_diverse_elencabili": [
                {"parola": w, "solo_" + a: len(insiemi[w][a] - insiemi[w][b]),
                 "solo_" + b: len(insiemi[w][b] - insiemi[w][a])} for w in dw if elencabile(w)]}


# 3. Gli effetti sulle altre query.
conf0, conf1 = carica(conf0_p), carica(conf1_p)
assert conf0["config"]["indice"] == INDICI_KX["elis0"] and conf1["config"]["indice"] == INDICI_KX["elis1"]
confronto_24 = []
for a, b in zip(conf0["query"], conf1["query"]):
    assert a["query"] == b["query"]
    s0, s1 = set(a["ids"]), set(b["ids"])
    confronto_24.append({"query": a["query"], "trovati_elis0": len(s0), "trovati_elis1": len(s1),
                         "persi": len(s0 - s1), "guadagnati": len(s1 - s0), "top10_uguali": a["ids"][:10] == b["ids"][:10]})

ki0, ki1 = carica(ki0_p), carica(ki1_p)
assert ki0["config"]["indice"] == INDICI_KX["lib0"] and ki1["config"]["indice"] == INDICI_KX["lib1"]
testi = [r.strip() for r in open(ki_queries_p, encoding="utf8") if r.strip()]
assert [q["query"] for q in ki0["query"]] == testi == [q["query"] for q in ki1["query"]]
con_apostrofo = [("'" in t or "’" in t) for t in testi]
top10 = [a["ids"][:10] == b["ids"][:10] for a, b in zip(ki0["query"], ki1["query"])]

val0, val1 = carica(val0_p), carica(val1_p)


def metriche(v):
    pq = v["per_query"]
    return {"valutazione": os.path.basename(v["_percorso"]), "mrr@10": round(v["mean_mrr@10"], 4),
            "atto_primo": sum(q["mrr@10"] == 1 for q in pq), "atto_entro_10": sum(q["mrr@10"] > 0 for q in pq),
            "a_vuoto": v["zero_results"], "ms_mediana": round(statistics.median(v["timings"]["per_query_ms"].values()), 2)}


val0["_percorso"], val1["_percorso"] = val0_p, val1_p
known_item = {"lib0": metriche(val0), "lib1": metriche(val1),
              "differenza_mrr@10": round(val1["mean_mrr@10"] - val0["mean_mrr@10"], 4),
              "query_senza_apostrofo": con_apostrofo.count(False),
              "query_senza_apostrofo_top10_uguali": sum(t for t, a in zip(top10, con_apostrofo) if not a),
              "query_con_apostrofo": con_apostrofo.count(True),
              "query_con_apostrofo_top10_uguali": sum(t for t, a in zip(top10, con_apostrofo) if a)}

esito = {
    "atti": len(ids),
    "parole": len(parole),
    "coppie_a_rischio": len(coppie),
    "perse": {"produzione": len(perse_prod), "controllo": len(perse_ctrl), "elis0": len(perse_k0), "elis1": len(perse_k1)},
    "perse_da_elis0_non_da_produzione": len(perse_k0 - perse_prod),
    "perse_da_produzione_non_da_elis0": len(perse_prod - perse_k0),
    "recuperate": {"controllo_su_produzione": len(rec_ctrl), "quota_controllo": round(len(rec_ctrl) / len(perse_prod), 4),
                   "elis1_su_elis0": len(rec_k1), "quota_elis1": round(len(rec_k1) / len(perse_k0), 4)},
    "residue": {"elis1": len(perse_k0 & perse_k1), "controllo": len(perse_prod & perse_ctrl),
                "in_comune": len(perse_k0 & perse_k1 & perse_prod & perse_ctrl),
                "prefissi_residui_elis1": prefissi_residui(perse_k0 & perse_k1),
                "prefissi_residui_controllo": prefissi_residui(perse_prod & perse_ctrl)},
    "elis0_contro_produzione": confronto_parole("elis0", "produzione"),
    "elis1_contro_controllo": confronto_parole("elis1", "controllo"),
    "in_piu": {"controllo": in_piu("controllo", "produzione"), "elis1": in_piu("elis1", "elis0")},
    "atti_persi": {k: len({d for d, _ in v}) for k, v in
                   (("produzione", perse_prod), ("controllo", perse_ctrl), ("elis0", perse_k0), ("elis1", perse_k1))},
    "confronto_24": confronto_24,
    "known_item": known_item,
    "id_atti_persi_elis1": sorted({d for d, _ in perse_k1}, key=int),
}

print(f"parole {len(parole)}, coppie a rischio {len(coppie)}")
print("perse:", esito["perse"])
print(f"elis0 vs produzione: stesse {esito['elis0_contro_produzione']['parole_con_lo_stesso_insieme']}/{len(parole)}, "
      f"perse solo elis0 {esito['perse_da_elis0_non_da_produzione']}, solo produzione {esito['perse_da_produzione_non_da_elis0']}")
print("recuperate:", esito["recuperate"])
print(f"elis1 vs controllo: stesse {esito['elis1_contro_controllo']['parole_con_lo_stesso_insieme']}/{len(parole)}")
print("in più:", esito["in_piu"], "residue:", {k: v for k, v in esito["residue"].items() if not k.startswith("prefissi")})
print("confronto 24: persi", sum(q["persi"] for q in confronto_24), "guadagnati", sum(q["guadagnati"] for q in confronto_24),
      "query con guadagni", sum(q["guadagnati"] > 0 for q in confronto_24))
print("known-item:", json.dumps(known_item, ensure_ascii=False))

ora = datetime.datetime.now(datetime.timezone.utc)
esito = {"ran_at": ora.strftime("%Y-%m-%dT%H:%M:%SZ"),
         "config": {"elasticsearch_versione": chiama("GET", "/")["version"]["number"],
                    "koskidex_versione": json.load(urllib.request.urlopen(f"{KX}/health"))["version"],
                    "indice": INDICE, "indici_koskidex": INDICI_KX, "impostazioni_koskidex": impostazioni,
                    "campi": CAMPI, "articoli_del_filtro": ARTICOLI,
                    "min_lettere_parola": MIN_LETTERE, "min_atti_per_elencare_una_parola": MIN_ATTI_PAROLA,
                    "query_elasticsearch": "multi_match best_fields, fuzziness AUTO, prefix_length 1, operator and, "
                                           "tie_breaker 0.3, pesi di ElasticsearchService::fuzzySearch, size 10000",
                    "query_koskidex": "GET /indexes/{indice}/search q, limit 10000, ids_only true, fuzziness AUTO "
                                      "(KoskidexClient::searchIds)",
                    "rapporti": [os.path.basename(p) for p in (conf0_p, conf1_p, ki0_p, ki1_p, val0_p, val1_p)],
                    "commit_documentale_rapporti": sorted({carica(p)["config"]["commit"][:7] for p in (conf0_p, conf1_p, ki0_p, ki1_p)}),
                    "commit": git("-C", QUI, "rev-parse", "--short", "HEAD"),
                    "modifiche_non_committate": "true" if git("-C", QUI, "status", "--porcelain", "--", QUI) else "false"},
         **esito,
         "timings": {m: {"ms_mediana": round(statistics.median(v), 3), "ms_totale": round(sum(v), 1)} for m, v in ms.items()}
         | {"totale_ms": round((time.perf_counter_ns() - inizio) / 1e6, 1)}}

if not os.environ.get("TESI_RISULTATI"):
    sys.exit("!!! RISULTATO NON ARCHIVIATO: TESI_RISULTATI non è impostata.")
d = os.path.join(os.environ["TESI_RISULTATI"], "esperimenti", "2026-09-25_elisioni-koskidex")
o = ora.strftime("%Y-%m-%dT%H%M%SZ"); p = os.path.join(d, f"{o}_esito.json"); n = 2
while os.path.exists(p):
    p = os.path.join(d, f"{o}-{n}_esito.json"); n += 1
open(p, "x").write(json.dumps(esito, indent=2, ensure_ascii=False))
print("archiviato in", p)
