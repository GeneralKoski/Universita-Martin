# 17. MISRA C e coding standard per sistemi critici

## Cos'è MISRA

**MISRA** = Motor Industry Software Reliability Association (UK). Pubblica linee guida per l'uso sicuro di linguaggi in sistemi critici. Le più usate:

- **MISRA C:2012** (e amendment 1, 2, 3, 4) — standard de facto per C in automotive, aerospace, medical.
- **MISRA C:2023** — aggiornamento più recente.
- **MISRA C++:2008** e **MISRA C++:2023**.
- **AUTOSAR C++14** (poi confluito in MISRA C++:2023).

Scopo: ridurre l'uso delle parti **insicure / ambigue / mal definite** di C/C++.

## Perché C è pericoloso

Il linguaggio C ha:
- **Undefined behavior** (UB) — il compilatore può fare qualsiasi cosa (es. signed overflow, dereference di NULL, accesso fuori array).
- **Unspecified behavior** — più comportamenti accettabili, non documentato quale.
- **Implementation-defined** — il compilatore deve documentare la scelta.
- **Locale-specific behavior**.

In MISRA si limitano fortemente i costrutti che portano a questi comportamenti.

## Struttura delle regole MISRA C:2012

Ogni regola ha:
- **Number** — es. Rule 14.4.
- **Category**: *Mandatory*, *Required*, *Advisory*.
- **Decidability**: *Decidable* / *Undecidable* (analizzabile staticamente?).
- **Scope**: *Single Translation Unit* / *System*.
- **Description** + Rationale + Esempi.

Categorie di severità:
- **Mandatory** — non si deroga.
- **Required** — deroga possibile con giustificazione formale (deviation).
- **Advisory** — raccomandazione, deroga libera ma documentata.

## Esempi di regole notevoli

### Tipi e conversioni

- **Rule 10.x** — restrizioni su conversioni implicite tra tipi.
- **Rule 11.x** — restrizioni su conversioni di puntatori.
- **Rule 12.x** — restrizioni su espressioni (precedenze, side effect).

### Control flow

- **Rule 14.4** — il controllo di un `if`, `while`, ecc. deve essere di tipo essenzialmente booleano.
- **Rule 15.5** — una funzione deve avere un singolo punto di uscita (advisory; spesso oggetto di deviation).
- **Rule 15.7** — `if ... else if` deve terminare con `else`.
- **Rule 16.x** — `switch` deve avere `default`, ogni `case` deve terminare con `break` (eccezioni esplicite).

### Memoria e puntatori

- **Rule 18.x** — restrizioni su aritmetica dei puntatori.
- **Rule 21.3** (Required) — niente uso di `malloc`, `calloc`, `realloc`, `free` dalla standard library (memoria dinamica disabilitata in molti sistemi safety-critical).
- **Rule 22.x** — chiusura di risorse, controllo di errori.

### Funzioni di libreria

- **Rule 21.6** — niente `printf`/`scanf` family (hanno UB su input scorretto).
- **Rule 21.7** — niente `atoi`/`atof` (no error reporting).
- **Rule 21.8** — niente `system`, `getenv`, `exit`, `abort`.
- **Rule 21.9** — niente `bsearch`, `qsort`.
- **Rule 21.10** — niente `<time.h>` (eccetto subset).

### Preprocessor

- **Rule 20.x** — restrizioni su macro, `#include`, `#define`.
- Macro con side effect → vietate.

## Deviation process

Quando una regola **Required** non può/deve essere rispettata:

1. **Identificare** la deviazione e dove avviene.
2. **Giustificare** tecnicamente (necessità reale, alternativa peggiore).
3. **Mitigare** (commenti, isolamento, test aggiuntivi).
4. **Approvare** da assessor / quality.
5. **Documentare** in deviation record.

Le deviazioni vanno gestite formalmente, non nascoste.

## Tool di verifica MISRA

