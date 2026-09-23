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

- [x] **Passo 4: commit** (`244207f`)

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

- [x] **Passo 1: scrivere il test che fallisce**

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

- [x] **Passo 2: lanciarlo e vederlo fallire**

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

- [x] **Passo 4: verificare**

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

- [x] **Passo 6: commit** (`ca4b7c4`)

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

Branch **`martin/tesi-magistrale`**, creato il 23 settembre 2026 da `fix/various-fixes` (commit `5c31647`), che conteneva già dei fix miei in corso.

**Correzione del 23/09/2026, seconda parte della giornata:** questa riga diceva "esiste solo in locale, non è su `origin`". È falso: il ramo è su `origin` a `5c31647`, spinto da GitHub Desktop pochi minuti dopo la creazione, non da me. È la seconda volta nella stessa giornata (era già successo con due commit di questo repo). **Su questa macchina un commit o un ramo esce in rete da solo nel giro di un minuto**, quindi qualunque frase del tipo "resta in locale" va verificata con `git ls-remote`, non data per scontata. Conseguenza pratica: niente dati di clienti in nessun commit di questo ramo, nemmeno temporaneo, perché non c'è una finestra in cui il commit è solo mio.

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

- [x] Verificare se il testo integrale sia già disponibile da qualche parte nella pipeline Python senza doverlo riestrarre - **verificato il 23/09/2026, la risposta è no, e cambia il costo dell'Opzione B**
- [x] ~~Chiedere in azienda se il testo integrale si può conservare~~ - **decaduta il 23/09/2026: l'azienda ha abbandonato Documentale**, non c'è più nessuno a cui chiedere né alcun archivio di clienti da usare
- [x] **Il C0 si chiude in favore dell'Opzione B**, e senza chiedere il permesso a nessuno. Il corpus viene da albi pretori pubblici (vedi Task E2): su documenti pubblicati per obbligo di legge non c'è riservatezza di clienti da tutelare, e conservare il testo integrale è una scelta dentro la tesi, non una modifica al prodotto di qualcun altro
- [x] E l'Opzione A non viene buttata: le due fonti trovate sono l'una il caso a soli metadati e l'altra il caso col testo intero, quindi **la domanda del C0 diventa un esperimento** invece di una decisione al buio - quanto guadagna il recupero quando al posto della scheda c'è il documento
- [ ] Portare comunque la scelta al relatore a dicembre: cambia il perimetro della tesi, e scoprirlo a marzo sarebbe tardi

### Cosa ho trovato guardando la pipeline (23/09/2026)

**Il testo integrale non esiste in nessun punto del processo, nemmeno di
passaggio.** Non è che venga estratto e poi buttato via: non viene mai estratto.
`apps/python/app/api/documents/routes.py` manda al modello il **base64 del file
intero** (`document_base64`, come `input_file` o `image_url`) e riceve indietro
solo il JSON strutturato. In `requirements.txt` non c'è nessuna libreria di
estrazione: niente pypdf, niente pdfplumber, niente OCR. La pipeline è
multimodale dall'inizio alla fine.

Quindi l'Opzione B non è "salviamo quello che già estraiamo", è **"aggiungiamo
una capacità di estrazione che oggi non c'è"**: una dipendenza nuova, un passo
nuovo nella pipeline, e la sua manutenzione. Il costo stimato nel task qui sopra
(una migration e un punto nella pipeline) era sottostimato, e va corretto prima
di portare la domanda in azienda.

**La buona notizia che compensa:** i file originali sono conservati
(`spatie/laravel-medialibrary`, tabella `media`, `document_versions.media_id`).
Quindi l'estrazione si può fare **a posteriori sui documenti già caricati**, in
un comando che gira una volta, senza aspettare nuovi upload. Per il calendario
di febbraio è la differenza fra avere un corpus e non averlo.

**L'opzione C, quella da rifiutare esplicitamente prima che qualcuno la
proponga.** Visto che il modello il documento lo legge già, verrebbe naturale
chiedergli in più anche la trascrizione integrale: nessuna dipendenza nuova, una
riga di prompt. **Non si fa.** Un testo prodotto da un LLM non è il documento: è
una parafrasi con dentro normalizzazioni, omissioni e, sui numeri e sui nomi
propri, invenzioni. Costruirci sopra un corpus di recupero vuol dire misurare
quanto bene il motore trova cose in un testo che nessuno ha mai scritto, e il
risultato sarebbe indifendibile in discussione. Se si fa l'Opzione B, si fa con
un estrattore deterministico.

Finché C0 non è chiuso, il Task C1 si fa comunque, perché il grosso dell'export è identico nelle due opzioni: cambia solo il campo `text`.

## Task C1: Comando di export del corpus di valutazione - FATTO il 23/09/2026

Genera il corpus nel formato del Task 0.1 del piano di tesi, con quello che in Documentale esiste davvero. `meta_true` resta vuoto: per definizione si scrive a mano.

**File:**
- Crea: `apps/laravel/app/Console/Commands/ExportEvalCorpus.php`
- Test: `apps/laravel/tests/Feature/ExportEvalCorpusTest.php`

**Interfacce:**
- Consuma: `DocumentVersion` con la relazione `fields()` verso `DocumentField` (`app/Models/DocumentVersion.php:150`) e l'accessor `getFieldsFlatAttribute()` (riga 113). `DocumentField` espone `name`, `string_value`, `boolean_value`, `number_value`, `date_value`.
- Produce: un file JSON Lines, un documento per riga, letto dal Task 0.2 del piano di tesi.

- [x] **Passo 1: scrivere il test che fallisce**

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

- [x] **Passo 2: lanciarlo e vederlo fallire**

```bash
cd apps/laravel && php artisan test --filter=ExportEvalCorpusTest
```

Atteso: FAIL, il comando `app:export-eval-corpus` non esiste.

- [x] **Passo 3: scrivere il comando**

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

- [x] **Passo 4: verificare**

```bash
php artisan test --filter=ExportEvalCorpusTest
```

Atteso: PASS.

- [ ] **Passo 5: girarlo su staging e guardare l'output** - da fare quando l'ambiente è su

```bash
php artisan app:export-eval-corpus --limit=20 --out=/tmp/corpus-prova.jsonl
head -1 /tmp/corpus-prova.jsonl | python3 -m json.tool
awk '{ print length($0) }' /tmp/corpus-prova.jsonl | sort -n | tail -3
```

