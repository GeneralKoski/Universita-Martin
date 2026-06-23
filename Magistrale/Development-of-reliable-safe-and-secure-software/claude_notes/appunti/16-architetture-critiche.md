# 16. Architetture per sistemi critici

## Principi generali

- **Simplicity** — meno componenti, meno failure mode (Saltzer & Schroeder #1).
- **Modularity** — alta coesione, basso accoppiamento.
- **Encapsulation** — nascondere implementazione, esporre interfacce stabili.
- **Defense in depth** — più barriere indipendenti.
- **Diversity** — eterogeneità per evitare common-mode failure.
- **Fail-safe / fail-operational** — comportamento al failure noto e progettato.

## Partitioning

Separazione di componenti a criticità diverse perché un fallimento in uno non si propaghi all'altro.

### Spatial partitioning

- Componente A non può accedere a memoria di B.
- Implementato con MMU/MPU, OS partizionante (ARINC 653 in avionica).

### Temporal partitioning

- A non può consumare CPU oltre la quota assegnata.
- Time-triggered scheduling, budget enforcement.

### Esempi

- **ARINC 653** (avionica) — Integrated Modular Avionics: più funzioni di criticità diverse su stesso HW, partitioning rigoroso.
- **AUTOSAR Adaptive** (automotive) — partitioning per applicazioni a livelli ASIL diversi.

## Ridondanza

### Hardware redundancy

- **Active redundancy** — più unità in parallelo, voter sceglie il risultato (TMR — 2-out-of-3).
- **Passive / standby** — backup attivato al failure (cold/warm/hot standby).
- **Hybrid** — combinazione.

### Software redundancy

- **N-version programming** — N implementazioni indipendenti.
  - Limite: fault correlati (specifica condivisa, errori simili tra team).
- **Recovery blocks** — primario + alternativi + acceptance test.
- **Diversity** — diversi linguaggi, team, toolchain.

### Information redundancy

- **ECC memory** — Error-Correcting Code.
- **CRC** — checksum su messaggi.
- **Replicated data** con consistency check.

### Time redundancy

- Rieseguire l'operazione per fault transitori.
- Utile in soft errors (radiazione cosmica, ecc.).

## Watchdog

Componente che monitora il funzionamento di un altro (heartbeat). Se non riceve segnale entro timeout → reset / shutdown / failover.

Tipi:
- **HW watchdog** — circuito separato, più affidabile.
- **SW watchdog** — task in OS che monitora altri task.

Buona pratica: watchdog **indipendente** da chi monitora (no auto-monitoraggio).

## Architetture safety-oriented

### Simplex

Due controllori:
- **High Performance Controller** (HPC) — algoritmo complesso/ottimizzato, non verificato pienamente.
- **High Assurance Controller** (HAC) — algoritmo semplice ma verificato.

**Decision module** osserva l'output dell'HPC; se viola un envelope di sicurezza → switch a HAC.

Filosofia: usa la complessità solo dove non compromette la safety.

### Triple Modular Redundancy (TMR)

3 unità identiche, voter a maggioranza. Tollera fault singolo. Costo: 3x HW.

Variante: **2-out-of-3** voting con HW diversificato per evitare common-mode.

### Lockstep

Due CPU eseguono in sincrono le stesse istruzioni; un comparator rileva divergenze.

Usato in: automotive (es. Infineon AURIX TriCore), avionica.

### Safety bag / safety monitor

Componente parallelo che monitora il sistema principale e può forzare uno shutdown / failsafe in caso di violazione di proprietà di sicurezza. È un'applicazione del principio "safety kernel".

## Decoupling temporale

In sistemi real-time:
- **Time-triggered** (es. TTEthernet, FlexRay) — comunicazione su slot temporali predefiniti, deterministico.
- **Event-triggered** — più flessibile ma meno prevedibile.
- Sistemi safety-critical preferiscono time-triggered per analizzabilità.

## Anti-pattern

- **Single point of failure** — un componente la cui rottura porta giù tutto.
- **Common-mode failure** — più componenti "ridondanti" che falliscono per la stessa causa (stesso bug, stessa alimentazione, stessa memoria).
- **Cascading failure** — failure in A scatena failure in B che scatena C.
- **Hidden coupling** — dipendenze non documentate (variabili globali, file system condiviso).

## Mixed-criticality systems

Sistemi che ospitano funzioni a criticità diverse (es. infotainment + ADAS in auto).

Sfide:
- **Isolation** — un bug nel componente low-criticality non deve impattare high-criticality.
- **Resource sharing** — CPU, memoria, bus condivisi: serve garantire QoS al critico.
- **Certification** — il sistema completo va certificato al massimo livello, oppure si dimostra l'isolamento.

Approccio: hypervisor partizionante (es. PikeOS, Wind River Helix), ARINC 653 multi-core.

## Trade-off

| Approccio    | Costo | Affidabilità | Determinismo |
|--------------|-------|--------------|--------------|
| Singolo HW + SW verificato          | basso | medio        | alto      |
| TMR identico                        | alto  | alto         | alto      |
| Diversity (HW + SW eterogenei)      | molto alto | molto alto   | medio  |
| Simplex                             | medio | alto         | alto      |
| N-version                           | alto  | medio (correlation) | medio |

Scelta dipende da SIL target, costi accettabili, tipi di fault attesi (random vs systematic).
