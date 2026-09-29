#!/usr/bin/env python3
"""I numeri che la tesi prendeva dal diario di Koskidex o da SOURCE.md, o che
nessuno strumento scriveva, senza un file in risultati/: le lunghezze delle
query in 4.2 e 5.1 (media e mediana), i gradi di rilevanza dei qrels in 4.2, le
query di NFCorpus ancora vuote in 5.1, i candidati persi togliendo le stopword e
le occorrenze di "of" in 5.4, le parole del vocabolario di prova dello stemmer in
5.6, la prova di AlboPOP in 4.3, gli atti distinti del Friuli Venezia Giulia e
la scheda più lunga (3.2, 4.3, 7.1). I conteggi si rifanno dalle valutazioni
archiviate in koskidex-beir/, dalle collezioni e dal corpus in Koskidex; la
prova di AlboPOP (23/09/2026) non si ripete, e se ne copia il resoconto con
commit e impronta. Allo stesso modo si copiano, parola per parola, le voci di
eval/DIARIO.md da cui la tesi prende previsioni e fatti che stanno solo lì
(le soglie dei difetti 0 e 1, delle stopword e della frequenza mescolata, il
campione delle query vuote, i 14 documenti di prova, i buchi F1-F7): il diario
è committato prima delle misure, ed è lui la prova. Scrive
risultati/corpus/<ora>_numeri-diario.json.

    numeri-diario.py
"""
import collections, datetime, hashlib, json, os, re, statistics, subprocess, sys

QUI = os.path.dirname(os.path.abspath(__file__))
KX = os.path.expanduser("~/Desktop/Progetti-personali/Koskidex")
BEIR = os.path.join(QUI, "..", "koskidex-beir")
git = lambda d, *x: subprocess.run(["git", "-C", d, *x], capture_output=True, text=True, check=True).stdout
kx = git(KX, "rev-parse", "--short", "HEAD").strip()


def run(nome):
    p = os.path.join(BEIR, nome)
    d = json.load(open(p))
    assert d["config"]["modifiche_non_committate"] in ("false", False), p
    return d, {"file": f"koskidex-beir/{nome}", "sha256": hashlib.sha256(open(p, "rb").read()).hexdigest(),
               "commit": d["config"]["commit"][:7], "recupero": d["config"]["recupero"],
               "punteggio": d["config"]["punteggio"], "analisi": d["config"]["analisi"]}


# 5.1: parole separate da spazi, sulla configurazione di partenza (tutti i termini obbligatori).
lunghezze = {}
for c, nome in [("scifact", "2026-09-23T155407Z_scifact-legacy.json"), ("nfcorpus", "2026-09-23T155526Z_nfcorpus-legacy.json")]:
    d, prov = run(nome)
    testo = {q["_id"]: q["text"] for q in map(json.loads, open(os.path.join(KX, "eval", "corpora", "c1-public", c, "queries.jsonl")))}
    parole = lambda qs: [len(testo[q["query_id"]].split()) for q in qs]
    con = [q for q in d["per_query"] if q["retrieved"] > 0]
    vuote = [q for q in d["per_query"] if q["retrieved"] == 0]
    lunghezze[c] = {"valutazione": prov, "query": len(d["per_query"]),
                    "parole_media": round(statistics.mean(parole(d["per_query"])), 2),
                    "parole_mediana": statistics.median(parole(d["per_query"])),
                    "con_risultati": {"query": len(con), "parole_media": round(statistics.mean(parole(con)), 2)},
                    "a_vuoto": {"query": len(vuote), "parole_media": round(statistics.mean(parole(vuote)), 2)}}

# 4.2: i gradi di rilevanza nei qrels di test.
gradi = {c: dict(sorted(collections.Counter(r.split("\t")[2].strip() for r in
                                           open(os.path.join(KX, "eval", "corpora", "c1-public", c, "qrels", "test.tsv")).read().splitlines()[1:]).items()))
         for c in ("scifact", "nfcorpus")}

