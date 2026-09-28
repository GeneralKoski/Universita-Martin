#!/usr/bin/env bash
# La misura 4 di 2026-09-28_carico: dove Koskidex spende CPU e memoria sotto
# carico. Compila una copia di main.go con net/http/pprof su localhost:6060
# (la copia vive in una cartella temporanea del modulo solo per la durata della
# compilazione, poi si cancella: il motore resta quello del commit), la avvia
# nativa su una copia dei dati di Koskidex nativo, la carica con 8 client e
# intanto prende il profilo CPU di 20 s e quello delle allocazioni.
#
#   profilo.sh <cartella dati di koskidex nativo>
#
# ESPERIMENTO cambia la cartella dell'archivio (2026-09-28_prestazioni lo usa
# per il suo "dopo").
set -euo pipefail
: "${TESI_RISULTATI:?TESI_RISULTATI non impostata: il risultato non verrebbe archiviato}"
SORGENTE=${1:?cartella dati}
KX=${KOSKIDEX:-$HOME/Desktop/Progetti-personali/Koskidex}
ESP=${ESPERIMENTO:-2026-09-28_carico}
T=$(cd "$(dirname "$0")/../../query" && pwd)
[ -z "$(git -C "$KX" status --porcelain)" ] || { echo "Koskidex ha modifiche non committate" >&2; exit 1; }
LAV=$(mktemp -d); trap 'kill $PID 2>/dev/null || true; rm -rf "$LAV"' EXIT
V=$(git -C "$KX" rev-parse --short HEAD)

mkdir "$KX/zz_profilo"
perl -pe 's#^import \(#import (\n\t_ "net/http/pprof"#; s#^func main\(\) \{#func main() {\n\tgo func() { _ = http.ListenAndServe("localhost:6060", nil) }()#' \
    "$KX/main.go" > "$KX/zz_profilo/main.go"
(cd "$KX" && go build -ldflags "-X main.version=$V" -o "$LAV/koskidex" ./zz_profilo) || { rm -rf "$KX/zz_profilo"; exit 1; }
rm -rf "$KX/zz_profilo"
[ -z "$(git -C "$KX" status --porcelain)" ] || { echo "l'albero di Koskidex non è tornato pulito" >&2; exit 1; }
(cd "$KX" && go build -o "$LAV/carico" ./scripts/carico)

cp -R "$SORGENTE" "$LAV/dati"
"$LAV/koskidex" -port 7716 -data-dir "$LAV/dati" -log-level warn > "$LAV/log" 2>&1 &
PID=$!
for _ in $(seq 1 60); do curl -sf localhost:7716/health | grep -q '"documents":10018' && break; sleep 1; done

(cd "$KX" && "$LAV/carico" -motore koskidex -url http://localhost:7716 -pid "$PID" \
  -query "known-item-auto=$KX/eval/corpora/c3-albo/known-item-auto/queries.jsonl" \
  -query "confronto-24=$T/confronto-24/queries.jsonl" -query "umane=$T/known-item-umane/queries.jsonl" \
  -modo carico -concorrenza 8 -durata 40s -riscaldamento 5s -esperimento "$ESP" -etichetta profilo-carico-koskidex-nativo) &
CARICO=$!
sleep 12
curl -sf -o "$LAV/cpu.pb.gz" "localhost:6060/debug/pprof/profile?seconds=20"
curl -sf -o "$LAV/allocs.pb.gz" "localhost:6060/debug/pprof/allocs"
wait $CARICO

D="$TESI_RISULTATI/esperimenti/$ESP/profilo"; mkdir -p "$D"
O=$(date -u +%Y-%m-%dT%H%M%SZ)
cp "$LAV/cpu.pb.gz" "$D/${O}_cpu.pb.gz"; cp "$LAV/allocs.pb.gz" "$D/${O}_allocs.pb.gz"
{ echo "# koskidex $V, profilo CPU di 20 s a 8 client"; go tool pprof -top -nodecount=30 "$LAV/koskidex" "$LAV/cpu.pb.gz"; } > "$D/${O}_cpu-top.txt" 2>&1
{ echo "# koskidex $V, profilo CPU cumulativo"; go tool pprof -top -cum -nodecount=40 "$LAV/koskidex" "$LAV/cpu.pb.gz"; } > "$D/${O}_cpu-cum.txt" 2>&1
{ echo "# koskidex $V, allocazioni (byte) dall'avvio"; go tool pprof -sample_index=alloc_space -top -nodecount=30 "$LAV/koskidex" "$LAV/allocs.pb.gz"; } > "$D/${O}_allocs-top.txt" 2>&1
echo "profili in $D con prefisso $O"
