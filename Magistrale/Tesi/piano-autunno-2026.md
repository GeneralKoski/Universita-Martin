# Piano autunno 2026 - lavoro propedeutico alla tesi

> **Per chi esegue:** i passi usano checkbox (`- [ ]`) per il tracciamento. Ogni task si chiude con un deliverable testabile da solo e un commit.

**Obiettivo:** portare avanti Koskidex e Documentale da qui a dicembre 2026 senza consumare il contributo della tesi, arrivando a febbraio 2027 con l'impianto di valutazione già pronto e il corpus già esportabile.

**Architettura:** tutto il lavoro di questo piano è *intorno* al ranking, mai *sul* ranking. Prima si mette in sicurezza il comportamento attuale (test che lo congelano, punteggi visibili), poi si costruisce il metro per misurarlo, poi si prepara il lato Documentale che fornisce i dati. Le correzioni al ranking restano intatte per la tesi.

**Stack:** Go 1.25 e zero dipendenze esterne oltre `golang.org/x/text` (Koskidex); Laravel 12 + PHP 8.4 (Documentale); Docker per far girare i servizi.

**Spec:** [appunti.md](appunti.md) per la domanda di tesi e il perimetro, [piano-implementazione.md](piano-implementazione.md) per il piano della tesi vera e propria. Questo documento **non lo sostituisce e non lo duplica**: dice quali sue parti si possono anticipare adesso e aggiunge i task che lì non ci sono.

---

## Le tre regole che rendono sicuro toccare il ranking

Le correzioni al ranking **si fanno adesso**, non a febbraio. Decisione del 23 settembre 2026, e il motivo è il tempo: da febbraio a luglio 2027 ci sono cinque mesi di sere per implementare, misurare e scrivere. Se a febbraio il codice esiste già e resta solo da misurare e raccontare, il rischio di non arrivare in fondo crolla.

Questo è sicuro solo se valgono tutte e tre queste regole. Se ne salta una, tornano i problemi veri.

**1. Il baseline resta eseguibile per sempre.** Ogni modifica al ranking sta dietro un campo di `Settings`, con il comportamento di oggi come valore di default. È già un vincolo di `piano-implementazione.md`, qui diventa la condizione che rende legittimo tutto il resto. Il Task A3 congela l'ordine attuale in un test: finché quel test passa a default, il baseline non si è mosso.

**2. Niente si misura a occhio.** Una modifica al ranking senza un numero accanto non è un capitolo di tesi, è un'opinione. Vale però una precisazione che cambia il calendario: **BM25 si valida sulla collezione pubblica C1, che ha giudizi già pubblicati e non richiede nessuna annotazione a mano.** Il corpus C2 annotato serve solo alla Fase 3, quella sulla fusione consapevole del tipo di query. Quindi la Fase 1 si può fare e misurare per intero in autunno, e le Fasi 2 e 3 no.

**3. Si scrive tutto sul diario, prima e dopo.** Ogni modifica al ranking ha una voce in `eval/DIARIO.md`, scritta in due tempi: cosa ti aspetti **prima** di misurare, e cosa è successo dopo. Non è burocrazia. È la cosa che a giugno ti permette di scrivere perché hai scelto un parametro invece di un altro, ed è anche la risposta alla domanda scomoda in discussione, cioè se le metriche siano state scelte dopo aver visto i risultati. Un'ipotesi scritta prima e smentita dai numeri vale più di un risultato pulito senza storia.

### Formato del diario

`eval/DIARIO.md` nel repo Koskidex, una voce per modifica, la più recente in cima:

