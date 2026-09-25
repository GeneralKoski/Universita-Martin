#!/usr/bin/env python3
"""Quanti atti la ricerca di Documentale perde per le elisioni.

Legge i termini che Elasticsearch ha indicizzato, trova le parole che in un
atto compaiono solo elise (dell'illuminazione, mai illuminazione), cerca
ciascuna con la query di produzione e conta gli atti che non tornano. Poi
ripete le stesse query su un indice di controllo con il filtro elision degli
articoli italiani, per confermare la causa. Metodo e ipotesi nel README.

    TESI_RISULTATI=... conta.py
"""
import collections, datetime, json, os, re, subprocess, sys, time, urllib.error, urllib.request

ES = "http://localhost:9201"
INDICE = "search-documents-local"
CONTROLLO = "elisioni-controllo"
CAMPI = ["name", "tags", "summary", "subjects", "notes", "additional_data"]
PESI = ["name^5", "tags^4", "summary^3", "subjects^3", "notes^2", "additional_data^1"]
# Gli articoli del filtro italian_elision dell'analizzatore italian di Elasticsearch.
ARTICOLI = ["c", "l", "all", "dall", "dell", "nell", "sull", "coll", "pell", "gl", "agl",
            "dagl", "degl", "negl", "sugl", "un", "m", "t", "s", "v", "d"]
ELISO = re.compile(r"^([^\W\d_]+)['’]([^\W\d_]+)$")
MIN_LETTERE = 3
MIN_ATTI_PAROLA = 20
QUI = os.path.dirname(os.path.abspath(__file__))


def chiama(metodo, percorso, corpo=None):
    dati = json.dumps(corpo).encode() if corpo is not None else None
    r = urllib.request.Request(ES + percorso, data=dati, method=metodo,
                               headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(r))


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout.strip()


def cerca(indice, parola):
    corpo = {"query": {"multi_match": {"query": parola, "type": "best_fields", "fuzziness": "AUTO",
                                       "prefix_length": 1, "operator": "and", "tie_breaker": 0.3,
                                       "fields": PESI}},
             "size": 10000, "_source": False}
    return {h["_id"] for h in chiama("POST", f"/{indice}/_search", corpo)["hits"]["hits"]}


if not os.environ.get("TESI_RISULTATI"):
    print("!!! RISULTATO NON ARCHIVIATO: TESI_RISULTATI non è impostata.")

inizio = time.perf_counter_ns()

# 1. Gli id, poi i termini veri di ogni atto.
res = chiama("POST", f"/{INDICE}/_search?scroll=2m", {"size": 5000, "_source": False, "query": {"match_all": {}}})
ids, sid = [], res["_scroll_id"]
while res["hits"]["hits"]:
    ids += [h["_id"] for h in res["hits"]["hits"]]
    res = chiama("POST", "/_search/scroll", {"scroll": "2m", "scroll_id": sid})
chiama("DELETE", "/_search/scroll", {"scroll_id": sid})

termini, per_campo = {}, {}
for i in range(0, len(ids), 500):
    blocco = chiama("POST", f"/{INDICE}/_mtermvectors",
                    {"ids": ids[i:i + 500], "parameters": {"fields": CAMPI, "positions": False, "offsets": False,
                                                          "term_statistics": False, "field_statistics": False}})
    for d in blocco["docs"]:
        per_campo[d["_id"]] = {c: set(v["terms"]) for c, v in d.get("term_vectors", {}).items()}
        termini[d["_id"]] = set().union(*per_campo[d["_id"]].values())
assert len(termini) == len(ids), "mancano i termini di qualche atto"
ms_termini = (time.perf_counter_ns() - inizio) / 1e6

# 2. Da quale fonte viene ogni atto: il percorso nel database dell'app dice il
# comune, e Crispiano è l'unico comune che non viene dal Friuli Venezia Giulia.
righe = subprocess.run(["docker", "exec", "doc-tesi-mysql", "mysql", "-uroot", "-proot", "-N",
                        "--default-character-set=utf8mb4", "albo", "-e",
                        "select document_id, path from document_versions"],
                       capture_output=True, text=True, check=True).stdout.splitlines()
fonte = {r.split("\t")[0]: "crispiano" if r.split("\t")[1].split("/")[2] == "comune-di-crispiano" else "fvg"
         for r in righe}
assert set(ids) <= set(fonte), "atti dell'indice senza versione nel database"

