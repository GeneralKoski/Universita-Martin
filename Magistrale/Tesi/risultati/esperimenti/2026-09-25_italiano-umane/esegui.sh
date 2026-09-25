#!/usr/bin/env bash
# Le sei esecuzioni nuove di 2026-09-25_italiano-umane: recupero any e all, con
# stopword, stemmer e tutti e due. Quelle senza analisi (LA e LT) sono di
# 2026-09-25_known-item-umane. KOSKIDEX e CORPORA cambiano le cartelle.
set -euo pipefail
: "${TESI_RISULTATI:?TESI_RISULTATI non impostata: il risultato non verrebbe archiviato}"
KX=${KOSKIDEX:-$HOME/Desktop/Progetti-personali/Koskidex}
CORPORA=${CORPORA:-$KX/eval/corpora/c3-albo}
[ -z "$(git -C "$KX" status --porcelain)" ] || { echo "Koskidex ha modifiche non committate" >&2; exit 1; }
for modo in any all; do
  for analisi in italian-stopwords italian-stemmer italian; do
    (cd "$KX" && go run ./scripts/evaluate -corpora "$CORPORA" -collection known-item-umane \
      -archivio valutazioni-albo -top 10 -run "ku-$modo-$analisi" \
      -mode "$modo" -scoring bm25 -bm25-espansioni blended -analyzer "$analisi")
  done
done
