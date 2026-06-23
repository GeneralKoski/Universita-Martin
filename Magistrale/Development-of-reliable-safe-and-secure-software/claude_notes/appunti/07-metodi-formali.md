# 7. Metodi formali

Tecniche basate su matematica e logica per **specificare** e **verificare** sistemi.

## Spettro

```
testing  ←  static analysis  ←  model checking  ←  theorem proving
(meno garanzie, più scalabile) ←———————————→ (più garanzie, meno scalabile)
```

## Specifiche formali

- **Pre/post-condizioni** (Hoare logic, Design by Contract).
- **Invarianti** di loop e di classe.
- **Temporal logic** (LTL, CTL) per proprietà comportamentali.
- Linguaggi: Z, B, VDM, Alloy, TLA+, Event-B.

## Hoare logic

Tripla: **{P} S {Q}**
- P = precondizione
- S = statement
- Q = postcondizione

Significato: se P vale prima di S e S termina, allora Q vale dopo.

### Regole principali

- **Assignment**: {Q[E/x]} x := E {Q}
- **Composition**: {P} S1 {R}, {R} S2 {Q} ⊢ {P} S1; S2 {Q}
- **If**: {P ∧ B} S1 {Q}, {P ∧ ¬B} S2 {Q} ⊢ {P} if B then S1 else S2 {Q}
- **While**: {I ∧ B} S {I} ⊢ {I} while B do S {I ∧ ¬B}  (I = invariante)
- **Consequence**: indebolire post, rafforzare pre.

**Total correctness**: Hoare + terminazione (variant function decrescente).

## Model checking

Dato un modello M (FSM/Kripke structure) e una formula φ in logica temporale, decidere se M ⊨ φ. Esplorazione esaustiva dello spazio degli stati.

### Logiche temporali

**LTL** (Linear Temporal Logic):
- X φ — next
- F φ — eventually (finally)
- G φ — globally (always)
- φ U ψ — until

**CTL** (Computation Tree Logic): aggiunge quantificatori sui path A (all) ed E (exists). Es. AG, EF, AF.

### Esempi di proprietà

- **Safety**: "qualcosa di brutto non accade mai" — G ¬bad
- **Liveness**: "qualcosa di buono accadrà" — F good
- **Fairness**: G F enabled → G F executed

### Problema

State explosion: |stati| esponenziale nelle variabili. Mitigazioni:
- **BDD** (Binary Decision Diagrams) — symbolic model checking.
- **Bounded model checking** (BMC) — esplora fino a profondità k, riduce a SAT.
- **Abstraction** — astrazione/raffinamento (CEGAR).
- **Partial order reduction**.

Tool: SPIN, NuSMV, CBMC, TLA+ TLC, UPPAAL (real-time).

## Theorem proving

Dimostrazione interattiva o automatica di teoremi. L'utente guida la prova, il tool verifica.

- **Interattivi**: Coq, Isabelle/HOL, Lean, Agda.
- **Automatici (SMT)**: Z3, CVC5, Yices.
- **Verification frameworks**: Dafny, F*, Why3, Frama-C/WP.

### Esempi famosi

- **CompCert** — compilatore C verificato in Coq.
- **seL4** — microkernel verificato (Isabelle/HOL).
- **AWS s2n** / **HACL\*** — librerie crittografiche verificate.

## Quando usare cosa

- Proprietà di reachability/temporali su sistemi finiti → model checking.
- Algoritmi/strutture dati → theorem proving.
- Protocolli concorrenti → TLA+, SPIN.
- Codice C critico → Frama-C, CBMC.
