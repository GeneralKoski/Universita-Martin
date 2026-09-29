# Istruzioni per Claude sul fisso di Martin (RTX 3060 da 12 GB, Ryzen 5 8500G)

Scritto il 29/09/2026 sul Mac di Martin, per un Claude che parte da zero su
un altro computer. Leggi tutto prima di toccare qualcosa. Rispondi a Martin in
italiano, breve e diretto.

## Dove sei

Repository `Universita-Martin` (branch `main`), cartella `Magistrale/Tesi/`: la
tesi magistrale di Martin, **Koskidex innestato in Documentale**. Il lavoro
tecnico è chiuso e pushato (tesi di 119 pagine, tutti gli esperimenti
misurati). Leggi `CLAUDE.md` alla radice del repository per il contesto e
`Magistrale/Tesi/TODO.md` per lo stato (la sezione «Regole» in fondo vale per
tutto). Quello che resta a te è **facoltativo**: due misure di sola prestazione
che servono a dire in tesi se i tempi misurati su un Mac M2 reggono su un'altra
macchina. Non cambiano nessuna conclusione: se un passo non riesce, ti fermi e
lo dici, non improvvisi.

Altri repository, solo se servono al compito B: `Koskidex` (Go, branch `main`,
`github.com/GeneralKoski/Koskidex`) e `Documentale` (Laravel, branch
`martin/tesi-magistrale`, `github.com/Dieffetech/Documentale`, **non
toccare** nient'altro che quel branch e mai `ElasticsearchService`).

## Regole che non si discutono

- **Git.** Mai creare branch: si committa su `main`. Messaggi di commit **in
  inglese**, con un corpo esaustivo (cosa è cambiato e perché). **Niente**
  `Co-Authored-By`, **niente** trailer o link `Claude-Session`. Push solo se
  Martin lo chiede: prima gli mostri i commit da pushare.
- **Privacy.** Il repository è pubblico. Non committare mai: il corpus degli
  albi, le pagine di raccolta o di annotazione, le risposte delle known-item
  umane (`risultati/query/known-item-umane/{risposte,queries.jsonl,queries.txt,
  raccolta.json}`) né i rapporti che contengono il testo di quelle query
  (`confronto/*known-item-umane*`, `riordinati/*known-item-umane*`: sono già in
  `.gitignore`, controlla con `git status` prima di ogni commit). Non citare
  mai testi di query umane in file o output. Nessun IP del server di Martin,
  nessuna chiave.
- **Le previsioni prima della misura.** Ogni esperimento nuovo ha un `README.md`
  con domanda, metodo e previsioni con una soglia numerica, **committato prima
  di lanciare la misura** (e prima di scrivere lo script, se possibile). Le
  sezioni «Prima di misurare» non si toccano mai dopo: le correzioni vanno
  nell'«Esito», con note datate.
- **Ogni numero ha il suo file.** Gli strumenti archiviano da soli in
  `risultati/` se è impostata `TESI_RISULTATI` (a questo repository:
  `export TESI_RISULTATI=<percorso>/Magistrale/Tesi/risultati`). Mai
  sovrascrivere un file archiviato. Per le prove di sviluppo lancia con
  `TESI_RISULTATI=` vuota o puntata a una cartella temporanea, e dopo ogni
  prova controlla `git status`. Se calcoli a mano un numero da citare, prima lo
  aggiungi allo strumento che archivia, poi lo citi.
- **Codice di misura committato.** Gli strumenti controllano che l'albero sia
  pulito: committa gli script prima di lanciarli.
- **Scrittura.** Accenti italiani veri (è, più, perché, già, così), mai lettera
  più apostrofo. Mai il trattino lungo (—): trattino normale. Per le persone,
  they/them se non sono dichiarati i pronomi.
- **Sistema operativo.** Va dichiarato in ogni esito (Windows con WSL2, o
  Linux): cambia i tempi. Scrivi la macchina in un file analogo a
  `risultati/macchina.md` dentro la cartella dell'esperimento (CPU, RAM, GPU,
  driver, sistema, versioni di Python, torch, Go, Docker).

