# Piano autunno 2026 - lavoro propedeutico alla tesi

> **Per chi esegue:** i passi usano checkbox (`- [ ]`) per il tracciamento. Ogni task si chiude con un deliverable testabile da solo e un commit.

**Obiettivo:** portare avanti Koskidex e Documentale da qui a dicembre 2026 senza consumare il contributo della tesi, arrivando a febbraio 2027 con l'impianto di valutazione già pronto e il corpus già esportabile.

**Architettura:** tutto il lavoro di questo piano è *intorno* al ranking, mai *sul* ranking. Prima si mette in sicurezza il comportamento attuale (test che lo congelano, punteggi visibili), poi si costruisce il metro per misurarlo, poi si prepara il lato Documentale che fornisce i dati. Le correzioni al ranking restano intatte per la tesi.

**Stack:** Go 1.25 e zero dipendenze esterne oltre `golang.org/x/text` (Koskidex); Laravel 12 + PHP 8.4 (Documentale); Docker per far girare i servizi.

**Spec:** [appunti.md](appunti.md) per la domanda di tesi e il perimetro, [piano-implementazione.md](piano-implementazione.md) per il piano della tesi vera e propria. Questo documento **non lo sostituisce e non lo duplica**: dice quali sue parti si possono anticipare adesso e aggiunge i task che lì non ci sono.

---

## La regola che decide tutto

**Non si tocca il ranking.** I tre difetti - niente IDF, ibrido che è solo re-ranking, fusione di scale incomparabili - sono i tre capitoli della tesi. Correggerli adesso, di sera, senza il metro per misurarli, costa tre volte:

1. si perde il baseline, perché il "codice di partenza" contro cui la tesi misura diventa un codice già modificato a intuito;
2. si perde il contributo, perché in discussione il lavoro risulta fatto prima e fuori dal percorso;
3. non si impara niente lo stesso, perché senza giudizi di rilevanza non si può dire se la modifica ha migliorato o peggiorato.

Quindi la domanda da farsi prima di ogni commit su Koskidex in questi mesi è una sola: **questa modifica cambia l'ordine dei risultati?** Se sì, non va fatta adesso.

## Vincoli globali

- Koskidex resta a **zero dipendenze esterne** oltre `golang.org/x/text`, che è già in `go.mod`. Vale anche per i test e per l'impianto di valutazione.
- Nessun task di questo piano modifica `Search`, `findDocsForToken`, `cosineSimilarity` o l'ordinamento finale in `internal/engine/ranker.go`. Si può **aggiungere** codice accanto, mai cambiare quello che decide l'ordine.
- Ogni task finisce con un commit. Messaggio in inglese, come da convenzione del repo.
- Su Documentale si lavora su branch dal `main` aziendale e non si committa niente che contenga dati reali di clienti.

## Capacità realistica

Da oggi (23 settembre 2026) a metà dicembre sono circa tredici settimane, ma sono le tredici settimane in cui seguo quattro corsi e a dicembre consegno due progetti d'esame. Le sere davvero disponibili sono poche: **contare su tre o quattro ore a settimana, non di più**, cioè quaranta o cinquanta ore in totale.

Questo piano è dimensionato su quel numero. La Parte A e la Parte C ci stanno. La Parte B ci sta solo in parte, ed è scritto sotto dove ci si ferma senza danno.

Se a novembre il tempo non c'è, si sacrifica nell'ordine: prima la Parte B (recuperabile a febbraio), poi la Parte C (recuperabile ma allunga i tempi), mai la Parte A (è quella che protegge il baseline, e va fatta prima che venga voglia di mettere le mani al ranking).

## Cosa può mordere

Le cose che questo piano deve reggere e che è facile scoprire tardi:

