#!/usr/bin/env bash
# Ambiente per provare Documentale con Koskidex P4 sul corpus degli albi:
# container doc-tesi-*, Koskidex P4 (7717), Laravel (8010), Next (3000).
# Login: admin@documentale.com / password (full-access), base@documentale.com / password.
set -euo pipefail
Q=$(cd "$(dirname "$0")" && pwd)
docker start doc-tesi-mysql doc-tesi-es >/dev/null
"$Q/avvia.sh"
cd "$HOME/Desktop/Dieffetech/Documentale/apps/laravel"
source "$Q/env-app.sh"
export APP_URL=http://localhost:8010 FRONTEND_URL=http://localhost:3000 SANCTUM_STATEFUL_DOMAINS=localhost:3000,localhost:8010 SESSION_DOMAIN=localhost
pgrep -f "artisan serve" >/dev/null || nohup php artisan serve --host=127.0.0.1 --port=8010 > "$Q/laravel.log" 2>&1 &
cd ../react
pgrep -f "next dev" >/dev/null || NEXT_PUBLIC_BACKEND_URL=http://localhost:8010 nohup npm run dev -- --port 3000 > "$Q/next.log" 2>&1 &
echo "Apri http://localhost:3000"