Tre cose da guardare a occhio prima di fidarsi: che `text` non sia quasi vuoto (se lo e', l'Opzione A non regge e il C0 si decide da solo), che i campi estratti abbiano senso, e **che non ci sia dentro niente di un cliente reale**. Il file resta in `/tmp` e non entra in nessun repo finche' l'azienda non ha detto cosa e' pubblicabile.

- [x] **Passo 6: commit** (`ca4b7c4`)

```bash
git add app/Console/Commands/ExportEvalCorpus.php tests/Feature/ExportEvalCorpusTest.php
git commit -m "feat: add eval corpus export command for thesis evaluation"
```

### Com'è andata

Tre test, ognuno provato con una mutazione per essere sicuro che sappia
fallire: tolto il limite il conteggio va a 5 invece di 2, tolto il cast a
oggetto un `meta_pred` vuoto esce come `[]` invece che `{}` e il lettore Go
non lo parserebbe.

**Il blocco del `TODO.md` non c'era.** In fondo a questa parte avevo scritto che
la voce sulla chiave combinata di `document_version_fields` andava fatta prima
del C1, altrimenti l'export sarebbe da riscrivere. Guardando il codice:
`getFieldsFlatAttribute()` indicizza per `$f->name`, cioè per il `path`, non per
l'`id`. Cambiare la chiave primaria da progressiva a combinata
(`document_version_id` + `path`) produrrebbe **lo stesso identico output**. I due
lavori sono indipendenti.

**Non ci sono factory** per questi modelli - in tutto il progetto ce n'è una,
`UserAdminFactory` - quindi la catena si costruisce a mano nel test, e lì sono
uscite due trappole: `document_id` non è fra i `$fillable` di `DocumentVersion`,
e il modello `Media` ha la chiave primaria su `uuid` con `incrementing = false`,
quindi `create()` non popola `id` e la foreign key esce nulla.

**Una correzione a me stesso, che è il motivo per cui questa sezione esiste.**
Ero convinto che `limit()` prima di `chunk()` venisse ignorato da Laravel, e
avevo scritto una guardia contro un export che avrebbe tirato fuori tutti i
documenti dei clienti invece di trecento. Poi ho fatto la mutazione per
verificare che la guardia servisse: il test è rimasto verde. In Laravel 12
`chunk()` legge `getLimit()` e lo scala chunk per chunk
(`BuildsQueries.php:43`), e `enforceOrderBy()` aggiunge l'ordinamento da sé. Il
frammento del piano era giusto dove dicevo che era sbagliato. La guardia è stata
tolta, il test è rimasto - `limit()` è l'unica cosa fra un export distratto e i
documenti dei clienti, e un dettaglio interno al framework merita un test che se
ne accorga se cambia.

Vale la pena notare come è emerso: **non leggendo meglio, ma facendo la
mutazione**. È la stessa disciplina che in mattinata su Koskidex aveva fatto
cadere tre previsioni su cinque. Un test che non si è mai visto fallire non è un
test, è una decorazione.

**Cosa resta:** il Passo 5, girarlo su staging e guardare l'output, che vuole
l'ambiente acceso. Con le tre cose da guardare a occhio già scritte lì sopra,
inclusa la più importante: che nel file non finisca niente di un cliente reale.

## Task C2: Registrare le query di ricerca - FATTO il 23/09/2026

Oggi le ricerche passano da `ElasticsearchService::fuzzySearch()` (riga 97) e non lasciano traccia. Registrarle costa poco e a febbraio fa la differenza fra scrivere sessanta query inventate e partire da quelle che la gente digita davvero.

Non risolve il problema di fondo, che resta scritto in `appunti.md`: c'e' solo staging, quindi il volume sara' piccolo. Ma anche duecento query vere valgono piu' di zero, e sono gratis se il log parte adesso invece che a febbraio.

**File:**
- Crea: `apps/laravel/database/migrations/xxxx_create_search_logs_table.php`
- Crea: `apps/laravel/app/Models/SearchLog.php`
- Modifica: `apps/laravel/app/Services/ElasticsearchService.php:97`

**Interfacce:**
- Produce: la tabella `search_logs`, letta a febbraio per estrarre le query del corpus C2.

- [x] **Passo 1: migration**

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

- [x] **Passo 2: registrare dentro fuzzySearch**

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

- [x] **Passo 3: verificare** (non a mano: vedi sotto)

Fare tre ricerche dall'interfaccia, poi:

```bash
php artisan tinker --execute="dump(\App\Models\SearchLog::latest()->take(3)->get(['term','results_count','duration_ms'])->toArray());"
```

Atteso: le tre query appena fatte, con numero di risultati e durata.

- [x] **Passo 4: commit** (`244207f`)

```bash
git add database/migrations app/Models/SearchLog.php app/Services/ElasticsearchService.php
git commit -m "feat: log search queries to build the thesis query set"
```

### Com'è andata, e due correzioni al task qui sopra

Non c'era nessun container di Documentale acceso, quindi il Passo 3 come scritto
- tre ricerche dall'interfaccia e poi `tinker` - non era eseguibile. Invece di
saltare la verifica ho tirato su un MySQL 8 usa-e-getta, fatto girare **tutte**
le migration, e verificato quattro cose: che la migration si applichi, che la
tabella e il vincolo vengano come previsto, che il modello scriva e rilegga, e
che il `down()` la tolga pulita. Poi container buttato. Senza quel giro, due
errori sarebbero entrati in un commit:

**1. `constrained('users')` non esiste.** In Documentale non c'è nessuna tabella
`users` e nessun modello `User`. L'utente autenticato è `UserAdmin` su
`user_admins`, ed è il provider del guard di default (`config/auth.php`, guard
`admin`). La colonna giusta è `user_admin_id`. Lo snippet nel task qui sopra è
sbagliato ed è stato corretto nel codice, non nel piano: resta scritto così per
memoria di cosa avevo dato per scontato.

**2. `strict => false` in `config/database.php`.** Avevo commentato il taglio del
termine a 512 caratteri dicendo che senza sarebbe fallito l'insert. Non è vero
qui: MySQL lo taglia da solo, in silenzio, **a byte**, il che su un accento
spezza il carattere. Il taglio in PHP resta, ma per la ragione giusta - a
caratteri, e senza dipendere da un flag di configurazione che qualcuno potrebbe
rimettere a `true`.

**Una nota sul volume:** in alcuni flussi `DocumentController` chiama
`fuzzySearch` due volte per una sola ricerca dell'utente, una su `documents` e
una su `folders`. Il log avrà quindi due righe con lo stesso `term` nello stesso
istante. Non è un bug e non va deduplicato in scrittura: la colonna `type` le
distingue, e a febbraio si raggruppa in lettura.

