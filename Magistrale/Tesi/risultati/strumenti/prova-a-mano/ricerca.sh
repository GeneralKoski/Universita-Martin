#!/usr/bin/env bash
# ricerca.sh "query": cerca dall'app (ai-search) con la sessione in cj

curl -s -b "$HOME/koskidex-p4/cj" -c "$HOME/koskidex-p4/cj" -G -H 'Origin: http://localhost:3000' -H 'Referer: http://localhost:3000/' -H 'Accept: application/json' -H 'X-Guard: admin' --data-urlencode "search=$1" http://localhost:8010/api/ai-search | python3 -c "
import sys,json
d=json.load(sys.stdin)
if 'documents' not in d: print(str(d)[:300]); sys.exit()
print(len(d['documents']), 'risultati; primi:')
for x in d['documents'][:5]:
    v=x.get('current_version') or x.get('currentVersion') or {}
    print(' -', (v.get('name') or x.get('name') or str(x)[:80])[:100])
"
