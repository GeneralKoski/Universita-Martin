# Istruzioni per Claude sul fisso di Martin (RTX 3060 Ti, Ryzen 5)

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
scende su una RTX 3060 Ti? Solo tempi, non metriche.

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

## Compito B: il carico su un'altra macchina (solo se l'ambiente c'è)

Domanda: il rapporto fra Koskidex ed Elasticsearch misurato sul Mac
(`2026-09-28_carico`: capacità circa sette volte, p50 0,89 contro 6,32 ms)
regge su un'altra macchina? Leggi il README di `2026-09-28_carico`, di
`2026-09-28_prestazioni` e di `2026-09-28_allocazioni`.

Prerequisiti (tutti da verificare prima di scrivere una riga di previsioni):
Docker, Go, Koskidex al commit di `2026-09-28_allocazioni` o successivo,
Documentale con Elasticsearch e MySQL in locale e il **database degli albi già
riempito** (10.018 atti: non è in git, sta sul Mac di Martin), e le 400 query
del carico. **Se il database o gli indici non ci sono, non ricostruirli: Compito
B saltato, dillo a Martin.**

Previsioni da scrivere prima (in un esperimento nuovo che rimanda a quello del
Mac): tempi per query simili al Mac (dipendono dal singolo core); capacità del
nativo nella zona del Mac (dipende dai core); rapporto fra i motori entro il 30%
di quello del Mac. Dichiara il sistema operativo: su Linux Docker gira senza
macchina virtuale, su Windows passa da WSL2, e sul Mac il nativo va il 70% più
veloce del container.

## Alla fine

- Lascia l'albero pulito e i commit in locale; **non pushare**.
- Riferisci a Martin: cosa hai misurato (numeri principali), cosa hai saltato e
  perché, i commit fatti (`git log --oneline` dall'ultimo pushato), e cosa deve
  fare il Claude del Mac per portare i risultati in tesi (sezione 8.2 per il
  riordino, 8.3 per il carico; registro delle previsioni; `TODO.md`).
- Non toccare i capitoli della tesi se non te lo chiede Martin.