### La scoperta che vale più del task

Guardando `fuzzySearch` per capire dove agganciare il log è saltato fuori questo,
alla riga 113:

```php
'operator' => 'and',  // tutte le parole devono comparire
```

**Elasticsearch, in produzione, è configurato congiuntivo.** È lo stesso
identico difetto 0 che stamattina ho trovato in Koskidex misurando su SciFact,
dove costava 290 query vuote su 300 - e qui è scritto a chiare lettere in un
commento, come una scelta deliberata, sul sistema vero che i colleghi usano
tutti i giorni.

Questo cambia il peso del capitolo. Fino a stamattina il difetto 0 era un difetto
del mio progetto personale, e correggerlo era un esercizio. Ora è **un difetto
condiviso con il sistema di produzione**, e la domanda di tesi diventa più
interessante di quella che avevo scritto: non "il mio motore ha un modello di
recupero tarato male", ma "il modello di recupero congiuntivo è una scelta
ragionevole che diventa sbagliata quando le query si allungano, e questo capita
in due sistemi indipendenti scritti da persone diverse".

E soprattutto: diventa **misurabile sul sistema vero**, e il metro è già
costruito. Appena il log del C2 ha raccolto abbastanza query, si può contare
quante ricerche reali tornano vuote su Documentale e quante parole hanno. Su
NFCorpus le query che tornavano qualcosa avevano in media 2,0 parole e quelle a
vuoto 4,7: se sul carico vero si vede la stessa forma, il capitolo ha un
riscontro in produzione invece che solo su collezioni pubbliche.

Il campo `results_count` del log è già quello che serve per contarlo. Non
l'avevo messo per questo, ma è quello che lo rende possibile.

- [ ] A febbraio: contare le ricerche a risultato zero e incrociarle con la
      lunghezza in parole del termine, come fatto su NFCorpus
- [ ] **Non toccare** l'`operator => and` di Elasticsearch prima di aver
      misurato: è il baseline di produzione, e cambiarlo adesso vuol dire
      perdere il termine di paragone. Vale la stessa regola del baseline
      congelato di Koskidex

## Il TODO.md di Documentale

`TODO.md` ha una decina di voci aperte che non c'entrano con la tesi: notifiche via websocket, rinomina di cartelle e file, il fix dell'upload di cartelle con molti file, la questione dei `document_version_fields` da ricreare con chiave combinata.

**Sono lavoro aziendale e vanno fatte con le priorita' dell'azienda, non con quelle di questo piano.** Le cito solo per dire che non le ho incluse.

~~Una pero' si incrocia: la voce sulla chiave combinata dei `document_version_fields` tocca proprio la tabella da cui l'export legge, quindi va fatta prima del Task C1, altrimenti l'export va riscritto.~~ **Falso, verificato il 23/09/2026:** l'export passa da `getFieldsFlatAttribute()`, che indicizza per `name` (il `path`) e non per `id`, quindi un cambio di chiave primaria non cambia una virgola dell'output. I due lavori sono indipendenti e il C1 non aspettava niente.

## Il confronto vero: Elasticsearch contro Koskidex sullo stesso archivio (23/09/2026)

Fatti C1 e C2, l'ambiente serviva comunque per chiudere l'ultima verifica in
sospeso. Tanto valeva usarlo per la cosa che interessa davvero: **le stesse
query sui due motori, sullo stesso archivio.**

**Come è montato.** MySQL 8 ed Elasticsearch 9.1 in locale, usa-e-getta, mai
toccato l'Elasticsearch in cloud dell'azienda che sta nel `.env`. Quattordici
documenti inventati, con la forma vera dei dati di Documentale (fatture,
contratti, DDT, verbali, offerte, polizze). Indicizzati con
`app:export-to-elastic-search`, cioè il codice dell'app, non una strada mia.
Poi `app:export-eval-corpus` produce il corpus, e `scripts/compare` di Koskidex
lo rilegge e fa le stesse identiche query.

Un dettaglio che cambia il risultato: Documentale cerca con `fuzziness: AUTO`.
Alla prima passata avevo confrontato con la tolleranza ai refusi **spenta** in
Koskidex, e due query su quattro sembravano dare insiemi diversi. Era mio, non
dei motori. Con le impostazioni allineate alla produzione i due recuperano lo
stesso identico insieme ovunque. Il default di `scripts/compare` è ora `auto`
proprio per questo.

### Il risultato

| Query | parole | Elasticsearch | Koskidex oggi | Koskidex or+BM25 |
|---|---|---|---|---|
| `manutenzione` | 1 | 4 | 4 | 4 |
| `manutenzione impianto` | 2 | 2 | 2 | 6 |
| `manutenzione impianto climatizzazione` | 3 | 2 | 2 | 6 |
| `fattura per la manutenzione dell'impianto di climatizzazione della sede` | 9 | **0** | **0** | 14 |
| `documenti sulla sicurezza del cantiere di Piacenza` | 7 | **0** | **0** | 14 |
| `quanto costa il noleggio della piattaforma aerea` | 7 | **0** | **0** | 7 |
| `contratto fornitura energia elettrica` | 4 | 1 | 1 | 2 |
| **Query a vuoto** | | **3 su 7** | **3 su 7** | **0 su 7** |

Due cose, e la seconda è quella che vale.

**Uno. I due motori falliscono sulle stesse identiche query.** Non una in più,
non una in meno. Ed è la conferma sul campo di quello che stamattina era solo
una riga di codice letta: `operator => and` in Elasticsearch e `MustTerms` in
Koskidex sono la stessa scelta, presa da persone diverse in progetti diversi,
con lo stesso identico effetto. La più eloquente è
`documenti sulla sicurezza del cantiere di Piacenza`: in archivio c'è un
*Verbale sopralluogo sicurezza cantiere Piacenza*, e nessuno dei due lo trova,
perché la query contiene anche "documenti", "sulla", "del" e "di".

**Due. Koskidex di oggi recupera lo stesso insieme di Elasticsearch su tutte e
quattro le query che Elasticsearch risponde.** Questo non era scontato ed è il
risultato metodologicamente più importante della giornata: vuol dire che
Koskidex non è un giocattolo che assomiglia a un motore di ricerca, è
**un'implementazione fedele dello stesso modello di recupero**, difetto
compreso. Senza questo, ogni miglioramento misurato su Koskidex sarebbe
contestabile con "sì, ma tu stai migliorando il tuo, non il nostro". Con
questo, il salto da 3 query a vuoto a 0 è un salto che vale anche per
Documentale.

