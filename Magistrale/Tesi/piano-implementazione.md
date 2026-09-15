# Piano di implementazione - Tesi magistrale

> **Per chi esegue:** i passi usano checkbox (`- [ ]`) per il tracciamento. Ogni task si chiude con un deliverable testabile da solo e un commit.

**Obiettivo:** portare il ranking di Koskidex da euristica scritta a mano a recupero misurato e difendibile, e usarlo come motore di ricerca di Documentale al posto di Elasticsearch, producendo per ogni correzione un risultato numerico sul corpus reale di un documentale.

**Architettura:** si costruisce per prima cosa l'impianto di valutazione della rilevanza, che oggi non esiste. Poi ogni difetto del ranking viene corretto dietro un interruttore di configurazione, in modo che il comportamento attuale resti sempre eseguibile come baseline e ogni capitolo abbia un confronto onesto contro il codice di partenza. L'integrazione in Documentale arriva per ultima, quando c'è qualcosa che vale la pena integrare.

**Stack:** Go 1.25 (Koskidex, zero dipendenze esterne), Laravel 12 + PHP 8.4 e React 19 (Documentale), FastAPI + Python (servizio AI di Documentale).

**Cosa resta fuori:** `rustann` e gli indici approssimati (HNSW, Product Quantization). La forza bruta regge il volume di un documentale aziendale, quindi un indice ANN sarebbe una domanda di ricerca senza un bisogno reale. Decisione presa il 15 settembre 2026.

## Vincoli globali

- Koskidex resta a **zero dipendenze esterne** oltre `golang.org/x/text`, che è già in `go.mod`. Vale anche per l'impianto di valutazione.
- Ogni modifica al ranking è **selezionabile da `Settings`**, con il comportamento attuale come valore di default. Nessun capitolo può rendere irriproducibile il baseline del capitolo precedente.
- Gli embedding **non** li genera Koskidex: arrivano dal client nel campo `_vector`, come oggi.
- Ogni numero riportato nella tesi nasce da un file di risultati versionato, mai da una esecuzione a mano non registrata.
- Le misure di rilevanza e quelle di sistema (latenza, memoria) restano separate: seedare dati va bene per le seconde, mai per le prime.

---

## Fase 0 - Impianto di valutazione

Senza questa fase nessuna delle successive ha un metro. È anche la fase che va fatta **prima** di guardare come si comporta il motore, per non scegliere le metriche a posteriori in modo che diano ragione.

### Task 0.1: Corpus e giudizi di rilevanza

**File:**
- Crea: `eval/corpora/README.md`
- Crea: `eval/corpora/c1-public/` (collezione pubblica)
- Crea: `eval/corpora/c2-documentale/` (corpus di dominio)

**Interfacce:**
- Produce: due corpora sul disco nel formato letto da `internal/eval/qrels.go` (Task 0.2).

Servono due corpora, e servono entrambi per ragioni diverse.

**C1, collezione pubblica.** Serve a dimostrare che l'implementazione di BM25 è corretta, non a rispondere alla domanda di tesi. Si prende una collezione con giudizi già pubblicati e si verifica di ottenere numeri in linea con quelli noti in letteratura. Se BM25 scritto da te dà nDCG@10 lontano dal valore atteso su una collezione standard, l'implementazione ha un bug, e lo scopri prima di costruirci sopra tre capitoli.

**C2, corpus di dominio.** È quello che risponde alla domanda di tesi. Documenti amministrativi italiani veri (fatture, DDT, contratti, delibere), con una parte di metadati estratti dalla pipeline di Documentale.

Sul C2 vale la regola che decide se la tesi sta in piedi: **i giudizi di rilevanza si scrivono prima di vedere cosa risponde il motore.** Altrimenti sono circolari e in discussione te lo contestano.

- [ ] **Passo 1: scegliere e scaricare C1**

Una collezione piccola e con giudizi pubblici, così gira in fretta a ogni modifica. Scaricala in `eval/corpora/c1-public/` con dentro un `SOURCE.md` che registra da dove viene, quale versione e in che data è stata scaricata.

- [ ] **Passo 2: costruire il corpus documentale C2**

Almeno 300 documenti, distribuiti per tipologia. Ogni documento è un JSON con testo pieno, metadati veri (scritti a mano) e metadati predetti dalla pipeline, tenuti in campi distinti:

```json
{
  "id": "doc-0001",
  "text": "...testo integrale del documento...",
  "tipo": "fattura",
  "meta_true":  {"fornitore": "Rossi SpA", "numero": "2026/0173", "data": "2026-03-14"},
  "meta_pred":  {"fornitore": "Rossi S.p.A.", "numero": "2026/0173", "data": "2026-03-14"},
  "meta_pred_confirmed": {"fornitore": false, "numero": true, "data": true}
}
```

`meta_true` è la verità scritta a mano. `meta_pred` è ciò che ha estratto il modello. `meta_pred_confirmed` dice se un umano ha confermato quel campo: è il surrogato del flusso `DocumentSuggestion` di Documentale, e serve alla Fase 3.

- [ ] **Passo 3: scrivere le query e i giudizi**

Almeno 60 query sul C2, scritte guardando i documenti e non il motore, ognuna etichettata con la sua classe:

| Classe | Esempio | Perché conta |
|---|---|---|
| `identifier` | `fattura 2026/0173` | è dove il denso sbaglia |
| `entity` | `Rossi SpA` | nome proprio, ortografia variabile |
| `concept` | `contratti di manutenzione scaduti` | è dove il denso serve |
| `mixed` | `fatture Rossi marzo 2026` | il caso reale più frequente |

Giudizi in formato TREC, un giudizio per riga, rilevanza da 0 a 3:

```
q001 0 doc-0001 3
q001 0 doc-0047 1
q002 0 doc-0112 2
```

- [ ] **Passo 4: commit**

```bash
git add eval/corpora
git commit -m "eval: add public and domain corpora with relevance judgments"
```

### Task 0.2: Lettura di qrels e query

**File:**
- Crea: `internal/eval/qrels.go`
- Test: `internal/eval/qrels_test.go`

**Interfacce:**
- Produce: `LoadQrels(path string) (map[string]map[string]int, error)`, `LoadQueries(path string) ([]Query, error)`, `type Query struct { ID, Text, Class string; Vector []float64 }`

- [ ] **Passo 1: scrivere il test che fallisce**

```go
package eval

import "testing"

func TestLoadQrels(t *testing.T) {
	q, err := LoadQrels("testdata/qrels.txt")
	if err != nil {
		t.Fatalf("errore inatteso: %v", err)
	}
	if got := q["q001"]["doc-0001"]; got != 3 {
		t.Errorf("q001/doc-0001 = %d, atteso 3", got)
	}
	if _, ok := q["q001"]["doc-9999"]; ok {
		t.Error("doc-9999 non deve esistere in q001")
	}
}

func TestLoadQrelsIgnoraRigheMalformate(t *testing.T) {
	q, err := LoadQrels("testdata/qrels_sporco.txt")
	if err != nil {
		t.Fatalf("una riga malformata non deve far fallire il caricamento: %v", err)
	}
	if len(q) != 1 {
		t.Errorf("attesa 1 query valida, trovate %d", len(q))
	}
}
```

Crea `internal/eval/testdata/qrels.txt` con le tre righe dell'esempio del Task 0.1, e `testdata/qrels_sporco.txt` con una riga valida e una a tre soli campi.

- [ ] **Passo 2: eseguire il test e verificare che fallisca**

Esegui: `go test ./internal/eval/ -run TestLoadQrels -v`
Atteso: FAIL, `undefined: LoadQrels`

- [ ] **Passo 3: implementare**

