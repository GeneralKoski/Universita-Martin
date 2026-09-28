#!/usr/bin/env bash
# Le misure di 2026-09-28_date-importi: Koskidex piatto, recupero congiuntivo e
# punteggio euristico, con il tokenizer di Koskidex e con lo standard,
# ciascuno spento e con -date -importi, sulle collezioni known-item-date,
# known-item-importi e known-item-auto (in eval/corpora/c3-albo di Koskidex,
# copiate da query/ con il corpus beir-metadata). Tre ripetizioni, per il tempo
# di indicizzazione.
#
#   esegui.sh
set -euo pipefail
: "${TESI_RISULTATI:?TESI_RISULTATI non impostata: il risultato non verrebbe archiviato}"
KX=${KOSKIDEX:-$HOME/Desktop/Progetti-personali/Koskidex}
ESP=2026-09-28_date-importi
[ -z "$(git -C "$KX" status --porcelain)" ] || { echo "Koskidex ha modifiche non committate" >&2; exit 1; }
BIN=$(mktemp -d); trap 'rm -rf "$BIN"' EXIT
(cd "$KX" && go build -o "$BIN/evaluate" ./scripts/evaluate)
for r in 1 2 3; do
  for c in known-item-date known-item-importi known-item-auto; do
    for t in koskidex standard; do
      T=(); [ "$t" = standard ] && T=(-tokenizer standard)
      for n in spento acceso; do
        N=(); [ "$n" = acceso ] && N=(-date -importi)
        (cd "$KX" && "$BIN/evaluate" -corpora eval/corpora/c3-albo -collection "$c" -mode all -scoring legacy -top 10 \
          -run "$t-$n-r$r" -archivio "esperimenti/$ESP/evaluate" ${T[@]+"${T[@]}"} ${N[@]+"${N[@]}"} >/dev/null)
      done
    done
  done
  echo "ripetizione $r fatta"
done