- **Il baseline si sposta senza accorgersene.** Un refactoring apparentemente innocuo su tokenizer o fuzzy cambia l'ordine dei risultati e nessuno se ne accorge finché in tesi i numeri non tornano. Coperto dal Task A3.
- **La valutazione senza punteggi visibili.** Oggi `Search` ritorna solo gli id: senza il punteggio e la sua scomposizione non si può spiegare *perché* un documento è in quella posizione, e la Fase 3 della tesi è tutta lì. Coperto dal Task A2.
- **Documenti senza `_vector`.** Il corpus esportato da Documentale non ha embedding: metà del codice ibrido non viene mai esercitato dai test. Coperto dal Task A3, che include un caso con e uno senza vettore.
- **Il corpus esportato contiene dati di clienti.** Se l'export finisce in un repo universitario pubblico è un problema serio, non una svista. Il Task C1 lo limita tenendo il file fuori da ogni repo finché l'azienda non si è espressa, ma **non anonimizza niente**: se serve, l'anonimizzazione è un task in più da scrivere, e la decisione sta nel Task C0.
- **Annotare richiede più tempo di quanto sembra.** Sessanta query con giudizi su trecento documenti sono settimane di sere. Non è un rischio tecnico ed è già scritto in `appunti.md`, ma è il motivo per cui il Task B1 va chiuso adesso e non a febbraio.

---

# Parte A - Koskidex: mettere in sicurezza prima di toccare

## Task A0: Ambiente di sviluppo Go

Sul Mac **Go non è installato**: `go` non è nel PATH e non c'è né in `/usr/local/go` né in Homebrew. Oggi Koskidex gira solo via `docker compose`. Senza toolchain locale non si possono lanciare i test, e tutto il resto del piano si ferma qui.

**File:**
- Nessuna modifica al repo.

**Interfacce:**
- Produce: `go test ./...` eseguibile in locale, prerequisito di ogni task successivo.

- [ ] **Passo 1: installare Go 1.25**

```bash
brew install go
go version
```

Atteso: `go version go1.25.x darwin/arm64`. La versione deve essere almeno 1.25, che è quella dichiarata in `go.mod` e a cui il repo è passato apposta per chiudere le vulnerabilità della stdlib (commit `d0d9c7b`).

- [ ] **Passo 2: verificare che i test attuali passino**

```bash
cd ~/Desktop/Progetti-personali/Koskidex
go test ./... 2>&1 | tail -20
```

Atteso: tutti i package `ok`. Se qualcosa fallisce, **fermarsi e capire perché prima di andare avanti**: un test rosso di partenza rende inutile ogni confronto successivo.

- [ ] **Passo 3: annotare lo stato di partenza**

Scrivere in `eval/BASELINE.md` (crearlo) la data, l'output di `go version` e l'esito dei test. Serve a sapere, fra sei mesi, con quale toolchain sono stati prodotti i primi numeri.

- [ ] **Passo 4: commit**

```bash
git add eval/BASELINE.md
git commit -m "eval: record the toolchain and test baseline"
```

## Task A1: Un comando solo per i controlli

Il repo ha rimosso le GitHub Actions di proposito (commit `df8a4be`, deploy manuale via `deploy.sh` dal `f369165`). Non si rimettono. Serve però un modo unico per lanciare tutti i controlli, perché da qui in poi ogni numero della tesi deve nascere da un'esecuzione ripetibile.

**File:**
- Crea: `Makefile`

**Interfacce:**
- Produce: `make check`, usato da tutti i task successivi al posto di ricordarsi i comandi a memoria.

- [ ] **Passo 1: scrivere il Makefile**

```makefile
.PHONY: test vet check bench

test:
	go test ./...

vet:
	go vet ./...

bench:
	go test -run=^$$ -bench=. -benchmem ./internal/engine/

check: vet test
```

- [ ] **Passo 2: verificare che giri**

```bash
make check
```

Atteso: `go vet` senza output e tutti i test `ok`.

- [ ] **Passo 3: commit**

```bash
git add Makefile
git commit -m "build: add make check for vet and tests"
```

## Task A2: Rendere visibili i punteggi senza cambiarli

Oggi `Search` in `internal/engine/ranker.go:126` ritorna `([]string, map[string][]string)`: solo gli id dei documenti e gli highlight. Il punteggio, che è l'oggetto stesso della tesi, non esce dal motore. Per valutare e soprattutto per spiegare la Fase 3 serve vederlo, scomposto in parte lessicale e parte vettoriale.

Il cambiamento è **additivo**: si estrae il corpo in un nuovo metodo che ritorna i match completi, e `Search` diventa un involucro che continua a ritornare esattamente quello che ritornava prima. L'ordine non cambia di una posizione.