# 3. Termini elisi e coppie a rischio.
prefissi = collections.Counter()
atti_con_eliso = set()
a_rischio = collections.defaultdict(set)  # parola -> atti in cui compare solo elisa
presente = collections.Counter()          # parola -> atti in cui compare a sé
# subjects è l'ente (Comune di Vito d'Asio): chi cerca un comune ne scrive il
# nome con l'apostrofo, e lo trova. Le coppie che vengono solo da lì si contano
# a parte.
fuori_ente = collections.defaultdict(set)  # parola -> atti in cui la forma elisa sta fuori da subjects
for doc, ts in termini.items():
    for t in ts:
        m = ELISO.match(t)
        if not m:
            continue
        atti_con_eliso.add(doc)
        p, w = m.group(1), m.group(2)
        prefissi[p] += 1
        if len(w) >= MIN_LETTERE and w not in ts:
            a_rischio[w].add(doc)
            if any(t in v for c, v in per_campo[doc].items() if c != "subjects"):
                fuori_ente[w].add(doc)
for w in a_rischio:
    presente[w] = sum(1 for ts in termini.values() if w in ts)

# 4. Indice di controllo: stesso mapping, più il filtro elision.
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
try:
    t0 = time.perf_counter_ns()
    chiama("POST", "/_reindex?refresh=true&wait_for_completion=true",
           {"source": {"index": INDICE}, "dest": {"index": CONTROLLO}})
    ms_reindex = (time.perf_counter_ns() - t0) / 1e6
    n_controllo = chiama("GET", f"/{CONTROLLO}/_count")["count"]
    assert n_controllo == len(ids), f"il controllo ha {n_controllo} atti invece di {len(ids)}"
    prova = chiama("POST", f"/{CONTROLLO}/_analyze", {"field": "summary", "text": "dell'illuminazione"})
    assert [t["token"] for t in prova["tokens"]] == ["illuminazione"], prova

    # 5. La query di produzione per ogni parola, sui due indici.
    persi, recuperati = collections.defaultdict(set), collections.defaultdict(set)
    in_piu = collections.Counter()  # parola -> atti che solo il controllo trova, fuori dalle coppie a rischio
    trovati_produzione = {}
    ms_query = []
    for w in sorted(a_rischio):
        t0 = time.perf_counter_ns()
        prod = cerca(INDICE, w)
        ms_query.append((time.perf_counter_ns() - t0) / 1e6)
        ctrl = cerca(CONTROLLO, w)
        trovati_produzione[w] = len(prod)
        for doc in a_rischio[w] - prod:
            persi[w].add(doc)
            if doc in ctrl:
                recuperati[w].add(doc)
        in_piu[w] = len(ctrl - prod - a_rischio[w])
finally:
    chiama("DELETE", f"/{CONTROLLO}")

# 6. Le cifre.
coppie_rischio = sum(len(s) for s in a_rischio.values())
coppie_perse = sum(len(s) for s in persi.values())
coppie_recuperate = sum(len(s) for s in recuperati.values())
atti_persi = set().union(*persi.values()) if persi else set()
atti_rischio = set().union(*a_rischio.values()) if a_rischio else set()
coppie_perse_fuori_ente = sum(len(persi[w] & fuori_ente[w]) for w in persi)
atti_persi_fuori_ente = set().union(*(persi[w] & fuori_ente[w] for w in persi)) if persi else set()


def per_fonte(insieme):
    c = collections.Counter(fonte[d] for d in insieme)
    return {f: c.get(f, 0) for f in sorted(set(fonte[d] for d in ids))}


parole = []
for w in a_rischio:
    atti_w = presente[w] + len(a_rischio[w])
    if atti_w >= MIN_ATTI_PAROLA:
        parole.append({"parola": w, "atti_con_la_parola": atti_w, "solo_elisa": len(a_rischio[w]),
                       "persi": len(persi[w]), "persi_fuori_dal_nome_dell_ente": len(persi[w] & fuori_ente[w]),
                       "recuperati_dal_filtro": len(recuperati[w]), "in_piu_nel_controllo": in_piu[w],
                       "trovati_in_produzione": trovati_produzione[w],
                       "quota_persa": round(len(persi[w]) / atti_w, 4)})
parole.sort(key=lambda r: (-r["persi"], r["parola"]))