- **PRQA / Helix QAC** (Perforce).
- **LDRA**.
- **Polyspace** (MathWorks) + Polyspace Bug Finder.
- **Coverity**.
- **Klocwork**.
- **Astrée**.
- **PVS-Studio**.
- **cppcheck** (open source, copertura parziale).
- **clang-tidy** con check MISRA (parziale).

Nessun tool copre il 100% delle regole; alcune sono **undecidable** e richiedono review manuale.

## Altri coding standard

### CERT C/C++

Da CMU SEI. Focus su **security** (vs MISRA che è primariamente safety). Categorizzato per:
- Rule (must) / Recommendation (should).
- Severity / Likelihood / Remediation cost → Priority.

Esempi: regole su integer overflow, null pointer, race conditions, format string.

CERT e MISRA hanno overlap ma scope diverso. Spesso applicati insieme.

### JSF C++ (Joint Strike Fighter)

Coding standard sviluppato per F-35. Predecessore di AUTOSAR C++. Storicamente importante.

### High Integrity C++ (HIC++)

Coding standard C++ confluito poi in MISRA C++.

### POWER OF TEN (NASA/JPL — Holzmann)

10 regole per software ad altissima integrità:

1. No flow construct complessi (`goto`, `setjmp`, recursion).
2. Tutti i loop devono avere upper bound staticamente determinabile.
3. No allocazione di memoria dinamica dopo l'init.
4. Funzioni < 60 righe (un foglio A4).
5. Almeno 2 assertion per funzione (densità ~2%).
6. Variabili nello scope più ristretto possibile.
7. Controllare il valore di ritorno di **ogni** funzione non-void; controllare validità dei parametri.
8. Uso del preprocessor limitato (header, macro semplici).
9. Uso dei puntatori limitato (no più di un livello di dereferenza, no function pointer).
10. Compilare con tutti i warning attivi e zero warning.

## Strongly typed language

Standard come IEC 61508 raccomandano linguaggi **strongly typed**. C non lo è. Mitigazioni:
- Sottoinsieme MISRA + restrizioni di progetto.
- Linguaggi alternativi: Ada (SPARK Ada), Rust, controlled-OO subset di C++.

### SPARK Ada

Sottoinsieme di Ada con annotazioni per analisi statica e verification formale. Usato in avionica, ferroviario, defence.
Esempi: codice di controllo del traffico aereo (UK NATS iFACTS), automotive ECU.

### Rust

Memory safety by construction (borrow checker). In crescita per safety-critical (es. progetti automotive di Volvo, Renault). MISRA-equivalent in sviluppo (Ferrocene).

## Defensive programming

Pratica raccomandata da IEC 61508 a SIL 2+. Esempi:

- **Input validation** — controllo range, NULL, lunghezze.
- **Assertion** — verifiche di invarianti runtime.
- **Range checks** prima di accessi array.
- **Default safe** in switch (anche se irraggiungibili).
- **Time-out** su operazioni che potrebbero bloccarsi.
- **Diagnostic logging** con livelli.

Trade-off: troppe assertion riducono performance e leggibilità; vanno calibrate.

## Static analysis come parte del coding

In progetti critici l'analisi statica è **integrata nella build** e bloccante:
- Pre-commit hook che esegue check MISRA.
- CI/CD pipeline con gate su violazioni.
- Code review obbligatoria su deviation.

Questo riflette la prescrizione di IEC 61508 (static analysis HR a SIL 2+).

## Riassunto

| Standard      | Lingua  | Focus       | Categoria              |
|---------------|---------|-------------|------------------------|
| MISRA C:2012  | C       | Safety      | Mandatory/Required/Advisory |
| MISRA C++:2023| C++     | Safety      | come sopra             |
| CERT C/C++    | C/C++   | Security    | Rule/Recommendation    |
| JSF C++       | C++     | Safety/Mil  | (legacy)               |
| Power of Ten  | C       | High integrity | 10 regole "hard"    |
| SPARK Ada     | Ada     | Safety + verification | sottoinsieme di linguaggio |
