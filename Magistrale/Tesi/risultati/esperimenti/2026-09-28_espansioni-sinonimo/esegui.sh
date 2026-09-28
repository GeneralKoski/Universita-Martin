#!/usr/bin/env bash
# Le valutazioni di 2026-09-28_espansioni-sinonimo: scripts/evaluate con BM25
# all e any, blended contro synonym, su SciFact, NFCorpus e le known-item
# automatiche; su SciFact e NFCorpus anche any con le stopword; ogni
# configurazione synonym anche con -ordine-fisso.
#
#   esegui.sh
set -euo pipefail
: "${TESI_RISULTATI:?TESI_RISULTATI non impostata: il risultato non verrebbe archiviato}"
KX=${KOSKIDEX:-$HOME/Desktop/Progetti-personali/Koskidex}
ESP=2026-09-28_espansioni-sinonimo
[ -z "$(git -C "$KX" status --porcelain)" ] || { echo "Koskidex ha modifiche non committate" >&2; exit 1; }
BIN=$(mktemp -d); trap 'rm -rf "$BIN"' EXIT
(cd "$KX" && go build -o "$BIN/evaluate" ./scripts/evaluate)
valuta() {  # corpora collezione etichetta opzioni...
  local c=$1 n=$2 e=$3; shift 3
  (cd "$KX" && "$BIN/evaluate" -corpora "$c" -collection "$n" -scoring bm25 -run "$e" -archivio "esperimenti/$ESP/evaluate" "$@" >/dev/null)
}
for c in "eval/corpora/c1-public scifact" "eval/corpora/c1-public nfcorpus" "eval/corpora/c3-albo known-item-auto"; do
  set -- $c
  for m in all any; do
    valuta "$1" "$2" "$m-blended" -mode $m -bm25-espansioni blended
    valuta "$1" "$2" "$m-synonym" -mode $m -bm25-espansioni synonym
    valuta "$1" "$2" "$m-synonym-ordine" -mode $m -bm25-espansioni synonym -ordine-fisso
  done
  if [ "$2" != known-item-auto ]; then
    valuta "$1" "$2" "any-stopwords-blended" -mode any -analyzer stopwords -bm25-espansioni blended
    valuta "$1" "$2" "any-stopwords-synonym" -mode any -analyzer stopwords -bm25-espansioni synonym
    valuta "$1" "$2" "any-stopwords-synonym-ordine" -mode any -analyzer stopwords -bm25-espansioni synonym -ordine-fisso
  fi
  echo "$2 fatto"
done