## Compito A: il riordino su una GPU consumer

Domanda: il costo del cross-encoder misurato sul Mac (`2026-09-28_reranker`)
scende su una RTX 3060? Solo tempi, non metriche.

Cosa c'è già (leggi `risultati/esperimenti/2026-09-28_reranker/README.md`):
`BAAI/bge-reranker-v2-m3` (568M parametri, revisione `953dc6f`), `max_length`
512, batch 32, primi 100 candidati; sul Mac (M2, MPS, fp32) la mediana è 12,0 s
a query su SciFact e 11,3 s su NFCorpus. I primi stadi sono archiviati in
`esperimenti/2026-09-28_reranker/primo-stadio/` (in git, solo id), i
rapporti riordinati sul Mac in `riordinati/` (in git quelli di SciFact, NFCorpus
e delle automatiche; quelli delle umane no, hanno il testo delle query).

**Fai solo SciFact e NFCorpus**, che sono pubbliche: le collezioni degli albi
non sono in git e non devi ricostruirle sul fisso.

Passi:

1. Ambiente Python a parte con torch per CUDA, `sentence-transformers` 6.x,
   `huggingface_hub`; scarica il modello (2,1 GB) e controlla la revisione
   `953dc6f`. Le collezioni SciFact e NFCorpus stanno nel repository Koskidex,
   `eval/corpora/c1-public/{scifact,nfcorpus}/` (`corpus.jsonl`, `queries.jsonl`,
   `qrels/test.tsv`, il formato che `strumenti/riordina.py` legge);
   `SOURCE.md` nella stessa cartella dà provenienza e md5: controllali. Se non riesci a ricostruirle uguali
   a quelle del Mac, fermati e dillo.
2. Crea `risultati/esperimenti/<data>_reranker-gpu/README.md` con domanda,
   metodo e previsioni, e **committalo**. Previsioni di partenza (stima scritta
   il 29/09 sul Mac, puoi affinarle prima di misurare ma non dopo): fp32 circa
   4 s a query su SciFact; fp16 fra 1,5 e 2,5 s; gli ordini riordinati in fp32
   coincidono con quelli del Mac; in fp16 differiscono di poco (dì una soglia,
   per esempio MRR/nDCG@10 entro 0,005).
3. `strumenti/riordina.py` non ha un'opzione per fp16: aggiungila (per
   esempio `--dtype float32|float16`, default `float32`, che non cambia il
   comportamento di prima), committa lo strumento, poi lancia con
   `--dispositivo cuda` in fp32 e in fp16, sugli stessi file di
   `primo-stadio/`. Il campo `ms` di ogni query del rapporto è il tempo del
   riordino. Il rapporto va in `riordinati/` dell'esperimento nuovo.
4. Valuta gli ordini con `scripts/evaluate -rankings` di Koskidex (come fa
   `2026-09-28_reranker/esegui.sh`) per confrontare le metriche con quelle
   del Mac.
5. Scrivi l'Esito nel README, previsione per previsione, con mediane e
   percentili dei tempi, la macchina, e la coincidenza degli ordini col Mac.
   Aggiungi la voce a `TODO.md` («Da allineare alla fine») con dove va citato
   in tesi (sezione 8.2, dove si dice che il costo è «5-12 s a query sul Mac»)
   e aggiorna il registro (`latex/capitoli/appendice-ipotesi.tex`) solo se
   Martin lo chiede: la tesi la ricompila e la verifica lui o il Claude del
   Mac.

## Compito B: il carico su un'altra macchina

> **Stato al 29/09/2026:** il compito B è stato fatto (`2026-09-29_carico-fisso`) e il
> pacchetto è stato cancellato dal server dopo l'uso. Se lo si rifà, va prima
> rigenerato dal Mac (dump del container `doc-tesi-mysql` e testi delle query) e
> ricaricato; le istruzioni sotto restano valide per il resto.