```go
package eval

import (
	"bufio"
	"os"
	"strconv"
	"strings"
)

// LoadQrels legge un file di giudizi in formato TREC:
//   queryID iterazione docID rilevanza
// Le righe malformate vengono saltate senza errore, così un refuso
// nell'annotazione non blocca un'intera sessione di valutazione.
func LoadQrels(path string) (map[string]map[string]int, error) {
	f, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer f.Close()

	out := make(map[string]map[string]int)
	sc := bufio.NewScanner(f)
	for sc.Scan() {
		fields := strings.Fields(sc.Text())
		if len(fields) != 4 {
			continue
		}
		rel, err := strconv.Atoi(fields[3])
		if err != nil {
			continue
		}
		if out[fields[0]] == nil {
			out[fields[0]] = make(map[string]int)
		}
		out[fields[0]][fields[2]] = rel
	}
	return out, sc.Err()
}
```

- [ ] **Passo 4: eseguire i test**

Esegui: `go test ./internal/eval/ -v`
Atteso: PASS

- [ ] **Passo 5: aggiungere `LoadQueries` con lo stesso ciclo**

Test da scrivere per primo, poi l'implementazione. Le query stanno in un JSONL, una per riga:

```json
{"id":"q001","text":"fattura 2026/0173","class":"identifier"}
```

```go
type Query struct {
	ID     string    `json:"id"`
	Text   string    `json:"text"`
	Class  string    `json:"class"`
	Vector []float64 `json:"vector,omitempty"`
}
```

- [ ] **Passo 6: commit**

```bash
git add internal/eval
git commit -m "eval: load TREC-style qrels and JSONL query sets"
```

### Task 0.3: Metriche

**File:**
- Crea: `internal/eval/metrics.go`
- Test: `internal/eval/metrics_test.go`

**Interfacce:**
- Produce: `NDCG(ranked []string, rel map[string]int, k int) float64`, `MRR(ranked []string, rel map[string]int) float64`, `RecallAt(ranked []string, rel map[string]int, k int) float64`, `PrecisionAt(ranked []string, rel map[string]int, k int) float64`

Le metriche vanno testate su casi calcolati a mano. È l'unico punto del progetto in cui un errore silenzioso invalida tutta la tesi, quindi i valori attesi si calcolano sulla carta prima di scrivere il codice.

- [ ] **Passo 1: scrivere il test che fallisce**

```go
package eval

import (
	"math"
	"testing"
)

func TestNDCGRankingPerfetto(t *testing.T) {
	ranked := []string{"a", "b", "c"}
	rel := map[string]int{"a": 3, "b": 2, "c": 1}
	if got := NDCG(ranked, rel, 3); math.Abs(got-1.0) > 1e-9 {
		t.Errorf("NDCG = %v, atteso 1.0", got)
	}
}

func TestNDCGRankingInvertito(t *testing.T) {
	// DCG  = 1/log2(2) + 3/log2(3) + 7/log2(4) = 1 + 1.8927892607 + 3.5 = 6.3927892607
	// IDCG = 7/log2(2) + 3/log2(3) + 1/log2(4) = 7 + 1.8927892607 + 0.5 = 9.3927892607
	// nDCG = 0.680615...
	ranked := []string{"c", "b", "a"}
	rel := map[string]int{"a": 3, "b": 2, "c": 1}
	want := 6.3927892607143 / 9.3927892607143
	if got := NDCG(ranked, rel, 3); math.Abs(got-want) > 1e-9 {
		t.Errorf("NDCG = %v, atteso %v", got, want)
	}
}

func TestNDCGNessunRilevante(t *testing.T) {
	if got := NDCG([]string{"x", "y"}, map[string]int{"a": 3}, 2); got != 0 {
		t.Errorf("NDCG = %v, atteso 0 quando nessun rilevante e' recuperato", got)
	}
}

func TestMRR(t *testing.T) {
	// primo rilevante in posizione 3 -> 1/3
	ranked := []string{"x", "y", "a"}
	rel := map[string]int{"a": 1}
	if got := MRR(ranked, rel); math.Abs(got-1.0/3.0) > 1e-9 {
		t.Errorf("MRR = %v, atteso 0.333...", got)
	}
}
```

- [ ] **Passo 2: eseguire e verificare che fallisca**

Esegui: `go test ./internal/eval/ -run "TestNDCG|TestMRR" -v`
Atteso: FAIL, `undefined: NDCG`

- [ ] **Passo 3: implementare**

```go
package eval

import (
	"math"
	"sort"
)

// gain usa il guadagno esponenziale 2^rel - 1, la convenzione piu' diffusa
// e quella usata dai lavori con cui confrontiamo i risultati.
func gain(rel int) float64 {
	if rel <= 0 {
		return 0
	}
	return math.Pow(2, float64(rel)) - 1
}

func dcg(gains []float64) float64 {
	var sum float64
	for i, g := range gains {
		sum += g / math.Log2(float64(i+2))
	}
	return sum
}

// NDCG calcola il guadagno cumulato scontato normalizzato ai primi k risultati.
// Ritorna 0 se per la query non esiste alcun documento rilevante.
func NDCG(ranked []string, rel map[string]int, k int) float64 {
	if k > len(ranked) {
		k = len(ranked)
	}
	got := make([]float64, 0, k)
	for _, id := range ranked[:k] {
		got = append(got, gain(rel[id]))
	}

	ideal := make([]float64, 0, len(rel))
	for _, r := range rel {
		ideal = append(ideal, gain(r))
	}
	sort.Sort(sort.Reverse(sort.Float64Slice(ideal)))
	if len(ideal) > k {
		ideal = ideal[:k]
	}

	idcg := dcg(ideal)
	if idcg == 0 {
		return 0
	}
	return dcg(got) / idcg
}

// MRR ritorna il reciproco della posizione del primo documento rilevante.
func MRR(ranked []string, rel map[string]int) float64 {
	for i, id := range ranked {
		if rel[id] > 0 {
			return 1.0 / float64(i+1)
		}
	}
	return 0
}

// RecallAt e' la frazione di documenti rilevanti recuperati nei primi k.
func RecallAt(ranked []string, rel map[string]int, k int) float64 {
	total := 0
	for _, r := range rel {
		if r > 0 {
			total++
		}
	}
	if total == 0 {
		return 0
	}
	if k > len(ranked) {
		k = len(ranked)
	}
	hit := 0
	for _, id := range ranked[:k] {
		if rel[id] > 0 {
			hit++
		}
	}
	return float64(hit) / float64(total)
}

// PrecisionAt e' la frazione di rilevanti fra i primi k risultati.
func PrecisionAt(ranked []string, rel map[string]int, k int) float64 {
	if k > len(ranked) {
		k = len(ranked)
	}
	if k == 0 {
		return 0
	}
	hit := 0
	for _, id := range ranked[:k] {
		if rel[id] > 0 {
			hit++
		}
	}
	return float64(hit) / float64(k)
}
```

- [ ] **Passo 4: eseguire i test**

Esegui: `go test ./internal/eval/ -v`
Atteso: PASS su tutti

- [ ] **Passo 5: commit**

```bash
git add internal/eval/metrics.go internal/eval/metrics_test.go
git commit -m "eval: add nDCG, MRR, recall@k and precision@k with hand-checked tests"
```

### Task 0.4: Esecutore della valutazione

**File:**
- Crea: `internal/eval/runner.go`
- Crea: `cmd/eval/main.go`
- Test: `internal/eval/runner_test.go`

**Interfacce:**
- Consuma: `LoadQrels`, `LoadQueries`, `NDCG`, `MRR`, `RecallAt`, `PrecisionAt` (Task 0.2, 0.3); `engine.InvertedIndex.Search` e `engine.Settings` esistenti.
- Produce: `type Result struct { Query, Class string; NDCG10, MRR, Recall10, Precision10 float64; LatencyMs float64 }`, `Run(idx *engine.InvertedIndex, qs []Query, qrels map[string]map[string]int, s engine.Settings) []Result`

