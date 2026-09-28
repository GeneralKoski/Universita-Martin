#!/usr/bin/env bash
# Le esecuzioni di 2026-09-28_reranker. Per ogni collezione: il primo stadio con
# scripts/evaluate -top 100 (archiviato in primo-stadio/), il riordino con
# strumenti/riordina.py nell'ambiente ~/.venvs/tesi-reranker (rapporto in
# riordinati/), la valutazione del riordino con scripts/evaluate -rankings
# (in evaluate/).
#
#   esegui.sh beir     SciFact, NFCorpus, known-item automatiche
#   esegui.sh umane    known-item umane, a raccolta chiusa (dopo collezioni-umane.py)
set -euo pipefail
: "${TESI_RISULTATI:?TESI_RISULTATI non impostata: il risultato non verrebbe archiviato}"
KX=${KOSKIDEX:-$HOME/Desktop/Progetti-personali/Koskidex}
PY=${PYTHON_RERANKER:-$HOME/.venvs/tesi-reranker/bin/python}
QUI=$(cd "$(dirname "$0")" && pwd)
R=$(cd "$QUI/../.." && pwd)
ESP=esperimenti/2026-09-28_reranker
COSA=${1:?beir o umane}
[ -z "$(git -C "$KX" status --porcelain)" ] || { echo "Koskidex ha modifiche non committate" >&2; exit 1; }
[ -z "$(git -C "$R" status --porcelain -- strumenti/riordina.py "$QUI")" ] || { echo "riordina.py o l'esperimento hanno modifiche non committate" >&2; exit 1; }
export HF_HUB_OFFLINE=1

BIN=$(mktemp -d); trap 'rm -rf "$BIN"' EXIT
(cd "$KX" && go build -o "$BIN/evaluate" ./scripts/evaluate)
valuta() {  # corpora, collezione, run, archivio, argomenti: stampa il file archiviato
  local corpora=$1 collezione=$2 run=$3 archivio=$4; shift 4
  (cd "$KX" && "$BIN/evaluate" -corpora "$corpora" -collection "$collezione" -run "$run" -archivio "$ESP/$archivio" "$@") \
    | sed -n 's/^archiviato in //p'
}
riordina() {  # corpora, collezione, configurazione, argomenti del primo stadio
  local corpora=$1 collezione=$2 conf=$3; shift 3
  local primo uscita
  primo=$(valuta "$corpora" "$collezione" "rr-primo-$conf" primo-stadio -top 100 "$@")
  uscita="$TESI_RISULTATI/$ESP/riordinati/$(date -u +%Y-%m-%dT%H%M%SZ)_$collezione-rr-$conf.json"
  "$PY" "$R/strumenti/riordina.py" --valutazione "$primo" --collezione "$KX/$corpora/$collezione" --uscita "$uscita" \
    > "$BIN/riordina-$collezione-$conf.log" 2>&1 || { tail -20 "$BIN/riordina-$collezione-$conf.log" >&2; exit 1; }
  valuta "$corpora" "$collezione" "rr-$conf" evaluate -rankings "$uscita" -top 10 > /dev/null
  echo "$collezione $conf fatto"
}

LA=(-mode any -scoring bm25 -bm25-espansioni blended)
if [ "$COSA" = beir ]; then
  riordina eval/corpora/c1-public scifact LA "${LA[@]}" -analyzer stopwords
  riordina eval/corpora/c1-public nfcorpus LA "${LA[@]}" -analyzer stopwords
  riordina eval/corpora/c3-albo known-item-auto LA "${LA[@]}"
  valuta eval/corpora/c3-albo known-item-auto rr-primo-LT primo-stadio -top 100 -mode all -scoring bm25 -bm25-espansioni blended > /dev/null
elif [ "$COSA" = umane ]; then
  [ -e "$KX/eval/corpora/c3-albo/known-item-umane/queries.jsonl" ] || { echo "manca la collezione: collezioni-umane.py" >&2; exit 1; }
  riordina eval/corpora/c3-albo known-item-umane LA "${LA[@]}"
  riordina eval/corpora/c3-albo known-item-umane A "${LA[@]}" -embedder bge-m3 -ibrido union -peso-vettore 160
else
  echo "beir o umane" >&2; exit 1
fi
