#!/usr/bin/env python3
"""La scelta fra A e B per ogni known-item umana: sempre A, sempre B, oracolo,
la regola (B se c'è una cifra e il congiuntivo lessicale trova qualcosa) e il
classificatore congelato di 2026-09-25_scelta-ibrida, applicato con i pesi, le
medie e le deviazioni del suo esito (arrotondati lì a quattro decimali).
Metodo e previsioni nel README.

    analizza.py <collezione> <esito di scelta-ibrida> <valutazione> [...]
        (collezione: in Koskidex eval/corpora/c3-albo/known-item-umane;
         valutazioni: A, B e LT di 2026-09-25_known-item-umane)
"""
import collections, datetime, json, math, os, subprocess, sys, unicodedata

collezione, precedente, *valutazioni = sys.argv[1:]
QUI = os.path.dirname(os.path.abspath(__file__))


def termini(testo):
    """La tokenizzazione predefinita di Koskidex, come in 2026-09-25_scelta-ibrida."""
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


def idf(df, n):
    return math.log(1 + (n - df + 0.5) / (df + 0.5))


def caratteristiche(testo, df, n, l_vuoto):
    qt = termini(testo) or [""]
    massimo = idf(0, n)
    idfs = [idf(df.get(t, 0), n) / massimo for t in qt]
    cifre = [t for t in qt if any(c.isdigit() for c in t)]
    return [math.log(1 + len(qt)), float(bool(cifre)), len(cifre) / len(qt), sum(idfs) / len(idfs), max(idfs), min(idfs),
            sum(df.get(t, 0) == 0 for t in qt) / len(qt), float(l_vuoto)]


per_conf = {}
for f in valutazioni:
    v = json.load(open(f))
    c = v["config"]
    assert v["collection"] == "known-item-umane" and c.get("split", "test") == "test", f
    assert c.get("modifiche_non_committate") == "false", f"{f}: codice non committato"
    assert c.get("punteggio") == "bm25" and c.get("bm25_espansioni") == "blended", f
    assert c["analisi"] == "none" and c["refusi"] == "0", f
    if "embedder" not in c:
        assert c["recupero"] == "all", f
        k = "LT"
    else:
        assert c["embedder"] == "ollama/bge-m3" and c["ibrido"] == "union" and c.get("fusione", "somma") == "somma", f
        k = {("any", "160"): "A", ("all", "10"): "B"}[(c["recupero"], c.get("peso_vettore", "20"))]
    assert k not in per_conf, f"{f}: {k} due volte"
    per_conf[k] = (f, v)
assert sorted(per_conf) == ["A", "B", "LT"], f"servono A, B e LT: {sorted(per_conf)}"

modello = json.load(open(precedente))["modello"]
nomi = modello["caratteristiche"]
pesi = [modello["pesi_standardizzati"][x] for x in nomi]
media = [modello["media"][x] for x in nomi]
dev = [modello["deviazione"][x] for x in nomi]
sigma = lambda z: 1 / (1 + math.exp(-max(-30, min(30, z))))
sceglie_b = lambda x: sigma(modello["intercetta"] + sum(w * (xi - m) / d for w, xi, m, d in zip(pesi, x, media, dev))) > modello["soglia"]

df, n = collections.Counter(), 0
for riga in open(os.path.join(collezione, "corpus.jsonl"), encoding="utf8"):
    d = json.loads(riga)
    df.update(set(termini((d.get("title", "") + " " + d.get("text", "")).strip())))
    n += 1
domande = {json.loads(r)["_id"]: json.loads(r)["text"] for r in open(os.path.join(collezione, "queries.jsonl"), encoding="utf8")}

qa, qb, ql = ({r["query_id"]: r for r in per_conf[k][1]["per_query"]} for k in ("A", "B", "LT"))
assert qa.keys() == qb.keys() == ql.keys()
esempi = []
for q in sorted(qa):
    l_vuoto = ql[q]["candidates"] == 0
    esempi.append({"query": q, "a": qa[q]["ndcg@10"], "b": qb[q]["ndcg@10"], "l_vuoto": l_vuoto,
                   "cifra": any(ch.isdigit() for ch in domande[q]),
                   "x": caratteristiche(domande[q], df, n, l_vuoto)})

strategie = {
    "sempre A": lambda _: False,
    "sempre B": lambda _: True,
    "oracolo": lambda e: e["b"] > e["a"],
    "regola": lambda e: e["cifra"] and not e["l_vuoto"],
    "classificatore": lambda e: sceglie_b(e["x"]),
}
gruppi = {"tutte": lambda _: True, "con cifra": lambda e: e["cifra"], "senza cifra": lambda e: not e["cifra"]}
risultati = {}
for g, dentro in gruppi.items():
    qs = [e for e in esempi if dentro(e)]
    risultati[g] = {"query": len(qs)}
    if qs:
        for nome, f in strategie.items():
            risultati[g][nome] = {"ndcg@10": round(sum(e["b"] if f(e) else e["a"] for e in qs) / len(qs), 4),
                                  "scelte_b": sum(f(e) for e in qs)}
        risultati[g]["b_batte_a"] = sum(e["b"] > e["a"] for e in qs)
        risultati[g]["a_batte_b"] = sum(e["a"] > e["b"] for e in qs)
print(json.dumps(risultati, indent=1, ensure_ascii=False))

ora = datetime.datetime.now(datetime.timezone.utc)
git = lambda *x: subprocess.run(["git", "-C", QUI, *x], capture_output=True, text=True, check=True).stdout.strip()
esito = {"ran_at": ora.strftime("%Y-%m-%dT%H:%M:%SZ"),
         "config": {"commit": git("rev-parse", "--short", "HEAD"),
                    "modifiche_non_committate": "true" if git("status", "--porcelain", "--", QUI) else "false",
                    "valutazioni": {k: os.path.basename(f) for k, (f, _) in sorted(per_conf.items())},
                    "koskidex": sorted({v["config"]["commit"][:7] for _, v in per_conf.values()}),
                    "classificatore_da": os.path.basename(precedente)},
         "risultati": risultati,
         "scelte": [{"query": e["query"], "cifra": e["cifra"], "l_vuoto": e["l_vuoto"], "ndcg_a": e["a"], "ndcg_b": e["b"],
                     "classificatore": "B" if sceglie_b(e["x"]) else "A"} for e in esempi]}
if not os.environ.get("TESI_RISULTATI"):
    sys.exit("!!! RISULTATO NON ARCHIVIATO: TESI_RISULTATI non è impostata.")
d = os.path.join(os.environ["TESI_RISULTATI"], "esperimenti", "2026-09-25_scelta-umane")
os.makedirs(d, exist_ok=True)
o = ora.strftime("%Y-%m-%dT%H%M%SZ"); p = os.path.join(d, f"{o}_esito.json"); k = 2
while os.path.exists(p):
    p = os.path.join(d, f"{o}-{k}_esito.json"); k += 1
open(p, "x").write(json.dumps(esito, indent=2, ensure_ascii=False))
print("archiviato in", p)