L'identificativo della configurazione non sta dentro `Result`: lo scrive `cmd/eval` una volta sola nell'intestazione del file dei risultati, perché è lo stesso per tutte le righe di una esecuzione e ripeterlo su ognuna è solo rumore.

L'esecutore scrive un JSONL con una riga per query. La riga porta l'identificativo della configurazione e il commit, così ogni numero della tesi si può risalire fino al codice che l'ha prodotto.

- [ ] **Passo 1: scrivere il test che fallisce**

```go
func TestRunProduceUnaRigaPerQuery(t *testing.T) {
	idx := engine.NewInvertedIndex()
	s := engine.DefaultSettings()
	idx.AddDocument("d1", map[string]interface{}{"text": "contratto di manutenzione"}, s)
	idx.AddDocument("d2", map[string]interface{}{"text": "fattura elettrica"}, s)

	qs := []Query{{ID: "q1", Text: "contratto", Class: "concept"}}
	qrels := map[string]map[string]int{"q1": {"d1": 3}}

	res := Run(idx, qs, qrels, s)
	if len(res) != 1 {
		t.Fatalf("attesa 1 riga, ottenute %d", len(res))
	}
	if res[0].NDCG10 != 1.0 {
		t.Errorf("NDCG10 = %v, atteso 1.0 (unico rilevante in prima posizione)", res[0].NDCG10)
	}
	if res[0].Class != "concept" {
		t.Errorf("la classe della query deve essere riportata nel risultato")
	}
}
```

- [ ] **Passo 2: eseguire e verificare che fallisca**

Esegui: `go test ./internal/eval/ -run TestRun -v`
Atteso: FAIL, `undefined: Run`

- [ ] **Passo 3: implementare `Run`**

```go
// Run esegue ogni query contro l'indice e ritorna una riga di metriche per query.
// La latenza misurata comprende solo la chiamata a Search, non la costruzione
// dell'indice, perche' e' quella che confrontiamo fra configurazioni diverse.
func Run(idx *engine.InvertedIndex, qs []Query, qrels map[string]map[string]int, s engine.Settings) []Result {
	out := make([]Result, 0, len(qs))
	for _, q := range qs {
		start := time.Now()
		ranked, _ := idx.Search(q.Text, s, "auto", q.Vector)
		elapsed := time.Since(start)

		rel := qrels[q.ID]
		out = append(out, Result{
			Query:       q.ID,
			Class:       q.Class,
			NDCG10:      NDCG(ranked, rel, 10),
			MRR:         MRR(ranked, rel),
			Recall10:    RecallAt(ranked, rel, 10),
			Precision10: PrecisionAt(ranked, rel, 10),
			LatencyMs:   float64(elapsed.Microseconds()) / 1000.0,
		})
	}
	return out
}
```

- [ ] **Passo 4: eseguire i test**

Esegui: `go test ./internal/eval/ -v`
Atteso: PASS

- [ ] **Passo 5: scrivere il comando `cmd/eval`**

Legge corpus, query e qrels dai percorsi passati come flag, costruisce l'indice, esegue, scrive `eval/results/<run-id>.jsonl` e stampa le medie per classe di query. Il `run-id` include il commit corrente:

```go
runID := fmt.Sprintf("%s-%s", time.Now().Format("20060102-150405"), gitCommitShort())
```

- [ ] **Passo 6: commit**

```bash
git add internal/eval cmd/eval
git commit -m "eval: add evaluation runner and cmd/eval CLI"
```

### Task 0.5: Misura del baseline

**File:**
- Crea: `eval/results/` (cartella dei risultati, versionata)
- Crea: `eval/BASELINE.md`

- [ ] **Passo 1: eseguire la valutazione sul codice attuale, senza modifiche**

```bash
go run ./cmd/eval --corpus eval/corpora/c2-documentale --queries eval/corpora/c2-documentale/queries.jsonl --qrels eval/corpora/c2-documentale/qrels.txt
```

- [ ] **Passo 2: ripetere l'esecuzione almeno 5 volte e registrare la dispersione della latenza**

La qualità è deterministica a parità di indice, la latenza no. Le due vanno riportate diversamente: la prima come valore singolo, la seconda come mediana con intervallo.

- [ ] **Passo 3: scrivere `eval/BASELINE.md`**

Tabella delle metriche complessive e per classe di query. Questo file è il punto di riferimento di tutta la tesi: ogni capitolo successivo si misura contro questi numeri.

- [ ] **Passo 4: commit**

```bash
git add eval/results eval/BASELINE.md
git commit -m "eval: record baseline measurements of the current ranker"
```

---

## Fase 1 - BM25

Il difetto: il punteggio lessicale è `(10 - refusi + 2*esatti) * peso_campo`. Non c'è frequenza di termine e non c'è frequenza inversa di documento. Un termine rarissimo e uno comunissimo pesano identico. Il campo `Posting.TF` esiste in `internal/engine/inverted.go:12` con il commento `// term frequency (calculated later)` e non viene usato da nessuna parte.

### Task 1.1: Statistiche dell'indice

**File:**
- Crea: `internal/engine/stats.go`
- Modifica: `internal/engine/inverted.go` (aggiunta dei campi di statistica a `InvertedIndex`)
- Test: `internal/engine/stats_test.go`

**Interfacce:**
- Produce: `func (idx *InvertedIndex) DocFreq(term string) int`, `func (idx *InvertedIndex) TermFreq(term, docID string) int`, `func (idx *InvertedIndex) DocLen(docID string) int`, `func (idx *InvertedIndex) AvgDocLen() float64`

Le statistiche si ricavano dalle postings già presenti: la frequenza di documento è il numero di `DocID` distinti in `idx.index[term]`, la frequenza di termine è quante postings ha quel documento per quel termine. La lunghezza del documento va invece accumulata durante l'indicizzazione, perché ricalcolarla a ogni query costerebbe troppo.

- [ ] **Passo 1: scrivere il test che fallisce**

```go
func TestDocFreqContaDocumentiDistinti(t *testing.T) {
	idx := NewInvertedIndex()
	s := DefaultSettings()
	// "fattura" appare due volte in d1 e una in d2: DF = 2, non 3
	idx.AddDocument("d1", map[string]interface{}{"text": "fattura fattura elettrica"}, s)
	idx.AddDocument("d2", map[string]interface{}{"text": "fattura gas"}, s)

	if got := idx.DocFreq("fattura"); got != 2 {
		t.Errorf("DocFreq = %d, atteso 2", got)
	}
	if got := idx.TermFreq("fattura", "d1"); got != 2 {
		t.Errorf("TermFreq = %d, atteso 2", got)
	}
}

func TestAvgDocLen(t *testing.T) {
	idx := NewInvertedIndex()
	s := DefaultSettings()
	idx.AddDocument("d1", map[string]interface{}{"text": "uno due tre"}, s)   // 3
	idx.AddDocument("d2", map[string]interface{}{"text": "uno"}, s)            // 1
	if got := idx.AvgDocLen(); got != 2.0 {
		t.Errorf("AvgDocLen = %v, atteso 2.0", got)
	}
}

func TestDocLenAggiornataSuCancellazione(t *testing.T) {
	idx := NewInvertedIndex()
	s := DefaultSettings()
	idx.AddDocument("d1", map[string]interface{}{"text": "uno due tre"}, s)
	idx.AddDocument("d2", map[string]interface{}{"text": "uno"}, s)
	idx.DeleteDocument("d1")
	if got := idx.AvgDocLen(); got != 1.0 {
		t.Errorf("AvgDocLen dopo cancellazione = %v, atteso 1.0", got)
	}
}
```

