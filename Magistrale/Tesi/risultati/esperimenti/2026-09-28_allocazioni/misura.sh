#!/usr/bin/env bash
# Le misure di 2026-09-28_allocazioni per la fase "prima" o "dopo": il motore
# del commit corrente di Koskidex, con gli strumenti e le query di
# 2026-09-28_prestazioni/misura-dopo.sh, archiviate in
# 2026-09-28_allocazioni/<fase>.
#
# - container kosk-alloc (alpine, binario Linux) su 7713, con una copia dei
#   dati che l'app aveva indicizzato nel container kosk-carico; nativo su 7714
#   con una copia dei dati di Koskidex nativo;
# - una alla volta e sotto carico, nel container e nativo;
# - una alla volta sulla copia da 100.000 documenti, in un container nuovo;
# - il profilo a 8 client, con profilo.sh.
#
#   misura.sh prima|dopo <dati del container kosk-carico> <dati di koskidex nativo>
set -euo pipefail
: "${TESI_RISULTATI:?TESI_RISULTATI non impostata: il risultato non verrebbe archiviato}"
FASE=${1:?prima o dopo}; DATI_C=${2:?dati del container}; DATI_N=${3:?dati del nativo}
KX=${KOSKIDEX:-$HOME/Desktop/Progetti-personali/Koskidex}
QUI=$(cd "$(dirname "$0")" && pwd)
T=$(cd "$QUI/../../query" && pwd)
ESP=2026-09-28_allocazioni/$FASE
Q=(-query "known-item-auto=$KX/eval/corpora/c3-albo/known-item-auto/queries.jsonl"
   -query "confronto-24=$T/confronto-24/queries.jsonl"
   -query "umane=$T/known-item-umane/queries.jsonl")
[ -z "$(git -C "$KX" status --porcelain)" ] || { echo "Koskidex ha modifiche non committate" >&2; exit 1; }
LAV=$(mktemp -d)
PN=
fine() { [ -n "$PN" ] && kill "$PN" 2>/dev/null; docker rm -f kosk-alloc kosk-alloc-100000 >/dev/null 2>&1; rm -rf "$LAV"; }
trap fine EXIT
V=$(git -C "$KX" rev-parse --short HEAD)
mkdir "$LAV/c" "$LAV/n"
(cd "$KX" && GOOS=linux GOARCH=arm64 CGO_ENABLED=0 go build -ldflags "-X main.version=$V" -o "$LAV/c/koskidex" . \
  && go build -ldflags "-X main.version=$V" -o "$LAV/n/koskidex" . && go build -o "$LAV/carico" ./scripts/carico)
carico() { (cd "$KX" && "$LAV/carico" -esperimento "$ESP" "$@"); }
aspetta() {  # url, testo atteso nella risposta
  for _ in $(seq 1 180); do curl -sf "$1" | grep -q "$2" && return; sleep 1; done
  echo "$1 non risponde come atteso" >&2; exit 1
}

cp -R "$DATI_C" "$LAV/c/data"
docker rm -f kosk-alloc >/dev/null 2>&1 || true
docker run -d --name kosk-alloc -p 7713:7700 -v "$LAV/c:/k" alpine:latest \
  /k/koskidex --port 7700 --data-dir /k/data --log-level warn >/dev/null
aspetta http://localhost:7713/health '"documents":10018'
cp -R "$DATI_N" "$LAV/n/data"
"$LAV/n/koskidex" -port 7714 -data-dir "$LAV/n/data" -log-level warn > "$LAV/n/log" 2>&1 & PN=$!
aspetta http://localhost:7714/health '"documents":10018'

KD=(-motore koskidex -url http://localhost:7713 -container kosk-alloc)
KN=(-motore koskidex -url http://localhost:7714 -pid "$PN")

carico "${KD[@]}" "${Q[@]}" -modo sequenziale -etichetta seq-koskidex-docker
carico "${KN[@]}" "${Q[@]}" -modo sequenziale -etichetta seq-koskidex-nativo
carico "${KD[@]}" "${Q[@]}" -modo carico -etichetta carico-koskidex-docker
carico "${KN[@]}" "${Q[@]}" -modo carico -etichetta carico-koskidex-nativo
kill "$PN"; PN=

N=100000; C=kosk-alloc-100000; mkdir "$LAV/d100"
docker rm -f "$C" >/dev/null 2>&1 || true
docker run -d --name "$C" -p 7715:7700 -v "$LAV/c:/k:ro" -v "$LAV/d100:/dati" alpine:latest \
  /k/koskidex --port 7700 --data-dir /dati --log-level warn >/dev/null
aspetta http://localhost:7715/health '"status":"ok"'
TESI_RISULTATI="$LAV/scarto" python3 "$QUI/../2026-09-28_carico/copia.py" koskidex http://localhost:7715 \
  search-documents-local "carico-$N" "$N" "$LAV/d100" http://localhost:7713 >/dev/null
docker restart "$C" >/dev/null
aspetta http://localhost:7715/health "\"documents\":$N"
carico -motore koskidex -url http://localhost:7715 -container "$C" -indice "carico-$N" "${Q[@]}" \
  -modo sequenziale -etichetta "seq-koskidex-docker-$N"
docker rm -f "$C" kosk-alloc >/dev/null

ESPERIMENTO=$ESP "$QUI/../2026-09-28_carico/profilo.sh" "$DATI_N"
