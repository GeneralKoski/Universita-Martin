#!/usr/bin/env bash
# Le misure di 2026-09-28_importi-esatti: Koskidex del commit corrente, un
# indice vuoto riempito dall'app con KOSKIDEX_PROFILO=consigliata in quattro
# configurazioni: A il profilo, B più KOSKIDEX_NORMALIZE_AMOUNTS, C più
# KOSKIDEX_TYPOS_ON_AMOUNTS=false, D più tutti e due. Per ciascuna: una
# indicizzazione completa (indicizza-koskidex.sh), poi dall'app le query di
# cinque collezioni, e scripts/evaluate -rankings sulle quattro con i giudizi.
#
#   esegui.sh
#
# Prima: collezioni-umane.py (la collezione known-item-umane in Koskidex).
set -euo pipefail
: "${TESI_RISULTATI:?TESI_RISULTATI non impostata: il risultato non verrebbe archiviato}"
KX=${KOSKIDEX:-$HOME/Desktop/Progetti-personali/Koskidex}
APP=$HOME/Desktop/Dieffetech/Documentale/apps/laravel
QUI=$(cd "$(dirname "$0")" && pwd)
R=$(cd "$QUI/../.." && pwd)
CORPORA=$KX/eval/corpora/c3-albo
ESP=esperimenti/2026-09-28_importi-esatti
[ -z "$(git -C "$KX" status --porcelain)" ] || { echo "Koskidex ha modifiche non committate" >&2; exit 1; }
[ -z "$(git -C "$APP" status --porcelain)" ] || { echo "Documentale ha modifiche non committate" >&2; exit 1; }
[ -e "$CORPORA/known-item-umane/queries.jsonl" ] || { echo "manca la collezione known-item-umane: collezioni-umane.py" >&2; exit 1; }

BIN=$(mktemp -d)
(cd "$KX" && go build -o "$BIN/koskidex" . && go build -o "$BIN/evaluate" ./scripts/evaluate)
"$BIN/koskidex" -port 7712 -data-dir "$BIN/data" -log-level warn > "$BIN/log" 2>&1 &
PID=$!
trap 'kill $PID 2>/dev/null; rm -rf "$BIN"' EXIT
for _ in $(seq 1 30); do curl -sf http://localhost:7712/health >/dev/null && break; sleep 1; done

export DB_HOST=127.0.0.1 DB_PORT=33061 DB_DATABASE=albo DB_USERNAME=root DB_PASSWORD=root TELESCOPE_ENABLED=false
export SEARCH_BACKEND=koskidex KOSKIDEX_HOST=http://localhost:7712 KOSKIDEX_PROFILO=consigliata
unset KOSKIDEX_EMBEDDER_MODEL KOSKIDEX_NORMALIZE_DATES KOSKIDEX_NORMALIZE_AMOUNTS KOSKIDEX_TYPOS_ON_AMOUNTS

domande() {  # file di query, etichetta: stampa il percorso del rapporto archiviato
  (cd "$APP" && php -d memory_limit=1G artisan app:eval-run-queries "$1" --label="$2") | sed -n 's/^Archiviato in //p'
}
valuta() {  # collezione, run, rapporto
  (cd "$KX" && "$BIN/evaluate" -corpora "$CORPORA" -collection "$1" -run "$2" -rankings "$3" -top 10 \
    -archivio "$ESP/evaluate" >/dev/null)
}

for FASE in A B C D; do
  unset KOSKIDEX_NORMALIZE_AMOUNTS KOSKIDEX_TYPOS_ON_AMOUNTS
  case "$FASE" in
    B) export KOSKIDEX_NORMALIZE_AMOUNTS=true ;;
    C) export KOSKIDEX_TYPOS_ON_AMOUNTS=false ;;
    D) export KOSKIDEX_NORMALIZE_AMOUNTS=true KOSKIDEX_TYPOS_ON_AMOUNTS=false ;;
  esac
  "$R/strumenti/indicizza-koskidex.sh" albo "importi-esatti-$FASE" http://localhost:7712 >/dev/null
  curl -sf "http://localhost:7712/indexes/search-documents-local/settings" > "$BIN/impostazioni-$FASE.json"
  python3 -c "import json,sys;s=json.load(open(sys.argv[1]));print('$FASE', s.get('normalize_amounts'), s.get('typo_tolerance'))" "$BIN/impostazioni-$FASE.json"
  for C in known-item-importi known-item-date known-item-auto; do
    valuta "$C" "importi-esatti-$FASE" "$(domande "$R/query/$C/queries.txt" "importi-esatti-$FASE-$C")"
  done
  # Il nome del rapporto deve contenere known-item-umane: .gitignore lo tiene fuori da git.
  valuta known-item-umane "importi-esatti-$FASE" "$(domande "$R/query/known-item-umane/queries.txt" "known-item-umane-importi-esatti-$FASE")"
  domande "$R/query/confronto-24.txt" "importi-esatti-$FASE-confronto-24" > /dev/null
  echo "$FASE fatto"
done
