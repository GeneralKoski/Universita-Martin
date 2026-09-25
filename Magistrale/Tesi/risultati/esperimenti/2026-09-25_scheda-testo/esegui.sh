#!/usr/bin/env bash
# Le esecuzioni di 2026-09-25_scheda-testo, sui soli atti di Crispiano (dopo
# importa-raccolta.py e collezioni-umane.py). KOSKIDEX e CORPORA cambiano le
# cartelle.
set -euo pipefail
: "${TESI_RISULTATI:?TESI_RISULTATI non impostata: il risultato non verrebbe archiviato}"
KX=${KOSKIDEX:-$HOME/Desktop/Progetti-personali/Koskidex}
CORPORA=${CORPORA:-$KX/eval/corpora/c3-albo}
[ -z "$(git -C "$KX" status --porcelain)" ] || { echo "Koskidex ha modifiche non committate" >&2; exit 1; }

valuta() {
  local collezione=$1 run=$2; shift 2
  (cd "$KX" && go run ./scripts/evaluate -corpora "$CORPORA" -collection "$collezione" -split crispiano \
    -archivio valutazioni-albo -top 10 -run "$run" -scoring bm25 -bm25-espansioni blended "$@")
}

for c in scheda testo; do
  valuta "crispiano-$c" "st-$c-LA" -mode any
  valuta "crispiano-$c" "st-$c-LT" -mode all
  valuta "crispiano-$c" "st-$c-A" -mode any -embedder bge-m3 -ibrido union -peso-vettore 160
done
for b in 0.25 0.5 1; do
  valuta crispiano-testo "st-testo-LA-b$b" -mode any -bm25-b "$b"
done
valuta crispiano-testo st-testo-A-8192 -mode any -embedder bge-m3 -ibrido union -peso-vettore 160 -contesto 8192
