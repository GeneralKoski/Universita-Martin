# Provare a mano Documentale con Koskidex P4

Non è una misura della tesi: serve a cercare a mano sul corpus degli albi con le
impostazioni del profilo P4 (recupero congiuntivo, BM25, ordine stabile, date e
importi normalizzati, vettori `bge-m3` a peso 10). Gli script vanno copiati in
`~/koskidex-p4/` (contengono percorsi del Mac di Martin).

1. Container `doc-tesi-mysql` e `doc-tesi-es` con il database `albo` popolato
   (`app:import-albo-corpus`), Ollama con `bge-m3`.
2. Utenti: in `Documentale/apps/laravel`, con le variabili del database,
   `php artisan db:seed --class=TesiSeeder` (`admin@documentale.com` e
   `base@documentale.com`, password `password`).
3. `~/koskidex-p4/avvia.sh` avvia Koskidex sulla porta 7717.
4. Indicizzare una volta (circa 8-25 minuti, per i vettori):
   `source env-app.sh` e `strumenti/indicizza-koskidex.sh albo p4-prova http://localhost:7717`
   con `TESI_RISULTATI` su una cartella temporanea.
5. `avvia-tutto.sh` alza container, Koskidex, Laravel (8010) e Next (3000):
   apri `http://localhost:3000` e accedi.

La porta 8000 è di un altro progetto (`koski-ats-app`), per questo Laravel sta
su 8010. Il front-end manda `X-Guard: admin` su ogni richiesta; senza, l'API
risponde 401 (`ricerca.sh` lo fa già).