```markdown
## 2026-11-08 - BM25 al posto del punteggio euristico

**Flag:** `Settings.RankingMode = "bm25"` (default resta `"legacy"`)
**Commit:** abc1234

### Prima di misurare

Mi aspetto che nDCG@10 su C1 salga rispetto al legacy, perche' il legacy non
ha IDF e su una collezione con termini molto comuni questo deve costare.
Mi aspetto che sulle query di un solo termine cambi poco.
Valore di riferimento in letteratura per BM25 su questa collezione: 0.42.

### Dopo

nDCG@10: legacy 0.28 -> bm25 0.41. In linea con il riferimento, quindi
l'implementazione non ha bug grossolani.
Sulle query di un termine: 0.31 -> 0.33, praticamente invariato come previsto.
Sorpresa: su tre query e' peggiorato, tutte con un nome proprio ripetuto.
Da guardare, forse e' saturazione del TF.

### Parametri

k1=1.2, b=0.75, i default della letteratura. Non calibrati: la calibrazione
e' la Fase 3.
```

La sezione "Prima di misurare" **si committa prima di lanciare la valutazione**. È l'unico modo perché valga qualcosa.

## Vincoli globali

- Koskidex resta a **zero dipendenze esterne** oltre `golang.org/x/text`, che è già in `go.mod`. Vale anche per i test e per l'impianto di valutazione.
- Ogni modifica che cambia l'ordine dei risultati sta **dietro un campo di `Settings`**, con il comportamento attuale come default, e ha la sua voce in `eval/DIARIO.md`. Nessuna eccezione: una modifica al ranking senza flag e senza voce di diario va annullata, non sanata dopo.
- I Task A0-A3 vanno fatti **prima** di qualunque modifica al ranking. Sono la rete: senza il baseline congelato, il flag non serve a niente perché nessuno si accorge se si è mosso.
- Ogni task finisce con un commit. Messaggio in inglese, come da convenzione del repo.
- Su Documentale **tutto il lavoro di tesi sta sul branch `martin/tesi-magistrale`**, creato il 23/09/2026 da `fix/various-fixes` (commit `5c31647`). Non si committa niente su altri branch e non si committa niente che contenga dati reali di clienti.

## Capacità realistica, e cosa salta

Da oggi (23 settembre 2026) a metà dicembre sono tredici settimane, ma sono le tredici settimane in cui seguo quattro corsi e a dicembre consegno due progetti d'esame. **Contare su tre o quattro ore a settimana**, cioè quaranta o cinquanta ore in tutto.

Messo tutto insieme, questo piano ne chiede di più. Vale la pena dirlo prima invece di scoprirlo a novembre:

| Blocco | Stima | Ci sta in autunno? |
|---|---|---|
| A0-A3, sicurezza Koskidex | ~8 h | Sì, ed è la precondizione di tutto |
| B1, scelta e download di C1 | ~3 h | Sì |
| C0, decisione sul testo integrale | ~2 h | Sì, ed è una domanda da fare presto perché la risposta arriva dall'azienda |
| C2, log delle query | ~3 h | Sì, e prima si fa più dati raccoglie |
| B2, metriche ed esecutore | ~14 h | Sì, è il blocco grosso di novembre |
| Fase 1, BM25 misurato | ~12 h | **Forse.** Solo se ottobre e novembre filano |
| C1, export del corpus | ~6 h | **No.** Slitta, e va bene così |

**Il criterio con cui si taglia:** l'export del corpus (C1) produce il C2, che serve alle Fasi 2 e 3, che sono comunque lavoro di febbraio. Quindi è la cosa giusta da far slittare, anche se è la più concreta da guardare. Il logging delle query (C2) invece va fatto subito proprio perché è cumulativo: ogni settimana in cui non gira è dato perso per sempre.

Se a novembre il tempo non c'è, si sacrifica in quest'ordine: prima C1, poi la Fase 1, poi B2. Mai A0-A3: sono la rete che rende sicuro tutto il resto, e vanno fatti prima che venga voglia di mettere le mani al ranking.

## Cosa può mordere

Le cose che questo piano deve reggere e che è facile scoprire tardi:

- **Il baseline si sposta senza accorgersene.** Un refactoring apparentemente innocuo su tokenizer o fuzzy cambia l'ordine dei risultati e nessuno se ne accorge finché in tesi i numeri non tornano. Coperto dal Task A3.
- **La valutazione senza punteggi visibili.** Oggi `Search` ritorna solo gli id: senza il punteggio e la sua scomposizione non si può spiegare *perché* un documento è in quella posizione, e la Fase 3 della tesi è tutta lì. Coperto dal Task A2.
- **Documenti senza `_vector`.** Il corpus esportato da Documentale non ha embedding: metà del codice ibrido non viene mai esercitato dai test. Coperto dal Task A3, che include un caso con e uno senza vettore.
- **Il corpus esportato contiene dati di clienti.** Se l'export finisce in un repo universitario pubblico è un problema serio, non una svista. Il Task C1 lo limita tenendo il file fuori da ogni repo finché l'azienda non si è espressa, ma **non anonimizza niente**: se serve, l'anonimizzazione è un task in più da scrivere, e la decisione sta nel Task C0.
- **Annotare richiede più tempo di quanto sembra.** Sessanta query con giudizi su trecento documenti sono settimane di sere. Non è un rischio tecnico ed è già scritto in `appunti.md`, ma è il motivo per cui il Task B1 va chiuso adesso e non a febbraio.
- **Una modifica al ranking entra senza flag.** Basta una volta e il baseline non è più riproducibile: da lì in poi ogni numero della tesi è contestabile e non c'è modo di rimediare a posteriori. Coperto dai Vincoli globali e dal Task A3, che si rompe rumorosamente.
- **Il diario si scrive dopo aver visto i numeri.** È la versione silenziosa dello stesso problema: la voce viene compilata a cose fatte, l'ipotesi diventa la conclusione e il diario perde l'unico valore che aveva. L'unica difesa è committare la sezione *Prima di misurare* prima di lanciare la valutazione, come commit separato.

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

## Task B1: Chiudere la scelta di C1 - FATTO il 23/09/2026

È il punto aperto numero 1 di `piano-implementazione.md`. È una decisione, non del codice, e blocca tutto il resto della Fase 0.

- [ ] Scegliere una collezione pubblica piccola e con giudizi già pubblicati, in modo che l'intera valutazione giri in minuti e non in ore a ogni modifica
- [ ] Scaricarla in `eval/corpora/c1-public/` con dentro un `SOURCE.md` che registra provenienza, versione e data
- [ ] Verificare che ci sia un valore di riferimento noto in letteratura per BM25 su quella collezione: senza, C1 non serve a niente, perché il suo unico scopo è dire se la mia implementazione di BM25 ha un bug
- [ ] Commit

## Task B2: Task 0.2, 0.3 e 0.4 del piano di tesi - FATTO il 23/09/2026

Lettura di qrels e query, le metriche, e l'esecutore che le mette insieme. Sono codice puro, senza dipendenze esterne, testabile con numeri calcolati a mano. È il pezzo che meglio si presta alle sere spezzate, perché ogni metrica è un test a sé.

- [ ] Task 0.2 - lettura di qrels e query (`piano-implementazione.md`, riga 92)
- [ ] Task 0.3 - metriche (`piano-implementazione.md`, riga 211)
- [ ] Task 0.4 - esecutore della valutazione (`piano-implementazione.md`, riga 390)

Il Task 0.4 sta qui e non a febbraio perché **serve già per la Fase 1**: senza esecutore non si misura BM25 su C1. Nel piano di tesi è descritto pensando al C2, ma non ha niente di specifico del dominio: legge un corpus, delle query, dei qrels, e produce numeri. C1 gli va bene esattamente come C2.

## Dove ci si ferma senza danno

**Resta a febbraio solo il Task 0.5, la misura del baseline sul corpus di dominio**, e con lui tutta l'annotazione del C2. Non perché sia difficile, ma perché annotare sessanta query su trecento documenti è lavoro continuativo e non si fa a pezzetti di sera fra un esame e l'altro.