- [ ] **Passo 2: eseguire e verificare che fallisca**

Esegui: `go test ./internal/engine/ -run "TestDocFreq|TestAvgDocLen|TestDocLen" -v`
Atteso: FAIL, `idx.DocFreq undefined`

- [ ] **Passo 3: aggiungere i campi a `InvertedIndex`**

In `internal/engine/inverted.go`, dentro lo struct:

```go
	docLen       map[string]int // docID -> numero di token indicizzati
	totalLen     int            // somma delle lunghezze, per AvgDocLen in O(1)
```

Inizializzali in `NewInvertedIndex`, incrementali in `addDocumentLocked` mentre si scorrono gli `expandedTokens`, e decrementali in `deleteDocumentLocked`. Attenzione: `addDocumentLocked` chiama già `deleteDocumentLocked` in testa per gestire gli aggiornamenti, quindi il decremento avviene da solo e non va duplicato.

- [ ] **Passo 4: implementare `stats.go`**

```go
package engine

// DocFreq ritorna il numero di documenti distinti che contengono il termine.
// Il caller non deve tenere il lock: la funzione lo prende in lettura.
func (idx *InvertedIndex) DocFreq(term string) int {
	idx.mu.RLock()
	defer idx.mu.RUnlock()
	return idx.docFreqLocked(term)
}

func (idx *InvertedIndex) docFreqLocked(term string) int {
	postings, ok := idx.index[term]
	if !ok {
		return 0
	}
	seen := make(map[string]bool, len(postings))
	for _, p := range postings {
		seen[p.DocID] = true
	}
	return len(seen)
}

// TermFreq ritorna quante volte il termine compare nel documento.
func (idx *InvertedIndex) TermFreq(term, docID string) int {
	idx.mu.RLock()
	defer idx.mu.RUnlock()
	n := 0
	for _, p := range idx.index[term] {
		if p.DocID == docID {
			n++
		}
	}
	return n
}

// DocLen ritorna il numero di token indicizzati per il documento.
func (idx *InvertedIndex) DocLen(docID string) int {
	idx.mu.RLock()
	defer idx.mu.RUnlock()
	return idx.docLen[docID]
}

// AvgDocLen ritorna la lunghezza media dei documenti indicizzati.
func (idx *InvertedIndex) AvgDocLen() float64 {
	idx.mu.RLock()
	defer idx.mu.RUnlock()
	if len(idx.docLen) == 0 {
		return 0
	}
	return float64(idx.totalLen) / float64(len(idx.docLen))
}
```

- [ ] **Passo 5: eseguire i test, compresi quelli esistenti**

Esegui: `go test ./... -v`
Atteso: PASS. I test esistenti in `inverted_test.go` e `v2_test.go` devono restare verdi: se falliscono, la contabilità di `docLen` sulle cancellazioni è sbagliata.

- [ ] **Passo 6: commit**

```bash
git add internal/engine/stats.go internal/engine/stats_test.go internal/engine/inverted.go
git commit -m "engine: track document lengths and expose index statistics"
```

### Task 1.2: Punteggio BM25 dietro interruttore

**File:**
- Crea: `internal/engine/bm25.go`
- Modifica: `internal/engine/inverted.go` (campi nuovi in `Settings`, `DefaultSettings`)
- Modifica: `internal/engine/ranker.go:159` e `:186` (scelta dello scorer)
- Test: `internal/engine/bm25_test.go`

**Interfacce:**
- Consuma: `DocFreq`, `TermFreq`, `DocLen`, `AvgDocLen` (Task 1.1)
- Produce: `func (idx *InvertedIndex) bm25Score(term, docID string, k1, b float64) float64`; campi `Settings.Ranker string`, `Settings.BM25K1 float64`, `Settings.BM25B float64`

- [ ] **Passo 1: scrivere il test che fallisce**

```go
func TestBM25PremiaTerminiRari(t *testing.T) {
	idx := NewInvertedIndex()
	s := DefaultSettings()
	// "documento" sta ovunque, "idrogeno" in un solo documento
	for i := 0; i < 20; i++ {
		idx.AddDocument(fmt.Sprintf("d%d", i),
			map[string]interface{}{"text": "documento generico di prova"}, s)
	}
	idx.AddDocument("raro", map[string]interface{}{"text": "documento su idrogeno"}, s)

	comune := idx.bm25Score("documento", "raro", 1.2, 0.75)
	raro := idx.bm25Score("idrogeno", "raro", 1.2, 0.75)
	if raro <= comune {
		t.Errorf("il termine raro deve pesare di piu': raro=%v comune=%v", raro, comune)
	}
}

func TestBM25TerminePresenteOvunqueValeZeroOMeno(t *testing.T) {
	idx := NewInvertedIndex()
	s := DefaultSettings()
	for i := 0; i < 10; i++ {
		idx.AddDocument(fmt.Sprintf("d%d", i), map[string]interface{}{"text": "uguale"}, s)
	}
	// con IDF a la Robertson, DF = N produce un contributo non positivo
	if got := idx.bm25Score("uguale", "d0", 1.2, 0.75); got > 0 {
		t.Errorf("bm25Score = %v, atteso <= 0 per un termine in tutti i documenti", got)
	}
}

func TestBM25TermineAssenteValeZero(t *testing.T) {
	idx := NewInvertedIndex()
	idx.AddDocument("d1", map[string]interface{}{"text": "uno"}, DefaultSettings())
	if got := idx.bm25Score("inesistente", "d1", 1.2, 0.75); got != 0 {
		t.Errorf("bm25Score = %v, atteso 0", got)
	}
}
```

- [ ] **Passo 2: eseguire e verificare che fallisca**

Esegui: `go test ./internal/engine/ -run TestBM25 -v`
Atteso: FAIL, `idx.bm25Score undefined`

- [ ] **Passo 3: implementare BM25**

```go
package engine

import "math"

// bm25Score calcola il contributo BM25 di un termine per un documento.
// k1 regola la saturazione della frequenza di termine, b la normalizzazione
// sulla lunghezza del documento. I valori usuali sono k1=1.2 e b=0.75.
//
// L'IDF e' quello di Robertson e Sparck Jones nella forma usata da Lucene:
//   log(1 + (N - df + 0.5) / (df + 0.5))
// Il +1 dentro il logaritmo evita valori negativi per i termini molto comuni,
// che con la forma classica renderebbero un documento peggiore per il fatto
// di contenere il termine cercato.
func (idx *InvertedIndex) bm25Score(term, docID string, k1, b float64) float64 {
	idx.mu.RLock()
	defer idx.mu.RUnlock()

	tf := 0
	for _, p := range idx.index[term] {
		if p.DocID == docID {
			tf++
		}
	}
	if tf == 0 {
		return 0
	}

	df := idx.docFreqLocked(term)
	n := float64(len(idx.docs))
	idf := math.Log(1 + (n-float64(df)+0.5)/(float64(df)+0.5))

	avg := 0.0
	if len(idx.docLen) > 0 {
		avg = float64(idx.totalLen) / float64(len(idx.docLen))
	}
	dl := float64(idx.docLen[docID])

	norm := 1.0
	if avg > 0 {
		norm = 1 - b + b*dl/avg
	}

	return idf * (float64(tf) * (k1 + 1)) / (float64(tf) + k1*norm)
}
```

Nota sul test `TestBM25TerminePresenteOvunqueValeZeroOMeno`: con la forma `log(1 + ...)` il valore tende a zero da sopra e non diventa negativo, quindi l'asserzione va scritta come `> 0.05` anziché `> 0`. Verifica il numero esatto eseguendo il test e allinea l'asserzione al valore reale, documentando in un commento perché quella soglia.

