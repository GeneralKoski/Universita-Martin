#!/usr/bin/env python3
"""I conteggi descrittivi che la tesi cita senza un esperimento: le righe di
Koskidex quando è stato scelto, la composizione delle due fonti dell'albo,
lunghezza e pagine dei testi di Crispiano, i marcatori di dati personali, i
formati di date e importi nelle schede, quante known-item umane contengono un
anno, una data, un importo o una cifra. Solo numeri: nessun testo di atti o di
query. Scrive risultati/corpus/<ora>_conteggi.json.

    conteggi.py
"""
import collections, datetime, glob, json, os, re, statistics, subprocess, sys

QUI = os.path.dirname(os.path.abspath(__file__))
KX = os.path.expanduser("~/Desktop/Progetti-personali/Koskidex")
ALBO = os.path.join(KX, "eval", "corpora", "c3-albo")
UMANE = os.path.join(QUI, "..", "query", "known-item-umane", "queries.txt")
git = lambda d, *x: subprocess.run(["git", "-C", d, *x], capture_output=True, text=True, check=True).stdout


def distribuzione(valori):
    v = sorted(valori)
    q = lambda p: v[min(len(v) - 1, int(p * len(v)))]
    return {"n": len(v), "min": v[0], "p10": q(0.10), "mediana": statistics.median(v), "p90": q(0.90), "max": v[-1]}


# Koskidex all'ultimo commit prima del 16/09/2026, il giorno dopo la scelta dell'argomento.
commit = git(KX, "rev-list", "-1", "--before=2026-09-16T00:00", "main").strip()
righe = collections.Counter()
for f in git(KX, "ls-tree", "-r", "--name-only", commit).split():
    if f.endswith(".go"):
        righe["test" if f.endswith("_test.go") else "codice"] += git(KX, "show", f"{commit}:{f}").count("\n")
koskidex = {"commit": commit[:7], "data": git(KX, "show", "-s", "--format=%ad", "--date=short", commit).strip(), **righe}

cr = [json.loads(r) for r in open(os.path.join(ALBO, "crispiano", "atti.jsonl"), encoding="utf8")]
generi = collections.Counter()
for a in cr:
    o = a["oggetto"].strip().lower()
    generi["determina" if o.startswith("determin") else "delibera" if o.startswith("delib") else
           "ordinanza" if o.startswith("ordinanz") else "altro"] += 1
pagine = []
for a in cr:
    pdf = os.path.join(ALBO, a.get("file_pdf") or "")
    if a.get("file_pdf") and os.path.exists(pdf):
        out = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout
        m = re.search(r"^Pages:\s+(\d+)", out, re.M)
        if m:
            pagine.append(int(m.group(1)))
caratteri = [len(open(os.path.join(ALBO, a["file_testo"]), encoding="utf8", errors="replace").read())
             for a in cr if a.get("file_testo") and os.path.exists(os.path.join(ALBO, a["file_testo"]))]
crispiano = {"atti": len(cr), "dal": min(a["data_pubblicazione"] for a in cr), "al": max(a["data_pubblicazione"] for a in cr),
             "generi_dall_oggetto": dict(generi), "pagine": distribuzione(pagine), "caratteri_testo": distribuzione(caratteri),
             "caratteri_oltre_30000": sum(c > 30000 for c in caratteri)}

fv = [json.loads(r) for r in open(os.path.join(ALBO, "fvg", "atti.jsonl"), encoding="utf8")]
MARCATORI = ["sig.", "nato a", "nata a", "codice fiscale", "residente in", "pubblicazione di matrimonio"]
# Parole intere: "sig." non dentro "consig.", "nato a" non dentro "assegnato a".
MARCATORE = re.compile(r"(?<!\w)(" + "|".join(re.escape(m) for m in MARCATORI) + r")(?!\w)", re.I)
fvg = {"atti": len(fv), "enti": len({a["ente"] for a in fv}), "tipologie": len({a["tipologia_atto"] for a in fv}),
       "dal": min(a["data_inizio_pubblicazione"] for a in fv), "al": max(a["data_inizio_pubblicazione"] for a in fv),
       "marcatori": MARCATORI,
       "oggetti_con_marcatori": sum(bool(MARCATORE.search(a["oggetto"] or "")) for a in fv)}

