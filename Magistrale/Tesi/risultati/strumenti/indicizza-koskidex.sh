#!/usr/bin/env bash
# Ricrea da zero l'indice dei documenti su un Koskidex LOCALE, lo riempie col
# comando dell'app (app:export-to-elastic-search, che passa da SearchBackend e
# quindi da KoskidexService con SEARCH_BACKEND=koskidex) e archivia il tempo
# impiegato in $TESI_RISULTATI/confronto. Gemello di indicizza-elasticsearch.sh.
#
#   indicizza-koskidex.sh <database> <etichetta> [host]
#   indicizza-koskidex.sh albo albo-metadata http://localhost:7711
set -euo pipefail

DB="${1:?database}"; ETICHETTA="${2:?etichetta}"; KX="${3:-http://localhost:7700}"
: "${TESI_RISULTATI:?TESI_RISULTATI non impostata: il risultato non verrebbe archiviato}"
case "$KX" in http://localhost:*) ;; *) echo "rifiuto: non e' un Koskidex locale" >&2; exit 1;; esac
APP="$HOME/Desktop/Dieffetech/Documentale/apps/laravel"
export DB_HOST=127.0.0.1 DB_PORT=33061 DB_DATABASE="$DB" DB_USERNAME=root DB_PASSWORD=root TELESCOPE_ENABLED=false
export SEARCH_BACKEND=koskidex KOSKIDEX_HOST="$KX"

cd "$APP"
INDICE=$(php artisan tinker --execute='echo app(App\Contracts\SearchBackend::class)->getIndexName("documents");' | tail -1)

curl -sS -X DELETE "$KX/indexes/$INDICE" >/dev/null || true
php artisan tinker --execute='app(App\Contracts\SearchBackend::class)->createDocumentsIndex();' >/dev/null

INIZIO=$(python3 -c 'import time;print(time.time_ns())')
php -d memory_limit=1G artisan app:export-to-elastic-search > /tmp/indicizza-kx.log 2>&1
FINE_NS=$(python3 -c 'import time;print(time.time_ns())')

python3 - "$INIZIO" "$FINE_NS" "$INDICE" "$DB" "$ETICHETTA" "$APP" "$KX" <<'PY'
import json,sys,urllib.request,subprocess,datetime,os
ini,fin,indice,db,etichetta,app,kx=sys.argv[1:]
get=lambda u: json.load(urllib.request.urlopen(u))
git=lambda *a: subprocess.run(['git','-C',app,*a],capture_output=True,text=True).stdout.strip()
ora=datetime.datetime.now(datetime.timezone.utc)
rap={'ran_at':ora.strftime('%Y-%m-%dT%H:%M:%SZ'),
     'config':{'motore':'koskidex','operazione':'indicizzazione completa da indice vuoto',
               'comando':'SEARCH_BACKEND=koskidex php -d memory_limit=1G artisan app:export-to-elastic-search',
               'database':db,'indice':indice,'koskidex_versione':get(f'{kx}/health')['version'],
               'commit':git('rev-parse','HEAD'),'modifiche_non_committate':str(bool(git('status','--porcelain'))).lower()},
     'documenti_indicizzati':get(f'{kx}/indexes/{indice}')['docs'],
     'timings':{'index_ms':(int(fin)-int(ini))/1e6}}
d=os.path.join(os.environ['TESI_RISULTATI'],'confronto'); os.makedirs(d,exist_ok=True)
o=ora.strftime('%Y-%m-%dT%H%M%SZ'); nome=f'{etichetta}-indicizzazione-koskidex'
p=os.path.join(d,f'{o}_{nome}.json'); n=2
while os.path.exists(p): p=os.path.join(d,f'{o}-{n}_{nome}.json'); n+=1
open(p,'x').write(json.dumps(rap,indent=2,ensure_ascii=False))
print(f"{rap['documenti_indicizzati']} documenti in {rap['timings']['index_ms']:.0f} ms\narchiviato in {p}")
PY