**File:**
- Modifica: `internal/engine/ranker.go:126-255`
- Test: `internal/engine/scored_test.go` (crea)

**Interfacce:**
- Consuma: `SearchMatch` (già esistente in `ranker.go:9-15`, campi `DocID`, `Score`, `WordsMatched`, `Typos`, `ExactMatches`).
- Produce: `func (idx *InvertedIndex) SearchScored(query string, settings Settings, fuzziness string, queryVector []float64) ([]SearchMatch, map[string][]string)`. La Fase 0 della tesi (esecutore della valutazione) legge da qui.

- [ ] **Passo 1: scrivere il test che fallisce**

```go
package engine

import "testing"

func TestSearchScoredMatchesSearchOrder(t *testing.T) {
	idx := NewInvertedIndex()
	s := DefaultSettings()
	s.SearchableFields = []string{"title"}

	idx.AddDocument("a", map[string]interface{}{"title": "gatto nero"}, s)
	idx.AddDocument("b", map[string]interface{}{"title": "gatto"}, s)
	idx.AddDocument("c", map[string]interface{}{"title": "cane"}, s)

	ids, _ := idx.Search("gatto nero", s, "auto", nil)
	scored, _ := idx.SearchScored("gatto nero", s, "auto", nil)

	if len(ids) != len(scored) {
		t.Fatalf("lunghezze diverse: Search %d, SearchScored %d", len(ids), len(scored))
	}
	for i := range ids {
		if ids[i] != scored[i].DocID {
			t.Fatalf("posizione %d: Search dice %q, SearchScored dice %q", i, ids[i], scored[i].DocID)
		}
	}
	if scored[0].Score <= 0 {
		t.Fatalf("il primo risultato ha punteggio %v, atteso maggiore di zero", scored[0].Score)
	}
}
```

- [ ] **Passo 2: lanciarlo e vederlo fallire**

```bash
go test ./internal/engine/ -run TestSearchScoredMatchesSearchOrder -v
```

Atteso: FAIL con `idx.SearchScored undefined`.

- [ ] **Passo 3: estrarre il corpo di Search**

Rinominare l'attuale `func (idx *InvertedIndex) Search(...)` in `SearchScored`, cambiandone **solo** la parte finale: dove oggi costruisce `docIDs` e ritorna `([]string, ...)`, deve ritornare `(results, highlights)` con `results` già ordinato come adesso. Poi aggiungere l'involucro:

```go
// Search ritorna solo gli id, nell'ordine deciso da SearchScored.
// Firma invariata: è l'API che usano gli handler.
func (idx *InvertedIndex) Search(query string, settings Settings, fuzziness string, queryVector []float64) ([]string, map[string][]string) {
	results, highlights := idx.SearchScored(query, settings, fuzziness, queryVector)

	var docIDs []string
	for _, r := range results {
		docIDs = append(docIDs, r.DocID)
	}
	return docIDs, highlights
}
```

Non spostare, non semplificare e non riordinare nient'altro dentro `SearchScored`. L'unico obiettivo è che il punteggio esca.

- [ ] **Passo 4: verificare**

```bash
make check
```

Atteso: il nuovo test passa e **tutti quelli già esistenti continuano a passare**. Se un test esistente cambia esito, l'estrazione ha modificato il comportamento: annullare e rifarla.

- [ ] **Passo 5: commit**

```bash
git add internal/engine/ranker.go internal/engine/scored_test.go
git commit -m "engine: expose ranked scores via SearchScored without changing order"
```

## Task A3: Congelare il baseline

È il task che rende possibile tutto il resto. Un test che fissa l'ordine esatto dei risultati su un corpus giocattolo: da qui in poi, qualunque modifica cambi quell'ordine lo fa rompere. Serve per non spostare il baseline senza accorgersene, ed è anche il test che in tesi dimostra che il comportamento di partenza è ancora eseguibile.

**File:**
- Test: `internal/engine/baseline_test.go` (crea)

**Interfacce:**
- Consuma: `SearchScored` dal Task A2.
- Produce: il test `TestBaselineRankingIsFrozen`, che ogni fase della tesi deve poter far passare con il flag di configurazione a default.