- [ ] **Passo 4: aggiungere i campi a `Settings`**

In `internal/engine/inverted.go`, dentro `Settings`:

```go
	Ranker string  `json:"ranker"` // "legacy" (default) oppure "bm25"
	BM25K1 float64 `json:"bm25_k1"`
	BM25B  float64 `json:"bm25_b"`
```

In `DefaultSettings()`:

```go
	Ranker: "legacy",
	BM25K1: 1.2,
	BM25B:  0.75,
```

Il default resta `legacy` perché nessun capitolo può togliere la possibilità di rieseguire il baseline.

- [ ] **Passo 5: innestare la scelta nel ranker**

In `internal/engine/ranker.go`, alle righe 159 e 186, sostituisci il calcolo diretto con:

```go
			var tokenScore float64
			if settings.Ranker == "bm25" {
				tokenScore = idx.bm25ScoreLocked(token, docID, settings.BM25K1, settings.BM25B) * match.MaxWeight
			} else {
				tokenScore = (10.0 - float64(match.Typos) + float64(match.ExactMatches*2)) * match.MaxWeight
			}
			docMatches[docID].Score += tokenScore
```

Attenzione al lock: `Search` tiene già `idx.mu.RLock()` alla riga 127, quindi qui serve la variante senza lock. Estrai il corpo di `bm25Score` in un `bm25ScoreLocked` e lascia `bm25Score` come wrapper che prende il lock, come già fatto per `docFreqLocked`. Chiamare `bm25Score` da dentro `Search` provoca un deadlock su `sync.RWMutex` se nel frattempo un writer è in attesa.

- [ ] **Passo 6: eseguire tutti i test**

Esegui: `go test ./... -race -v`
Atteso: PASS. Il flag `-race` qui serve davvero: è il passo che introduce il rischio di deadlock descritto sopra.

- [ ] **Passo 7: commit**

```bash
git add internal/engine/bm25.go internal/engine/bm25_test.go internal/engine/ranker.go internal/engine/inverted.go
git commit -m "engine: add BM25 scoring behind the Ranker setting, legacy stays default"
```

### Task 1.3: Misura di BM25 contro il baseline

- [ ] **Passo 1: validare l'implementazione su C1**

Esegui la valutazione sul corpus pubblico con `Ranker: "bm25"` e confronta con i valori noti in letteratura per quella collezione. Uno scarto ampio significa che c'è un bug, non che la tua variante è migliore.

- [ ] **Passo 2: eseguire su C2 entrambe le configurazioni**

```bash
go run ./cmd/eval --corpus eval/corpora/c2-documentale --ranker legacy
go run ./cmd/eval --corpus eval/corpora/c2-documentale --ranker bm25
```

- [ ] **Passo 3: scrivere `eval/FASE1.md`**

Tabella con nDCG@10, MRR e recall@10, complessivi e divisi per classe di query. La divisione per classe è il risultato interessante: è probabile che BM25 guadagni molto su `concept` e poco o niente su `identifier`, e quel dettaglio è già materiale per il capitolo successivo.

- [ ] **Passo 4: commit**

```bash
git add eval/results eval/FASE1.md
git commit -m "eval: measure BM25 against the legacy ranker on both corpora"
```

---

## Fase 2 - Recupero ibrido vero

Il difetto: in `internal/engine/ranker.go:203-222`, quando la query ha termini testuali il punteggio vettoriale viene sommato **solo ai documenti già trovati dal lessicale**. Un documento semanticamente pertinente che il lessicale non ha pescato non entra mai nei risultati. La ricerca semantica pura si attiva solo se `len(allTokens) == 0 && len(pq.OrTerms) == 0`. Nel README è descritto come "hybrid mode", e non lo è: è un re-ranking.

### Task 2.1: Insieme dei candidati vettoriali

**File:**
- Crea: `internal/engine/vector.go` (sposta qui `cosineSimilarity` e `toFloat64Array` da `ranker.go`)
- Test: `internal/engine/vector_test.go`

**Interfacce:**
- Produce: `func (idx *InvertedIndex) vectorCandidatesLocked(queryVector []float64, topK int) map[string]float64`

- [ ] **Passo 1: scrivere il test che fallisce**

```go
func TestVectorCandidatesRitornaITopK(t *testing.T) {
	idx := NewInvertedIndex()
	s := DefaultSettings()
	idx.AddDocument("vicino",  map[string]interface{}{"text": "a", "_vector": []interface{}{1.0, 0.0}}, s)
	idx.AddDocument("medio",   map[string]interface{}{"text": "b", "_vector": []interface{}{0.7, 0.7}}, s)
	idx.AddDocument("lontano", map[string]interface{}{"text": "c", "_vector": []interface{}{0.0, 1.0}}, s)

	got := idx.vectorCandidatesLocked([]float64{1.0, 0.0}, 2)
	if len(got) != 2 {
		t.Fatalf("attesi 2 candidati, ottenuti %d", len(got))
	}
	if _, ok := got["vicino"]; !ok {
		t.Error("il documento piu' simile deve essere fra i candidati")
	}
	if _, ok := got["lontano"]; ok {
		t.Error("il documento meno simile non deve entrare con topK=2")
	}
}

func TestVectorCandidatesSaltaDimensioniDiverse(t *testing.T) {
	idx := NewInvertedIndex()
	s := DefaultSettings()
	idx.AddDocument("ok",    map[string]interface{}{"text": "a", "_vector": []interface{}{1.0, 0.0}}, s)
	idx.AddDocument("corto", map[string]interface{}{"text": "b", "_vector": []interface{}{1.0}}, s)

	got := idx.vectorCandidatesLocked([]float64{1.0, 0.0}, 10)
	if _, ok := got["corto"]; ok {
		t.Error("un vettore di dimensione diversa va saltato")
	}
	if len(got) != 1 {
		t.Errorf("atteso 1 candidato valido, ottenuti %d", len(got))
	}
}
```

Il secondo test fissa a norma un comportamento che oggi esiste ma è silenzioso: un documento con vettore di dimensione sbagliata sparisce senza che nessuno se ne accorga. Lasciarlo silenzioso è una scelta, ma va testata e documentata, non subita.

- [ ] **Passo 2: eseguire e verificare che fallisca**

Esegui: `go test ./internal/engine/ -run TestVectorCandidates -v`
Atteso: FAIL, `idx.vectorCandidatesLocked undefined`

- [ ] **Passo 3: implementare**

```go
package engine

import "sort"

// vectorCandidatesLocked scandisce tutti i documenti con un campo _vector
// e ritorna i topK piu' simili al vettore della query, con la similarita'.
// Il caller deve gia' tenere idx.mu in lettura.
//
// La scansione e' lineare: O(n*d). Per i volumi di un documentale aziendale
// e' adeguata; il punto in cui smette di esserlo e' misurato in eval/FASE2.md.
func (idx *InvertedIndex) vectorCandidatesLocked(queryVector []float64, topK int) map[string]float64 {
	if len(queryVector) == 0 {
		return nil
	}
	type pair struct {
		id  string
		sim float64
	}
	all := make([]pair, 0, len(idx.docs))
	for docID, doc := range idx.docs {
		vecVal, ok := doc["_vector"]
		if !ok {
			continue
		}
		docVec, valid := toFloat64Array(vecVal)
		if !valid || len(docVec) != len(queryVector) {
			continue
		}
		all = append(all, pair{docID, cosineSimilarity(queryVector, docVec)})
	}
	sort.Slice(all, func(i, j int) bool { return all[i].sim > all[j].sim })
	if topK > 0 && len(all) > topK {
		all = all[:topK]
	}
	out := make(map[string]float64, len(all))
	for _, p := range all {
		out[p.id] = p.sim
	}
	return out
}
```

