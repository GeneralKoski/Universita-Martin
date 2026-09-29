#!/usr/bin/env bash
# La prova sulla cache dei vettori (README, "La cache dei vettori"): indicizza due volte da un indice vuoto con il profilo P4, riavviando Koskidex sulla stessa cartella di dati. Copia esatta dello script lanciato dalla cartella temporanea della sessione (i percorsi in $CLAUDE_JOB_DIR/tmp/cache-prova erano quelli); i due rapporti sono in confronto/.
set -euo pipefail
export TESI_RISULTATI=$CLAUDE_JOB_DIR/tmp/cache-prova
KX=$HOME/Desktop/Progetti-personali/Koskidex
R=$HOME/Desktop/Università-Martin/Magistrale/Tesi/risultati
B=$CLAUDE_JOB_DIR/tmp/cache-prova; rm -rf $B/dati; mkdir -p $B/dati
(cd $KX && go build -o $B/koskidex .)
export KOSKIDEX_PROFILO=consigliata KOSKIDEX_TIMEOUT=1800 KOSKIDEX_NORMALIZE_DATES=true KOSKIDEX_NORMALIZE_AMOUNTS=true KOSKIDEX_TYPOS_ON_AMOUNTS=false KOSKIDEX_SCORING=bm25 KOSKIDEX_STABLE_TERM_ORDER=true KOSKIDEX_EMBEDDER_MODEL=bge-m3 KOSKIDEX_HYBRID_MODE=union KOSKIDEX_VECTOR_WEIGHT=10
for giro in prima seconda; do
  $B/koskidex -port 7718 -data-dir $B/dati -log-level warn > $B/log-$giro 2>&1 & PID=$!
  for _ in $(seq 1 30); do curl -sf http://localhost:7718/health >/dev/null && break; sleep 1; done
  echo "$giro: righe cache all'avvio $(wc -l < $B/dati/embeddings.jsonl 2>/dev/null || echo 0)"
  $R/strumenti/indicizza-koskidex.sh albo prova-cache-$giro http://localhost:7718 >/dev/null
  python3 -c "import json,glob;d=json.load(open(sorted(glob.glob('$B/confronto/*prova-cache-$giro*'))[-1]));print('$giro: index_ms',d['timings']['index_ms'])"
  kill $PID; wait $PID 2>/dev/null || true
done
echo fine
