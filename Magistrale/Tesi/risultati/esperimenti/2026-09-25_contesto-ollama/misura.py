#!/usr/bin/env python3
"""Quanti token di un testo legge bge-m3 attraverso Ollama: dove taglia, con il
contesto predefinito, con num_ctx 8192 e con num_ctx e num_batch 8192, e quanti
documenti restano tagliati.
Metodo e previsioni nel README.

    misura.py <koskidex>
"""
import datetime, hashlib, json, os, subprocess, sys, urllib.request

kx = sys.argv[1]
QUI = os.path.dirname(os.path.abspath(__file__))
OLLAMA, MODELLO, GRANDE = "http://localhost:11434", "bge-m3", 8192
CORPORA = {"albo": "eval/corpora/c3-albo/beir-full/corpus.jsonl",
           "scifact": "eval/corpora/c1-public/scifact/corpus.jsonl",
           "nfcorpus": "eval/corpora/c1-public/nfcorpus/corpus.jsonl"}


def chiedi(percorso, dati=None):
    req = urllib.request.Request(OLLAMA + percorso, data=json.dumps(dati).encode() if dati else None,
                                 headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req))


PIENO = {"num_ctx": GRANDE, "num_batch": GRANDE}
VARIANTI = {"predefinito": None, "num_ctx 8192": {"num_ctx": GRANDE}, "num_ctx e num_batch 8192": PIENO}


def vettore(testo, opzioni=None):
    corpo = {"model": MODELLO, "input": [testo]}
    if opzioni:
        corpo["options"] = opzioni
    r = chiedi("/api/embed", corpo)
    return r["embeddings"][0], r["prompt_eval_count"]


def documenti(nome):
    return [json.loads(riga) for riga in open(os.path.join(kx, CORPORA[nome]), encoding="utf8")]


albo = documenti("albo")
interi = [d for d in albo if d["_id"] <= "doc-0563"]
assert len(interi) == 563
lungo = " ".join(d["text"] for d in sorted(interi, key=lambda d: d["_id"]))

taglio = []
for variante, opzioni in VARIANTI.items():
    for n in (1000, 2000, 4000, 6000, 8000, 10000, 12000, 16000, 20000, 25000, 30000, 35000, 40000):
        a, ta = vettore(lungo[:n] + " coda uno, del tutto diversa dall'altra." * 30, opzioni)
        b, tb = vettore(lungo[:n] + " ### seconda coda: parole che non c'entrano." * 30, opzioni)
        taglio.append({"opzioni": variante, "caratteri_prefisso": n, "token_letti": [ta, tb],
                       "differenza_massima": max(abs(x - y) for x, y in zip(a, b))})
        print(taglio[-1], flush=True)

conteggi = {}
for nome, docs in (("albo_testi_interi", interi), ("albo_schede", [d for d in albo if d["_id"] > "doc-0563"]),
                   ("scifact", documenti("scifact")), ("nfcorpus", documenti("nfcorpus"))):
    token = []
    for d in docs:
        testo = (d.get("title", "") + " " + d.get("text", "")).strip() if nome in ("scifact", "nfcorpus") else d["text"]
        token.append(vettore(testo, PIENO)[1] if testo else 0)
    token.sort()
    conteggi[nome] = {"documenti": len(token), "oltre_2048": sum(t > 2048 for t in token),
                      "a_8192": sum(t >= GRANDE for t in token), "mediana": token[len(token) // 2], "massimo": token[-1]}
    print(nome, conteggi[nome], flush=True)

digest = next(m["digest"] for m in chiedi("/api/tags")["models"] if m["name"] in (MODELLO, MODELLO + ":latest"))
ora = datetime.datetime.now(datetime.timezone.utc)
git = lambda *a: subprocess.run(["git", "-C", QUI, *a], capture_output=True, text=True, check=True).stdout.strip()
impronta = lambda p: hashlib.sha256(open(os.path.join(kx, p), "rb").read()).hexdigest()
esito = {"ran_at": ora.strftime("%Y-%m-%dT%H:%M:%SZ"),
         "config": {"commit": git("rev-parse", "--short", "HEAD"),
                    "modifiche_non_committate": "true" if git("status", "--porcelain", "--", QUI) else "false",
                    "modello": MODELLO, "digest": digest, "opzioni_conteggio": PIENO, "corpora_sha256": {k: impronta(p) for k, p in CORPORA.items()}},
         "taglio": taglio, "conteggi": conteggi}
if not os.environ.get("TESI_RISULTATI"):
    sys.exit("!!! RISULTATO NON ARCHIVIATO: TESI_RISULTATI non è impostata.")
d = os.path.join(os.environ["TESI_RISULTATI"], "esperimenti", "2026-09-25_contesto-ollama")
o = ora.strftime("%Y-%m-%dT%H%M%SZ"); p = os.path.join(d, f"{o}_esito.json"); n = 2
while os.path.exists(p):
    p = os.path.join(d, f"{o}-{n}_esito.json"); n += 1
open(p, "x").write(json.dumps(esito, indent=2, ensure_ascii=False))
print("archiviato in", p)
