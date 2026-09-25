#!/usr/bin/env python3
"""L'accordo fra i due annotatori del pool delle 24 query del confronto.

Legge giudizi-primo.tsv e giudizi-secondo.tsv, scritti da importa-giudizi.py
in query/confronto-24/, e sulle righe giudicate da tutti e due calcola, come
dice la parte 3 di ../../istruzioni-annotazione.md:

- l'accordo semplice;
- il kappa di Cohen sui tre gradi;
- il kappa pesato linearmente (pesi 1 - |i - j| / 2), perché fra 1 e 2 si
  sbaglia meno che fra 0 e 2.

Più la matrice di confusione e l'accordo per query, per guardare dove sono i
disaccordi. Si rifiuta di partire se il secondo annotatore non ha finito le
query estratte (campione-secondo.json): un kappa su metà del campione non è
quello da riportare.

    kappa.py
"""
import csv, datetime, hashlib, json, os, subprocess, sys

QUI = os.path.dirname(os.path.abspath(__file__))
CARTELLA = os.path.join(QUI, "..", "query", "confronto-24")
GRADI = (0, 1, 2)


def leggi(ruolo):
    percorso = os.path.join(CARTELLA, f"giudizi-{ruolo}.tsv")
    if not os.path.exists(percorso):
        sys.exit(f"manca {os.path.basename(percorso)}: prima importa-giudizi.py")
    righe = {(r["query_id"], r["doc_id"]): int(r["grado"])
             for r in csv.DictReader(open(percorso, encoding="utf8"), delimiter="\t")}
    return percorso, righe


def kappa(coppie, peso):
    n = len(coppie)
    osservato = sum(peso(a, b) for a, b in coppie) / n
    righe = {g: sum(a == g for a, _ in coppie) / n for g in GRADI}
    colonne = {g: sum(b == g for _, b in coppie) / n for g in GRADI}
    atteso = sum(peso(i, j) * righe[i] * colonne[j] for i in GRADI for j in GRADI)
    return None if atteso == 1 else (osservato - atteso) / (1 - atteso)


percorso_primo, primo = leggi("primo")
percorso_secondo, secondo = leggi("secondo")
scelte = set(json.load(open(os.path.join(CARTELLA, "campione-secondo.json")))["query"])
foglio = [(r["query_id"], r["doc_id"]) for r in
          csv.DictReader(open(os.path.join(CARTELLA, "foglio", "giudizi.tsv"), encoding="utf8"), delimiter="\t")]
campione = [r for r in foglio if r[0] in scelte]

mancanti = [r for r in campione if r not in secondo]
if mancanti:
    sys.exit(f"il secondo annotatore ha {len(campione) - len(mancanti)} righe su {len(campione)}: "
             f"il kappa si calcola a campione finito")
senza_primo = [r for r in campione if r not in primo]
if senza_primo:
    sys.exit(f"{len(senza_primo)} righe del campione non hanno il giudizio del primo annotatore, "
             f"per esempio {senza_primo[0]}")

coppie = [(primo[r], secondo[r]) for r in campione]
per_query = {}
for (q, _), (a, b) in zip(campione, coppie):
    per_query.setdefault(q, [0, 0])
    per_query[q][0] += a == b
    per_query[q][1] += 1

esito = {
    "righe": len(coppie),
    "query": sorted(scelte),
    "accordo_semplice": sum(a == b for a, b in coppie) / len(coppie),
    "kappa_cohen": kappa(coppie, lambda i, j: 1.0 if i == j else 0.0),
    "kappa_pesato_lineare": kappa(coppie, lambda i, j: 1 - abs(i - j) / 2),
    "confusione": {f"primo {i}": {f"secondo {j}": sum(a == i and b == j for a, b in coppie) for j in GRADI}
                   for i in GRADI},
    "per_query": {q: {"uguali": u, "righe": t} for q, (u, t) in sorted(per_query.items())},
}
print(json.dumps({k: v for k, v in esito.items() if k not in ("per_query", "query")}, indent=2, ensure_ascii=False))

ora = datetime.datetime.now(datetime.timezone.utc)
git = lambda *a: subprocess.run(["git", "-C", QUI, *a], capture_output=True, text=True, check=True).stdout.strip()
impronta = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
esito = {"ran_at": ora.strftime("%Y-%m-%dT%H:%M:%SZ"),
         "config": {"commit": git("rev-parse", "--short", "HEAD"),
                    "modifiche_non_committate": "true" if git("status", "--porcelain", "--", QUI) else "false",
                    "giudizi_primo_sha256": impronta(percorso_primo),
                    "giudizi_secondo_sha256": impronta(percorso_secondo)},
         **esito}
if not os.environ.get("TESI_RISULTATI"):
    sys.exit("!!! RISULTATO NON ARCHIVIATO: TESI_RISULTATI non è impostata.")
d = os.path.join(os.environ["TESI_RISULTATI"], "query", "confronto-24", "accordo")
os.makedirs(d, exist_ok=True)
o = ora.strftime("%Y-%m-%dT%H%M%SZ"); p = os.path.join(d, f"{o}_kappa.json"); n = 2
while os.path.exists(p):
    p = os.path.join(d, f"{o}-{n}_kappa.json"); n += 1
open(p, "x").write(json.dumps(esito, indent=2, ensure_ascii=False))
print("archiviato in", p)
