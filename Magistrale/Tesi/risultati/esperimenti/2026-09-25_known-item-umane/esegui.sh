#!/usr/bin/env bash
# Le esecuzioni di 2026-09-25_known-item-umane, a raccolta chiusa (dopo
# importa-raccolta.py e collezioni-umane.py). Koskidex e Documentale da alberi
# puliti; tutto finisce nell'archivio di TESI_RISULTATI.
#
#   esegui.sh piatte    le sei configurazioni di Koskidex piatto
#   esegui.sh app       Elasticsearch di produzione e Koskidex consigliata, dall'app
#   esegui.sh           tutte e due
#
# KOSKIDEX, CORPORA e QUERY cambiano le cartelle (per le prove su dati inventati).
set -euo pipefail
: "${TESI_RISULTATI:?TESI_RISULTATI non impostata: il risultato non verrebbe archiviato}"
KX=${KOSKIDEX:-$HOME/Desktop/Progetti-personali/Koskidex}
CORPORA=${CORPORA:-$KX/eval/corpora/c3-albo}
Q=${QUERY:-$(cd "$(dirname "$0")/../../query/known-item-umane" && pwd)}
APP=$HOME/Desktop/Dieffetech/Documentale/apps/laravel
STRUMENTI=$(cd "$(dirname "$0")/../../strumenti" && pwd)
COSA=${1:-tutte}

[ -z "$(git -C "$KX" status --porcelain)" ] || { echo "Koskidex ha modifiche non committate" >&2; exit 1; }

valuta() {
  local run=$1; shift
  (cd "$KX" && go run ./scripts/evaluate -corpora "$CORPORA" -collection known-item-umane \
    -archivio valutazioni-albo -top 10 -run "$run" "$@")
}

if [ "$COSA" != app ]; then
  valuta ku-K0 -mode all -scoring legacy
  valuta ku-LA -mode any -scoring bm25 -bm25-espansioni blended
  valuta ku-LT -mode all -scoring bm25 -bm25-espansioni blended
  valuta ku-A -mode any -scoring bm25 -bm25-espansioni blended -embedder bge-m3 -ibrido union -peso-vettore 160
  valuta ku-B -mode all -scoring bm25 -bm25-espansioni blended -embedder bge-m3 -ibrido union -peso-vettore 10
  valuta ku-V -mode any -scoring bm25 -bm25-espansioni blended -embedder bge-m3 -ibrido vector
fi

if [ "$COSA" != piatte ]; then
  [ -z "$(git -C "$APP" status --porcelain)" ] || { echo "Documentale ha modifiche non committate" >&2; exit 1; }
  export DB_HOST=127.0.0.1 DB_PORT=33061 DB_DATABASE=albo DB_USERNAME=root DB_PASSWORD=root TELESCOPE_ENABLED=false
  unset KOSKIDEX_EMBEDDER_MODEL SEARCH_BACKEND KOSKIDEX_HOST KOSKIDEX_PROFILO

  domande() {  # esegue le query dall'app e stampa il percorso del rapporto archiviato
    (cd "$APP" && php -d memory_limit=1G artisan app:eval-run-queries "$Q/queries.txt" --label="$1") \
      | tee /dev/stderr | sed -n 's/^Archiviato in //p'
  }

  rapporto=$(domande known-item-umane)
  valuta ku-app-elasticsearch -rankings "$rapporto"

  BIN=$(mktemp -d)
  (cd "$KX" && go build -o "$BIN/koskidex" .)
  "$BIN/koskidex" -port 7711 -data-dir "$BIN/data" -log-level warn &
  PID=$!
  trap 'kill $PID 2>/dev/null; rm -rf "$BIN"' EXIT
  sleep 2
  export SEARCH_BACKEND=koskidex KOSKIDEX_HOST=http://localhost:7711 KOSKIDEX_PROFILO=consigliata
  "$STRUMENTI/indicizza-koskidex.sh" albo known-item-umane-consigliata http://localhost:7711
  rapporto=$(domande known-item-umane-consigliata)
  valuta ku-app-koskidex-consigliata -rankings "$rapporto"
fi