Sull'ordinamento BM25 concorda con Elasticsearch su 3 query su 4, il punteggio
euristico su 2 su 4. Con quattordici documenti è un indizio, non un numero: va
rifatto sul corpus vero.

### Cosa serve per farne un numero da tesi

Oggi è una tabella di conteggi su documenti inventati. Per diventare un
capitolo servono i giudizi di rilevanza, che è esattamente il C2 (le query
vere) più l'annotazione a mano. Ma l'impianto che li legge esiste già ed è lo
stesso usato su SciFact e NFCorpus, quindi il lavoro che resta è
l'annotazione, non il codice.

**Da segnalare in azienda, separatamente dalla tesi:** `ElasticsearchService`
toglie l'estensione dal nome con `pathinfo(..., PATHINFO_FILENAME)`, che legge
la barra come separatore di cartelle. `Fattura 2026/0173.pdf` viene indicizzata
con nome `0173`, e la numerazione italiana delle fatture usa la barra sempre.
Cercare "Fattura 2026" non trova quei documenti per nome. È una riga.

## Il C2 chiuso davvero: dalle query vere ai numeri (23/09/2026)

Il confronto qui sopra conta i risultati ma non sa dire se sono buoni: mancavano
i giudizi di rilevanza. Questo è il pezzo che collega le due metà, e con questo
la catena è completa senza interventi a mano in mezzo.

```
search_logs                                   (il log acceso oggi)
  -> app:export-eval-queries   -> queries.jsonl
document_versions
  -> app:export-eval-corpus    -> corpus.jsonl      (formato BEIR)
  -> scripts/pool              -> giudizi.tsv       <- qui si annota
  -> scripts/pool -sheet       -> qrels/test.tsv
  -> scripts/evaluate          -> nDCG@10, Recall@100, MRR@10
```

**La scelta che fa risparmiare più lavoro:** l'export scrive `_id`, `title` e
`text`, cioè le chiavi di BEIR, tenendosi i campi della tesi accanto dove un
lettore BEIR li ignora. Quindi la collezione di Documentale passa dallo stesso
`LoadCorpus` e dallo stesso esecutore già usati su SciFact e NFCorpus: **zero
righe di Go in più**, e le due collezioni restano confrontabili invece di avere
ognuna il suo lettore che diverge col tempo.

### Due decisioni sul pooling che contano più del codice

**Il foglio è ordinato per id del documento, mai per posizione e mai raggruppato
per configurazione.** Se chi annota vede i risultati in ordine di ranking, legge
la posizione come un suggerimento e finisce per confermarla: i giudizi
concordano col sistema che li ha prodotti per costruzione, e la valutazione non
misura più niente. È lo stesso motivo per cui TREC mescola i pool.

**Un grado vuoto è un errore, non uno zero.** «L'ho guardato e non c'entra» e
«non ci sono ancora arrivato» sono due fatti diversi, e leggere il secondo come
il primo gonfia ogni numero che esce dal file. La conversione si rifiuta di
procedere e dice quale riga manca.

Il bias che resta non si toglie: un documento che nessuna configurazione ha
pescato non viene mai giudicato e vale zero, quindi il recall misurato così è un
limite superiore. È il compromesso standard, ed è la ragione per cui il pool si
costruisce da tutte e tre le configurazioni e non da quella che si vuole
promuovere.

### Il collaudo, e perché i suoi numeri non valgono niente

Ho fatto girare la catena intera: 14 documenti, le 7 query che il log aveva
registrato, 47 giudizi.

| configurazione | nDCG@10 | Recall@100 | MRR@10 | a vuoto |
|---|---|---|---|---|
| oggi (and + euristico) | 0,4604 | 0,3929 | 0,5714 | 3/7 |
| or + euristico | 0,9721 | 1,0000 | 1,0000 | 0/7 |
| or + BM25 | 0,9737 | 1,0000 | 1,0000 | 0/7 |

**Questi numeri non vanno in tesi e non vanno mostrati a nessuno.** I documenti
me li sono inventati io, i giudizi li ho scritti io, e il recall fa 1,0 solo
perché il taglio è a 100 su un corpus di 14. Con quattordici documenti ordinare
bene è quasi impossibile da sbagliare: 0,97 non dice che il motore è buono, dice
che il compito era banale.

Quello che il collaudo dimostra è un'altra cosa, ed è quella che serviva: **la
catena funziona dal database al numero, senza passaggi manuali.** Il giorno in
cui il log avrà query vere e ci sarà un pomeriggio per annotare, i numeri escono.
Non c'è più codice da scrivere prima.

### Cosa manca ancora, per onestà

- **Elasticsearch non è nel pool.** Le tre configurazioni sono tutte di
  Koskidex. Sul corpus di prova non cambia niente, perché in modalità
  disgiuntiva il pool copre praticamente tutto, ma su un archivio vero i
  risultati di Elasticsearch vanno aggiunti al pool, altrimenti il confronto
  parte svantaggiato per lui.
- **Una sola persona che annota.** Senza un secondo annotatore non c'è modo di
  misurare l'accordo, e su un lavoro fatto dalla stessa persona che scrive il
  motore è un'obiezione che in discussione arriva. Vale la pena farne annotare
  un pezzo a qualcun altro, anche solo trenta coppie, per avere un numero da
  citare.

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

**Aggiornamento di fine giornata, 23/09/2026: è finito anche il resto.** C1 e C2 sono fatti, e del C0 è chiusa la parte che dipendeva da me. Il piano copriva da fine settembre a febbraio ed è esaurito in un giorno, il che dice soprattutto che era sovradimensionato nei tempi, non che il lavoro fosse poco.

Quello che resta in calendario **non è più lavoro mio**, sono tre cose che dipendono da altri:

| Cosa | Da chi | Quando |
|---|---|---|
| C0: si può conservare il testo integrale dei documenti, e con quali vincoli? | Azienda | Prima possibile: se la risposta è sì, va messo in conto un estrattore |
| C1 passo 5: girare l'export su staging e guardare cosa esce | Ambiente acceso | Quando c'è |
| C2: aspettare che il log raccolga query vere | Tempo | Più sta acceso più vale |
| Riproposta della tesi | Bonnici e Dal Palù | Dicembre, con i progetti d'esame consegnati |

E una cosa che dipende dal calendario e basta: le Fasi 2 e 3, che vogliono il corpus C2 annotato e restano a febbraio.

