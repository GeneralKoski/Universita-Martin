# 5. Testing

## V&V

- **Verification**: stiamo costruendo il prodotto in modo corretto? (rispetto delle specifiche)
- **Validation**: stiamo costruendo il prodotto giusto? (soddisfa i bisogni dell'utente)

## Livelli di test

- **Unit test** — singola unità (funzione, classe).
- **Integration test** — interazione tra moduli.
- **System test** — sistema completo end-to-end.
- **Acceptance test** — verifica con l'utente/cliente.
- **Regression test** — assicura che modifiche non rompano funzionalità esistenti.

## Approcci

- **Black-box** (functional): si testa il comportamento senza conoscere l'implementazione. Tecniche: equivalence partitioning, boundary value analysis, decision tables, state-based.
- **White-box** (structural): si usa la conoscenza del codice. Tecniche: coverage criteria.
- **Grey-box**: ibrido.

## Coverage criteria (white-box)

- **Statement coverage** — ogni istruzione eseguita almeno una volta.
- **Branch coverage** — ogni ramo (if/else) eseguito.
- **Condition coverage** — ogni condizione booleana valutata true e false.
- **MC/DC** (Modified Condition/Decision Coverage) — richiesto da DO-178C livello A; ogni condizione mostra indipendentemente il proprio effetto sul decision.
- **Path coverage** — ogni cammino (esplosione combinatoria).
- **Loop coverage**: 0, 1, n iterazioni.

Gerarchia: path ⊃ branch ⊃ statement.

## Black-box: tecniche

### Equivalence partitioning

Dividere il dominio in classi di equivalenza, scegliere un rappresentante per classe.

### Boundary value analysis

Bug si annidano ai bordi: testare min, min+1, max-1, max, fuori range.

### Decision tables

Tabelle con condizioni e azioni per coprire tutte le combinazioni rilevanti.

### State transition

Modellare il sistema come FSM, coprire stati e transizioni.

## Mutation testing

Misura la qualità della test suite:
1. Si introducono **mutanti** (piccole modifiche al codice: cambiare operatore, costanti, ecc.).
2. Si esegue la test suite.
3. Un mutante è **killed** se almeno un test fallisce, altrimenti **survived**.
4. **Mutation score** = killed / (totali − equivalenti).

Mutanti equivalenti: semanticamente identici all'originale, non killable.

## Fuzz testing

Generare input casuali o malformati per scoprire crash/vulnerabilità. Tipi:
- **Black-box random**
- **Mutation-based** (es. AFL, libFuzzer): parte da seed e muta.
- **Generation-based**: usa una grammatica.
- **Coverage-guided**: usa feedback di coverage per esplorare nuovi rami.

## Property-based testing

Specificare proprietà invarianti, lo strumento genera input casuali per cercare controesempi (QuickCheck, Hypothesis).

## Test doubles

- **Dummy** — passato ma non usato.
- **Stub** — risposta predefinita.
- **Fake** — implementazione semplificata funzionante.
- **Mock** — verifica le interazioni.
- **Spy** — registra le chiamate.

## Limiti

> Testing can show the presence of bugs, never their absence. — Dijkstra