- [ ] **Passo 4: eseguire i test**

Esegui: `go test ./internal/engine/ -v`
Atteso: PASS

- [ ] **Passo 5: commit**

```bash
git add internal/engine/vector.go internal/engine/vector_test.go internal/engine/ranker.go
git commit -m "engine: extract vector helpers and add a top-k candidate set"
```

### Task 2.2: Unione invece di intersezione

**File:**
- Modifica: `internal/engine/ranker.go:203-222`
- Modifica: `internal/engine/inverted.go` (`Settings.HybridMode`, `Settings.VectorTopK`)
- Test: `internal/engine/hybrid_test.go`

**Interfacce:**
- Consuma: `vectorCandidatesLocked` (Task 2.1)
- Produce: `Settings.HybridMode string` con valori `"rerank"` (default, comportamento attuale) e `"union"`; `Settings.VectorTopK int` (default 100)

- [ ] **Passo 1: scrivere il test che fallisce**

```go
func TestHybridUnionRecuperaDocumentiCheIlLessicaleHaPerso(t *testing.T) {
	idx := NewInvertedIndex()
	s := DefaultSettings()
	s.HybridMode = "union"
	s.VectorTopK = 10

	// "contratto" c'e' solo nel primo documento. Il secondo parla della stessa
	// cosa con parole diverse, ed e' vicino nel vettore.
	idx.AddDocument("lessicale", map[string]interface{}{
		"text": "contratto di manutenzione", "_vector": []interface{}{1.0, 0.0}}, s)
	idx.AddDocument("semantico", map[string]interface{}{
		"text": "accordo di assistenza tecnica", "_vector": []interface{}{0.98, 0.2}}, s)

	ranked, _ := idx.Search("contratto", s, "auto", []float64{1.0, 0.0})

	found := false
	for _, id := range ranked {
		if id == "semantico" {
			found = true
		}
	}
	if !found {
		t.Error("in modalita' union il documento semanticamente simile deve comparire")
	}
}

func TestHybridRerankRestaIlComportamentoDiDefault(t *testing.T) {
	idx := NewInvertedIndex()
	s := DefaultSettings() // HybridMode deve valere "rerank"
	idx.AddDocument("lessicale", map[string]interface{}{
		"text": "contratto di manutenzione", "_vector": []interface{}{1.0, 0.0}}, s)
	idx.AddDocument("semantico", map[string]interface{}{
		"text": "accordo di assistenza tecnica", "_vector": []interface{}{0.98, 0.2}}, s)

	ranked, _ := idx.Search("contratto", s, "auto", []float64{1.0, 0.0})
	for _, id := range ranked {
		if id == "semantico" {
			t.Error("in modalita' rerank il documento non lessicale non deve comparire")
		}
	}
}
```

Il secondo test è quello che protegge la tesi: fissa il comportamento del baseline in modo che nessuna modifica futura lo alteri per sbaglio, rendendo incomparabili i numeri dei capitoli precedenti.

- [ ] **Passo 2: eseguire e verificare che fallisca**

Esegui: `go test ./internal/engine/ -run TestHybrid -v`
Atteso: il primo test FAIL, il secondo PASS

- [ ] **Passo 3: sostituire il blocco vettoriale in `Search`**

```go
	if len(queryVector) > 0 {
		pureVector := len(allTokens) == 0 && len(pq.OrTerms) == 0
		if pureVector || settings.HybridMode == "union" {
			topK := settings.VectorTopK
			if topK <= 0 {
				topK = 100
			}
			for docID, sim := range idx.vectorCandidatesLocked(queryVector, topK) {
				if m, ok := docMatches[docID]; ok {
					m.VectorScore = sim
				} else {
					docMatches[docID] = &SearchMatch{DocID: docID, VectorScore: sim}
				}
			}
		} else {
			// rerank: la similarita' si aggiunge solo a chi il lessicale ha gia' trovato
			for docID, m := range docMatches {
				if doc, ok := idx.docs[docID]; ok {
					if vecVal, ok := doc["_vector"]; ok {
						if docVec, valid := toFloat64Array(vecVal); valid && len(docVec) == len(queryVector) {
							m.VectorScore = cosineSimilarity(queryVector, docVec)
						}
					}
				}
			}
		}
	}
```

Aggiungi il campo a `SearchMatch` in `internal/engine/ranker.go`:

```go
	VectorScore float64 // similarita' coseno, 0 se il documento non ha vettore
```

La combinazione fra `Score` e `VectorScore` non si fa qui: è il tema della Fase 3. Per ora, per non rompere l'ordinamento, sommale nel punto in cui si costruisce `results` con la stessa formula di oggi:

```go
	for _, m := range docMatches {
		m.Score += m.VectorScore * 20.0
		results = append(results, *m)
	}
```

Il `20.0` resta, brutto e visibile, con un commento che rimanda alla Fase 3. È volutamente lasciato lì: è la cosa che il capitolo successivo sostituisce.

- [ ] **Passo 4: eseguire tutti i test**

Esegui: `go test ./... -race -v`
Atteso: PASS, compresi `v2_test.go` e `tests/api_v2_test.go` che esercitano la ricerca vettoriale dalle API.

- [ ] **Passo 5: commit**

```bash
git add internal/engine
git commit -m "engine: add union hybrid retrieval behind HybridMode, rerank stays default"
```

### Task 2.3: Misura del guadagno di richiamo

- [ ] **Passo 1: eseguire le tre configurazioni su C2**

Solo lessicale, `rerank`, `union`. Con `Ranker: "bm25"` in tutte e tre, così l'unica variabile è la modalità ibrida.

- [ ] **Passo 2: scrivere `eval/FASE2.md`**

La misura che conta è il **recall@10 per classe di query**. L'ipotesi da verificare: `union` guadagna su `concept`, non cambia nulla su `identifier`, e su `mixed` dipende. Se `union` peggiora la precisione su `identifier`, è il risultato più interessante della fase e va riportato, non nascosto.

- [ ] **Passo 3: correggere il README di Koskidex**

La riga 70 e la riga 326 descrivono come "hybrid" quello che finora era re-ranking. Ora che entrambe le modalità esistono vanno distinte a parole, altrimenti la documentazione mente.

- [ ] **Passo 4: commit**

```bash
git add eval/results eval/FASE2.md README.md
git commit -m "eval: measure union vs rerank hybrid retrieval, fix README wording"
```

---

## Fase 3 - Fusione dei punteggi

Il difetto: `m.Score += sim * 20.0`. Il punteggio lessicale si accumula per token e cresce con la lunghezza della query senza limite superiore; quello vettoriale è limitato a 20. Su una query di una parola il vettore domina, su una di cinque è rumore. Il `20.0` è una costante messa a occhio.

### Task 3.1: Reciprocal Rank Fusion e pesatura normalizzata

**File:**
- Crea: `internal/engine/fusion.go`
- Modifica: `internal/engine/ranker.go` (punto di combinazione)
- Modifica: `internal/engine/inverted.go` (`Settings.Fusion`, `Settings.FusionAlpha`, `Settings.RRFK`)
- Test: `internal/engine/fusion_test.go`

**Interfacce:**
- Produce: `func fuseRRF(lexRank, vecRank map[string]int, k float64) map[string]float64`, `func fuseWeighted(lex, vec map[string]float64, alpha float64) map[string]float64`; `Settings.Fusion string` con valori `"legacy"` (default), `"rrf"`, `"weighted"`

- [ ] **Passo 1: scrivere il test che fallisce**