# Le espressioni di strumenti/known-item-formati.py, sulle stesse schede.
MESI = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto", "settembre",
        "ottobre", "novembre", "dicembre"]
FORMATI = {
    "barra": re.compile(r"(?<![\d./,-])(\d{1,2})/(\d{1,2})/(\d{4}|\d{2})(?![\d/])"),
    "punto": re.compile(r"(?<![\d./,-])(\d{1,2})\.(\d{1,2})\.(\d{4})(?![\d.,/]\d)"),
    "trattino": re.compile(r"(?<![\d./,-])(\d{1,2})-(\d{1,2})-(\d{4})(?![\d-])"),
    "mese": re.compile(r"(?<!\d)(\d{1,2})\s+(" + "|".join(MESI) + r")\s+(\d{4})(?!\d)", re.I),
    "importo_con_punti": re.compile(r"(?<![\d.,])(\d{1,3}(?:\.\d{3})+,\d{2})(?![\d,.])"),
    "importo_senza_punti": re.compile(r"(?<![\d.,])(\d{4,},\d{2})(?![\d,.])"),
}
volte, atti = collections.Counter(), collections.Counter()


def valida(m):
    g, mese, a = m.groups()
    mese = MESI.index(mese.lower()) + 1 if not mese.isdigit() else int(mese)
    a = int(a) + (2000 if len(a) == 2 else 0)
    return 1 <= int(g) <= 31 and 1 <= mese <= 12 and 1900 <= a <= 2099


for r in open(os.path.join(ALBO, "beir-metadata", "corpus.jsonl"), encoding="utf8"):
    d = json.loads(r)
    t = (d.get("title") or "") + "\n" + (d.get("text") or "")
    for nome, p in FORMATI.items():
        n = sum(nome.startswith("importo") or valida(m) for m in p.finditer(t))
        volte[nome] += n
        atti[nome] += n > 0
formati = {n: {"volte": volte[n], "atti": atti[n]} for n in FORMATI}

q = [l.strip() for l in open(UMANE, encoding="utf8") if l.strip()]
umane = {"query": len(q),
         "con_anno": sum(bool(re.search(r"(?<!\d)(19|20)\d\d(?!\d)", x)) for x in q),
         "con_data": sum(any(p.search(x) for n, p in FORMATI.items() if not n.startswith("importo")) for x in q),
         "con_importo": sum(any(p.search(x) for n, p in FORMATI.items() if n.startswith("importo")) for x in q),
         "con_una_cifra": sum(bool(re.search(r"\d", x)) for x in q)}

ora = datetime.datetime.now(datetime.timezone.utc)
esito = {"ran_at": ora.strftime("%Y-%m-%dT%H:%M:%SZ"),
         "config": {"commit": git(QUI, "rev-parse", "--short", "HEAD").strip(),
                    "modifiche_non_committate": "true" if git(QUI, "status", "--porcelain", "--", os.path.abspath(__file__)).strip() else "false",
                    "koskidex_corpus": git(KX, "rev-parse", "--short", "HEAD").strip()},
         "koskidex_all_inizio": koskidex, "crispiano": crispiano, "fvg": fvg, "formati_nelle_schede": formati,
         "known_item_umane": umane}
print(json.dumps(esito, indent=1, ensure_ascii=False))
if not os.environ.get("TESI_RISULTATI"):
    sys.exit("!!! RISULTATO NON ARCHIVIATO: TESI_RISULTATI non è impostata.")
d = os.path.join(os.environ["TESI_RISULTATI"], "corpus"); os.makedirs(d, exist_ok=True)
o = ora.strftime("%Y-%m-%dT%H%M%SZ"); p = os.path.join(d, f"{o}_conteggi.json"); k = 2
while os.path.exists(p):
    p = os.path.join(d, f"{o}-{k}_conteggi.json"); k += 1
open(p, "x").write(json.dumps(esito, indent=2, ensure_ascii=False))
print("archiviato in", p)
