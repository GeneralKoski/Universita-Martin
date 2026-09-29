# 3. Safety

## Definizione

Assenza di conseguenze catastrofiche per utenti, terzi e ambiente. Sistemi safety-critical: avionica, automotive, medicale, ferroviario, nucleare.

## Concetti

- **Hazard**: condizione del sistema che, combinata con condizioni ambientali, può portare ad accidente.
- **Risk** = probabilità × severità del danno.
- **Mishap/Accident**: evento indesiderato con danni.
- **Safety-critical function**: funzione il cui malfunzionamento può causare hazard.

## Hazard Analysis

### FTA - Fault Tree Analysis

Top-down: si parte da un evento indesiderato (top event) e si scompone con porte logiche AND/OR fino ai basic events.

- Utile per individuare **cut set minimi** (combinazioni minime di fault che causano il top event).
- Quantitativa se si associano probabilità ai basic events.

### FMEA - Failure Mode and Effects Analysis

Bottom-up: per ogni componente si elencano i modi di failure, gli effetti locali e globali, le cause.

Tabella tipica: Component | Failure Mode | Cause | Local Effect | System Effect | Severity | Probability | RPN.

**FMECA** = FMEA + Criticality analysis (RPN = Severity × Occurrence × Detection).

### HAZOP

Hazard and Operability Study: usa parole guida (NO, MORE, LESS, REVERSE, AS WELL AS, OTHER THAN) applicate ai parametri di processo.

## SIL - Safety Integrity Level

IEC 61508 definisce 4 livelli (SIL 1–4) in base alla riduzione del rischio richiesta:

| SIL | PFD (low demand)   | PFH (high demand)     |
|-----|--------------------|-----------------------|
| 1   | 10⁻² – 10⁻¹        | 10⁻⁶ – 10⁻⁵           |
| 2   | 10⁻³ – 10⁻²        | 10⁻⁷ – 10⁻⁶           |
| 3   | 10⁻⁴ – 10⁻³        | 10⁻⁸ – 10⁻⁷           |
| 4   | 10⁻⁵ – 10⁻⁴        | 10⁻⁹ – 10⁻⁸           |

Standard derivati:
- **ISO 26262** (automotive, livelli ASIL A–D)
- **DO-178C** (avionica, livelli DAL A–E)
- **IEC 62304** (dispositivi medici)
- **EN 50128** (ferroviario)

## Principi di progettazione safety

- **Fail-safe**: in caso di failure il sistema entra in stato sicuro (es. semaforo che va al rosso lampeggiante).
- **Fail-operational**: il sistema continua a funzionare anche dopo un fault (avionica fly-by-wire).
- **Defense in depth**: più barriere indipendenti.
- **Diversity**: implementazioni eterogenee per evitare common-mode failure.
- **Interlock**: blocchi che impediscono combinazioni pericolose di stati.

## Differenza Safety vs Security

- Safety: sistema → ambiente (proteggere il mondo dal sistema).
- Security: ambiente → sistema (proteggere il sistema dal mondo).
- In sistemi cyber-physical i due concetti convergono: un attacco di security può causare un evento safety-critical.
