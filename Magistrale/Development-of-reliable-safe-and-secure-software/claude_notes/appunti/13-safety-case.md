# 13. Safety case e argomentazione

## Definizione

Un **safety case** è un'argomentazione strutturata, supportata da un corpo di evidenze, che giustifica che un sistema è **accettabilmente sicuro** per una determinata applicazione in un determinato ambiente operativo.

Definizione formale (UK MoD Def Stan 00-56):

> A structured argument, supported by a body of evidence that provides a compelling, comprehensible and valid case that a system is safe for a given application in a given operating environment.

## Tre componenti

1. **Claim** — l'affermazione da dimostrare ("il sistema è safe per uso X in ambiente Y").
2. **Argument** — il ragionamento che lega evidenze al claim.
3. **Evidence** — i fatti oggettivi: risultati di test, analisi, ispezioni, esperienza operativa.

```
        CLAIM
          │
       (sostenuto da)
          │
       ARGUMENT
          │
       (basato su)
          │
       EVIDENCE
```

## Perché è necessario

- Gli standard moderni (UK MoD, ISO 26262 Part 2, IEC 61508 in modo implicito) richiedono safety case.
- Il sistema **non può essere dimostrato sicuro** in senso assoluto: ci si limita a fornire un'argomentazione convincente.
- Costringe gli sviluppatori a esplicitare i ragionamenti che spesso restano impliciti.
- Permette agli **assessor** indipendenti di valutare critiche e debolezze.

## GSN — Goal Structuring Notation

Notazione grafica più diffusa per safety case. Elementi principali:

- **Goal** (rettangolo): claim da dimostrare.
- **Strategy** (parallelogramma): come si suddivide il goal in sotto-goal.
- **Solution** (cerchio): evidenza che chiude un goal.
- **Context** (rettangolo arrotondato): contesto, definizioni.
- **Assumption** (ovale "A"): ipotesi non dimostrate.
- **Justification** (ovale "J"): motivazione di una scelta.

Esempio sintetico:

```
G1: Il sistema XYZ è accettabilmente safe
        │
       S1: argomento per scomposizione su hazard
        │
        ├── G2: H1 è mitigato (occorrenza < 10⁻⁹/h)
        │       └── Sn1: Report FTA
        ├── G3: H2 è mitigato
        │       └── Sn2: Report di test
        └── G4: nessun hazard residuo
                └── Sn3: Hazard log
```

## Struttura tipica di un safety case

1. **Sistema e scope** — cosa è il sistema, confini, modalità operative.
2. **Operational environment** — ipotesi sull'ambiente.
3. **Hazard identification & risk assessment** — hazard log, classificazione.
4. **Safety requirements** — derivati dagli hazard, allocati ai componenti.
5. **Safety architecture** — come l'architettura raggiunge i requisiti.
6. **Implementation evidence** — verifiche, test, analisi.
7. **Operational evidence** — esperienza in field, monitoring.
8. **Limitations and assumptions** — ciò che il safety case NON copre.

## Tipi di argomento

- **Deterministico** (process-based): "abbiamo seguito lo standard X al SIL Y → siamo safe".
  - Pro: oggettivo, accettato dai certificatori.
  - Contro: process compliance ≠ safety reale.
- **Probabilistico**: "PFH < 10⁻⁹ basato su modello e dati storici".
  - Pro: quantitativo.
  - Contro: assunzioni di indipendenza spesso ottimistiche.
- **Qualitativo / experiential**: "milioni di ore di operazione senza failure".
  - Pro: forte se i dati ci sono.
  - Contro: dati raramente disponibili per nuovi sistemi.

In pratica si combinano tutti e tre.

## Confutazione e fallacie comuni

Critica a safety case (Kelly, Leveson):
- **Argument by appeal to compliance** — "abbiamo seguito lo standard, quindi safe" senza guardare al sistema reale.
- **Fallacious diversity** — diversità sostenuta ma non realmente indipendente (stessi sviluppatori, stessa toolchain).
- **Hidden assumptions** — assunzioni non documentate che si rivelano false in operation.
- **Confirmation bias** — solo evidenze che confermano, ignorate quelle contrarie.
- **Quantification senza dati** — numeri di affidabilità inventati o estrapolati troppo aggressivamente.

## Safety case e il corso

Bagnara nel programma sottolinea proprio la capacità di **argomentare di fronte a pari** l'adeguatezza delle scelte. Il safety case è il manufatto chiave dove questa argomentazione si concretizza. Atteso che il progetto finale del corso includa la stesura (anche parziale) di un safety case per il sistema embedded scelto.

## Confronto con altre forme

| Documento            | Scopo                                          |
|----------------------|------------------------------------------------|
| Safety case          | Argomentare la safety complessiva              |
| Safety requirements  | Specificare cosa il sistema deve fare/non fare |
| Hazard log           | Tracciare hazard e mitigazioni                 |
| FMECA / FTA report   | Analisi specifiche, evidenze del safety case   |
| Verification report  | Risultati delle attività V&V, evidenze         |

Il safety case è il **documento di sintesi** che lega tutti gli altri.
