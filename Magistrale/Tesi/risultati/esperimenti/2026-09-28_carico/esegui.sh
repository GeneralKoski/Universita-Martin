#!/usr/bin/env bash
# Le misure di 2026-09-28_carico. Presuppone i motori già avviati e riempiti
# dall'app (vedi README): Elasticsearch su 9201 (container doc-tesi-es),
# Koskidex nel container kosk-carico su 7713, Koskidex nativo su 7714.
#
#   esegui.sh sequenziale | carico | riposo | tutto
#
# KOSKIDEX cambia la cartella del motore; K_NATIVO_PID è il processo nativo.
set -euo pipefail
: "${TESI_RISULTATI:?TESI_RISULTATI non impostata: il risultato non verrebbe archiviato}"
KX=${KOSKIDEX:-$HOME/Desktop/Progetti-personali/Koskidex}
T=$(cd "$(dirname "$0")/../../query" && pwd)
COSA=${1:-tutto}
Q=(-query "known-item-auto=$KX/eval/corpora/c3-albo/known-item-auto/queries.jsonl"
   -query "confronto-24=$T/confronto-24/queries.jsonl"
   -query "umane=$T/known-item-umane/queries.jsonl")
[ -z "$(git -C "$KX" status --porcelain)" ] || { echo "Koskidex ha modifiche non committate" >&2; exit 1; }
BIN=$(mktemp -d); trap 'rm -rf "$BIN"' EXIT
(cd "$KX" && go build -o "$BIN/carico" ./scripts/carico)
carico() { (cd "$KX" && "$BIN/carico" "$@"); }

ES=(-motore es -url http://localhost:9201 -container doc-tesi-es)
KD=(-motore koskidex -url http://localhost:7713 -container kosk-carico)
KN=(-motore koskidex -url http://localhost:7714 ${K_NATIVO_PID:+-pid "$K_NATIVO_PID"})

if [ "$COSA" = verifica ] || [ "$COSA" = tutto ]; then
  carico "${ES[@]}" "${Q[@]}" -modo verifica -etichetta verifica-es
  carico "${KD[@]}" "${Q[@]}" -modo verifica -etichetta verifica-koskidex-docker
fi
if [ "$COSA" = riposo ] || [ "$COSA" = tutto ]; then
  carico "${ES[@]}" "${Q[@]}" -modo riposo -durata 20s -etichetta riposo-es
  carico "${KD[@]}" "${Q[@]}" -modo riposo -durata 20s -etichetta riposo-koskidex-docker
fi
# La prima passata di una misura una alla volta è a motore appena avviato:
# prima di ognuna il container riparte e si aspetta che risponda.
riavvia() {
  docker restart "$1" >/dev/null
  for _ in $(seq 1 120); do
    if [ "$1" = doc-tesi-es ]; then
      curl -sf "http://localhost:9201/_cluster/health?wait_for_status=yellow&timeout=1s" >/dev/null && return
    else
      curl -sf http://localhost:7713/health | grep -q '"documents":10018' && return
    fi
    sleep 1
  done
  echo "$1 non risponde dopo il riavvio" >&2; exit 1
}

if [ "$COSA" = sequenziale ] || [ "$COSA" = tutto ]; then
  riavvia doc-tesi-es
  carico "${ES[@]}" "${Q[@]}" -modo sequenziale -etichetta seq-es-app
  riavvia doc-tesi-es
  carico "${ES[@]}" "${Q[@]}" -modo sequenziale -sorgente=false -etichetta seq-es-senza-source
  riavvia kosk-carico
  carico "${KD[@]}" "${Q[@]}" -modo sequenziale -etichetta seq-koskidex-docker
  riavvia kosk-carico
  carico "${KD[@]}" "${Q[@]}" -modo sequenziale -senza-cache=false -etichetta seq-koskidex-docker-cache
  carico "${KN[@]}" "${Q[@]}" -modo sequenziale -etichetta seq-koskidex-nativo
fi
if [ "$COSA" = carico ] || [ "$COSA" = tutto ]; then
  carico "${ES[@]}" "${Q[@]}" -modo carico -etichetta carico-es-app
  carico "${ES[@]}" "${Q[@]}" -modo carico -sorgente=false -etichetta carico-es-senza-source
  carico "${KD[@]}" "${Q[@]}" -modo carico -etichetta carico-koskidex-docker
  carico "${KN[@]}" "${Q[@]}" -modo carico -etichetta carico-koskidex-nativo
fi
