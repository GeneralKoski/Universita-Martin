# 15. Specifiche formali e semi-formali

## Perché formalizzare

Linguaggio naturale è ambiguo. Specifiche formali offrono:
- **Precisione** - interpretazione unica.
- **Analizzabilità** - verifica automatica di consistenza, completezza, proprietà.
- **Generazione** - di test, codice, documentazione da una sorgente unica.
- **Comunicazione** - tra stakeholder con linguaggio condiviso.

Costo: skill richiesto, tempo iniziale alto, difficoltà di review da parte di non esperti.

## Spettro di formalizzazione

```
linguaggio naturale → strutturato → semi-formale → formale
```

- **Naturale**: prosa libera.
- **Strutturato**: template, "shall" requirements.
- **Semi-formale**: UML, SysML, state machines, decision tables.
- **Formale**: logiche, calculi (Z, B, TLA+, VDM, Event-B).

Il corso, da programma, **non si addentra nei metodi formali** ma li cita per il rapporto costi/benefici.

## Design by Contract (Meyer)

Specificare il comportamento di una funzione/metodo con:

- **Pre-condizione** - stato richiesto al chiamante.
- **Post-condizione** - stato garantito al ritorno.
- **Invariante** - proprietà sempre vera per la classe/modulo.

Esempio (sintassi Eiffel-like):

```
square_root(x: REAL): REAL
  require
    x >= 0
  ensure
    Result * Result ≈ x
    Result >= 0
```

Vantaggi:
- Documentazione eseguibile.
- Errori catturati al confine giusto.
- Base per test, analisi statica, verification.

Strumenti moderni: JML (Java), Spec# (C#), ACSL (Frama-C), Dafny, contratti Python (icontract), Eiffel.

## Specifiche basate su tabelle

### Decision tables

Per logica complessa con molte combinazioni:

| C1: età ≥ 18 | C2: patente | A1: noleggio | A2: deposito doppio |
|--------------|-------------|--------------|---------------------|
| F            | -           | F            | -                   |
| V            | F           | F            | -                   |
| V            | V (>3 anni) | V            | F                   |
| V            | V (≤3 anni) | V            | V                   |

Buone proprietà: completezza (tutte le combinazioni), assenza di contraddizioni.

### Tabular notation (Parnas)

Usata in software safety-critical (es. Darlington nuclear). Tabelle per definire funzioni in modo completo e verificabile.

## State machines

Modello reattivo: stati + transizioni etichettate da eventi/condizioni/azioni.

Estensioni:
- **Statecharts** (Harel) - stati gerarchici, parallelismo, history.
- **UML state machines** - basati su statecharts, standardizzati.

Buoni per:
- Sistemi reattivi e protocolli.
- Generazione automatica di codice.
- Model checking di proprietà di sicurezza/liveness.

Non adatti a:
- Logica computazionale complessa (meglio funzionale/imperativa).
- Spazi di stato grandi non strutturati.

## Linguaggi formali notevoli

### Z

Notazione basata su set theory + logic. Schema:
- **State schema** - stato del sistema con invarianti.
- **Operation schema** - pre/post condizioni di operazioni.

Pesante per esecuzione, forte per analisi e prova.

### B / Event-B

Sviluppato da J.-R. Abrial. Supporta **refinement**: dalla specifica astratta a un'implementazione concreta in passi giustificati. Tool: Atelier B, Rodin.

Caso d'uso famoso: software della **linea 14 della metro di Parigi** (driverless), sviluppato in B.

### TLA+

Leslie Lamport. Specialità: sistemi distribuiti, concorrenti. Modello + proprietà temporali (TLA).
Tool: TLC (model checker), TLAPS (proof system).

Usato da AWS, Microsoft Azure, MongoDB per protocolli critici.

### VDM-SL / VDM++

Vienna Development Method. Specifiche eseguibili, tool VDMTools, Overture.

### Alloy

Linguaggio basato su relational logic. Analisi automatica con SAT solver.
Buono per esplorare modelli ed individuare controesempi piccoli (small-scope hypothesis).

## Refinement

Trasformazione da specifica astratta a implementazione concreta preservando le proprietà.

```
Spec₀ ⊑ Spec₁ ⊑ ... ⊑ Implementation
```

Ogni passo deve essere giustificato (proof obligation). Tool come Event-B/Rodin generano automaticamente le obbligazioni.

## Quando usare cosa (rapporto costo/beneficio)

| Tecnica                | Costo | Beneficio | Quando                                        |
|------------------------|-------|-----------|-----------------------------------------------|
| NL strutturato         | basso | basso     | Sempre, baseline                              |
| Decision tables        | basso | medio     | Logica con molte combinazioni                 |
| State machines (UML)   | medio | medio     | Sistemi reattivi, protocolli                  |
| Design by Contract     | medio | alto      | API, librerie critiche                        |
| Z/B/VDM                | alto  | alto      | SIL 3-4, certificazione                       |
| TLA+                   | medio | alto      | Protocolli concorrenti/distribuiti            |
| Theorem proving        | molto alto | molto alto | Componenti critici per safety/security    |

L'approccio pragmatico negli standard: **livello di formalismo proporzionale al SIL**.

## Limiti

- **Specifica corretta del problema sbagliato**: formalismo non aiuta se il problema iniziale è mal compreso.
- **Validation** dei modelli formali resta un problema (animation, simulation, prototyping).
- **Cost of change**: modificare una specifica formale è più costoso di modificare prosa.
- **Skill scarcity**: pochi ingegneri sanno usarli, scarsa familiarità nel team.
