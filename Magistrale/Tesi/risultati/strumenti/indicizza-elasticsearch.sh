#!/usr/bin/env bash
# Ricrea da zero l'indice dei documenti sull'Elasticsearch LOCALE, lo riempie
# col comando dell'app (app:export-to-elastic-search, non toccato) e archivia
# il tempo impiegato in $TESI_RISULTATI/confronto.
#
#   indicizza-elasticsearch.sh <database> <etichetta>
#   indicizza-elasticsearch.sh albo albo-metadata
#
# memory_limit=1G perche' con i 128M di default il comando muore in silenzio
# intorno ai 10.000 documenti (exit 255, nessun messaggio): e' un difetto
# dell'app, annotato nel piano, e l'override finisce nel file dei risultati.
set -euo pipefail

DB="${1:?database}"; ETICHETTA="${2:?etichetta}"
: "${TESI_RISULTATI:?TESI_RISULTATI non impostata: il risultato non verrebbe archiviato}"
APP="$HOME/Desktop/Dieffetech/Documentale/apps/laravel"
ES="http://localhost:9201"
export DB_HOST=127.0.0.1 DB_PORT=33061 DB_DATABASE="$DB" DB_USERNAME=root DB_PASSWORD=root TELESCOPE_ENABLED=false

cd "$APP"
INDICE=$(php artisan tinker --execute='echo (new App\Services\ElasticsearchService())->getIndexName("documents");' | tail -1)
case "$ES" in http://localhost:*) ;; *) echo "rifiuto: non e' l'Elasticsearch locale" >&2; exit 1;; esac

curl -sS -X DELETE "$ES/$INDICE" >/dev/null || true
php artisan tinker --execute='(new App\Services\ElasticsearchService())->createDocumentsIndex();' >/dev/null

INIZIO=$(python3 -c 'import time;print(time.time_ns())')
php -d memory_limit=1G artisan app:export-to-elastic-search > /tmp/indicizza-es.log 2>&1
FINE_NS=$(python3 -c 'import time;print(time.time_ns())')
curl -sS -X POST "$ES/$INDICE/_refresh" >/dev/null

python3 - "$INIZIO" "$FINE_NS" "$INDICE" "$DB" "$ETICHETTA" "$APP" <<'PY'
import json,sys,urllib.request,subprocess,datetime,os
ini,fin,indice,db,etichetta,app=sys.argv[1:]
es='http://localhost:9201'
get=lambda u: json.load(urllib.request.urlopen(u))
git=lambda *a: subprocess.run(['git','-C',app,*a],capture_output=True,text=True).stdout.strip()
ora=datetime.datetime.now(datetime.timezone.utc)
rap={'ran_at':ora.strftime('%Y-%m-%dT%H:%M:%SZ'),
     'config':{'motore':'elasticsearch','operazione':'indicizzazione completa da indice vuoto',
               'comando':'php -d memory_limit=1G artisan app:export-to-elastic-search',
               'database':db,'indice':indice,'elasticsearch_versione':get(es)['version']['number'],
               'commit':git('rev-parse','HEAD'),'modifiche_non_committate':str(bool(git('status','--porcelain'))).lower()},
     'documenti_indicizzati':get(f'{es}/{indice}/_count')['count'],
     'timings':{'index_ms':(int(fin)-int(ini))/1e6}}
d=os.path.join(os.environ['TESI_RISULTATI'],'confronto'); os.makedirs(d,exist_ok=True)
o=ora.strftime('%Y-%m-%dT%H%M%SZ'); nome=f'{etichetta}-indicizzazione-elasticsearch'
p=os.path.join(d,f'{o}_{nome}.json'); n=2
while os.path.exists(p): p=os.path.join(d,f'{o}-{n}_{nome}.json'); n+=1
open(p,'x').write(json.dumps(rap,indent=2,ensure_ascii=False))
print(f"{rap['documenti_indicizzati']} documenti in {rap['timings']['index_ms']:.0f} ms\narchiviato in {p}")
PY