Domanda: il rapporto fra Koskidex ed Elasticsearch misurato sul Mac
(`2026-09-28_carico`: capacità circa sette volte, p50 0,89 contro 6,32 ms)
regge su un'altra macchina? Leggi prima i README di `2026-09-28_carico`,
`2026-09-28_prestazioni` e `2026-09-28_allocazioni`, e `risultati/macchina.md`
(la macchina del Mac).

**Serve un file che non sta in git**: `bundle-fisso-tesi.tar.gz`. *(Nota del
30/09/2026: il compito B è fatto e il file è stato cancellato dal server il
29/09; se serve di nuovo va rigenerato dal Mac.)* Stava sul
server personale di Martin, alias SSH `hetzner` (definito in `~/.ssh/config`;
l'indirizzo non si scrive mai in nessun file del repository). Martin ha dato
il permesso di connettersi anche a questo computer. Scaricalo così:

    scp 'hetzner:/srv/backups/tesi-bundle-fisso/bundle-fisso-tesi.tar.gz' .

La cartella sul server è leggibile solo da root e contiene anche un
`LEGGIMI.txt`. Se `ssh hetzner` non risponde o chiede una password, **non
insistere e non cercare altre strade**: chiedi a Martin di copiartelo (chiavetta
o AirDrop) e, se non si riesce, **il compito B è saltato**: dillo e passa oltre.
Non cancellare né modificare niente sul server, a parte leggere il file. Contiene il dump esatto del database `albo` (10.018 atti, id
originali: **non reimportare gli albi da zero**, gli id cambierebbero) e i testi
delle query. È privato: mai in git, mai in chat, mai in cloud pubblici. La sua impronta
sha256 è
`c44ba7f3926e8df76f6de4640aa2e528c0ca9d21ee7cf65581f0aa5c7670a3e6`: controllala
prima di usarlo. Dentro c'è un `LEGGIMI.txt` e un `SHA256SUMS`.

### Preparazione (una volta, poi si misura)

Presupposti da verificare: Docker funzionante, Go, PHP 8.4 o superiore con
Composer, git. Se qualcosa non si installa con poca fatica, fermati e dillo a
Martin: è una misura facoltativa.

1. **Clona i repository** (accanto a questo): `Koskidex`
   (`github.com/GeneralKoski/Koskidex`, branch `main`) e `Documentale`
   (`github.com/Dieffetech/Documentale`, branch `martin/tesi-magistrale`,
   codice in `apps/laravel`; `composer install`). Se il clone di Documentale
   non parte (repository privato), chiedi a Martin come dare l'accesso.
2. **MySQL con gli albi.**
   `docker run -d --name doc-tesi-mysql -e MYSQL_ROOT_PASSWORD=root -p 33061:3306 mysql:8.4.10`,
   poi, dalla cartella del bundle scompattato,
   `gzip -dc albo.sql.gz | docker exec -i doc-tesi-mysql mysql -uroot -proot`.
   Controlla: `select count(*) from albo.documents` e `from albo.document_versions`
   danno 10018 tutti e due, `min(id)` 1 e `max(id)` 10045.
3. **Elasticsearch come sul Mac.**
   `docker run -d --name doc-tesi-es -p 9201:9200 -e xpack.security.enabled=false -e "ES_JAVA_OPTS=-Xms1g -Xmx1g" -e discovery.type=single-node docker.elastic.co/elasticsearch/elasticsearch:9.1.0`.
   Sul Mac Docker gira in una macchina virtuale con 4 CPU e circa 7-8 GB: sul
   fisso dichiara quante risorse ha Docker (su Linux nessuna VM, su Windows
   WSL2, e dichiara anche quante CPU e quanta RAM gli dai).
4. **Le query nei posti giusti**, dal bundle:
   `query/known-item-auto.queries.jsonl` in
   `<Koskidex>/eval/corpora/c3-albo/known-item-auto/queries.jsonl` (crea le
   cartelle se mancano) e `query/known-item-umane.queries.jsonl` in
   `Magistrale/Tesi/risultati/query/known-item-umane/queries.jsonl` (è in
   `.gitignore`: controlla con `git status` che non compaia).
5. **Riempi Elasticsearch dall'app.** Il `.env` di Documentale non serve e
   punta a servizi che non esistono più: passa le variabili sulla riga di
   comando. Da `Documentale/apps/laravel`, con
   `DB_HOST=127.0.0.1 DB_PORT=33061 DB_DATABASE=albo DB_USERNAME=root DB_PASSWORD=root TELESCOPE_ENABLED=false ELASTICSEARCH_HOST=http://localhost:9201`,
   lancia dal repository `strumenti/indicizza-elasticsearch.sh albo prova-fisso`
   con `TESI_RISULTATI` puntata a una **cartella temporanea** (non ai risultati
   veri: è un'indicizzazione di preparazione). Controlla
   `curl localhost:9201/search-documents-local/_count` = 10018.
6. **Koskidex due volte.** Compila da `Koskidex`: il binario nativo
   (`go build -o k-nativo .`) e quello per il container
   (`GOOS=linux GOARCH=amd64 CGO_ENABLED=0 go build -o k-linux .`, o `arm64`
   se il container è arm). Avvia il nativo sulla porta 7714
   (`-port 7714 -data-dir <cartella> -log-level warn`) e il container sulla 7713:
   `docker run -d --name kosk-carico -p 7713:7700 -v <cartella-con-k-linux>:/k alpine:latest /k/k-linux --port 7700 --data-dir /k/data --log-level warn`.
   Riempili dall'app con `SEARCH_BACKEND=koskidex KOSKIDEX_PROFILO=consigliata`
   e `KOSKIDEX_HOST` sulla porta giusta, con
   `strumenti/indicizza-koskidex.sh albo prova-fisso http://localhost:7713` (e
   `:7714`; lo script accetta solo `localhost`), sempre con `TESI_RISULTATI`
   temporanea. Controlla `curl localhost:7713/health` e `:7714/health`:
   `"documents":10018`.

### Misura

Con tutto acceso, il flusso è quello di `2026-09-28_carico/esegui.sh`, che
presuppone proprio questi nomi e porte (`doc-tesi-es` su 9201, `kosk-carico` su
7713, nativo su 7714, con `K_NATIVO_PID` il processo del nativo).

1. **Prima delle misure** crea `risultati/esperimenti/<data>_carico-fisso/README.md`
   che rimanda a quello del Mac, dichiara la macchina e il sistema operativo
   (file `macchina.md` accanto), e scrive le previsioni con soglia. Quelle di
   partenza (stimate il 29/09 sul Mac, puoi affinarle prima di misurare ma non
   dopo): i tempi per query sono simili a quelli del Mac (dipendono dal singolo
   core); la capacità del nativo sta nella zona del Mac (dipende dai core);
   il rapporto fra i motori sta entro il 30% di quello del Mac. **Committalo**.
2. Adatta `esegui.sh`, `analizza.py` e le loro cartelle nell'esperimento
   nuovo (copia, non modificare gli originali), committa, poi lancia con
   `TESI_RISULTATI` sul repository vero.
3. Scrivi l'Esito, previsione per previsione, con le mediane e i percentili,
   e le risorse date a Docker.
4. **Prima di ogni commit** controlla che nei file nuovi non compaia il testo
   di nessuna query umana: per esempio confronta ogni riga di
   `known-item-umane.queries.jsonl` (il campo `text`) con `grep -rF` su tutti i
   file nuovi. I rapporti del carico contengono numeri, non testi, ma va
   verificato e non assunto.

## Alla fine

- Lascia l'albero pulito e i commit in locale; **non pushare**.
- Riferisci a Martin: cosa hai misurato (numeri principali), cosa hai saltato e
  perché, i commit fatti (`git log --oneline` dall'ultimo pushato), e cosa deve
  fare il Claude del Mac per portare i risultati in tesi (sezione 8.2 per il
  riordino, 8.3 per il carico; registro delle previsioni; `TODO.md`).
- Non toccare i capitoli della tesi se non te lo chiede Martin.
