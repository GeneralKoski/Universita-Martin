#!/usr/bin/env bash
# Le misure di 2026-09-28_ordine-fisso, con il motore del commit corrente di
# Koskidex:
# - scripts/evaluate cinque volte, spento e acceso (-ordine-fisso), su SciFact,
#   NFCorpus e le known-item automatiche, in baseline, bm25-all e bm25-any
#   blended; le ripetizioni si alternano, spento e acceso, per non mettere una
#   deriva della macchina tutta da una parte;
# - le impronte delle 429 query di 2026-09-28_prestazioni sull'indice dell'app
#   (una copia dei dati di Koskidex nativo) con stable_term_order acceso.
#
#   esegui.sh <cartella dati di koskidex nativo>
set -euo pipefail
: "${TESI_RISULTATI:?TESI_RISULTATI non impostata: il risultato non verrebbe archiviato}"
DATI=${1:?cartella dati}
KX=${KOSKIDEX:-$HOME/Desktop/Progetti-personali/Koskidex}
QUI=$(cd "$(dirname "$0")" && pwd)
T=$(cd "$QUI/../../query" && pwd)
ESP=2026-09-28_ordine-fisso
[ -z "$(git -C "$KX" status --porcelain)" ] || { echo "Koskidex ha modifiche non committate" >&2; exit 1; }
LAV=$(mktemp -d); P=
trap '[ -n "$P" ] && kill $P 2>/dev/null; rm -rf "$LAV"' EXIT
V=$(git -C "$KX" rev-parse --short HEAD)
(cd "$KX" && go build -ldflags "-X main.version=$V" -o "$LAV/koskidex" . && go build -o "$LAV/carico" ./scripts/carico \
  && go build -o "$LAV/evaluate" ./scripts/evaluate)

valuta() {  # corpora collezione etichetta, poi le opzioni
  local c=$1 n=$2 e=$3; shift 3
  (cd "$KX" && "$LAV/evaluate" -corpora "$c" -collection "$n" -run "$e" -archivio "esperimenti/$ESP/evaluate" "$@" >/dev/null)
}
for r in 1 2 3 4 5; do
  for ordine in spento acceso; do
    O=(); [ "$ordine" = acceso ] && O=(-ordine-fisso)
    for c in "eval/corpora/c1-public scifact" "eval/corpora/c1-public nfcorpus" "eval/corpora/c3-albo known-item-auto"; do
      set -- $c
      valuta "$1" "$2" "$ordine-baseline-r$r" -mode all -scoring legacy ${O[@]+"${O[@]}"}
      valuta "$1" "$2" "$ordine-bm25-all-r$r" -mode all -scoring bm25 -bm25-espansioni blended ${O[@]+"${O[@]}"}
      valuta "$1" "$2" "$ordine-bm25-any-r$r" -mode any -scoring bm25 -bm25-espansioni blended ${O[@]+"${O[@]}"}
    done
    echo "ripetizione $r, $ordine: fatto"
  done
done

cp -R "$DATI" "$LAV/d"
"$LAV/koskidex" -port 7720 -data-dir "$LAV/d" -log-level warn > "$LAV/log" 2>&1 & P=$!
aspetta() { for _ in $(seq 1 120); do curl -sf http://localhost:7720/health | grep -q '"documents":10018' && return; sleep 1; done; exit 1; }
aspetta
I=search-documents-local
curl -sf "http://localhost:7720/indexes/$I/settings" | python3 -c 'import json,sys; s=json.load(sys.stdin); s["stable_term_order"]=True; print(json.dumps(s))' \
  > "$LAV/impostazioni.json"
curl -sf -X PUT -H 'Content-Type: application/json' --data @"$LAV/impostazioni.json" "http://localhost:7720/indexes/$I/settings" >/dev/null
curl -sf "http://localhost:7720/indexes/$I/settings" | grep -q '"stable_term_order":true' || { echo "impostazione non applicata" >&2; exit 1; }
aspetta
(cd "$KX" && "$LAV/carico" -motore koskidex -url http://localhost:7720 \
  -query "known-item-auto=$KX/eval/corpora/c3-albo/known-item-auto/queries.jsonl" \
  -query "confronto-24=$T/confronto-24/queries.jsonl" -query "umane=$T/known-item-umane/queries.jsonl" \
  -query "verifica=$QUI/../2026-09-28_prestazioni/query-verifica.jsonl" \
  -modo risposte -esperimento "$ESP" -etichetta risposte-acceso-10018)
