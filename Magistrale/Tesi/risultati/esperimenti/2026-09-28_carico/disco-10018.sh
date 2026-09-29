#!/usr/bin/env bash
# L'indice su disco a 10.018 documenti, la riga che la tabella della crescita
# riportava senza un file. Stesso metodo di copia.py: per Elasticsearch
# store.size dell'indice dell'app dopo un _flush; per Koskidex koskidex.db più
# operations.log di un Koskidex nativo del commit corrente, con una cartella di
# dati vuota, riempito dall'app con KOSKIDEX_PROFILO=consigliata come in
# 2026-09-29_accenti. Archivia in questa cartella.
#
#   disco-10018.sh
set -euo pipefail
: "${TESI_RISULTATI:?TESI_RISULTATI non impostata: il risultato non verrebbe archiviato}"
KX=${KOSKIDEX:-$HOME/Desktop/Progetti-personali/Koskidex}
QUI=$(cd "$(dirname "$0")" && pwd)
R=$(cd "$QUI/../.." && pwd)
[ -z "$(git -C "$KX" status --porcelain)" ] || { echo "Koskidex ha modifiche non committate" >&2; exit 1; }

BIN=$(mktemp -d)
(cd "$KX" && go build -o "$BIN/koskidex" .)
mkdir "$BIN/dati"
"$BIN/koskidex" -port 7716 -data-dir "$BIN/dati" -log-level warn > "$BIN/log" 2>&1 &
PID=$!
trap 'kill $PID 2>/dev/null; wait $PID 2>/dev/null || true; rm -rf "$BIN"' EXIT
for _ in $(seq 1 30); do curl -sf http://localhost:7716/health >/dev/null && break; sleep 1; done

export KOSKIDEX_PROFILO=consigliata
"$R/strumenti/indicizza-koskidex.sh" albo disco-10018 http://localhost:7716 >/dev/null
sleep 5
curl -sf -X POST http://localhost:9201/search-documents-local/_flush >/dev/null

python3 - "$BIN/dati" "$KX" "$QUI" <<'PY'
import datetime, json, os, subprocess, sys, urllib.request
dati, kx, qui = sys.argv[1:]
get = lambda u: json.load(urllib.request.urlopen(u, timeout=60))
es = get("http://localhost:9201/_cat/indices/search-documents-local?format=json&bytes=b")[0]
kd = get("http://localhost:7716/indexes/search-documents-local")
git = lambda d, *a: subprocess.run(["git", "-C", d, *a], capture_output=True, text=True, check=True).stdout.strip()
ora = datetime.datetime.now(datetime.timezone.utc)
esito = {"ran_at": ora.strftime("%Y-%m-%dT%H:%M:%SZ"),
         "config": {"commit": git(qui, "rev-parse", "--short", "HEAD"),
                    "modifiche_non_committate": "true" if git(qui, "status", "--porcelain", "--untracked-files=no", "--", qui) else "false",
                    "koskidex": git(kx, "rev-parse", "--short", "HEAD"), "profilo": "consigliata"},
         "elasticsearch": {"documenti": int(es["docs.count"]), "byte_su_disco": int(es["store.size"])},
         "koskidex": {"documenti": kd["docs"], "byte_su_disco": sum(os.path.getsize(os.path.join(dati, f))
                                                                 for f in os.listdir(dati) if f in ("koskidex.db", "operations.log"))}}
print(json.dumps({k: v for k, v in esito.items() if k != "config"}))
o = ora.strftime("%Y-%m-%dT%H%M%SZ"); p = os.path.join(os.environ["TESI_RISULTATI"], "esperimenti", "2026-09-28_carico", f"{o}_disco-10018.json")
open(p, "x").write(json.dumps(esito, indent=2, ensure_ascii=False))
print("archiviato in", p)
PY
