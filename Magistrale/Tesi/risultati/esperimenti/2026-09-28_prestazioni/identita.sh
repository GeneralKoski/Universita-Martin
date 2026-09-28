#!/usr/bin/env bash
# Le prove di identità di 2026-09-28_prestazioni, per la fase "prima" o "dopo":
# il motore del commit corrente di Koskidex, nativo, sui dati che l'app ha
# indicizzato il 28/09 (Koskidex nativo di 2026-09-28_carico), poi su una copia
# da 100.000 documenti; impronte di tutte le risposte; scripts/evaluate su tre
# collezioni in tre configurazioni.
#
#   identita.sh prima|dopo <cartella dati di koskidex nativo>
#
# ESPERIMENTO cambia la cartella dell'archivio (2026-09-28_allocazioni lo usa
# per le sue prove).
set -euo pipefail
: "${TESI_RISULTATI:?TESI_RISULTATI non impostata: il risultato non verrebbe archiviato}"
FASE=${1:?prima o dopo}; DATI=${2:?cartella dati}
KX=${KOSKIDEX:-$HOME/Desktop/Progetti-personali/Koskidex}
QUI=$(cd "$(dirname "$0")" && pwd)
T=$(cd "$QUI/../../query" && pwd)
ESP=${ESPERIMENTO:-2026-09-28_prestazioni}
[ -z "$(git -C "$KX" status --porcelain)" ] || { echo "Koskidex ha modifiche non committate" >&2; exit 1; }
LAV=$(mktemp -d); trap 'kill $P1 $P2 2>/dev/null || true; rm -rf "$LAV"' EXIT
V=$(git -C "$KX" rev-parse --short HEAD)
(cd "$KX" && go build -ldflags "-X main.version=$V" -o "$LAV/koskidex" . && go build -o "$LAV/carico" ./scripts/carico \
  && go build -o "$LAV/evaluate" ./scripts/evaluate)
Q=(-query "known-item-auto=$KX/eval/corpora/c3-albo/known-item-auto/queries.jsonl"
   -query "confronto-24=$T/confronto-24/queries.jsonl" -query "umane=$T/known-item-umane/queries.jsonl"
   -query "verifica=$QUI/query-verifica.jsonl")
aspetta() { for _ in $(seq 1 120); do curl -sf "$1/health" | grep -q "\"documents\":$2" && return; sleep 1; done; exit 1; }

cp -R "$DATI" "$LAV/d10"
"$LAV/koskidex" -port 7720 -data-dir "$LAV/d10" -log-level warn > "$LAV/l1" 2>&1 & P1=$!
aspetta http://localhost:7720 10018
(cd "$KX" && "$LAV/carico" -motore koskidex -url http://localhost:7720 "${Q[@]}" -modo risposte \
  -esperimento "$ESP" -etichetta "risposte-$FASE-10018")

mkdir "$LAV/d100"
"$LAV/koskidex" -port 7721 -data-dir "$LAV/d100" -log-level warn > "$LAV/l2" 2>&1 & P2=$!
for _ in $(seq 1 60); do curl -sf http://localhost:7721/health >/dev/null && break; sleep 1; done
# La copia è solo preparazione: il suo esito va in una cartella temporanea.
TESI_RISULTATI="$LAV/scarto" python3 "$QUI/../2026-09-28_carico/copia.py" koskidex http://localhost:7721 \
  search-documents-local search-documents-local 100000 "$LAV/d100" http://localhost:7720 >/dev/null
(cd "$KX" && "$LAV/carico" -motore koskidex -url http://localhost:7721 "${Q[@]}" -modo risposte \
  -esperimento "$ESP" -etichetta "risposte-$FASE-100000")

for c in "eval/corpora/c1-public scifact" "eval/corpora/c1-public nfcorpus" "eval/corpora/c3-albo known-item-auto"; do
  set -- $c
  (cd "$KX" && "$LAV/evaluate" -corpora "$1" -collection "$2" -run "$FASE-baseline" -mode all -scoring legacy \
     -archivio "esperimenti/$ESP/evaluate" >/dev/null
   "$LAV/evaluate" -corpora "$1" -collection "$2" -run "$FASE-bm25-all" -mode all -scoring bm25 -bm25-espansioni blended \
     -archivio "esperimenti/$ESP/evaluate" >/dev/null
   "$LAV/evaluate" -corpora "$1" -collection "$2" -run "$FASE-bm25-any" -mode any -scoring bm25 -bm25-espansioni blended \
     -archivio "esperimenti/$ESP/evaluate" >/dev/null)
  echo "evaluate $2 fatto"
done
