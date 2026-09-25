#!/usr/bin/env python3
"""Estrae gli atti da mostrare alle persone per le known-item umane.

Metà da ciascuna fonte (Crispiano col testo intero, Friuli Venezia Giulia coi
soli metadati), dentro ogni fonte per genere in proporzione alla fonte, con un
seme fissato; poi li divide in lotti di 40, 20 per fonte, in ordine casuale.
Esclusi gli atti delle known-item automatiche, e da Crispiano quelli senza
testo integrale estratto. Regole in ../../istruzioni-annotazione.md, parte 1.

Legge il database dell'app (doc-tesi-mysql, database albo) per fonte e genere,
e i due export del corpus di Koskidex per sapere chi ha il testo integrale.
Scrive solo id: query/known-item-umane/campione.json.

    campione-atti.py <cartella c3-albo di Koskidex>
"""
import collections, hashlib, json, os, random, subprocess, sys

SEME = 20260927
PER_FONTE = 80
PER_LOTTO_PER_FONTE = 20
# Sotto questa differenza fra testo integrale e scheda l'estrazione non ha dato
# niente: cinque atti di Crispiano sono scansioni con 2-182 caratteri, il
# successivo ne ha 957.
TESTO_MINIMO = 500
GENERI = [("determin", "determina"), ("deliber", "delibera"), ("ordinanz", "ordinanza"), ("avvis", "avviso")]
QUI = os.path.dirname(os.path.abspath(__file__))
USCITA = os.path.join(QUI, "..", "query", "known-item-umane")
albo = sys.argv[1]

if os.path.exists(os.path.join(USCITA, "campione.json")):
    raise SystemExit("campione.json esiste già: il campione non si rigenera sopra se stesso")

sql = ("select json_object('id', document_id, 'nome', name, 'subjects', subjects, "
       "'additional_data', additional_data) from document_versions order by document_id")
righe = subprocess.run(["docker", "exec", "doc-tesi-mysql", "mysql", "-uroot", "-proot", "-N", "-B", "--raw",
                        "--default-character-set=utf8mb4", "albo", "-e", sql],
                       capture_output=True, text=True, check=True).stdout.splitlines()
atti = [json.loads(r) for r in righe]


def genere(testo):
    t = (testo or "").lower()
    return next((g for chiave, g in GENERI if chiave in t), "altro")


testi = {}
for nome in ("beir-full", "beir-metadata"):
    for r in open(os.path.join(albo, nome, "corpus.jsonl"), encoding="utf8"):
        d = json.loads(r)
        testi.setdefault(d["_id"], {})[nome] = d["text"]

esclusi_auto = set()
for lotto, split in (("known-item-auto", "test"), ("known-item-auto-train", "train")):
    for r in open(os.path.join(QUI, "..", "query", lotto, "qrels", f"{split}.tsv")).read().splitlines()[1:]:
        esclusi_auto.add(r.split("\t")[1])

conteggi = collections.Counter()
popolazione = {"crispiano": collections.defaultdict(list), "fvg": collections.defaultdict(list)}
for a in atti:
    doc = f"doc-{str(a['id']).zfill(4)}"
    ente = ((a["subjects"] or [{}])[0].get("name") or "")
    fonte = "crispiano" if "crispiano" in ente.lower() else "fvg"
    if fonte == "crispiano":
        g = genere((a["nome"] or "").split(":")[0].split()[0] if a["nome"] else "")
        if len(testi[doc]["beir-full"]) - len(testi[doc]["beir-metadata"]) < TESTO_MINIMO:
            conteggi["crispiano_senza_testo_integrale"] += 1
            continue
    else:
        tip = {x["name"]: x.get("value") for x in (a["additional_data"] or [])}.get("tipologia_atto")
        g = genere(tip)
    if doc in esclusi_auto:
        conteggi[f"{fonte}_gia_nelle_known_item_automatiche"] += 1
        continue
    popolazione[fonte][g].append(doc)

rng = random.Random(SEME)
estratti, quote = {}, {}
for fonte, per_genere in popolazione.items():
    totale = sum(len(v) for v in per_genere.values())
    # Quote proporzionali col metodo dei resti più grandi, così la somma è esatta.
    esatte = {g: PER_FONTE * len(v) / totale for g, v in per_genere.items()}
    q = {g: int(x) for g, x in esatte.items()}
    for g in sorted(esatte, key=lambda g: (-(esatte[g] - q[g]), g))[:PER_FONTE - sum(q.values())]:
        q[g] += 1
    quote[fonte] = {g: {"popolazione": len(per_genere[g]), "estratti": q[g]} for g in sorted(per_genere)}
    scelti = []
    for g in sorted(per_genere):
        scelti += rng.sample(sorted(per_genere[g]), q[g])
    rng.shuffle(scelti)
    estratti[fonte] = scelti

lotti = {}
for k in range(PER_FONTE // PER_LOTTO_PER_FONTE):
    fetta = slice(k * PER_LOTTO_PER_FONTE, (k + 1) * PER_LOTTO_PER_FONTE)
    lotto = estratti["crispiano"][fetta] + estratti["fvg"][fetta]
    rng.shuffle(lotto)
    lotti[f"lotto-{k + 1}"] = lotto

impronta = lambda p: hashlib.sha256(open(os.path.join(albo, p, "corpus.jsonl"), "rb").read()).hexdigest()
commit = subprocess.run(["git", "-C", os.path.expanduser("~/Desktop/Dieffetech/Documentale"), "rev-parse", "--short", "HEAD"],
                        capture_output=True, text=True, check=True).stdout.strip()
campione = {"seme": SEME, "per_fonte": PER_FONTE, "per_lotto_per_fonte": PER_LOTTO_PER_FONTE, "testo_minimo": TESTO_MINIMO,
            "generi": {g: chiave for chiave, g in GENERI} | {"altro": "nessuna delle altre"},
            "esclusi": dict(sorted(conteggi.items())), "quote": quote,
            "corpus_sha256": {"beir-full": impronta("beir-full"), "beir-metadata": impronta("beir-metadata")},
            "commit_documentale": commit, "lotti": lotti,
            "atti": {d: {"fonte": f, "genere": g} for f, per_genere in popolazione.items()
                     for g, docs in per_genere.items() for d in docs if d in set(sum(lotti.values(), []))}}
os.makedirs(USCITA, exist_ok=True)
with open(os.path.join(USCITA, "campione.json"), "x", encoding="utf8") as f:
    f.write(json.dumps(campione, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({k: v for k, v in campione.items() if k not in ("lotti", "atti")}, indent=2, ensure_ascii=False))