```go
func TestRRFPremiaChiStaInAltoInEntrambeLeListe(t *testing.T) {
	lex := map[string]int{"a": 1, "b": 2, "c": 3}
	vec := map[string]int{"c": 1, "b": 2, "a": 3}
	out := fuseRRF(lex, vec, 60)
	// b e' secondo in entrambe: deve battere a e c, primi in una sola
	if out["b"] <= out["a"] || out["b"] <= out["c"] {
		t.Errorf("b deve vincere: a=%v b=%v c=%v", out["a"], out["b"], out["c"])
	}
}

func TestRRFNonDipendeDallaScalaDeiPunteggi(t *testing.T) {
	// e' la proprieta' per cui si usa RRF: conta la posizione, non il valore
	lex := map[string]int{"a": 1, "b": 2}
	vec := map[string]int{"a": 1, "b": 2}
	if got := fuseRRF(lex, vec, 60); got["a"] <= got["b"] {
		t.Error("a e' primo in entrambe, deve vincere")
	}
}

func TestWeightedAlphaUnoIgnoraIlVettore(t *testing.T) {
	lex := map[string]float64{"a": 1.0, "b": 0.0}
	vec := map[string]float64{"a": 0.0, "b": 1.0}
	out := fuseWeighted(lex, vec, 1.0)
	if out["a"] <= out["b"] {
		t.Error("con alpha=1 conta solo il lessicale")
	}
}

func TestWeightedAlphaZeroIgnoraIlLessicale(t *testing.T) {
	lex := map[string]float64{"a": 1.0, "b": 0.0}
	vec := map[string]float64{"a": 0.0, "b": 1.0}
	out := fuseWeighted(lex, vec, 0.0)
	if out["b"] <= out["a"] {
		t.Error("con alpha=0 conta solo il vettore")
	}
}
```

- [ ] **Passo 2: eseguire e verificare che fallisca**

Esegui: `go test ./internal/engine/ -run "TestRRF|TestWeighted" -v`
Atteso: FAIL, `undefined: fuseRRF`

- [ ] **Passo 3: implementare**

```go
package engine

// fuseRRF combina due liste ordinate con Reciprocal Rank Fusion.
// Il punteggio di un documento e' la somma di 1/(k+posizione) sulle liste
// in cui compare. Usa solo la posizione, quindi non richiede che i due
// punteggi siano sulla stessa scala: e' esattamente il problema che aveva
// la somma con costante 20.0.
// Il valore k=60 e' quello proposto da Cormack, Clarke e Buettcher (2009).
func fuseRRF(lexRank, vecRank map[string]int, k float64) map[string]float64 {
	out := make(map[string]float64)
	for id, r := range lexRank {
		out[id] += 1.0 / (k + float64(r))
	}
	for id, r := range vecRank {
		out[id] += 1.0 / (k + float64(r))
	}
	return out
}

// normalize riporta i valori nell'intervallo [0,1] con la normalizzazione
// min-max. Se tutti i valori coincidono ritorna 1 per ciascuno, perche' in
// quel caso nessun documento e' distinguibile dagli altri.
func normalize(m map[string]float64) map[string]float64 {
	if len(m) == 0 {
		return m
	}
	first := true
	var min, max float64
	for _, v := range m {
		if first {
			min, max, first = v, v, false
			continue
		}
		if v < min {
			min = v
		}
		if v > max {
			max = v
		}
	}
	out := make(map[string]float64, len(m))
	span := max - min
	for id, v := range m {
		if span == 0 {
			out[id] = 1
		} else {
			out[id] = (v - min) / span
		}
	}
	return out
}

// fuseWeighted normalizza le due liste e le combina con
//   alpha*lessicale + (1-alpha)*vettoriale.
// alpha=1 usa solo il lessicale, alpha=0 solo il vettoriale.
func fuseWeighted(lex, vec map[string]float64, alpha float64) map[string]float64 {
	nl, nv := normalize(lex), normalize(vec)
	out := make(map[string]float64)
	for id, v := range nl {
		out[id] += alpha * v
	}
	for id, v := range nv {
		out[id] += (1 - alpha) * v
	}
	return out
}
```

- [ ] **Passo 4: innestare in `Search`**

Nel punto in cui oggi si fa `m.Score += m.VectorScore * 20.0`, dirama su `settings.Fusion`. Per `"rrf"` servono le posizioni, quindi ordina due volte: una per `Score` lessicale, una per `VectorScore`, costruisci le due mappe posizione e fondi.

- [ ] **Passo 5: eseguire tutti i test**

Esegui: `go test ./... -race -v`
Atteso: PASS

- [ ] **Passo 6: commit**

```bash
git add internal/engine/fusion.go internal/engine/fusion_test.go internal/engine/ranker.go internal/engine/inverted.go
git commit -m "engine: add RRF and normalized weighted fusion behind the Fusion setting"
```

### Task 3.2: Calibrazione di alpha e scelta della fusione

- [ ] **Passo 1: spazzolare alpha su C2**

Da 0 a 1 a passi di 0.1, per ogni classe di query, registrando nDCG@10. Il grafico che ne esce è una figura della tesi.

- [ ] **Passo 2: confrontare con RRF e con la costante 20.0**

Tre righe per classe di query. L'ipotesi da verificare: l'alpha ottimo è **diverso per classe**, alto su `identifier` e basso su `concept`. Se è così, la pesatura fissa è battuta da entrambe le alternative e la Fase 3.3 ha una ragione d'essere; se l'alpha ottimo è uguale ovunque, il risultato è comunque pubblicabile ed è una smentita onesta dell'ipotesi.

- [ ] **Passo 3: scrivere `eval/FASE3.md` e commit**

```bash
git add eval/results eval/FASE3.md
git commit -m "eval: calibrate fusion alpha per query class, compare with RRF"
```

### Task 3.3: Fusione consapevole del tipo di query

Questa task si esegue **solo se** il Passo 2 della 3.2 ha mostrato che l'alpha ottimo dipende dalla classe. Se non è così va saltata, e il fatto che sia stata saltata va scritto nella tesi: è un risultato negativo, non un buco.

**File:**
- Crea: `internal/engine/querytype.go`
- Test: `internal/engine/querytype_test.go`

**Interfacce:**
- Produce: `func ClassifyQuery(q string) string` che ritorna `"identifier"`, `"entity"`, `"concept"` o `"mixed"`

- [ ] **Passo 1: scrivere il test che fallisce**

```go
func TestClassifyQuery(t *testing.T) {
	casi := []struct{ in, want string }{
		{"fattura 2026/0173", "identifier"},
		{"IT01234567890", "identifier"},
		{"Rossi SpA", "entity"},
		{"contratti di manutenzione scaduti", "concept"},
		{"fatture Rossi marzo 2026", "mixed"},
	}
	for _, c := range casi {
		if got := ClassifyQuery(c.in); got != c.want {
			t.Errorf("ClassifyQuery(%q) = %q, atteso %q", c.in, got, c.want)
		}
	}
}
```

- [ ] **Passo 2: eseguire, implementare con regole esplicite (presenza di cifre, di separatori come `/` e `-`, di maiuscole interne, lunghezza), rieseguire**

Le regole scritte a mano vanno bene e sono preferibili a un modello: sono ispezionabili, non vanno addestrate e in tesi si spiegano in un paragrafo. Il punto non è la classificazione in sé, è dimostrare che conoscere il tipo di query migliora la fusione.

- [ ] **Passo 3: alpha per classe, misura, commit**

---

## Fase 4 - Innesto in Documentale

Da fare per ultima. Prima serve un motore che valga la pena di innestare.

**Stato attuale verificato il 15 settembre 2026:** `apps/laravel/composer.json` richiede `elasticsearch/elasticsearch: ^9.1`. La ricerca passa da `apps/laravel/app/Services/ElasticsearchService.php`, l'indicizzazione dal comando `apps/laravel/app/Console/Commands/ExportToElasticSearch.php`, e lato interfaccia ci sono `apps/react/src/components/AISearch.tsx` e `apps/react/src/app/admin/file-system/[...path]/(table)/AiSearchTableFilters.tsx`.