- [ ] **Passo 1: scrivere il test con l'ordine atteso vuoto**

```go
package engine

import "testing"

func baselineIndex() (*InvertedIndex, Settings) {
	idx := NewInvertedIndex()
	s := DefaultSettings()
	s.SearchableFields = []string{"titolo", "testo"}
	s.FieldWeights = map[string]float64{"titolo": 2.0, "testo": 1.0}

	idx.AddDocument("d1", map[string]interface{}{
		"titolo": "Fattura 2026/0173 Rossi SpA",
		"testo":  "manutenzione impianto, imponibile 1.200 euro",
	}, s)
	idx.AddDocument("d2", map[string]interface{}{
		"titolo": "Contratto di manutenzione Rossi",
		"testo":  "durata annuale, rinnovo tacito",
	}, s)
	idx.AddDocument("d3", map[string]interface{}{
		"titolo": "DDT 2026/0173",
		"testo":  "consegna materiale Rossi SpA",
	}, s)
	idx.AddDocument("d4", map[string]interface{}{
		"titolo": "Delibera comunale",
		"testo":  "nessuna attinenza",
	}, s)
	return idx, s
}

func TestBaselineRankingIsFrozen(t *testing.T) {
	idx, s := baselineIndex()

	casi := []struct {
		nome    string
		query   string
		atteso  []string
	}{
		{"identificatore", "2026/0173", nil},
		{"entita", "Rossi SpA", nil},
		{"concetto", "manutenzione", nil},
		{"refuso", "manutenzine", nil},
	}

	for _, c := range casi {
		t.Run(c.nome, func(t *testing.T) {
			got, _ := idx.Search(c.query, s, "auto", nil)
			if len(got) != len(c.atteso) {
				t.Fatalf("query %q: attesi %v, ottenuti %v", c.query, c.atteso, got)
			}
			for i := range got {
				if got[i] != c.atteso[i] {
					t.Fatalf("query %q: attesi %v, ottenuti %v", c.query, c.atteso, got)
				}
			}
		})
	}
}
```

- [ ] **Passo 2: lanciarlo per leggere l'ordine reale**

```bash
go test ./internal/engine/ -run TestBaselineRankingIsFrozen -v
```

Fallisce per forza, perché `atteso` è `nil` ovunque. Il messaggio di errore stampa `ottenuti`: **quello è il baseline**. Copiarlo dentro `atteso`, caso per caso.

Attenzione: si trascrive quello che il motore fa **oggi**, non quello che dovrebbe fare. Se un ordine sembra sbagliato, è esattamente il difetto che la tesi deve correggere: va congelato così com'è e annotato, non aggiustato.

- [ ] **Passo 3: annotare cosa si vede**

Sotto ogni caso, un commento con l'ordine ottenuto e, se salta all'occhio, quale dei tre difetti lo spiega. Esempio della forma da usare:

```go
// "Rossi SpA" -> d1, d3, d2: d2 contiene "Rossi" ma non "SpA".
// Nessun IDF: "SpA" pesa come "Rossi" anche se compare ovunque.
```

Questi commenti sono materiale di tesi già scritto, non decorazione.

- [ ] **Passo 4: aggiungere il caso vettoriale**

Stesso corpus, con `_vector` su due documenti e un `queryVector` fisso, per esercitare il ramo ibrido di `ranker.go:203-222`. Vettori corti scritti a mano, deterministici:

```go
func TestBaselineHybridIsFrozen(t *testing.T) {
	idx, s := baselineIndex()
	idx.AddDocument("v1", map[string]interface{}{
		"titolo":  "Assistenza tecnica",
		"_vector": []interface{}{1.0, 0.0, 0.0},
	}, s)
	idx.AddDocument("v2", map[string]interface{}{
		"titolo":  "Assistenza legale",
		"_vector": []interface{}{0.0, 1.0, 0.0},
	}, s)

	got, _ := idx.Search("assistenza", s, "auto", []float64{1.0, 0.0, 0.0})
	atteso := []string{} // da riempire come al Passo 2
	if len(got) != len(atteso) {
		t.Fatalf("attesi %v, ottenuti %v", atteso, got)
	}
	for i := range got {
		if got[i] != atteso[i] {
			t.Fatalf("attesi %v, ottenuti %v", atteso, got)
		}
	}
}
```

