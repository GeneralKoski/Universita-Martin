#!/usr/bin/env python3
"""L'avanzamento di esegui.sh di 2026-09-28_reranker, una barra per passo:
query riordinate, percentuale, tempo medio per query, tempo che manca. Legge
i log di riordina.py nella cartella temporanea di esegui.sh e i primi stadi
archiviati; non tocca l'esecuzione. Si aggiorna ogni 5 secondi, Ctrl-C per
uscire.

    avanzamento.py [beir|umane] [--una-volta]
"""
import datetime, glob, json, os, sys, time

COSA = next((a for a in sys.argv[1:] if not a.startswith("--")), "beir")
PASSI = {"beir": [("scifact", "LA"), ("nfcorpus", "LA"), ("known-item-auto", "LA")],
         "umane": [("known-item-umane", "LA"), ("known-item-umane", "A")]}[COSA]
QUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.environ.get("TESI_RISULTATI") or os.path.join(QUI, "..", "..")
DIR = os.path.join(BASE, "esperimenti", "2026-09-28_reranker")
TMP = os.environ.get("TMPDIR", "/tmp")
LARGHEZZA = 36
# Le query con giudizi di ogni collezione, per stimare i passi non ancora partiti.
ATTESE = {"scifact": 300, "nfcorpus": 323, "known-item-auto": 300, "known-item-umane": 156}


def piu_recente(schema):
    trovati = glob.glob(schema)
    return max(trovati, key=os.path.getmtime) if trovati else None


def stato(collezione, conf):
    log = piu_recente(os.path.join(TMP, "tmp.*", f"riordina-{collezione}-{conf}.log")) \
        or piu_recente(f"/var/folders/*/*/T/tmp.*/riordina-{collezione}-{conf}.log")
    primo = piu_recente(os.path.join(DIR, "primo-stadio", f"*_{collezione}-rr-primo-{conf}.json"))
    totale = len(json.load(open(primo))["per_query"]) if primo else None
    tempi = []
    if log:
        for riga in open(log, errors="replace"):
            parti = riga.split()
            if len(parti) >= 4 and parti[2] == "candidati":
                tempi.append(float(parti[3]) / 1000)
    fatto = bool(log) and any("scritto in" in r for r in open(log, errors="replace"))
    return totale, tempi, fatto


def barra(frazione):
    pieni = int(round(frazione * LARGHEZZA))
    return "█" * pieni + "░" * (LARGHEZZA - pieni)


def durata(secondi):
    m, s = divmod(int(secondi), 60)
    h, m = divmod(m, 60)
    return f"{h}h{m:02d}m" if h else f"{m}m{s:02d}s"


def disegna():
    righe = [f"Reranker, {COSA} - {datetime.datetime.now():%H:%M:%S}", ""]
    manca_tutto, media_nota, in_attesa = 0.0, None, []
    for collezione, conf in PASSI:
        totale, tempi, fatto = stato(collezione, conf)
        if tempi:
            media_nota = sum(tempi[-40:]) / len(tempi[-40:])
        nome = f"{collezione} {conf}"
        if totale is None:
            in_attesa.append(ATTESE[collezione])
            righe.append(f"{nome:22} {barra(0)}   0.0%  in attesa, {ATTESE[collezione]} query")
            continue
        n = len(tempi)
        frazione = 1.0 if fatto else n / totale
        media = sum(tempi[-40:]) / len(tempi[-40:]) if tempi else None
        if fatto:
            coda = "fatto"
        elif media:
            manca = (totale - n) * media
            manca_tutto += manca
            coda = f"{n}/{totale}  {media:4.1f} s/query  mancano {durata(manca)}"
        else:
            coda = f"0/{totale}  avvio del modello"
        righe.append(f"{nome:22} {barra(frazione)} {100 * frazione:5.1f}%  {coda}")
    if media_nota and in_attesa:
        manca_tutto += sum(in_attesa) * media_nota
    righe += ["", f"manca in tutto: circa {durata(manca_tutto)}"
              + ("  (i passi in attesa stimati con l'ultima media nota)" if in_attesa else ""),
              f"fine prevista: {datetime.datetime.now() + datetime.timedelta(seconds=manca_tutto):%H:%M}"]
    return "\n".join(righe)


if "--una-volta" in sys.argv:
    print(disegna())
    sys.exit()
try:
    while True:
        sys.stdout.write("\033[H\033[J" + disegna() + "\n")
        sys.stdout.flush()
        time.sleep(5)
except KeyboardInterrupt:
    print()