Arrivare a febbraio con A0-A3, B1, B2 e magari la Fase 1 fatti significa partire con il metro scritto, testato e già usato almeno una volta su dati veri. È un ottimo punto di arrivo per l'autunno.

---

# Parte C - Documentale

## Dove si lavora

Branch **`martin/tesi-magistrale`**, creato il 23 settembre 2026 da `fix/various-fixes` (commit `5c31647`), che conteneva già dei fix miei in corso. Esiste solo in locale: non è su `origin` e non ci va finché non serve davvero.

Il senso è tenere separato quello che nasce per la tesi da quello che nasce per il prodotto, anche se in pratica questo ramo non verrà probabilmente mai integrato. Se una singola modifica si rivelasse utile all'azienda - il caso più probabile è la persistenza del testo integrale del Task C0 - si porta di là con un cherry-pick, come una cosa sua, non trascinando il ramo della tesi.

```bash
cd ~/Desktop/Dieffetech/Documentale
git switch martin/tesi-magistrale
```

Attenzione a una cosa: il ramo parte da `fix/various-fixes`, non da `main`. Quindi porta dentro anche quei fix, e se a un certo punto `fix/various-fixes` viene integrato o riscritto, questo ramo va allineato prima di fare confronti. Il branch di partenza al momento della creazione era allineato a `origin/fix/various-fixes`.

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

# Parte D - Le correzioni al ranking

Sono le Fasi 1, 2 e 3 di [piano-implementazione.md](piano-implementazione.md), già scritte task per task lì dentro. Qui dico solo quali si possono fare adesso e a quali condizioni.

## Prima di tutto: il recupero disgiuntivo (difetto 0) - FATTO il 23/09/2026

**Questo non era nel piano.** È emerso misurando il baseline il 23/09/2026, e
scavalca la Fase 1.

Il recupero di Koskidex è congiuntivo: `ParseQuery` mette ogni parola della
query in `MustTerms`, quindi un documento deve contenerle tutte. Misurato:

| | SciFact | NFCorpus |
|---|---|---|
| nDCG@10 legacy | 0,0246 | 0,1659 |
| **Query a vuoto** | **290 su 300 (97%)** | **160 su 323 (50%)** |
| Riferimento BM25 | 0,6789 | 0,3218 |

Su NFCorpus le query che tornano qualcosa hanno in media 2,0 parole, quelle a
vuoto 4,7: stessa collezione, stesso indice, cambia solo la lunghezza.

**Perché viene prima di BM25.** Applicare BM25 a un recupero congiuntivo
riordinerebbe il nulla: la Fase 1 misurerebbe zero su SciFact. E questo è il
difetto che conta di più per il documentale, dove le query sono in lingua
naturale e sempre più spesso riscritte da un LLM, cioè lunghe.

**Non è un bug.** L'AND è una scelta ragionevole per la barra di ricerca di un
e-commerce, che è il caso d'uso per cui Koskidex era nato. Va raccontato così in
tesi: non "avevo sbagliato", ma "il modello di recupero era tarato su un regime
di query diverso da quello del documentale", che è una tesi più interessante.

- [x] `Settings.RetrievalMode`, `"all"` di default, `"any"` disgiuntivo. Stringa
      vuota trattata come `"all"`: le settings sono persistite e un indice
      salvato prima non deve cambiare comportamento da solo
- [x] `TestBaselineRankingIsFrozen` verde a default, senza modifiche al test
- [x] Ipotesi nel diario, committata prima di misurare
- [x] Misurato su entrambe le collezioni

### Risultato

| | SciFact `all` → `any` | NFCorpus `all` → `any` |
|---|---|---|
| nDCG@10 | 0,0246 → **0,4936** | 0,1659 → **0,2246** |
| Recall@100 | 0,0242 → **0,7571** | 0,0967 → **0,1898** |
| Query a vuoto | 290/300 → **0** | 160/323 → **24** |
| Riferimento BM25 | 0,6789 | 0,3218 |

