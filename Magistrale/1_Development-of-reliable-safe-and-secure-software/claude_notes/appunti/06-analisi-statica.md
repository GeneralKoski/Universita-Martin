# 6. Analisi statica

Analisi del codice **senza eseguirlo**. Complementare al testing.

## Tipi

- **Linting** - convenzioni, code smell (ESLint, PHPStan a livello base, pylint).
- **Type checking** - sistemi di tipi (TypeScript, mypy, Psalm).
- **Data-flow analysis** - propagazione di valori/proprietà nel CFG.
- **Control-flow analysis** - costruzione del CFG, dead code, unreachable.
- **Abstract interpretation** - semantica approssimata su domini astratti.
- **Symbolic execution** - analisi con valori simbolici, accumula path conditions.
- **Model checking** - verifica automatica di proprietà su un modello finito.

## Soundness vs completeness

- **Sound**: se l'analisi dice "no bug", allora non c'è bug (nessun falso negativo). Può avere falsi positivi.
- **Complete**: se c'è bug, l'analisi lo trova (nessun falso positivo). Può avere falsi negativi.
- **Rice's theorem**: ogni proprietà semantica non banale è indecidibile → trade-off inevitabile.

Tool sound: Astrée, Frama-C, Infer (parziale).
Tool unsound ma utili: SonarQube, CodeQL, PHPStan, Coverity.

## Abstract interpretation

Cousot & Cousot, 1977. Si lavora su un **dominio astratto** che approssima i valori concreti.

Esempi di domini:
- **Sign**: {⊥, −, 0, +, ⊤}
- **Intervals**: [a, b]
- **Octagons**: vincoli ±x ±y ≤ c
- **Polyhedra**: combinazioni lineari

Ogni operazione concreta ha una controparte astratta che deve essere **sound** (over-approximation).

## Taint analysis

Tracciare il flusso di dati non fidati (**source**) verso operazioni sensibili (**sink**).

- **Source**: input utente, query string, cookie, file esterni.
- **Sink**: query SQL, chiamate al sistema, valutazione di codice dinamica, output HTML.
- **Sanitizer**: funzione che "pulisce" il dato (escape, prepared statements).

Una variabile è **tainted** se deriva da source senza passare per sanitizer. Un sink che riceve un valore tainted è una potenziale vulnerabilità (SQLi, XSS, command injection).

## Symbolic execution

Esplorazione con variabili simboliche. Per ogni branch si forka:
- ramo true: aggiunge condizione c
- ramo false: aggiunge condizione ¬c

Un solver SMT (Z3) verifica la soddisfacibilità delle path conditions e genera input concreti.

Limiti: **path explosion**, loop simbolici, chiamate esterne, vincoli non lineari.

Tool: KLEE, angr, SAGE.

## Tool tipici per linguaggio

- C/C++: Clang Static Analyzer, Coverity, Infer, Astrée.
- Java: SpotBugs, SonarQube, ErrorProne.
- Python: mypy, pylint, bandit (security).
- JS/TS: ESLint, TypeScript, CodeQL.
- PHP: PHPStan, Psalm.
- Multi-linguaggio: Semgrep, CodeQL.
