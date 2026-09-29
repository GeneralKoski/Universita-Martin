#!/usr/bin/env bash
# Le misure di 2026-09-29_es-corretto: l'indice es-corretto ricreato dal
# contenuto dell'indice dell'app, poi ESC ed ESO sulle quattro collezioni, e
# scripts/evaluate -rankings su ognuna (in evaluate/).
#
#   esegui.sh
set -euo pipefail
: "${TESI_RISULTATI:?TESI_RISULTATI non impostata: il risultato non verrebbe archiviato}"
KX=${KOSKIDEX:-$HOME/Desktop/Progetti-personali/Koskidex}
QUI=$(cd "$(dirname "$0")" && pwd)
R=$(cd "$QUI/../.." && pwd)
ESP=esperimenti/2026-09-29_es-corretto
[ -z "$(git -C "$KX" status --porcelain)" ] || { echo "Koskidex ha modifiche non committate" >&2; exit 1; }
[ -z "$(git -C "$R" status --porcelain -- "$QUI")" ] || { echo "l'esperimento ha modifiche non committate" >&2; exit 1; }
BIN=$(mktemp -d); trap 'rm -rf "$BIN"' EXIT
(cd "$KX" && go build -o "$BIN/evaluate" ./scripts/evaluate)

python3 "$QUI/es-corretto.py" indice
for V in ESC ESO; do
  for C in known-item-auto known-item-date known-item-importi known-item-umane; do
    # Il nome del rapporto delle umane deve contenere known-item-umane: .gitignore lo tiene fuori da git.
    E="es-corretto-$V-$C"; [ "$C" = known-item-umane ] && E="known-item-umane-es-corretto-$V"
    rap=$(python3 "$QUI/es-corretto.py" "$V" "$R/query/$C/queries.txt" "$E")
    [ -n "$rap" ] || { echo "rapporto non scritto per $V $C" >&2; exit 1; }
    (cd "$KX" && "$BIN/evaluate" -corpora "$KX/eval/corpora/c3-albo" -collection "$C" -run "es-corretto-$V" \
      -rankings "$rap" -top 10 -archivio "$ESP/evaluate" >/dev/null)
  done
  echo "$V fatto"
done