- [ ] **Passo 5: verificare**

```bash
make check
```

Atteso: tutto verde, con i due nuovi test che passano.

- [ ] **Passo 6: commit**

```bash
git add internal/engine/baseline_test.go
git commit -m "test: freeze the current ranking order as the thesis baseline"
```

---

# Parte B - Anticipare la Fase 0 della tesi

La Fase 0 di [piano-implementazione.md](piano-implementazione.md) è l'impianto di valutazione. È l'unica parte del piano di tesi che si può tirare avanti adesso senza rischi, perché non tocca il ranking: costruisce il metro, non cambia la cosa misurata. Ed è anche la più noiosa, quindi averla dietro le spalle a febbraio vale molto.

I task non li riscrivo qui: stanno già scritti per intero in quel documento. Qui dico **quali e in che ordine**.

## Task B1: Chiudere la scelta di C1 (entro ottobre)

È il punto aperto numero 1 di `piano-implementazione.md`. È una decisione, non del codice, e blocca tutto il resto della Fase 0.

- [ ] Scegliere una collezione pubblica piccola e con giudizi già pubblicati, in modo che l'intera valutazione giri in minuti e non in ore a ogni modifica
- [ ] Scaricarla in `eval/corpora/c1-public/` con dentro un `SOURCE.md` che registra provenienza, versione e data
- [ ] Verificare che ci sia un valore di riferimento noto in letteratura per BM25 su quella collezione: senza, C1 non serve a niente, perché il suo unico scopo è dire se la mia implementazione di BM25 ha un bug
- [ ] Commit

## Task B2: Task 0.2 e 0.3 del piano di tesi (novembre)

Lettura di qrels e query, poi le metriche. Sono codice puro, senza dipendenze esterne, testabile con numeri calcolati a mano. È il pezzo che meglio si presta alle sere spezzate, perché ogni metrica è un test a sé.

- [ ] Task 0.2 - lettura di qrels e query (`piano-implementazione.md`, riga 92)
- [ ] Task 0.3 - metriche (`piano-implementazione.md`, riga 211)

## Dove ci si ferma senza danno

**Il Task 0.4 (esecutore della valutazione) e il Task 0.5 (misura del baseline) restano a febbraio.** Non perché siano difficili, ma perché richiedono il corpus C2 annotato, e annotare è la cosa che non si riesce a fare a pezzetti di sera fra un esame e l'altro.

Arrivare a febbraio con A0-A3, B1 e B2 fatti significa partire con il metro già scritto e testato, e dover fare solo la parte di annotazione. È un buon punto di arrivo per l'autunno.

---

# Parte C - Documentale

## Quello che ho scoperto guardando il database, e che cambia le carte

Prima di scrivere i task ho controllato lo schema. Due cose che il piano di tesi dà per scontate **non esistono in Documentale**, ed è meglio saperlo adesso che a febbraio.

**1. Il testo integrale dei documenti non è salvato da nessuna parte.** La tabella `document_versions` ha `name`, `summary`, `notes`, `tags`, `subjects`, `document_date`, `expiration_date`, `has_signature`. Non c'è nessuna colonna con il contenuto del PDF, e la ricerca non ne cerca: l'indice Elasticsearch (`ElasticsearchService::createDocumentsIndex()`, riga 25) mappa esattamente `name`, `tags`, `summary`, `subjects`, `notes`, `additional_data`. Il testo del documento passa dal modello e torna indietro solo come output strutturato: nessuno lo conserva.

**2. Non esiste una conferma per singolo campo.** Il piano di tesi prevede `meta_pred_confirmed`, con `DocumentSuggestion` come surrogato. Ma `document_suggestions` ha solo `document_id`, `entity_id` e uno `status`: è una conferma **per documento sull'entità**, non per campo. Su `document_fields` (`string_value`, `boolean_value`, `number_value`, `date_value` dopo l'alter del 5 agosto) non c'è nessun flag di conferma.

La prima è quella che conta. Cambia cosa vuol dire "documento" nel corpus di tesi, quindi va decisa prima di scrivere l'export, non dopo.

