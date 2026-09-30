#!/usr/bin/env bash
# Koskidex con il profilo P4 (recupero congiuntivo, BM25, ordine stabile, date e
# importi normalizzati, vettori bge-m3 a peso 10) sulla porta 7717, dati in
# ~/koskidex-p4/dati. Serve Ollama con bge-m3 e i container doc-tesi-*.
set -euo pipefail
cd "$(dirname "$0")"
curl -sf http://localhost:7717/health >/dev/null && { echo "già in esecuzione"; exit 0; }
nohup ./koskidex -port 7717 -data-dir "$PWD/dati" -log-level warn > koskidex.log 2>&1 &
for _ in $(seq 1 30); do curl -sf http://localhost:7717/health >/dev/null && break; sleep 1; done
echo "Koskidex P4 su http://localhost:7717"
