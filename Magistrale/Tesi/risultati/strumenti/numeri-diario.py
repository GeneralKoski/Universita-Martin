#!/usr/bin/env python3
"""I numeri che la tesi prendeva dal diario di Koskidex o da SOURCE.md, senza un
file in risultati/: le lunghezze delle query in 5.1, i candidati persi togliendo
le stopword in 5.4, le parole del vocabolario di prova dello stemmer in 5.6, la
prova di AlboPOP in 4.3. I primi due si ricalcolano dalle valutazioni archiviate
in koskidex-beir/, il terzo dal file di test di Koskidex; la prova di AlboPOP
(23/09/2026) non si ripete, e se ne copia il resoconto con commit e impronta.
Scrive risultati/corpus/<ora>_numeri-diario.json.

    numeri-diario.py
"""
import datetime, hashlib, json, os, statistics, subprocess, sys

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
                    "con_risultati": {"query": len(con), "parole_media": round(statistics.mean(parole(con)), 2)},
                    "a_vuoto": {"query": len(vuote), "parole_media": round(statistics.mean(parole(vuote)), 2)}}

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

ora = datetime.datetime.now(datetime.timezone.utc)
esito = {"ran_at": ora.strftime("%Y-%m-%dT%H:%M:%SZ"),
         "config": {"commit": git(QUI, "rev-parse", "--short", "HEAD").strip(),
                    "modifiche_non_committate": "true" if git(QUI, "status", "--porcelain", "--", os.path.abspath(__file__)).strip() else "false",
                    "koskidex": kx},
         "lunghezza_query": lunghezze, "stopword_candidati": stopword, "vocabolario_stemmer": vocabolario,
         "albopop": albopop}
print(json.dumps(esito, indent=1, ensure_ascii=False))
if not os.environ.get("TESI_RISULTATI"):
    sys.exit("!!! RISULTATO NON ARCHIVIATO: TESI_RISULTATI non è impostata.")
d = os.path.join(os.environ["TESI_RISULTATI"], "corpus"); os.makedirs(d, exist_ok=True)
o = ora.strftime("%Y-%m-%dT%H%M%SZ"); p = os.path.join(d, f"{o}_numeri-diario.json"); k = 2
while os.path.exists(p):
    p = os.path.join(d, f"{o}-{k}_numeri-diario.json"); k += 1
open(p, "x").write(json.dumps(esito, indent=2, ensure_ascii=False))
print("archiviato in", p)