## Task C0: Decidere cosa è un documento nel corpus (entro ottobre)

Non è codice, è la decisione che tiene in piedi o fa cadere il corpus C2.

**Opzione A - il corpus è fatto di schede di metadati.** Ogni documento è `name` + `summary` + `tags` + `subjects` + `notes` + i campi estratti. Testi corti, cento o duecento parole.

- A favore: è esattamente ciò che Documentale cerca oggi, quindi la tesi misura il sistema vero e il confronto con Elasticsearch è onesto.
- Contro: su testi così corti l'IDF conta meno di quanto conti su documenti lunghi, e una parte dell'interesse della domanda di tesi si sgonfia.
- Costo: zero, i dati ci sono già.

**Opzione B - si aggiunge la persistenza del testo integrale**, e il corpus contiene i documenti veri.

- A favore: è il caso in cui la domanda di tesi ha più senso, ed è **una funzionalità che a Documentale manca davvero**: oggi un documento non si trova cercando una parola che sta nel suo corpo, solo nel riassunto. Per l'azienda è valore, non un favore alla tesi.
- Contro: è una modifica al prodotto, quindi va concordata, e conservare il testo integrale di documenti di clienti ha implicazioni di spazio e di riservatezza che non decido io.
- Costo: una migration, un punto nella pipeline di estrazione, la reindicizzazione.

- [ ] Verificare se il testo integrale sia già disponibile da qualche parte nella pipeline Python senza doverlo riestrarre
- [ ] Chiedere in azienda se il testo integrale si può conservare, e con quali vincoli
- [ ] Se la risposta è sì, l'Opzione B diventa un task vero di Documentale e il corpus lo aspetta; se è no, si va con l'Opzione A e lo si scrive in `appunti.md` come vincolo della tesi, non come ripiego
- [ ] Portare la domanda al relatore a dicembre: è il tipo di vincolo su cui un relatore ha un'opinione, e scoprirlo a marzo sarebbe tardi

Finché C0 non è chiuso, il Task C1 si fa comunque, perché il grosso dell'export è identico nelle due opzioni: cambia solo il campo `text`.

## Task C1: Comando di export del corpus di valutazione

Genera il corpus nel formato del Task 0.1 del piano di tesi, con quello che in Documentale esiste davvero. `meta_true` resta vuoto: per definizione si scrive a mano.

**File:**
- Crea: `apps/laravel/app/Console/Commands/ExportEvalCorpus.php`
- Test: `apps/laravel/tests/Feature/ExportEvalCorpusTest.php`

**Interfacce:**
- Consuma: `DocumentVersion` con la relazione `fields()` verso `DocumentField` (`app/Models/DocumentVersion.php:150`) e l'accessor `getFieldsFlatAttribute()` (riga 113). `DocumentField` espone `name`, `string_value`, `boolean_value`, `number_value`, `date_value`.
- Produce: un file JSON Lines, un documento per riga, letto dal Task 0.2 del piano di tesi.

- [ ] **Passo 1: scrivere il test che fallisce**

```php
public function test_export_produces_one_json_line_per_document(): void
{
    $version = DocumentVersion::factory()->create([
        'name'    => 'Fattura 2026/0173',
        'summary' => 'Manutenzione impianto, imponibile 1.200 euro',
    ]);
    DocumentField::factory()->create([
        'document_version_id' => $version->id,
        'name'                => 'numero',
        'string_value'        => '2026/0173',
    ]);

    $path = storage_path('app/eval/corpus-test.jsonl');
    $this->artisan('app:export-eval-corpus', ['--out' => $path])->assertExitCode(0);

    $righe = file($path, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
    $this->assertCount(1, $righe);

    $doc = json_decode($righe[0], true);
    $this->assertStringContainsString('Fattura 2026/0173', $doc['text']);
    $this->assertStringContainsString('Manutenzione impianto', $doc['text']);
    $this->assertSame('2026/0173', $doc['meta_pred']['numero']);
    $this->assertSame([], $doc['meta_true']);
    $this->assertSame('metadata', $doc['text_source']);
}
```

`text_source` è il campo che rende esplicito cosa c'è dentro `text`: vale `metadata` con l'Opzione A e `full` con la B. Senza, fra sei mesi non si sa più su cosa sono stati calcolati i numeri.

