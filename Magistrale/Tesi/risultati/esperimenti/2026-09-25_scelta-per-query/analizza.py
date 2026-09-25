#!/usr/bin/env python3
"""Scegliere fra A (BM25 any) e B (BM25 all) query per query: oracolo, regola
della cifra, ripiego e regressione logistica, valutati sul test a partire dalle
valutazioni di A e B. Metodo e parametri, fissati prima, nel README.

    analizza.py <koskidex> <valutazione> [...]   (A e B, train e test, tre collezioni)
"""
import collections, datetime, json, math, os, subprocess, sys, unicodedata

kx, *valutazioni = sys.argv[1:]
QUI = os.path.dirname(os.path.abspath(__file__))
TESI = os.path.join(QUI, "..", "..", "query")
FONTI = {  # collezione -> (corpus, query)
    "known-item-auto": ("eval/corpora/c3-albo/beir-metadata/corpus.jsonl", os.path.join(TESI, "known-item-auto/queries.jsonl")),
    "known-item-auto-train": ("eval/corpora/c3-albo/beir-metadata/corpus.jsonl", os.path.join(TESI, "known-item-auto-train/queries.jsonl")),
    "scifact": ("eval/corpora/c1-public/scifact/corpus.jsonl", "eval/corpora/c1-public/scifact/queries.jsonl"),
    "nfcorpus": ("eval/corpora/c1-public/nfcorpus/corpus.jsonl", "eval/corpora/c1-public/nfcorpus/queries.jsonl"),
}
FAMIGLIA = {"known-item-auto": "known-item", "known-item-auto-train": "known-item", "scifact": "scifact", "nfcorpus": "nfcorpus"}
CARATTERISTICHE = ["log_termini", "ha_cifra", "quota_cifre", "idf_medio", "idf_max", "idf_min", "quota_fuori_vocabolario", "b_vuoto"]
PASSO, ITERAZIONI, L2, SOGLIA = 0.5, 3000, 0.01, 0.5


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


statistiche = {}


def stat_corpus(percorso):
    if percorso not in statistiche:
        df, n = collections.Counter(), 0
        for riga in open(os.path.join(kx, percorso), encoding="utf8"):
            d = json.loads(riga)
            df.update(set(termini((d.get("title", "") + " " + d.get("text", "")).strip())))
            n += 1
        statistiche[percorso] = (df, n)
    return statistiche[percorso]


def idf(df, n):
    return math.log(1 + (n - df + 0.5) / (df + 0.5))


def caratteristiche(testo, df, n, b_vuoto):
    qt = termini(testo) or [""]
    massimo = idf(0, n)
    idfs = [idf(df.get(t, 0), n) / massimo for t in qt]
    cifre = [t for t in qt if any(c.isdigit() for c in t)]
    return [math.log(1 + len(qt)), float(bool(cifre)), len(cifre) / len(qt), sum(idfs) / len(idfs), max(idfs), min(idfs),
            sum(df.get(t, 0) == 0 for t in qt) / len(qt), float(b_vuoto)]


# (collezione, split, configurazione) -> valutazione
per_chiave = {}
for f in valutazioni:
    v = json.load(open(f))
    c = v["config"]
    assert c.get("modifiche_non_committate") == "false", f"{f}: codice non committato"
    assert c.get("punteggio") == "bm25" and c.get("bm25_espansioni") == "blended", f
    conf = {"any": "A", "all": "B"}[c["recupero"]]
    per_chiave[(v["collection"], c.get("split", "test"), conf)] = (f, v)
assert len(per_chiave) == 12, f"servono A e B, train e test, per tre collezioni: {sorted(per_chiave)}"

esempi = {"train": [], "test": []}
for (coll, split, conf), (f, v) in sorted(per_chiave.items()):
    if conf != "A":
        continue
    vb = per_chiave[(coll, split, "B")][1]
    corpus, query_path = FONTI[coll]
    df, n = stat_corpus(corpus)
    domande = {json.loads(r)["_id"]: json.loads(r)["text"] for r in open(os.path.join(kx, query_path), encoding="utf8")}
    qa = {q["query_id"]: q for q in v["per_query"]}
    qb = {q["query_id"]: q for q in vb["per_query"]}
    assert qa.keys() == qb.keys()
    for qid in sorted(qa):
        esempi[split].append({"collezione": FAMIGLIA[coll], "query": qid, "a": qa[qid]["ndcg@10"], "b": qb[qid]["ndcg@10"],
                              "cifra": any(ch.isdigit() for ch in domande[qid]), "b_vuoto": qb[qid]["candidates"] == 0,
                              "x": caratteristiche(domande[qid], df, n, qb[qid]["candidates"] == 0)})

# Addestramento: solo le query in cui A e B differiscono, pesate per la differenza,
# ogni collezione con peso totale 1.
addestra = [e for e in esempi["train"] if e["a"] != e["b"]]
totale = collections.Counter()
for e in addestra:
    totale[e["collezione"]] += abs(e["b"] - e["a"])
