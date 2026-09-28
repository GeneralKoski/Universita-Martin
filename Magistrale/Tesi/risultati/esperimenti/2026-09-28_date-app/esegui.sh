#!/usr/bin/env bash
# Le misure di 2026-09-28_date-app: Koskidex del commit corrente, un indice
# vuoto riempito dall'app con KOSKIDEX_PROFILO=consigliata, spento (nessun'altra
# variabile) e acceso (KOSKIDEX_NORMALIZE_DATES e KOSKIDEX_NORMALIZE_AMOUNTS).
# Per ciascuno: tre indicizzazioni complete (indicizza-koskidex.sh, il tempo va
# in confronto/), poi dall'app le query di cinque collezioni, e scripts/evaluate
# -rankings sulle quattro con i giudizi.
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
ESP=esperimenti/2026-09-28_date-app
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
unset KOSKIDEX_EMBEDDER_MODEL KOSKIDEX_NORMALIZE_DATES KOSKIDEX_NORMALIZE_AMOUNTS

domande() {  # file di query, etichetta: stampa il percorso del rapporto archiviato
  (cd "$APP" && php -d memory_limit=1G artisan app:eval-run-queries "$1" --label="$2") | sed -n 's/^Archiviato in //p'
}
valuta() {  # collezione, run, rapporto
  (cd "$KX" && "$BIN/evaluate" -corpora "$CORPORA" -collection "$1" -run "$2" -rankings "$3" -top 10 \
    -archivio "$ESP/evaluate" >/dev/null)
}

for FASE in spento acceso; do
  if [ "$FASE" = acceso ]; then export KOSKIDEX_NORMALIZE_DATES=true KOSKIDEX_NORMALIZE_AMOUNTS=true; fi
  for i in 1 2 3; do
    "$R/strumenti/indicizza-koskidex.sh" albo "date-app-$FASE" http://localhost:7712 >/dev/null
  done
  curl -sf "http://localhost:7712/indexes/search-documents-local/settings" > "$BIN/impostazioni-$FASE.json"
  python3 -c "import json,sys;s=json.load(open(sys.argv[1]));print('$FASE', {k:s.get(k) for k in ('normalize_dates','normalize_amounts','tokenizer','all_terms_in_one_field')})" "$BIN/impostazioni-$FASE.json"
  for C in known-item-auto known-item-date known-item-importi; do
    valuta "$C" "date-app-$FASE" "$(domande "$R/query/$C/queries.txt" "date-app-$FASE-$C")"
  done
  # Il nome del rapporto deve contenere known-item-umane: .gitignore lo tiene fuori da git.
  valuta known-item-umane "date-app-$FASE" "$(domande "$R/query/known-item-umane/queries.txt" "known-item-umane-date-app-$FASE")"
  domande "$R/query/confronto-24.txt" "date-app-$FASE-confronto-24" > /dev/null
  echo "$FASE fatto"
done
