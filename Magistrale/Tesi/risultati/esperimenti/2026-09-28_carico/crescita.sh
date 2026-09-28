#!/usr/bin/env bash
# La misura 3 di 2026-09-28_carico: gli stessi atti copiati fino a 50.000 e
# 100.000 documenti (copia.py), per ogni dimensione e per ogni motore: copia,
# riavvio, memoria a riposo, ricerche una alla volta sull'indice copiato.
# Elasticsearch nel suo container (l'indice copiato si aggiunge a quello
# dell'app, poi si cancella); Koskidex in un container nuovo per dimensione,
# con il solo indice copiato, dallo stesso binario di kosk-carico.
#
#   crescita.sh <cartella del binario linux di koskidex>
set -euo pipefail
: "${TESI_RISULTATI:?TESI_RISULTATI non impostata: il risultato non verrebbe archiviato}"
KBIN=${1:?cartella con il binario linux koskidex}
KX=${KOSKIDEX:-$HOME/Desktop/Progetti-personali/Koskidex}
QUI=$(cd "$(dirname "$0")" && pwd)
T=$(cd "$QUI/../../query" && pwd)
Q=(-query "known-item-auto=$KX/eval/corpora/c3-albo/known-item-auto/queries.jsonl"
   -query "confronto-24=$T/confronto-24/queries.jsonl"
   -query "umane=$T/known-item-umane/queries.jsonl")
[ -z "$(git -C "$KX" status --porcelain)" ] || { echo "Koskidex ha modifiche non committate" >&2; exit 1; }
BIN=$(mktemp -d); trap 'rm -rf "$BIN"' EXIT
(cd "$KX" && go build -o "$BIN/carico" ./scripts/carico)
carico() { (cd "$KX" && "$BIN/carico" "$@"); }
aspetta() {  # url, testo atteso nella risposta
  for _ in $(seq 1 180); do curl -sf "$1" | grep -q "$2" && return; sleep 1; done
  echo "$1 non risponde come atteso" >&2; exit 1
}

# La base, 10.018 atti come li ha dati l'app, a riposo dopo un riavvio come le
# dimensioni copiate (le ricerche una alla volta a questa dimensione sono
# quelle di esegui.sh).
docker restart doc-tesi-es >/dev/null
aspetta "http://localhost:9201/_cluster/health?wait_for_status=yellow&timeout=1s" '"status"'
carico -motore es -url http://localhost:9201 -container doc-tesi-es "${Q[@]}" -modo riposo -durata 20s -etichetta riposo-es-10018
docker restart kosk-carico >/dev/null
aspetta http://localhost:7713/health '"documents":10018'
carico -motore koskidex -url http://localhost:7713 -container kosk-carico "${Q[@]}" -modo riposo -durata 20s \
  -etichetta riposo-koskidex-docker-10018

for N in 50000 100000; do
  python3 "$QUI/copia.py" es http://localhost:9201 search-documents-local "carico-$N" "$N"
  docker restart doc-tesi-es >/dev/null
  aspetta "http://localhost:9201/_cluster/health?wait_for_status=yellow&timeout=1s" '"status"'
  carico -motore es -url http://localhost:9201 -container doc-tesi-es -indice "carico-$N" "${Q[@]}" \
    -modo riposo -durata 20s -etichetta "riposo-es-$N"
  carico -motore es -url http://localhost:9201 -container doc-tesi-es -indice "carico-$N" "${Q[@]}" \
    -modo sequenziale -etichetta "seq-es-app-$N"
  curl -sf -X DELETE "http://localhost:9201/carico-$N" >/dev/null

  DATI=$(mktemp -d); C="kosk-$N"
  docker rm -f "$C" >/dev/null 2>&1 || true
  docker run -d --name "$C" -p 7715:7700 -v "$KBIN:/k:ro" -v "$DATI:/dati" alpine:latest \
    /k/koskidex --port 7700 --data-dir /dati --log-level warn >/dev/null
  aspetta http://localhost:7715/health '"status":"ok"'
  python3 "$QUI/copia.py" koskidex http://localhost:7715 search-documents-local "carico-$N" "$N" "$DATI" http://localhost:7713 \
    || { echo "copia.py koskidex fallita" >&2; exit 1; }
  docker restart "$C" >/dev/null
  aspetta http://localhost:7715/health "\"documents\":$N"
  carico -motore koskidex -url http://localhost:7715 -container "$C" -indice "carico-$N" "${Q[@]}" \
    -modo riposo -durata 20s -etichetta "riposo-koskidex-docker-$N"
  carico -motore koskidex -url http://localhost:7715 -container "$C" -indice "carico-$N" "${Q[@]}" \
    -modo sequenziale -etichetta "seq-koskidex-docker-$N"
  docker rm -f "$C" >/dev/null; rm -rf "$DATI"
done