d = len(CARATTERISTICHE)
media = [sum(e["x"][j] for e in addestra) / len(addestra) for j in range(d)]
dev = [math.sqrt(sum((e["x"][j] - media[j]) ** 2 for e in addestra) / len(addestra)) or 1.0 for j in range(d)]
std = lambda x: [(x[j] - media[j]) / dev[j] for j in range(d)]
X = [std(e["x"]) for e in addestra]
Y = [1.0 if e["b"] > e["a"] else 0.0 for e in addestra]
S = [abs(e["b"] - e["a"]) / totale[e["collezione"]] for e in addestra]
somma_s = sum(S)
w, b0 = [0.0] * d, 0.0
sigma = lambda z: 1 / (1 + math.exp(-max(-30, min(30, z))))
for _ in range(ITERAZIONI):
    gw, gb = [0.0] * d, 0.0
    for x, y, s in zip(X, Y, S):
        r = s * (sigma(b0 + sum(wj * xj for wj, xj in zip(w, x))) - y)
        gb += r
        for j in range(d):
            gw[j] += r * x[j]
    w = [w[j] - PASSO * (gw[j] / somma_s + L2 * w[j]) for j in range(d)]
    b0 -= PASSO * gb / somma_s
sceglie_b = lambda e: sigma(b0 + sum(wj * xj for wj, xj in zip(w, std(e["x"])))) > SOGLIA

strategie = {
    "sempre A": lambda e: False,
    "sempre B": lambda e: True,
    "oracolo": lambda e: e["b"] > e["a"],
    "regola della cifra": lambda e: e["cifra"],
    "ripiego (B, se vuoto A)": lambda e: not e["b_vuoto"],
    "classificatore": sceglie_b,
    # Aggiunta dopo aver visto una prova non archiviata: i pesi del modello
    # dicevano "cifre, ma non se B torna vuoto". Dichiarata nel README.
    "cifra e B non vuoto (aggiunta dopo)": lambda e: e["cifra"] and not e["b_vuoto"],
}
risultati = {}
for split in ("test", "train"):
    risultati[split] = {}
    for coll in ("known-item", "scifact", "nfcorpus"):
        qs = [e for e in esempi[split] if e["collezione"] == coll]
        risultati[split][coll] = {nome: {"ndcg@10": round(sum(e["b"] if f(e) else e["a"] for e in qs) / len(qs), 4),
                                         "query_a_b": sum(f(e) for e in qs)}
                                  for nome, f in strategie.items()}
        risultati[split][coll]["query"] = len(qs)
    for nome in strategie:
        risultati[split].setdefault("media delle tre", {})[nome] = round(
            sum(risultati[split][c][nome]["ndcg@10"] for c in ("known-item", "scifact", "nfcorpus")) / 3, 4)

modello = {"caratteristiche": CARATTERISTICHE, "pesi_standardizzati": dict(zip(CARATTERISTICHE, [round(x, 4) for x in w])),
           "intercetta": round(b0, 4), "media": dict(zip(CARATTERISTICHE, [round(x, 4) for x in media])),
           "deviazione": dict(zip(CARATTERISTICHE, [round(x, 4) for x in dev])),
           "passo": PASSO, "iterazioni": ITERAZIONI, "l2": L2, "soglia": SOGLIA,
           "esempi_di_addestramento": len(addestra), "per_collezione": dict(collections.Counter(e["collezione"] for e in addestra)),
           "pari_escluse": len(esempi["train"]) - len(addestra)}
print(json.dumps(risultati["test"], indent=1, ensure_ascii=False))
print(json.dumps(modello, indent=1, ensure_ascii=False))

ora = datetime.datetime.now(datetime.timezone.utc)
git = lambda *a: subprocess.run(["git", "-C", QUI, *a], capture_output=True, text=True, check=True).stdout.strip()
esito = {"ran_at": ora.strftime("%Y-%m-%dT%H:%M:%SZ"),
         "config": {"commit": git("rev-parse", "--short", "HEAD"),
                    "modifiche_non_committate": "true" if git("status", "--porcelain", "--", "*.py") else "false",
                    "valutazioni": {f"{k[0]}/{k[1]}/{k[2]}": os.path.basename(p) for k, (p, _) in sorted(per_chiave.items())},
                    "koskidex": sorted({v["config"]["commit"][:7] for _, v in per_chiave.values()})},
         "risultati": risultati, "modello": modello,
         "scelte_sul_test": [{"collezione": e["collezione"], "query": e["query"], "classificatore": "B" if sceglie_b(e) else "A",
                              "ndcg_a": e["a"], "ndcg_b": e["b"]} for e in esempi["test"]]}
if not os.environ.get("TESI_RISULTATI"):
    sys.exit("!!! RISULTATO NON ARCHIVIATO: TESI_RISULTATI non è impostata.")
dd = os.path.join(os.environ["TESI_RISULTATI"], "esperimenti", "2026-09-25_scelta-per-query")
o = ora.strftime("%Y-%m-%dT%H%M%SZ"); p = os.path.join(dd, f"{o}_esito.json"); n = 2
while os.path.exists(p):
    p = os.path.join(dd, f"{o}-{n}_esito.json"); n += 1
open(p, "x").write(json.dumps(esito, indent=2, ensure_ascii=False))
print("archiviato in", p)
