# 14. Requirements engineering

## Perché i requisiti sono critici

Studi storici (Leveson, FAA): la **maggior parte** degli incidenti software-related in sistemi critici NON è dovuta a bug di codice ma a **requisiti errati, ambigui o incompleti**. Il software fa esattamente quello che gli si dice — il problema è che gli si dice la cosa sbagliata.

Esempi celebri:
- **Therac-25** (1985–87) — race condition + requisiti incompleti su modalità incompatibili → morti per overdose.
- **Ariane 5** Flight 501 (1996) — riuso software Ariane 4 senza riconvalidare i requisiti per il nuovo profilo di volo.
- **Boeing 737 MAX** MCAS (2018–19) — requisiti sull'autorità del MCAS e sull'input AoA singolo non adeguatamente analizzati.

## Modello di Jackson — World e Machine

Michael Jackson (libro in bibliografia) introduce la distinzione fondamentale:

- **Machine** — il sistema da costruire (computer + software).
- **World** — l'ambiente fisico/sociale in cui la machine opera.
- **Specification** — descrizione del comportamento alla **interfaccia** machine/world (variabili condivise).
- **Requirement** — proprietà desiderata del **world**.
- **Domain knowledge** — proprietà del world indipendenti dalla machine.

Equazione di Jackson:

```
S, D ⊢ R
```

> Le specifiche S, in presenza delle proprietà di dominio D, devono implicare il requisito R.

Conseguenze pratiche:
- Un requisito non si soddisfa solo con la machine: dipende da assunzioni sul world.
- Se le assunzioni D sono sbagliate, S corretto produce R violato.
- Documentare D è importante quanto S e R.

### Esempio

Requisito (R): "il treno deve fermarsi prima del segnale rosso".
Spec (S): "se input == ROSSO allora output_freni = ON".
Domain (D): "il sensore di colore funziona; i freni rispondono in T < tempo di arresto".

Se D non vale (sensore guasto, frenata lenta a causa pioggia) il sistema fallisce nonostante S sia rispettata.

## High-level vs low-level requirements

Distinzione tipica negli standard (DO-178C, IEC 61508):

- **System requirements** — proprietà del sistema completo (HW + SW + ambiente).
- **High-level software requirements (HLR)** — derivati dai system requirements, esprimono **cosa** il software deve fare in termini di funzioni e prestazioni.
- **Low-level software requirements (LLR)** — sufficienti per implementare il codice senza ulteriore decisione di design; descrivono **come** a livello di moduli/funzioni.
- **Source code** — implementazione delle LLR.

Tracciabilità bidirezionale: ogni requisito deve essere derivabile da quello sopra e implementato in quello sotto.

## Caratteristiche di un buon requisito

Linee guida classiche (IEEE 830, INCOSE):

- **Correct** — riflette il bisogno reale.
- **Unambiguous** — interpretazione unica.
- **Complete** — copre tutti i casi (incluso comportamento in errore).
- **Consistent** — non contraddice altri requisiti.
- **Verifiable** — esiste un metodo per controllare la conformità.
- **Modifiable** — strutturato per essere aggiornato.
- **Traceable** — collegabile a fonti e implementazione.
- **Feasible** — implementabile entro vincoli di costo/tecnologia.
- **Necessary** — non over-specification.

Anti-pattern: "il sistema deve essere veloce/affidabile/user-friendly" → non verificabile.

## Tipi di requisiti

- **Functional** — cosa fa.
- **Non-functional / quality** — performance, reliability, usability, security, safety.
- **Constraints** — vincoli imposti (linguaggio, HW target, standard di conformità).
- **Interface** — interazione con altri sistemi.
- **Operational / environmental** — condizioni d'uso (temperatura, umidità, alimentazione).
- **Safety / security requirements** — derivati da hazard analysis / threat analysis.

## FAA Requirements Engineering Management Handbook

Il REMH (in bibliografia) propone una metodologia in 6 step:

1. **Define the problem** — capire il bisogno reale prima di scrivere requisiti.
2. **Understand user/stakeholder needs** — interviste, scenari, casi d'uso.
3. **Define the system boundaries** — cosa è dentro, cosa è fuori.
4. **Develop the system requirements** — alta qualità, tracciabili.
5. **Allocate requirements** — assegnare a HW/SW/operatore/ambiente.
6. **Verify and validate requirements** — review, prototipi, esecuzione.

Concetti chiave del REMH:
- **Operational concept** prima dei requisiti — narrare come il sistema sarà usato.
- **Use cases / scenarios** per disambiguare.
- **Requirements review** strutturate (con checklist).
- **Validation in early phase** — prototipi, simulazione.

## Tecniche di elicitazione

- **Interviste** strutturate / semi-strutturate.
- **Workshop** (JAD - Joint Application Design).
- **Osservazione etnografica** — vedere gli utenti al lavoro.
- **Analisi di documenti** esistenti.
- **Prototipazione** (throwaway, evolutionary).
- **Use cases / user stories**.
- **Goal-oriented** (KAOS, i*).

## Specifica formale dei requisiti

Per requisiti critici, linguaggio naturale insufficiente. Tecniche:

- **Strutturato** — boilerplate ("the system shall...").
- **Tabelle di decisione** — combinazioni input/output.
- **State machines** — comportamento reattivo.
- **Pre/post-condizioni** — Hoare logic, Design by Contract.
- **Logiche temporali** — proprietà su sequenze (LTL, CTL).
- **Linguaggi formali** — Z, B, VDM, Alloy, TLA+.

In pratica, il linguaggio naturale (controllato) resta predominante, integrato da diagrammi e tabelle dove utile.

## Requirements review

Tecniche per valutare la qualità dei requisiti:
- **Inspection** (Fagan) — formal review con ruoli definiti.
- **Walkthrough** — autore guida la review.
- **Checklist** — domande standard (testabilità, completezza, ambiguità).
- **Scenari** — eseguire mentalmente i requisiti su casi concreti.
- **Prototyping** — il prototipo come oracolo dei requisiti.

## Volere vs poter cambiare

I requisiti **cambieranno**. Un buon processo:
- Tracciabilità per impact analysis.
- Versioning dei requisiti.
- Change control board per modifiche significative.
- Re-verification per requisiti modificati e dipendenti.
