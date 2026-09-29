#!/usr/bin/env bash
# Le esecuzioni di 2026-09-29_reranker-gpu, sul fisso (Windows, Git Bash). Per
# SciFact e NFCorpus: il riordino con strumenti/riordina.py su CUDA in float32 e
# float16, sui primi stadi di 2026-09-28_reranker estratti da git in LF (la loro
# impronta è quella registrata nei rapporti del Mac), rapporti in riordinati/;
# la valutazione con scripts/evaluate -rankings, in evaluate/, anche dei
# rapporti riordinati del Mac con lo stesso binario (run rr-LA-mac).
#
#   esegui.sh
set -euo pipefail
: "${TESI_RISULTATI:?TESI_RISULTATI non impostata: il risultato non verrebbe archiviato}"
KX=${KOSKIDEX:-$HOME/Desktop/GitHub/Koskidex}
PY=${PYTHON_RERANKER:-$HOME/.venvs/tesi-reranker/Scripts/python}
GO=${GO:-go}
QUI=$(cd "$(dirname "$0")" && pwd)
R=$(cd "$QUI/../.." && pwd)
ESP=esperimenti/2026-09-29_reranker-gpu
MAC=esperimenti/2026-09-28_reranker
[ -z "$(git -C "$KX" status --porcelain)" ] || { echo "Koskidex ha modifiche non committate" >&2; exit 1; }
[ -z "$(git -C "$R" status --porcelain -- strumenti/riordina.py "$QUI")" ] || { echo "riordina.py o l'esperimento hanno modifiche non committate" >&2; exit 1; }
export HF_HUB_OFFLINE=1 PYTHONUTF8=1
export TESI_RISULTATI=$(cygpath -m "$TESI_RISULTATI")

BIN=$(mktemp -d); trap 'rm -rf "$BIN"' EXIT
(cd "$KX" && "$GO" build -o "$BIN/evaluate.exe" ./scripts/evaluate)
valuta() {  # collezione, run, rapporto da valutare
  (cd "$KX" && "$BIN/evaluate.exe" -corpora eval/corpora/c1-public -collection "$1" -run "$2" \
    -archivio "$ESP/evaluate" -rankings "$(cygpath -m "$3")" -top 10) | sed -n 's/^archiviato in //p'
}

for c in scifact nfcorpus; do
  primo=$(cd "$R/$MAC/primo-stadio" && ls *_"$c"-rr-primo-LA.json)
  git -C "$R" show "HEAD:./$MAC/primo-stadio/$primo" > "$BIN/$primo"
  mac=$(cd "$R/$MAC/riordinati" && ls *_"$c"-rr-LA.json)
  valuta "$c" rr-LA-mac "$R/$MAC/riordinati/$mac" > /dev/null
  for t in float32 float16; do
    uscita="$TESI_RISULTATI/$ESP/riordinati/$(date -u +%Y-%m-%dT%H%M%SZ)_$c-rr-LA-$t.json"
    "$PY" "$(cygpath -m "$R/strumenti/riordina.py")" --valutazione "$(cygpath -m "$BIN/$primo")" \
      --collezione "$(cygpath -m "$KX/eval/corpora/c1-public/$c")" --uscita "$uscita" --dispositivo cuda --dtype "$t" \
      > "$BIN/riordina-$c-$t.log" 2>&1 || { tail -20 "$BIN/riordina-$c-$t.log" >&2; exit 1; }
    valuta "$c" "rr-LA-$t" "$uscita" > /dev/null
    echo "$c $t fatto"
  done
done