Entrambe arrivano intorno al **70% del riferimento**, partendo dal 4% e dal 52%.

**La sorpresa, ed è quella da mettere in tesi:** avevo previsto che su NFCorpus,
con query da due parole, togliere l'AND avrebbe alzato il recall ma peggiorato
l'ordinamento, perché l'AND faceva da filtro di precisione. È migliorato tutto.
Il motivo è che il filtro congiuntivo **era ridondante rispetto al punteggio che
c'era già**: chi trova più termini prende più punti, quindi i documenti completi
restano in testa da soli. Il filtro non li promuoveva, cancellava tutto il resto.
L'AND non aggiungeva precisione, toglieva recall.

Il divario che resta su SciFact, 0,4936 contro 0,6789, è dove dovrebbe esserci
l'IDF. Ora la Fase 1 ha un baseline sensato contro cui misurarsi.

## Poi la Fase 1, BM25 - FATTA il 23/09/2026

Si misura sulla collezione pubblica C1, che ha i giudizi già pubblicati e non
richiede nessuna annotazione a mano. Questo resta vero.

**Precondizioni:**

- [x] A0-A3 fatti, con `TestBaselineRankingIsFrozen` verde
- [x] B1 fatto: SciFact e NFCorpus scaricate, con i riferimenti in `SOURCE.md`
- [x] B2 fatto: metriche ed esecutore girano su dati veri
- [x] Difetto 0 chiuso, altrimenti su SciFact non c'è niente da riordinare

**Come si è eseguita:**

- [x] Task 1.1 - statistiche dell'indice: `df(t)`, `|D|` e `tf(t,D)` mantenute
      in inserimento, cancellazione, aggiornamento e reindicizzazione
- [x] Task 1.2 - punteggio BM25 dietro `Settings.ScoringMode`, `k1=1.2`,
      `b=0.75` letti dalle settings e non cablati
- [x] Sezione *Prima di misurare* nel diario, committata prima di lanciare
      (commit `998e11c`)
- [x] Task 1.3 - misura contro il baseline
- [x] Voce di diario completata, sorprese comprese

### Risultato

| | legacy | `any` | **bm25** | riferimento |
|---|---|---|---|---|
| SciFact nDCG@10 | 0,0246 | 0,4936 | **0,6197** | 0,6789 |
| SciFact Recall@100 | 0,0242 | 0,7571 | **0,8746** | - |
| NFCorpus nDCG@10 | 0,1659 | 0,2246 | **0,2810** | 0,3218 |
| NFCorpus Recall@100 | 0,0967 | 0,1898 | **0,2280** | - |

**91% e 87% del riferimento pubblicato**, partendo dal 4% e dal 52% di
stamattina. Il 9-13% che manca ha due cause già scritte in `SOURCE.md` prima di
misurare, nessuno stemmer e un tokenizer diverso, ed è materia della Fase 2.

**La sorpresa di questa fase è un mio errore di metodo, e va in tesi come tale.**
Avevo scritto nel diario una *guardia*: se il recall si muove di più di ±0,02 ho
cambiato il recupero per sbaglio e il nDCG non vale niente. Il recall si è mosso
di +0,117 su SciFact. Non era il risultato a essere falso, era la guardia a
essere scritta male: `recall@k` non dice quanto hai recuperato, dice quanti
rilevanti sono entrati nei primi `k`, e quando i candidati sono molti più di `k`
è una metrica di ordinamento esattamente come il nDCG. In modalità disgiuntiva
la query mediana di SciFact pesca 5182 documenti su 5183: dentro il taglio ci
entra l'1,9% dei candidati.

