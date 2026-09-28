#!/usr/bin/env python3
"""Genera le query known-item sui formati di date e importi, per
esperimenti/2026-09-28_date-importi (metodo nel README).

Date: "<data> <comune>". Da un atto si prende una data che, in quel comune,
compare in quell'atto solo (in qualunque formato) e che nell'atto è scritta in
un formato solo; fino a 50 atti per formato di partenza (barra, punto, mese),
ciascuno con tre query, una per formato. Quella nel formato dell'atto è la data
copiata com'è; le altre sono scritte gg/mm/aaaa, gg.mm.aaaa, g <mese> aaaa.

Importi: "<importo> <comune>", allo stesso modo, formati con i punti delle
migliaia e senza, due query ciascuno.

Le date e gli importi si cercano nel titolo e nel testo delle schede
(beir-metadata), cioè in quello che Koskidex piatto indicizza; il comune viene
dal database dell'app, come in known-item-auto.py. Scrive in
query/known-item-date/ e query/known-item-importi/: queries.jsonl,
queries.txt, qrels/test.tsv, formati.json (per ogni query il formato di
partenza e quello della query) e generazione.json.

    known-item-formati.py
"""
import collections, json, os, random, re, subprocess

QUI = os.path.dirname(os.path.abspath(__file__))
SEME, PER_FORMATO = 20260928, 50
CORPUS = os.path.expanduser("~/Desktop/Progetti-personali/Koskidex/eval/corpora/c3-albo/beir-metadata/corpus.jsonl")
MESI = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto", "settembre",
        "ottobre", "novembre", "dicembre"]

DATE = [
    ("barra", re.compile(r"(?<![\d./,-])(\d{1,2})/(\d{1,2})/(\d{4}|\d{2})(?![\d/])")),
    ("punto", re.compile(r"(?<![\d./,-])(\d{1,2})\.(\d{1,2})\.(\d{4})(?![\d.,/]\d)")),
    ("trattino", re.compile(r"(?<![\d./,-])(\d{1,2})-(\d{1,2})-(\d{4})(?![\d-])")),
    ("mese", re.compile(r"(?<!\d)(\d{1,2})\s+(" + "|".join(MESI) + r")\s+(\d{4})(?!\d)", re.I)),
]
IMPORTI = [
    ("punti", re.compile(r"(?<![\d.,])(\d{1,3}(?:\.\d{3})+,\d{2})(?![\d,.])")),
    ("senza", re.compile(r"(?<![\d.,])(\d{4,},\d{2})(?![\d,.])")),
]


def data_valida(g, m, a):
    g, a = int(g), int(a)
    m = MESI.index(m.lower()) + 1 if not m.isdigit() else int(m)
    if a < 100:
        a += 2000
    return (a, m, g) if 1 <= g <= 31 and 1 <= m <= 12 and 1900 <= a <= 2099 else None


def scrivi_data(formato, a, m, g):
    return {"barra": f"{g:02d}/{m:02d}/{a}", "punto": f"{g:02d}.{m:02d}.{a}", "mese": f"{g} {MESI[m - 1]} {a}"}[formato]


def importo(s):
    return s.replace(".", "")


def scrivi_importo(formato, valore):
    intero, dec = valore.split(",")
    if formato == "senza":
        return valore
    gruppi = []
    while len(intero) > 3:
        gruppi.insert(0, intero[-3:]); intero = intero[:-3]
    return ".".join([intero] + gruppi) + "," + dec


sql = "select json_object('id', document_id, 'subjects', subjects) from document_versions order by document_id"
righe = subprocess.run(["docker", "exec", "doc-tesi-mysql", "mysql", "-uroot", "-proot", "-N", "-B", "--raw",
                        "--default-character-set=utf8mb4", "albo", "-e", sql],
                       capture_output=True, text=True, check=True).stdout.splitlines()
comuni = {}
for r in righe:
    a = json.loads(r)
    ente = ((a["subjects"] or [{}])[0].get("name") or "").strip()
    comuni[f"doc-{str(a['id']).zfill(4)}"] = re.sub(r"(?i)^comune di\s+", "", ente)

docs = [json.loads(l) for l in open(CORPUS)]


def genera(nome, schemi, chiave, formati_query, scrivi, prefisso):
    dove = collections.defaultdict(set)          # (comune, valore) -> atti
    occorrenze = collections.defaultdict(list)   # (atto, valore) -> [(formato, testo)]
    for d in docs:
        c = comuni.get(d["_id"], "")
        if not c:
            continue
        testo = (d.get("title") or "") + "\n" + (d.get("text") or "")
        for formato, p in schemi:
            for m in p.finditer(testo):
                v = chiave(m)
                if v is None:
                    continue
                dove[(c.lower(), v)].add(d["_id"])
                occorrenze[(d["_id"], v)].append((formato, m.group(0)))
    candidati = collections.defaultdict(list)
    for (i, v), occ in occorrenze.items():
        formati = {f for f, _ in occ}
        if len(dove[(comuni[i].lower(), v)]) == 1 and len(formati) == 1 and next(iter(formati)) in formati_query:
            candidati[next(iter(formati))].append((i, v, occ[0][1]))
    rng = random.Random(SEME)
    estratti = []
    for f in formati_query:
        lista = sorted(candidati[f])
        estratti += [(f, x) for x in sorted(rng.sample(lista, min(PER_FORMATO, len(lista))))]
    uscita = os.path.join(QUI, "..", "query", nome)
    os.makedirs(os.path.join(uscita, "qrels"), exist_ok=True)
    formati = {}
    with open(os.path.join(uscita, "queries.jsonl"), "w", encoding="utf8") as q, \
         open(os.path.join(uscita, "queries.txt"), "w", encoding="utf8") as t, \
         open(os.path.join(uscita, "qrels", "test.tsv"), "w", encoding="utf8") as g:
        g.write("query-id\tcorpus-id\tscore\n")
        for k, (partenza, (i, v, originale)) in enumerate(estratti, 1):
            for fq in formati_query:
                qid = f"{prefisso}-{k:03d}-{fq}"
                valore = originale if fq == partenza else scrivi(fq, v)
                testo = f"{valore} {comuni[i]}"
                q.write(json.dumps({"_id": qid, "text": testo}, ensure_ascii=False) + "\n")
                t.write(testo + "\n")
                g.write(f"{qid}\t{i}\t2\n")
                formati[qid] = {"partenza": partenza, "query": fq}
    open(os.path.join(uscita, "formati.json"), "w").write(json.dumps(formati, indent=1) + "\n")
    generazione = {"seme": SEME, "per_formato": PER_FORMATO,
                   "candidati": {f: len(candidati[f]) for f in formati_query},
                   "estratti": dict(collections.Counter(f for f, _ in estratti)),
                   "query": len(formati), "corpus": os.path.basename(os.path.dirname(CORPUS))}
    open(os.path.join(uscita, "generazione.json"), "w").write(json.dumps(generazione, indent=2) + "\n")
    print(nome, json.dumps(generazione))


genera("known-item-date", DATE, lambda m: data_valida(*m.groups()), ["barra", "punto", "mese"],
       lambda f, v: scrivi_data(f, *v), "kd")
genera("known-item-importi", IMPORTI, lambda m: importo(m.group(1)), ["punti", "senza"], scrivi_importo, "kx")
