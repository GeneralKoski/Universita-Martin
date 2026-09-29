#!/usr/bin/env bash
# Le misure di 2026-09-29_profilo-completo: Koskidex del commit corrente,
# nativo, un indice vuoto per profilo riempito dall'app con
# KOSKIDEX_PROFILO=consigliata e le variabili del profilo (README). Per ognuno:
# l'indicizzazione (indicizza-koskidex.sh, il tempo va in confronto/), le
# impostazioni rilette dall'indice, poi dall'app le query di cinque
# collezioni, e scripts/evaluate -rankings sulle quattro con i giudizi.
#
#   esegui.sh [profilo ...]     (P0 P1 P2 P3 P4 se non se ne danno)
#
# Serve Ollama con bge-m3 per P3 e P4. I vettori degli atti calcolati
# indicizzando P3, prima di ogni query, si riusano per P4: i vettori delle
# query si calcolano da capo in tutti e due.
set -euo pipefail
: "${TESI_RISULTATI:?TESI_RISULTATI non impostata: il risultato non verrebbe archiviato}"
KX=${KOSKIDEX:-$HOME/Desktop/Progetti-personali/Koskidex}
APP=$HOME/Desktop/Dieffetech/Documentale/apps/laravel
QUI=$(cd "$(dirname "$0")" && pwd)
R=$(cd "$QUI/../.." && pwd)
CORPORA=$KX/eval/corpora/c3-albo
ESP=esperimenti/2026-09-29_profilo-completo
PROFILI=("$@"); [ ${#PROFILI[@]} -gt 0 ] || PROFILI=(P0 P1 P2 P3 P4)
[ -z "$(git -C "$KX" status --porcelain)" ] || { echo "Koskidex ha modifiche non committate" >&2; exit 1; }
[ -z "$(git -C "$APP" status --porcelain)" ] || { echo "Documentale ha modifiche non committate" >&2; exit 1; }
[ -e "$CORPORA/known-item-umane/queries.jsonl" ] || { echo "manca la collezione known-item-umane: collezioni-umane.py" >&2; exit 1; }

BIN=$(mktemp -d); PID=
trap '[ -n "$PID" ] && kill $PID 2>/dev/null; wait 2>/dev/null || true; rm -rf "$BIN"' EXIT
(cd "$KX" && go build -o "$BIN/koskidex" . && go build -o "$BIN/evaluate" ./scripts/evaluate)

export DB_HOST=127.0.0.1 DB_PORT=33061 DB_DATABASE=albo DB_USERNAME=root DB_PASSWORD=root TELESCOPE_ENABLED=false
export SEARCH_BACKEND=koskidex KOSKIDEX_HOST=http://localhost:7717 KOSKIDEX_PROFILO=consigliata KOSKIDEX_TIMEOUT=1800

domande() {  # file di query, etichetta: stampa il percorso del rapporto archiviato
  (cd "$APP" && php -d memory_limit=1G artisan app:eval-run-queries --no-ansi "$1" --label="$2") | sed -n 's/^Archiviato in //p'
}
valuta() {  # collezione, run, rapporto
  [ -n "$3" ] || { echo "rapporto dell'app non trovato per $1" >&2; exit 1; }
  (cd "$KX" && "$BIN/evaluate" -corpora "$CORPORA" -collection "$1" -run "$2" -rankings "$3" -top 10 \
    -archivio "$ESP/evaluate" >/dev/null)
}
variabili() {  # profilo: le variabili in più, una per riga
  local numeri="KOSKIDEX_NORMALIZE_DATES=true KOSKIDEX_NORMALIZE_AMOUNTS=true KOSKIDEX_TYPOS_ON_AMOUNTS=false"
  local vettori="KOSKIDEX_EMBEDDER_MODEL=bge-m3 KOSKIDEX_HYBRID_MODE=union"
  case "$1" in
    P0) ;;
    P1) echo $numeri ;;
    P2) echo $numeri KOSKIDEX_RETRIEVAL_MODE=any KOSKIDEX_SCORING=bm25 KOSKIDEX_STABLE_TERM_ORDER=true ;;
    P3) echo $numeri KOSKIDEX_RETRIEVAL_MODE=any KOSKIDEX_SCORING=bm25 KOSKIDEX_STABLE_TERM_ORDER=true $vettori KOSKIDEX_VECTOR_WEIGHT=160 ;;
    P4) echo $numeri KOSKIDEX_SCORING=bm25 KOSKIDEX_STABLE_TERM_ORDER=true $vettori KOSKIDEX_VECTOR_WEIGHT=10 ;;
    *) echo "profilo sconosciuto: $1" >&2; exit 1 ;;
  esac
}

for P in "${PROFILI[@]}"; do
  V=$(variabili "$P")
  mkdir "$BIN/dati-$P"
  [ -e "$BIN/embeddings.jsonl" ] && case "$V" in *EMBEDDER*) cp "$BIN/embeddings.jsonl" "$BIN/dati-$P/" ;; esac
  "$BIN/koskidex" -port 7717 -data-dir "$BIN/dati-$P" -log-level warn > "$BIN/log-$P" 2>&1 &
  PID=$!
  for _ in $(seq 1 30); do curl -sf http://localhost:7717/health >/dev/null && break; sleep 1; done
  (
    unset KOSKIDEX_NORMALIZE_DATES KOSKIDEX_NORMALIZE_AMOUNTS KOSKIDEX_TYPOS_ON_AMOUNTS KOSKIDEX_RETRIEVAL_MODE \
      KOSKIDEX_SCORING KOSKIDEX_STABLE_TERM_ORDER KOSKIDEX_EMBEDDER_MODEL KOSKIDEX_HYBRID_MODE KOSKIDEX_VECTOR_WEIGHT
    for v in $V; do export "$v"; done
    "$R/strumenti/indicizza-koskidex.sh" albo "profilo-completo-$P" http://localhost:7717 >/dev/null
    [ -e "$BIN/embeddings.jsonl" ] || [ ! -e "$BIN/dati-$P/embeddings.jsonl" ] || cp "$BIN/dati-$P/embeddings.jsonl" "$BIN/"
    curl -sf "http://localhost:7717/indexes/search-documents-local/settings" > "$BIN/impostazioni-$P.json"
    python3 -c "import json,sys;s=json.load(open(sys.argv[1]));print('$P', {k:s.get(k) for k in ('retrieval_mode','scoring_mode','bm25_k1','bm25_b','bm25_expansion','stable_term_order','hybrid_mode','vector_weight','normalize_dates','normalize_amounts','all_terms_in_one_field')}, s['typo_tolerance'].get('disable_on_numbers'), s['typo_tolerance'].get('disable_on_amounts'), s.get('embedder',{}).get('model'))" "$BIN/impostazioni-$P.json"
    for C in known-item-auto known-item-date known-item-importi; do
      valuta "$C" "profilo-completo-$P" "$(domande "$R/query/$C/queries.txt" "profilo-completo-$P-$C")"
    done
    # Il nome del rapporto deve contenere known-item-umane: .gitignore lo tiene fuori da git.
    valuta known-item-umane "profilo-completo-$P" "$(domande "$R/query/known-item-umane/queries.txt" "known-item-umane-profilo-completo-$P")"
    domande "$R/query/confronto-24.txt" "profilo-completo-$P-confronto-24" > /dev/null
  )
  kill $PID; wait $PID 2>/dev/null || true; PID=
  echo "$P fatto"
done
