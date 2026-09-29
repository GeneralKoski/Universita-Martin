#!/usr/bin/env bash
# Le esecuzioni di 2026-09-29_riordino-corto: strumenti/riordina.py con k 20 e
# 30 sui primi stadi di 2026-09-28_reranker (i più recenti per ogni caso),
# rapporti in riordinati/, valutazioni con scripts/evaluate -rankings in
# evaluate/.
#
#   esegui.sh
set -euo pipefail
: "${TESI_RISULTATI:?TESI_RISULTATI non impostata: il risultato non verrebbe archiviato}"
KX=${KOSKIDEX:-$HOME/Desktop/Progetti-personali/Koskidex}
PY=${PYTHON_RERANKER:-$HOME/.venvs/tesi-reranker/bin/python}
QUI=$(cd "$(dirname "$0")" && pwd)
R=$(cd "$QUI/../.." && pwd)
ESP=esperimenti/2026-09-29_riordino-corto
PRIMO=$R/esperimenti/2026-09-28_reranker/primo-stadio
[ -z "$(git -C "$KX" status --porcelain)" ] || { echo "Koskidex ha modifiche non committate" >&2; exit 1; }
[ -z "$(git -C "$R" status --porcelain -- strumenti/riordina.py "$QUI")" ] || { echo "riordina.py o l'esperimento hanno modifiche non committate" >&2; exit 1; }
[ -e "$KX/eval/corpora/c3-albo/known-item-umane/queries.jsonl" ] || { echo "manca la collezione: collezioni-umane.py" >&2; exit 1; }
export HF_HUB_OFFLINE=1

BIN=$(mktemp -d); trap 'rm -rf "$BIN"' EXIT
(cd "$KX" && go build -o "$BIN/evaluate" ./scripts/evaluate)
for caso in known-item-umane:LA known-item-umane:A known-item-auto:LA; do
  C=${caso%%:*}; CONF=${caso##*:}
  primo=$(ls "$PRIMO"/*_"$C"-rr-primo-"$CONF".json | tail -1)
  for K in 20 30; do
    uscita="$TESI_RISULTATI/$ESP/riordinati/$(date -u +%Y-%m-%dT%H%M%SZ)_$C-rr$K-$CONF.json"
    "$PY" "$R/strumenti/riordina.py" --valutazione "$primo" --collezione "$KX/eval/corpora/c3-albo/$C" --uscita "$uscita" \
      --k "$K" > "$BIN/riordina.log" 2>&1 || { tail -20 "$BIN/riordina.log" >&2; exit 1; }
    (cd "$KX" && "$BIN/evaluate" -corpora eval/corpora/c3-albo -collection "$C" -run "rr$K-$CONF" -rankings "$uscita" \
      -top 10 -archivio "$ESP/evaluate" >/dev/null)
    echo "$C $CONF k $K fatto"
  done
done