- [ ] **Passo 2: lanciarlo e vederlo fallire**

```bash
cd apps/laravel && php artisan test --filter=ExportEvalCorpusTest
```

Atteso: FAIL, il comando `app:export-eval-corpus` non esiste.

- [ ] **Passo 3: scrivere il comando**

```php
protected $signature = 'app:export-eval-corpus {--out=} {--limit=300}';
protected $description = 'Exports document metadata and extracted fields as a JSONL evaluation corpus';

public function handle(): int
{
    $out = $this->option('out') ?: storage_path('app/eval/corpus.jsonl');
    @mkdir(dirname($out), 0775, true);
    $fh = fopen($out, 'w');
    $n = 0;

    DocumentVersion::with('fields')
        ->limit((int) $this->option('limit'))
        ->chunk(50, function ($versioni) use ($fh, &$n) {
            foreach ($versioni as $v) {
                // Opzione A: il testo cercabile e' l'unione dei campi che
                // Elasticsearch indicizza oggi. Con l'Opzione B qui ci va il
                // testo integrale e text_source diventa 'full'.
                $text = trim(implode("
", array_filter([
                    $v->name,
                    $v->summary,
                    $v->notes,
                    is_array($v->tags) ? implode(' ', $v->tags) : null,
                    is_array($v->subjects) ? implode(' ', $v->subjects) : null,
                ])));

                fwrite($fh, json_encode([
                    'id'          => 'doc-' . str_pad((string) $v->id, 4, '0', STR_PAD_LEFT),
                    'text'        => $text,
                    'text_source' => 'metadata',
                    'meta_true'   => (object) [],
                    'meta_pred'   => $v->fields_flat,
                ], JSON_UNESCAPED_UNICODE) . "\n");
                $n++;
            }
        });

    fclose($fh);
    $this->info("Corpus scritto in {$out}: {$n} documenti");
    return self::SUCCESS;
}
```

Nota su `meta_pred_confirmed`: **non c'e' e non si inventa.** In Documentale la conferma e' per documento sull'entita' (`document_suggestions.status`), non per campo. Se la Fase 3 della tesi ne ha bisogno per campo, o lo si aggiunge come funzionalita' vera oppure si riscrive quel pezzo del piano di tesi usando la conferma per documento. Da decidere insieme al C0, non qui.

- [ ] **Passo 4: verificare**

```bash
php artisan test --filter=ExportEvalCorpusTest
```

Atteso: PASS.

- [ ] **Passo 5: girarlo su staging e guardare l'output**

```bash
php artisan app:export-eval-corpus --limit=20 --out=/tmp/corpus-prova.jsonl
head -1 /tmp/corpus-prova.jsonl | python3 -m json.tool
awk '{ print length($0) }' /tmp/corpus-prova.jsonl | sort -n | tail -3
```

Tre cose da guardare a occhio prima di fidarsi: che `text` non sia quasi vuoto (se lo e', l'Opzione A non regge e il C0 si decide da solo), che i campi estratti abbiano senso, e **che non ci sia dentro niente di un cliente reale**. Il file resta in `/tmp` e non entra in nessun repo finche' l'azienda non ha detto cosa e' pubblicabile.

- [ ] **Passo 6: commit**

```bash
git add app/Console/Commands/ExportEvalCorpus.php tests/Feature/ExportEvalCorpusTest.php
git commit -m "feat: add eval corpus export command for thesis evaluation"
```

## Task C2: Registrare le query di ricerca

Oggi le ricerche passano da `ElasticsearchService::fuzzySearch()` (riga 97) e non lasciano traccia. Registrarle costa poco e a febbraio fa la differenza fra scrivere sessanta query inventate e partire da quelle che la gente digita davvero.

Non risolve il problema di fondo, che resta scritto in `appunti.md`: c'e' solo staging, quindi il volume sara' piccolo. Ma anche duecento query vere valgono piu' di zero, e sono gratis se il log parte adesso invece che a febbraio.

**File:**
- Crea: `apps/laravel/database/migrations/xxxx_create_search_logs_table.php`
- Crea: `apps/laravel/app/Models/SearchLog.php`
- Modifica: `apps/laravel/app/Services/ElasticsearchService.php:97`