esito = {
    "atti": len(ids),
    "atti_per_fonte": per_fonte(ids),
    "atti_con_termine_eliso": len(atti_con_eliso),
    "atti_con_termine_eliso_per_fonte": per_fonte(atti_con_eliso),
    "parole_a_rischio": len(a_rischio),
    "coppie_a_rischio": coppie_rischio,
    "coppie_salvate_dalla_ricerca": coppie_rischio - coppie_perse,
    "coppie_perse": coppie_perse,
    "coppie_perse_recuperate_dal_filtro": coppie_recuperate,
    "atti_a_rischio": len(atti_rischio),
    "atti_persi": len(atti_persi),
    "atti_persi_per_fonte": per_fonte(atti_persi),
    "coppie_perse_fuori_dal_nome_dell_ente": coppie_perse_fuori_ente,
    "atti_persi_fuori_dal_nome_dell_ente": len(atti_persi_fuori_ente),
    "atti_persi_fuori_dal_nome_dell_ente_per_fonte": per_fonte(atti_persi_fuori_ente),
    # Atti che il controllo trova per una parola senza che la parola vi compaia
    # elisa: vi compare elisa una forma vicina, raggiunta dai refusi.
    "coppie_in_piu_nel_controllo_fuori_dalle_coppie_a_rischio": sum(in_piu.values()),
    # I prefissi rari sono per lo più parole attaccate per uno spazio mancante.
    "prefissi": [{"prefisso": p, "termini": n, "nell_elenco_del_filtro": p in ARTICOLI}
                 for p, n in prefissi.most_common() if n >= 5],
    "prefissi_rari": {"prefissi": sum(1 for n in prefissi.values() if n < 5),
                      "termini": sum(n for n in prefissi.values() if n < 5)},
    "parole_con_almeno_20_atti": parole,
    "id_atti_persi": sorted(atti_persi, key=int),
}

print(f"atti con un termine eliso: {len(atti_con_eliso)}/{len(ids)} ({len(atti_con_eliso) / len(ids):.1%})")
print(f"coppie a rischio {coppie_rischio}, salvate dalla ricerca {coppie_rischio - coppie_perse} "
      f"({(coppie_rischio - coppie_perse) / coppie_rischio:.1%}), perse {coppie_perse}")
print(f"perse recuperate dal filtro elision: {coppie_recuperate}/{coppie_perse} ({coppie_recuperate / coppie_perse:.1%})")
print(f"atti con almeno una coppia persa: {len(atti_persi)}/{len(ids)} ({len(atti_persi) / len(ids):.1%}) "
      f"- per fonte {esito['atti_persi_per_fonte']}")
print(f"escluse le coppie dal solo nome dell'ente: coppie perse {coppie_perse_fuori_ente}, atti "
      f"{len(atti_persi_fuori_ente)} ({len(atti_persi_fuori_ente) / len(ids):.1%}) - per fonte "
      f"{esito['atti_persi_fuori_dal_nome_dell_ente_per_fonte']}")
print(f"atti con un termine eliso per fonte {esito['atti_con_termine_eliso_per_fonte']} su {esito['atti_per_fonte']}")
print("prime parole:", ", ".join(f"{r['parola']} {r['persi']}" for r in parole[:20]))

ora = datetime.datetime.now(datetime.timezone.utc)
esito = {"ran_at": ora.strftime("%Y-%m-%dT%H:%M:%SZ"),
         "config": {"elasticsearch_versione": chiama("GET", "/")["version"]["number"],
                    "indice": INDICE, "campi": CAMPI, "articoli_del_filtro": ARTICOLI,
                    "min_lettere_parola": MIN_LETTERE, "min_atti_per_elencare_una_parola": MIN_ATTI_PAROLA,
                    "query": "multi_match best_fields, fuzziness AUTO, prefix_length 1, operator and, tie_breaker 0.3, "
                             "pesi di ElasticsearchService::fuzzySearch, size 10000",
                    "commit": git("-C", QUI, "rev-parse", "--short", "HEAD"),
                    "modifiche_non_committate": "true" if git("-C", QUI, "status", "--porcelain", "--", QUI) else "false",
                    "commit_documentale": git("-C", os.path.expanduser("~/Desktop/Dieffetech/Documentale"),
                                              "rev-parse", "--short", "HEAD")},
         **esito,
         "timings": {"termini_ms": round(ms_termini, 1), "reindex_controllo_ms": round(ms_reindex, 1),
                     "query_produzione_ms_totale": round(sum(ms_query), 1),
                     "query_produzione_ms_mediana": round(sorted(ms_query)[len(ms_query) // 2], 3),
                     "totale_ms": round((time.perf_counter_ns() - inizio) / 1e6, 1)}}

if not os.environ.get("TESI_RISULTATI"):
    sys.exit("!!! RISULTATO NON ARCHIVIATO: TESI_RISULTATI non è impostata.")
d = os.path.join(os.environ["TESI_RISULTATI"], "esperimenti", "2026-09-25_elisioni")
o = ora.strftime("%Y-%m-%dT%H%M%SZ"); p = os.path.join(d, f"{o}_esito.json"); n = 2
while os.path.exists(p):
    p = os.path.join(d, f"{o}-{n}_esito.json"); n += 1
open(p, "x").write(json.dumps(esito, indent=2, ensure_ascii=False))
print("archiviato in", p)