Il recupero è invariato, e ora è dimostrato invece che argomentato: il runner
registra quanti documenti corrispondono **prima** del taglio, e quel numero non
cambia per nessuna delle 623 query. La guardia corretta, d'ora in avanti, è
quella - non il recall.

È il tipo di episodio che una tesi sperimentale dovrebbe raccontare e quasi
sempre nasconde: un controllo scritto in buona fede, scattato, e la disciplina
di andare a vedere se aveva ragione il controllo o il risultato.

## Cosa resta a febbraio, e perché

**Fase 2, recupero ibrido vero.** Serve un corpus con embedding e giudizi.
Attenzione: il difetto 0 e la Fase 2 si assomigliano ma non sono la stessa cosa.
Il difetto 0 è il lessicale che non fa OR fra i suoi termini; la Fase 2 è il
vettoriale che non porta candidati propri. Vanno tenuti distinti, anche in tesi.

**Fase 3, fusione dei punteggi.** Ha bisogno del C2 annotato per classe di
query. Il collo di bottiglia è l'annotazione, non la difficoltà.

## Cosa cambia nel racconto della tesi

Facendo le correzioni prima della tesi, la narrazione non è più "ho misurato, poi ho corretto" ma "ho corretto, poi ho misurato". È più debole, e il diario è esattamente quello che la rimette in piedi: se la sezione *Prima di misurare* è committata prima della valutazione, l'ipotesi è verificabilmente antecedente al risultato. Senza diario questo argomento non ce l'hai, e in discussione è una domanda che arriva.

## Fuori perimetro

- **Le Fasi 2 e 3 del piano di tesi.** Non per prudenza: gli serve il corpus C2 annotato, che è lavoro da settimane continuative e non da sere spezzate. Restano a febbraio.
- **`rustann` e gli indici approssimati.** Già fuori dal perimetro della tesi, decisione del 15 settembre 2026.
- **La Fase 4 del piano di tesi** (innesto vero in Documentale accanto a Elasticsearch). Va fatta quando c'è qualcosa che vale la pena innestare, cioè dopo le Fasi 1-3.
- **Rimettere le GitHub Actions.** Sono state tolte di proposito, il Task A1 dà lo stesso servizio in locale.

## Ordine e calendario

| Quando | Cosa | Perché lì |
|---|---|---|
| Fine settembre | A0, A1 | Senza Go non si fa niente, e sono due sere |
| Ottobre | A2, A3, B1, C0, C2 | A3 è la rete; B1 e C0 sono decisioni che sbloccano il resto; C2 prima si accende più raccoglie |
| Novembre | B2 | Metriche ed esecutore: il blocco grosso, ma testabile a pezzetti |
| Dicembre | Progetti d'esame e riproposta ai relatori | La Fase 1 era prevista qui e si è chiusa il 23/09: dicembre resta libero per gli esami |
| Febbraio | C1, Task 0.5, Fasi 2 e 3 | Vogliono il corpus C2 annotato, che è lavoro continuativo |

**La Fase 1 non aveva una data, aveva una condizione:** partire il giorno in cui B2 è verde e non un giorno prima. La condizione si è avverata il 23 settembre, cioè con quasi tre mesi di anticipo sulla casella di dicembre, e la fase è chiusa. L'anticipo non si è preso saltando il metro, si è preso costruendolo per primo: è esattamente il motivo per cui la regola era scritta così.

Quello che resta in calendario da qui a febbraio è la Parte C, il lato Documentale: C0 (decidere cosa è un documento nel corpus), C1 (comando di export) e C2 (log delle query, che più presto si accende più raccoglie).

A dicembre c'è anche la riproposta della tesi a Bonnici e Dal Palù descritta in [appunti.md](appunti.md). Il Task A3 e il diario servono anche lì: far vedere un baseline congelato, un flag e un diario con ipotesi datate è la differenza, in trenta secondi, fra "ho un motore di ricerca" e "ho un esperimento in corso".