**Interfacce:**
- Produce: la tabella `search_logs`, letta a febbraio per estrarre le query del corpus C2.

- [ ] **Passo 1: migration**

```php
Schema::create('search_logs', function (Blueprint $table) {
    $table->id();
    $table->string('term');
    $table->string('type')->nullable();
    $table->unsignedInteger('results_count')->default(0);
    $table->unsignedInteger('duration_ms')->nullable();
    $table->foreignId('user_id')->nullable()->constrained('users')->nullOnDelete();
    $table->timestamps();
    $table->index('created_at');
});
```

- [ ] **Passo 2: registrare dentro fuzzySearch**

In `fuzzySearch`, cronometrare la chiamata e scrivere il log prima del return. Il log **non deve mai far fallire la ricerca**: e' uno dei pochi punti in cui ingoiare l'eccezione e' giustificato, perche' e' telemetria e non fa parte del flusso.

```php
$inizio = microtime(true);
// ... corpo attuale di fuzzySearch, invariato, che produce $risultati ...

try {
    SearchLog::create([
        'term'          => $term,
        'type'          => $type,
        'results_count' => count($risultati),
        'duration_ms'   => (int) ((microtime(true) - $inizio) * 1000),
        'user_id'       => auth()->id(),
    ]);
} catch (\Throwable $e) {
    report($e);
}

return $risultati;
```

- [ ] **Passo 3: verificare a mano**

Fare tre ricerche dall'interfaccia, poi:

```bash
php artisan tinker --execute="dump(\App\Models\SearchLog::latest()->take(3)->get(['term','results_count','duration_ms'])->toArray());"
```

Atteso: le tre query appena fatte, con numero di risultati e durata.

- [ ] **Passo 4: commit**

```bash
git add database/migrations app/Models/SearchLog.php app/Services/ElasticsearchService.php
git commit -m "feat: log search queries to build the thesis query set"
```

## Il TODO.md di Documentale

`TODO.md` ha una decina di voci aperte che non c'entrano con la tesi: notifiche via websocket, rinomina di cartelle e file, il fix dell'upload di cartelle con molti file, la questione dei `document_version_fields` da ricreare con chiave combinata.

**Sono lavoro aziendale e vanno fatte con le priorita' dell'azienda, non con quelle di questo piano.** Le cito solo per dire che non le ho incluse. Una pero' si incrocia: la voce sulla chiave combinata dei `document_version_fields` tocca proprio la tabella da cui l'export legge, quindi **va fatta prima del Task C1**, altrimenti l'export va riscritto.

## Fuori perimetro

- **Qualunque modifica al ranking.** È il punto di tutto il documento.
- **`rustann` e gli indici approssimati.** Già fuori dal perimetro della tesi, decisione del 15 settembre 2026.
- **La Fase 4 del piano di tesi** (innesto vero in Documentale accanto a Elasticsearch). Va fatta quando c'è qualcosa che vale la pena innestare, cioè dopo le Fasi 1-3.
- **Rimettere le GitHub Actions.** Sono state tolte di proposito, il Task A1 dà lo stesso servizio in locale.

## Ordine e calendario

| Quando | Cosa | Perché lì |
|---|---|---|
| Fine settembre | A0, A1 | Senza Go non si fa niente, e sono due sere |
| Ottobre | A2, A3, B1, **C0** | A3 protegge tutto il resto; B1 e C0 sono decisioni che bloccano il lavoro di novembre |
| Novembre | C1, B2 | C1 va fatto quando c'è accesso a staging con calma, B2 sono metriche testabili a pezzetti |
| Dicembre | C2, e basta | Il mese dei progetti d'esame: mettere altro qui è illudersi |

C0 e B1 sono le due decisioni, e vanno chiuse entro ottobre: se slittano, novembre si blocca e l'autunno si perde.

A dicembre, oltre a questo, c'è la riproposta della tesi a Bonnici e Dal Palù descritta in [appunti.md](appunti.md). Il Task A3 serve anche lì: fa vedere in trenta secondi che il baseline è congelato e misurabile, che è esattamente la differenza fra "ho un motore di ricerca" e "ho un esperimento".