### Task 4.1: Client Koskidex affiancato a Elasticsearch

**File:**
- Crea: `apps/laravel/app/Services/KoskidexService.php`
- Crea: `apps/laravel/app/Contracts/SearchBackend.php`
- Modifica: `apps/laravel/app/Services/ElasticsearchService.php` (implementa l'interfaccia)
- Crea: `apps/laravel/config/search.php`
- Test: `apps/laravel/tests/Feature/SearchBackendTest.php`

I due backend devono convivere dietro la stessa interfaccia, selezionabili da configurazione. Serve per due motivi: si può tornare indietro in un istante, e soprattutto si possono eseguire le **stesse query sui due motori** e confrontarli, che è il capitolo conclusivo della tesi.

Il repo ha già in `examples/laravel/` un `KoskidexClient.php` e un trait `Searchable.php`: sono il punto di partenza, non vanno riscritti da zero.

- [ ] **Passo 1: definire `SearchBackend` sulle firme reali di `ElasticsearchService`**

Le firme sono queste, verificate nel file:

```php
<?php

namespace App\Contracts;

interface SearchBackend
{
    public function getIndexName(string $type = 'documents'): string;

    public function createDocumentsIndex(): void;
    public function createFoldersIndex(): void;

    public function indexElement(string $type, $id, array $data): void;
    public function bulkIndex(array $body);

    /** Ritorna gli id dei documenti trovati, nell'ordine di rilevanza del motore. */
    public function fuzzySearch(string $term, string $type): array;

    public function deleteElement(string $type, $id): void;
    public function bulkDeleteElement(string $type, array $ids): void;
    public function documentExists(string $type, $id);
    public function updateDocument(int|string $id, array $data): void;
}
```

Due cose da notare, perché condizionano il resto. `fuzzySearch` oggi fa `collect($hits)->pluck('_id')->toArray()`: **restituisce solo gli id e butta via i punteggi**. Per il confronto finale servono anche quelli, quindi va aggiunto un metodo `fuzzySearchScored(string $term, string $type): array` che ritorna coppie id/punteggio, implementato da entrambi i backend e usato solo dall'impianto di valutazione. E ci sono due indici distinti, `documents` e `folders`: Koskidex li mappa su due indici con lo stesso nome, quindi `getIndexName` resta identico.

- [ ] **Passo 2: far implementare l'interfaccia a `ElasticsearchService` senza cambiarne il corpo**

È una modifica di sola dichiarazione. Se PHP si lamenta di una firma, l'interfaccia è sbagliata e va allineata al codice esistente, mai il contrario: il backend che funziona in produzione è la verità.

- [ ] **Passo 3: test di parità fra i due backend**

```php
public function test_i_due_backend_trovano_gli_stessi_documenti(): void
{
    $docs = $this->seedDocumentiDiProva(); // 20 documenti noti

    foreach (['elasticsearch', 'koskidex'] as $backend) {
        config(['search.backend' => $backend]);
        $svc = app(SearchBackend::class);
        foreach ($docs as $d) {
            $svc->indexElement('documents', $d['id'], $d);
        }
        $risultati[$backend] = $svc->fuzzySearch('fattura', 'documents');
    }

    $this->assertEqualsCanonicalizing(
        $risultati['elasticsearch'],
        $risultati['koskidex'],
        'i due backend devono trovare lo stesso insieme di documenti'
    );
}
```

Nota che l'asserzione è su **insieme**, non su ordine: l'ordine è precisamente ciò che la tesi confronta, quindi imporlo qui come test renderebbe impossibile misurarne la differenza.

- [ ] **Passo 4: implementare `KoskidexService`**

Parti da `examples/laravel/app/Services/KoskidexClient.php` nel repo di Koskidex, che parla già con l'API REST, e avvolgilo per soddisfare `SearchBackend`.

- [ ] **Passo 5: `config/search.php` e registrazione nel container**

```php
// config/search.php
return ['backend' => env('SEARCH_BACKEND', 'elasticsearch')];
```

In `AppServiceProvider::register()`:

```php
$this->app->bind(SearchBackend::class, fn () => match (config('search.backend')) {
    'koskidex' => new KoskidexService(),
    default    => new ElasticsearchService(),
});
```

Poi sostituisci le iniezioni dirette di `ElasticsearchService` con `SearchBackend` nei punti che lo usano.

- [ ] **Passo 6: eseguire i test e commit**

```bash
cd apps/laravel && php artisan test --filter SearchBackend
git add apps/laravel/app/Contracts apps/laravel/app/Services apps/laravel/config/search.php apps/laravel/tests/Feature/SearchBackendTest.php
git commit -m "search: introduce SearchBackend contract with Elasticsearch and Koskidex implementations"
```

### Task 4.2: Indicizzazione e vettori

**File:**
- Crea: `apps/laravel/app/Console/Commands/ExportToKoskidex.php`
- Modifica: `apps/python/app/api/documents/routes.py` (generazione degli embedding)

Koskidex non genera embedding: li deve ricevere nel campo `_vector`. Il servizio Python di Documentale è il posto giusto per produrli, perché è già quello che parla con OpenAI.

- [ ] **Passo 1: aggiungere l'endpoint di embedding nel servizio Python**
- [ ] **Passo 2: estendere il comando di export perché includa `_vector` e i campi estratti**
- [ ] **Passo 3: decidere e documentare la strategia di suddivisione dei documenti lunghi in parti**

Un contratto di quaranta pagine non sta in un solo embedding. Come lo si spezza, e se si indicizzano le parti o il documento intero, cambia i risultati: va deciso, scritto e misurato, non lasciato implicito.

- [ ] **Passo 4: commit**

### Task 4.3: Confronto finale

- [ ] **Passo 1: eseguire lo stesso insieme di query su Elasticsearch e su Koskidex nella sua configurazione migliore**
- [ ] **Passo 2: confrontare qualità, latenza, memoria e dimensione dell'indice**
- [ ] **Passo 3: scrivere `eval/FASE4.md`**

Qui l'onestà conta più che altrove. Elasticsearch è maturo e battuto da molti: se perde su qualche dimensione va detto perché, e se vince va detto altrettanto chiaramente. Una tesi che dimostra "il mio è meglio di Elasticsearch su tutto" non la crede nessuno, giustamente. Una che mostra dove un motore piccolo e senza dipendenze è competitivo e dove non lo è, invece, è un risultato.

---

## Cosa resta aperto

Decisioni non ancora prese, da chiudere prima di partire con la Fase 0.

1. **Quale collezione pubblica per C1.** Serve piccola e con giudizi pubblicati.
2. **Chi annota C2, e in quanto tempo.** Trecento documenti e sessanta query con giudizi sono settimane di lavoro, non giorni. Se il tempo non c'è, si riduce il numero di documenti prima che quello delle query: poche query su molti documenti valgono meno di molte query su pochi.
3. **Relatore, e se l'impianto gli va bene.** Da sentire prima di iniziare ad annotare, non dopo.
4. **Autorizzazione dell'azienda su cosa è pubblicabile.** Con C2 costruito ad hoc il problema si riduce molto, ma la Fase 4 tocca comunque Documentale.

## Ordine di esecuzione

Fase 0 per intera, poi 1, poi 2, poi 3. Le fasi 1, 2 e 3 dipendono ognuna dalla precedente perché il baseline di ciascuna è il risultato di quella prima. La Fase 4 può partire in parallelo alla 3, perché tocca un repo diverso.

La Fase 0 è la più noiosa ed è l'unica che non si può saltare. Ogni fase successiva, senza, produce numeri che non significano niente.