# 5.1: le query di NFCorpus ancora vuote col recupero disgiuntivo, e quante ne salva lo stemmer.
(qa, pqa), (qs, pqs) = run("2026-09-23T155531Z_nfcorpus-any.json"), run("2026-09-23T155542Z_nfcorpus-bm25-stemmer.json")
testo_nf = {q["_id"]: q["text"] for q in map(json.loads, open(os.path.join(KX, "eval", "corpora", "c1-public", "nfcorpus", "queries.jsonl")))}
vuote_any = [q["query_id"] for q in qa["per_query"] if q["candidates"] == 0]
vuote_stem = {q["query_id"] for q in qs["per_query"] if q["candidates"] == 0}
residuo = {"disgiuntivo": pqa, "con_stemmer": pqs, "vuote": len(vuote_any),
           "parole_per_query": dict(sorted(collections.Counter(len(testo_nf[q].split()) for q in vuote_any).items())),
           "salvate_dallo_stemmer": sorted(q for q in vuote_any if q not in vuote_stem)}

# 5.4: SciFact, BM25 disgiuntivo, senza e con le stopword inglesi.
(a, pa), (b, pb) = run("2026-09-23T155448Z_scifact-bm25.json"), run("2026-09-23T155503Z_scifact-bm25-stopwords.json")
A, B = {q["query_id"]: q for q in a["per_query"]}, {q["query_id"]: q for q in b["per_query"]}
taglio = {k: A[k]["candidates"] - B[k]["candidates"] for k in A}
mediana = statistics.median(taglio.values())
delta = lambda ks: round(statistics.mean(B[k]["ndcg@10"] - A[k]["ndcg@10"] for k in ks), 4)
sopra = [k for k in A if taglio[k] > mediana]
sotto = [k for k in A if taglio[k] <= mediana]
nessuno = [k for k in A if taglio[k] == 0]
stopword = {"senza_stopword": pa, "con_stopword": pb,
            "candidati_medi": {"prima": round(statistics.mean(q["candidates"] for q in A.values())),
                               "dopo": round(statistics.mean(q["candidates"] for q in B.values()))},
            "delta_ndcg@10": {"taglio_sopra_la_mediana": {"query": len(sopra), "media": delta(sopra)},
                              "taglio_non_sopra_la_mediana": {"query": len(sotto), "media": delta(sotto)},
                              "nessun_candidato_perso": {"query": len(nessuno), "media": delta(nessuno)}}}

# 5.4: "of" nelle 300 query di test di SciFact, parole in minuscolo separate da ciò che non è lettera o cifra.
testo_sf = {q["_id"]: q["text"] for q in map(json.loads, open(os.path.join(KX, "eval", "corpora", "c1-public", "scifact", "queries.jsonl")))}
parole_sf = [re.findall(r"\w+", testo_sf[k].lower()) for k in A]
of = {"query": len(parole_sf), "query_con_of": sum("of" in p for p in parole_sf), "occorrenze": sum(p.count("of") for p in parole_sf)}

# 5.6: il vocabolario con cui Lucene prova ItalianLightStemmer, una parola per riga.
voc = "internal/engine/testdata/itlight.txt"
vocabolario = {"file": voc, "commit": kx, "righe": len(git(KX, "show", f"HEAD:{voc}").splitlines())}

# 4.3: il resoconto della prova, dal paragrafo di AlboPOP a quello su dati.gov.it escluso.
src = "eval/corpora/c3-albo/SOURCE.md"
testo = git(KX, "show", f"HEAD:{src}")
inizio, fine = testo.index("**AlboPOP**"), testo.index("Su **dati.gov.it**")
albopop = {"file": src, "commit": kx, "sha256": hashlib.sha256(testo.encode()).hexdigest(),
           "commit_del_file": git(KX, "log", "-1", "--format=%h %ad", "--date=short", "--", src).strip(),
           "resoconto": testo[inizio:fine].strip()}