**Il lavoro che invece dipende solo da me sta nella [Parte E](#parte-e---quello-che-viene-dopo-aperta-il-23092026)**, aperta lo stesso giorno: analisi lessicale, proposta sul testo integrale, difetto 2 e le due falle del metro. Senza date, uno alla volta.

A dicembre c'è anche la riproposta della tesi a Bonnici e Dal Palù descritta in [appunti.md](appunti.md). Il Task A3 e il diario servono anche lì: far vedere un baseline congelato, un flag e un diario con ipotesi datate è la differenza, in trenta secondi, fra "ho un motore di ricerca" e "ho un esperimento in corso".

---

# Parte E - Quello che viene dopo (aperta il 23/09/2026)

Il piano A-D è chiuso. Questa parte raccoglie i quattro filoni rimasti, nell'ordine in cui conviene prenderli. Non hanno date: si fanno man mano, uno alla volta, con le stesse tre regole di sopra - flag, baseline congelato, voce nel diario prima di misurare.

**L'ordine è ragionato, non arbitrario:**

| | Perché lì |
|---|---|
| **E1** Analisi lessicale | È l'unico misurabile oggi, senza dipendere da nessuno, ed è la leva più grossa rimasta sui numeri |
| **E2** Proposta sul testo integrale | Va fatta partire presto perché la risposta non dipende da me: prima si chiede, prima si sa |
| **E3** Difetto 2, l'ibrido | Bloccato su un corpus con embedding. Si può scrivere, non si può misurare |
| **E4** Rendere il metro difendibile | Non urgente finché non ci sono giudizi veri, ma va fatto **prima** dell'annotazione vera, non dopo |

E4 dopo E1 ma prima dell'annotazione: rifare i giudizi perché il pool era incompleto è lavoro buttato, e l'annotazione è la cosa più cara di tutte.

## Task E1: Analisi lessicale - stemmer e stopword - FATTO il 23/09/2026

### Risultato

| | nessuna | solo stopword | solo stemmer | entrambi | riferimento |
|---|---|---|---|---|---|
| SciFact nDCG@10 | 0,6197 | **0,6641** | 0,6243 | 0,6585 | 0,6789 |
| NFCorpus nDCG@10 | 0,2810 | 0,2900 | 0,2861 | **0,2941** | 0,3218 |

**Dal 91% al 97% del riferimento su SciFact, dall'87% al 91% su NFCorpus.** Su NFCorpus le query che tornano a vuoto scendono da 24 a 15.

**Tre previsioni su sei smentite**, e quella che conta è la terza. Avevo scritto che lo stemmer avrebbe portato molto più delle stopword, perché con BM25 l'IDF schiaccia già i termini frequentissimi. È il contrario: su SciFact le stopword danno +0,0444 e lo stemmer +0,0046. Il ragionamento era giusto sul punteggio e irrilevante, perché il guadagno non viene dal punteggio: viene dal recupero. In modalità disgiuntiva ogni documento che contiene «the» è un candidato, e i candidati medi passano da 4833 a 2522. Le 25 query che non contengono nessuna stopword guadagnano +0,0035, contro +0,0523 di quelle sopra la mediana del taglio.

**Lo schema da portare in tesi.** Due volte in una giornata ho ragionato sul punteggio dimenticando il recupero: stamattina con la guardia sul recall, stasera con le stopword. È lo stesso punto cieco, e adesso è una domanda scritta nel diario da farsi prima di ogni ipotesi: *questa modifica tocca chi entra, o solo in che ordine?*

Dettagli, indagini e le altre previsioni sbagliate in `Koskidex/eval/DIARIO.md`.

### Come era stato pianificato



**Il numero da battere.** SciFact 0,6197 contro 0,6789 di riferimento, NFCorpus 0,2810 contro 0,3218. Manca il 9% e il 13%.

**Dove sta il divario, guardato nel codice.** `Tokenize` in `internal/engine/tokenizer.go:27` fa tre cose: minuscolo, rimozione degli accenti, e spezza su tutto ciò che non è lettera o numero. Punto. Nessuno stemmer, e `DefaultSettings` (`inverted.go:281`) inizializza `StopWords` a una mappa **vuota**.

I riferimenti pubblicati girano su Lucene con `EnglishAnalyzer`, che fa stemming Porter e ha la sua lista di stopword. Non è un'ipotesi: è scritto in `SOURCE.md` come causa prevista **prima** di misurare, ed è il motivo per cui il criterio era "una fascia plausibile più un distacco netto sul legacy" e non "riprodurre il numero".

Un riscontro già in mano, dall'indagine sulle 24 query vuote di NFCorpus: su dieci termini assenti dal corpus, **nove non ci sono in nessuna forma** e uno solo, `leeks` → `leek`, è una mancanza di stemming. Quindi lo stemmer non è la soluzione delle query vuote: è una spinta sull'ordinamento, e l'ipotesi va scritta in quei termini, senza gonfiarla.

### La decisione che viene prima del codice

**Lo stemmer di quale lingua?** Le collezioni pubbliche sono inglesi, Documentale è italiano. Sono due strade e non si sovrappongono:

- **Porter inglese** chiude il divario coi riferimenti, che è l'unico modo di dimostrare che l'implementazione di BM25 è corretta. Ma a Documentale non serve a niente.
- **Snowball italiano** è quello che il prodotto userebbe davvero. Ma non c'è nessun riferimento pubblicato su cui validarlo, quindi il numero che produce non si può confrontare con niente.

**Non è un aut-aut, è un ordine.** Si fa prima l'inglese, perché serve a validare; poi l'italiano, perché serve al prodotto. E il pezzo che conta è che vadano dietro un'**interfaccia**, non un `if` sulla lingua: l'analizzatore è un parametro dell'indice, non una proprietà del motore. Detto in tesi: la lingua è una configurazione, e un motore che non la tratta come tale non è portabile fuori dal caso per cui è nato.

**Il costo da mettere in conto.** Koskidex ha zero dipendenze esterne oltre `golang.org/x/text`, ed è una proprietà che vale la pena difendere. Porter è ~200 righe implementabili a mano; Snowball italiano è più grosso. Se serve una dipendenza, la decisione va scritta nel diario con la sua ragione, non presa di straforo.

- [x] `Settings.Stemmer`, vuoto = comportamento di oggi. Stessa ragione di `RetrievalMode` e `ScoringMode`: le settings sono persistite
- [x] Interfaccia `Analyzer` con `Normalize(term string) string`, chiamata da `Tokenize` **sia in indicizzazione sia in query** - se le due divergono, l'indice non trova più niente e il sintomo sembra un altro bug
- [x] Lista di stopword inglesi, quella di Lucene, come dato e non come codice
- [x] Stemmer Porter, con i casi di prova presi dalla suite ufficiale di Porter: è l'unico modo di sapere che è giusto invece che plausibile
- [x] `TestBaselineRankingIsFrozen` verde a default, senza toccare il test
- [x] Voce nel diario **prima** di misurare (commit `1c30ad0`), con la fascia dichiarata. Attenzione a non promettere troppo: lo stemmer sposta l'ordinamento, non riempie le query vuote
- [x] Misurare separatamente **solo stopword**, **solo stemmer**, **tutti e due**: sapere quale dei due porta cosa vale più del totale
- [x] La guardia giusta, quella imparata oggi: `candidates` **cambierà**, ed è normale - lo stemming cambia il recupero, non solo l'ordine. Quindi qui la guardia è un'altra: il numero di query a vuoto non deve salire

**Cosa resta aperto di E1.** Lo stemmer italiano non è fatto: l'interfaccia c'è, l'implementazione no. E c'è una differenza nota e non corretta, `removeAccents` in Koskidex contro `EnglishAnalyzer` di Lucene che non toglie gli accenti. Non l'ho toccata perché per l'italiano toglierli è probabilmente giusto, ed è una decisione che va presa con l'analizzatore italiano, non di straforo adesso.

**Una cosa che non si spiega e resta aperta:** su SciFact la configurazione migliore è solo stopword (0,6641), non tutte e due (0,6585). Lo stemmer, aggiunto alle stopword, peggiora il nDCG@10 e alza il Recall@100 da 0,8792 a 0,9103. Lettura plausibile: porta dentro più rilevanti in profondità e più rumore in testa. Ma il riferimento usa entrambi e arriva più in alto di tutte e quattro le configurazioni, quindi la spiegazione non è completa e non la forzo.

## Task E2: Il corpus pubblico - il documentale senza l'azienda

**Il task di prima non esiste più.** Era "portare all'azienda la proposta di
conservare il testo integrale". L'azienda ha abbandonato Documentale: non c'è
più nessuno a cui chiedere il permesso, e soprattutto non c'è più nessun
archivio di clienti da cui prendere i documenti. Il C0 non si decide più
chiedendo, e il corpus non può venire da lì.

Quello che resta in piedi è tutto il resto, ed è parecchio: il software gira in
locale, il comando di export del C1 funziona, il log delle query del C2 c'è, il
confronto con Elasticsearch è stato fatto. Manca una cosa sola, i documenti da
metterci dentro. Quindi il task diventa: **trovare un archivio pubblico che
abbia la forma di un documentale, e caricarlo in Documentale.**

Il caso applicativo non cambia. Documentale resta il sistema di cui si misura
il recupero; cambia solo da dove arrivano i documenti, e diventano dati che
chiunque può riscaricare - che per una tesi è meglio, non peggio, perché il
risultato diventa riproducibile da un lettore.

### Cosa serve davvero

Non "tanti documenti". Un archivio di **una organizzazione sola**, che copra un
periodo continuo, con generi ricorrenti e un vocabolario suo. È quello che
rende un documentale diverso da una collezione di articoli: chi cerca sa già
cosa c'è dentro, e cerca un atto che sa esistere. Devono esserci il testo, dei
metadati veri e una licenza che ne consenta il riuso.

L'albo pretorio è questo. Ogni comune pubblica per obbligo di legge determine,
delibere, ordinanze, avvisi e liquidazioni; sono documenti amministrativi
italiani, della stessa famiglia di quelli che un documentale aziendale
custodisce, e sono pubblici all'origine.

### Le fonti, provate davvero il 23/09/2026

Tre strade cercate, due tenute. I numeri qui sotto vengono tutti da download
eseguiti, non da pagine di descrizione.

**Tenuta - Albo pretorio del Comune di Crispiano (TA).** Feed RSS su
`https://www.trasparenzacrispiano.it/rss.xml`, censito su dati.gov.it e sul
CKAN della Regione Puglia, licenza CC BY 4.0.

- 563 atti, dal 03/11/2025 al 22/09/2026
- 551 item con il **link diretto al PDF**, 12 in `.p7m` (firmati), 1 altro
- generi: 390 determine, 82 delibere, 58 ordinanze, il resto avvisi e pubblicazioni
- cinque PDF scaricati a campione: da 2 a 6 pagine, da 5.472 a 13.311 caratteri
  estratti con `pdftotext`. **Testo nativo, non scansioni.** Nessun OCR da mettere in mezzo

Una precisazione che conta: la scheda del dataset sul CKAN dice che i PDF non
ci sono e che il feed rimanda alla piattaforma dell'ente. È sbagliata.
Scaricando il feed, il `<link>` di ogni item **è** il PDF. Se mi fossi fermato
alla descrizione avrei scartato l'unica fonte buona.

**Tenuta - Albo pretorio della Regione Friuli Venezia Giulia.** Dataset Socrata
`vny3-2fkg`, API JSON senza chiave, licenza IODL 2.0, attribuzione Regione
autonoma Friuli Venezia Giulia.

- 9.457 atti, dal 14/04/2011 al 23/09/2026, **aggiornato lo stesso giorno in cui l'ho scaricato**
- 171 enti distinti, 46 tipologie di atto
- campi: `ente`, `tipologia_atto`, `ufficio_competente`, `oggetto`,
  `numero_atto`, `data_inizio_pubblicazione`, `data_fine_pubblicazione`,
  `link_albo_comunale`
- l'`oggetto` è lungo in media 201 caratteri: è un titolo lungo, non un testo

**Scartata - AlboPOP.** È il progetto che converte gli albi pretori in feed di
formato comune, ed è la strada che sembrava giusta: 253 comuni schedati, 215
con un feed dichiarato. Verificati tutti e 215, uno per uno:

- 105 feed rispondono ancora e hanno almeno un item
- 71 dichiarano allegati, per 9.564 allegati in totale
- scaricandone 14 a campione, **3 arrivano davvero.** Gli altri rispondono
  HTTP 200 con 944 byte di HTML, una pagina di errore travestita da successo

I feed vivi sono quasi tutti fermi al 2021 - venivano dagli scraper del
progetto sulla ricostruzione post-terremoto, che non girano più. AlboPOP resta
un ottimo catalogo per sapere chi pubblica cosa; come sorgente di documenti a
volume non regge, e il modo in cui non regge (200 OK su un errore) è la ragione
per cui andava provato scaricando invece che contando le righe del catalogo.

Per completezza: su dati.gov.it ci sono 297 dataset che parlano di albo
pretorio, ma solo 2 espongono un feed o un XML, e sono i due qui sopra.

### La decisione

**Si usano tutte e due, e non è un compromesso: sono le due opzioni del C0,
diventate misurabili invece che da decidere.**

- Il **FVG** è il corpus grande, con 9.457 schede di metadati e nessun testo
  integrale. È l'**Opzione A** del C0, in scala, con 171 enti che si comportano
  come 171 clienti di un documentale multi-tenant.
- **Crispiano** è il corpus piccolo con il testo intero dietro ogni scheda. È
  l'**Opzione B**.

E così la domanda del C0 smette di essere una decisione da prendere al buio e
diventa un esperimento: *quanto guadagna il recupero quando al posto della
scheda c'è il documento?* Si misura sullo stesso archivio, con le stesse query,
cambiando solo cosa è stato indicizzato. Era il capitolo che mancava.

**Il C0 quindi si chiude qui, in favore dell'Opzione B**, senza chiedere niente
a nessuno: su documenti pubblici per legge non c'è nessuna riservatezza di
clienti da tutelare, e conservare il testo integrale non è più una modifica al
prodotto di qualcun altro - è una scelta mia dentro una tesi.

Cade anche il problema delle credenziali. La pipeline di scansione usa OpenAI
`gpt-4.1` (`apps/python/app/services/ai.py`, via `init_chat_model`) e io non ho
più la chiave. Non serve: il testo del corpus lo produce `pdftotext`, che è
deterministico e non chiama nessuno. E i campi che l'IA dovrebbe indovinare, nel
FVG **ci sono già scritti** - `tipologia_atto` e `ufficio_competente` sono
esattamente un `meta_true` regalato da chi ha pubblicato il dato. Il `meta_pred`
diventa un secondo esperimento, facoltativo e rimandabile, con qualunque modello.

### Le query, che restano il problema vero

Il log del C2 non si riempirà mai: non c'è più un'azienda che usa il sistema.
Le query bisogna fabbricarle, e va detto in tesi con questa parola.

Due strade, entrambe praticabili su queste fonti:

- **Known-item.** Si prende un atto, lo si mostra a una persona senza dirle
  niente, le si chiede di scrivere la ricerca che farebbe per ritrovarlo. Il
  giudizio di rilevanza arriva gratis - il documento giusto è quello di
  partenza - e la query è realistica perché l'ha scritta un umano che voleva
  quel documento. Costa solo tempo di persone.
- **Known-item automatico**, per avere volume. `numero_atto` + `ente`
  identificano un atto in modo univoco, e "determina 1223 Crispiano" è
  letteralmente come si cerca in un documentale. Si generano a centinaia, a
  costo zero, e servono a misurare il caso identificativo - che è poi quello su
  cui BM25 ha già mostrato di fare la differenza nel test del pareggio.

Le due misurano cose diverse e vanno tenute separate: la seconda dice se il
motore trova un atto di cui sai il numero, la prima se lo trova chi il numero
non se lo ricorda.

### Una cosa da non fare finta di non vedere

Gli atti dell'albo pretorio contengono nomi di persone. Cercando marcatori
espliciti (`sig.`, `nato a`, `codice fiscale`, `residente in`) negli oggetti del
FVG ne vengono fuori 67 su 9.457, lo 0,7%, e nel feed di Crispiano ci sono le
pubblicazioni di matrimonio, che sono nomi e cognomi nel titolo.

Sono dati pubblicati per obbligo di legge, quindi usarli per una ricerca è
legittimo. Ma **il corpus non va committato nel repo della tesi**, per la stessa
ragione per cui si è tolta la mail del professore: una cosa è un dato pubblico
sul sito di un comune, un'altra è ripubblicarlo in un archivio su GitHub. Nel
repo ci vanno gli script che lo riscaricano e il file dei giudizi, che rimanda
agli id. In tesi, gli esempi si citano anonimizzati.

### I passi

- [x] **`eval/corpora/fetch-albo.py`** in Koskidex, sola libreria standard: scarica
      tutte e due le fonti, estrae il testo con `pdftotext` e scrive
      `falliti.tsv` **sempre, anche vuoto** - un file assente non si distingue
      da un file che nessuno ha guardato
- [x] I `.p7m` si aprono: sono PDF dentro una busta PKCS#7, e
      `openssl smime -verify -noverify -inform DER` li tira fuori. La firma non
      si verifica, interessa il contenuto e non chi l'ha firmato
- [x] FVG scaricato: 9.457 atti. **E il controllo sugli id ha trovato un
      difetto vero** - il 9% degli atti ha un `numero_atto` che non è un numero
      (`-`, `.`, `///`), e 37 atti diversi finivano sullo stesso id. La chiave
      porta ora in coda l'impronta SHA-1 dell'oggetto, che è deterministica e
      viene uguale a ogni riscaricamento. Restano 2 id ripetuti, e sono atti
      pubblicati due volte con lo stesso oggetto: quelli è giusto che collassino
- [x] **L'Opzione B è nel modello:** `full_text` longText nullable su
      `document_versions`, vuoto per tutto quello che c'era prima, così un
      documento senza testo estratto si comporta esattamente come prima
- [x] **`app:import-albo-corpus`**, che passa dal modello vero. Idempotente sul
      `path`, che è già indicizzato: un import che raddoppia l'archivio a ogni
      esecuzione falserebbe ogni misura fatta dopo, e in silenzio. 8 test
- [x] L'export del C1 non è stato toccato nel comportamento: ha una nuova
      opzione `--text-source=metadata|full`, e **il default resta `metadata`**.
      È il punto che conta - se bastasse dimenticare un'opzione per misurare i
      due motori su basi diverse, il confronto sarebbe truccato di default. 4
      test nuovi, 12 in tutto
- [x] Mutation testing su tutto: cinque mutazioni, cinque uccise. **Una era
      sopravvissuta** - il test sul troncamento del nome passava anche con un
      taglio secco a 255 caratteri, perché controllavo solo che non finisse con
      uno spazio. Rifatto verificando che il taglio cada su un confine di parola
- [x] **Fatto girare sui dati veri, ed e' li' che sono usciti i difetti.**
      10.018 documenti importati (563 Crispiano col testo, 9.455 FVG a sola
      scheda), esportati nelle due varianti, e i due file differiscono in
      esattamente 563 testi e in nient'altro. Tre difetti trovati solo
      eseguendo: Telescope teneva in memoria ogni query e il processo moriva a
      meta' import senza stampare niente (due volte prima di accorgersene); una
      transazione per atto sono novanta minuti; `--limit=0` scriveva un corpus
      vuoto, perche' `limit(0)` in SQL vuol dire zero righe e non "nessun limite"
- [x] **`scripts/compare` leggeva la chiave sbagliata.** Dichiarava `json:"id"`
      mentre l'export scrive `_id` dal passaggio a BEIR: tutti i documenti
      arrivavano con id vuoto, si sovrascrivevano, e l'indice si riduceva a **un
      documento solo** senza un errore. Il confronto ES/Koskidex di stamattina
      **non e' invalidato** - verificato nella storia, allora l'export scriveva
      ancora `id` - ma chiunque l'avesse rilanciato dopo avrebbe avuto numeri
      falsi senza un segnale. Ora `compare` si rifiuta di partire se il corpus
      ha id vuoti o ripetuti
- [x] **E i due corpora non si possono mischiare in un indice solo.** Contando
      quanti dei primi 10 risultati hanno il testo integrale (il 5,4% del
      corpus): l'euristico ne mette 9, 2 e 10 su tre query; BM25 ne mette **0,
      0 e 0**. Non e' pertinenza, e' la normalizzazione della lunghezza: 9.455
      schede da 200 caratteri tirano giu' la lunghezza media e `b = 0,75`
      penalizza tutto cio' che e' lungo. Se avessi misurato prima e guardato
      dopo, la risposta sarebbe stata *"il testo integrale peggiora il
      recupero"*, che e' falsa. La domanda del C0 va posta come due misure sugli
      **stessi 563 documenti**, una con la sola scheda e una col testo
- [ ] Indicizzare su Elasticsearch **locale** e rifare il confronto testa a testa
      sul corpus vero. Attenzione: il `.env` del repo punta a un cluster in
      cloud aziendale, non a `localhost:9201`
- [ ] Rimisurare `b` sul corpus dei soli documenti lunghi: 0,75 e' un default
      tarato su collezioni di articoli
- [ ] `eval/corpora/` continua a stare fuori dal git, come già è
- [ ] Generare le query known-item automatiche da `numero_atto` + `ente`
- [ ] Raccogliere le known-item umane: trenta o quaranta, chiedendole a persone
      diverse, con le istruzioni scritte prima (vedi E4)
- [ ] Scrivere in `appunti.md` che il corpus è pubblico e perché, con le fonti e
      le licenze. È una domanda che arriva in discussione di sicuro

## Task E3: Difetto 2 - l'ibrido che non è ibrido

**Il difetto, alla riga esatta.** In `ranker.go:228-250` il punteggio vettoriale entra in due modi diversi. Se la query non ha nessun termine lessicale, scorre tutti i documenti e li punteggia col coseno. Se invece ha dei termini - cioè sempre, nell'uso reale - il ramo `else` itera su `docMatches`, che contiene **solo quello che il lessicale ha già trovato**. Un documento semanticamente pertinente che il lessicale non pesca non entra mai. Non è recupero ibrido, è re-ranking.

Da tenere distinto dal difetto 0, anche in tesi: il difetto 0 era il lessicale che non fa OR fra i suoi termini, questo è il vettoriale che non porta candidati propri. Si assomigliano e non sono la stessa cosa.

**Perché è l'ultimo della fila.** Per misurarlo serve un corpus con embedding e giudizi, e Koskidex non ha un modello né dipendenze esterne. Si può scrivere la correzione dietro flag adesso, ma senza un numero resta un'opinione, e la regola che ci siamo dati dice il contrario.

- [ ] Decidere **prima** da dove vengono gli embedding: un modello locale è una dipendenza nuova, un servizio esterno è una chiamata in rete dentro un motore che oggi non ne fa. È la stessa decisione del C0: si scrive, non si subisce
- [ ] `Settings.HybridMode`, vuoto = re-ranking di oggi
- [ ] Nel ramo ibrido, il vettoriale deve poter **aggiungere** documenti a `docMatches`, non solo sommare punteggio a quelli che ci sono
- [ ] Un test che fallisce col comportamento di oggi: un documento pertinente solo semanticamente, che il lessicale non pesca, deve comparire fra i risultati
- [ ] Attenzione al costo: scorrere tutti i vettori a ogni query è O(n) sul corpus. Sul volume di un documentale aziendale regge - è la ragione per cui `rustann` e gli indici approssimati sono fuori perimetro - ma il numero va misurato, non dato per buono
- [ ] Il difetto 3, la fusione che somma scale incomparabili (`sim * 20.0` contro un lessicale che cresce con la lunghezza della query), viene subito dopo e sullo stesso corpus

## Task E4: Rendere il metro difendibile

Due buchi noti nell'impianto di valutazione. Nessuno dei due è urgente adesso, tutti e due vanno chiusi **prima** dell'annotazione vera: rifare i giudizi perché il pool era incompleto è l'unico lavoro davvero buttato di tutto il piano.

**Buco 1: Elasticsearch non è nel pool.** `scripts/pool` costruisce il pool da tre configurazioni, tutte di Koskidex. Sul corpus di prova non cambia niente, perché in modalità disgiuntiva il pool copre quasi tutto. Su un archivio vero no: i documenti che solo Elasticsearch pesca non verrebbero mai giudicati, conterebbero zero, e il confronto partirebbe **svantaggiato per lui**. Un confronto truccato a proprio favore è la cosa peggiore che possa esserci in una tesi, anche involontariamente.

- [ ] `scripts/pool` accetta ranking esterni da file e li unisce al pool
- [ ] Il file va scritto con gli **id del corpus**, non con quelli di Elasticsearch: oggi ES indicizza per `Document::id` e il corpus usa `doc-0001`, e l'export porta già `document_id` apposta
- [ ] Un comando in Documentale che produce quel file eseguendo `fuzzySearch` sulle query del log
- [ ] Verificare che il pool cresca davvero: se aggiungere ES non aggiunge nessun documento, o va bene o il convertitore non funziona, e le due cose vanno distinte

**Buco 2: un solo annotatore, che è anche chi scrive il motore.** In discussione è un'obiezione che arriva, e ha ragione di arrivare.

- [ ] Far annotare **le stesse** trenta o quaranta coppie a qualcun altro - Leopoldo è la persona ovvia, ha già lavorato con me su Constraint Programming
- [ ] Calcolare l'accordo (Cohen's kappa) e **riportarlo comunque**, anche se viene basso: un kappa mediocre dichiarato vale più di un kappa assente, e se viene basso dice che le istruzioni di annotazione sono ambigue, il che è un risultato
- [ ] Scrivere le istruzioni di annotazione **prima** di darle a qualcun altro, e metterle nel repo. Sono quelle che rendono i giudizi ripetibili, ed è anche l'unico modo di misurare se il disaccordo è sulle istruzioni o sui documenti