# 3.2, 4.3: gli atti del Friuli Venezia Giulia (righe e id distinti) e quanti entrano nel corpus indicizzato.
# 7.1: la scheda più lunga, titolo e testo come li indicizza la valutazione piatta.
ALBO = os.path.join(KX, "eval", "corpora", "c3-albo")
fv = [json.loads(r)["id"] for r in open(os.path.join(ALBO, "fvg", "atti.jsonl"), encoding="utf8")]
schede = [json.loads(r) for r in open(os.path.join(ALBO, "beir-metadata", "corpus.jsonl"), encoding="utf8")]
lung = lambda ds: max(len(d["title"]) + 1 + len(d["text"]) for d in ds)
cr = [d for d in schede if d["_id"] <= "doc-0563"]
albo = {"corpus": "eval/corpora/c3-albo/beir-metadata/corpus.jsonl",
        "sha256": hashlib.sha256(open(os.path.join(ALBO, "beir-metadata", "corpus.jsonl"), "rb").read()).hexdigest(),
        "atti": len(schede), "crispiano": len(cr), "fvg": len(schede) - len(cr),
        "fvg_righe_di_atti_jsonl": len(fv), "fvg_id_distinti": len(set(fv)),
        "fvg_id_ripetuti": sum(n > 1 for n in collections.Counter(fv).values()),
        "caratteri_scheda_max": {"crispiano": lung(cr), "fvg": lung([d for d in schede if d["_id"] > "doc-0563"])}}

# Le voci del diario, dall'intestazione alla successiva.
DIARIO = "eval/DIARIO.md"
diario_testo = git(KX, "show", f"HEAD:{DIARIO}")
VOCI = ["Prima misura del baseline legacy su C1", "Recupero disgiuntivo (difetto 0)",
        "BM25 al posto del punteggio euristico (difetto 1)", "Analisi lessicale: stopword e stemmer (Task E1)",
        "BM25: le espansioni pesate con la frequenza mescolata",
        "Contro Elasticsearch sul corpus vero: il modello è lo stesso, il matching no",
        "Parte F: Koskidex completo, e gli stessi insiemi di Elasticsearch"]
intestazioni = list(re.finditer(r"^## (.+)$", diario_testo, re.M))
voci = []
for v in VOCI:
    [i] = [k for k, m in enumerate(intestazioni) if m.group(1).endswith(" - " + v)]
    fine = intestazioni[i + 1].start() if i + 1 < len(intestazioni) else len(diario_testo)
    voci.append({"voce": intestazioni[i].group(1), "testo": diario_testo[intestazioni[i].start():fine].strip()})
diario = {"file": DIARIO, "commit": kx, "sha256": hashlib.sha256(diario_testo.encode()).hexdigest(),
          "commit_del_file": git(KX, "log", "-1", "--format=%h %ad", "--date=short", "--", DIARIO).strip(), "voci": voci}

ora = datetime.datetime.now(datetime.timezone.utc)
esito = {"ran_at": ora.strftime("%Y-%m-%dT%H:%M:%SZ"),
         "config": {"commit": git(QUI, "rev-parse", "--short", "HEAD").strip(),
                    "modifiche_non_committate": "true" if git(QUI, "status", "--porcelain", "--", os.path.abspath(__file__)).strip() else "false",
                    "koskidex": kx},
         "lunghezza_query": lunghezze, "gradi_di_rilevanza": gradi, "nfcorpus_residuo": residuo,
         "stopword_candidati": stopword, "of_nelle_query": of, "vocabolario_stemmer": vocabolario,
         "albo": albo, "albopop": albopop, "diario": diario}
print(json.dumps(esito, indent=1, ensure_ascii=False))
if not os.environ.get("TESI_RISULTATI"):
    sys.exit("!!! RISULTATO NON ARCHIVIATO: TESI_RISULTATI non è impostata.")
d = os.path.join(os.environ["TESI_RISULTATI"], "corpus"); os.makedirs(d, exist_ok=True)
o = ora.strftime("%Y-%m-%dT%H%M%SZ"); p = os.path.join(d, f"{o}_numeri-diario.json"); k = 2
while os.path.exists(p):
    p = os.path.join(d, f"{o}-{k}_numeri-diario.json"); k += 1
open(p, "x").write(json.dumps(esito, indent=2, ensure_ascii=False))
print("archiviato in", p)
