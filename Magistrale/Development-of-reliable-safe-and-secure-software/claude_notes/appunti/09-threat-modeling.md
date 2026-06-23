# 9. Threat modeling

Processo strutturato per identificare, comunicare e capire le minacce e le mitigazioni nel contesto di un sistema.

## Quattro domande chiave (Shostack)

1. **Cosa stiamo costruendo?** (modello del sistema, DFD)
2. **Cosa può andare storto?** (identificare minacce)
3. **Cosa facciamo a riguardo?** (mitigazioni)
4. **Abbiamo fatto un buon lavoro?** (validazione)

## STRIDE (Microsoft)

Tassonomia di minacce, una per proprietà di sicurezza violata:

| Threat                  | Property violata     | Esempio                                    |
|-------------------------|----------------------|--------------------------------------------|
| **S**poofing            | Authentication       | Fingere un'altra identità                  |
| **T**ampering           | Integrity            | Modificare dati in transito o a riposo     |
| **R**epudiation         | Non-repudiation      | Negare di aver compiuto un'azione          |
| **I**nformation disclosure | Confidentiality   | Esporre dati a chi non dovrebbe vederli    |
| **D**enial of service   | Availability         | Rendere il servizio non disponibile        |
| **E**levation of privilege | Authorization     | Ottenere permessi non concessi             |

## DREAD (scoring, deprecato ma usato)

Ogni rischio si valuta su 5 dimensioni (1–10):
- **D**amage potential
- **R**eproducibility
- **E**xploitability
- **A**ffected users
- **D**iscoverability

Score = media. Criticato per soggettività; oggi si preferisce **CVSS**.

## CVSS (Common Vulnerability Scoring System)

Standard per scoring di vulnerabilità (0–10):
- **Base metrics**: AV (attack vector), AC (complexity), PR (privileges), UI (user interaction), Scope, CIA impact.
- **Temporal metrics**: maturità exploit, livello di fix.
- **Environmental metrics**: contesto specifico.

## PASTA, OCTAVE, Trike

Framework alternativi:
- **PASTA**: Process for Attack Simulation and Threat Analysis (7 stage, business-centric).
- **OCTAVE**: focus organizzativo, asset-centric.
- **Trike**: requirements-driven.

## Attack trees (Schneier)

Albero con goal dell'attaccante alla radice; figli sono sotto-goal collegati con AND/OR. Permette analisi qualitativa (più semplice via?) e quantitativa (costo, probabilità).

```
Goal: leggere email del CEO
├─ OR: comprometti laptop
│   ├─ AND: phishing + malware
│   └─ accesso fisico
├─ OR: comprometti server mail
└─ OR: corrompi sysadmin
```

## DFD (Data Flow Diagram)

Notazione tipica per modellare il sistema in threat modeling:
- **External entity** (rettangolo): utente, sistema esterno.
- **Process** (cerchio): logica.
- **Data store** (due linee parallele): DB, file.
- **Data flow** (freccia): trasferimento di dati.
- **Trust boundary** (linea tratteggiata): dove cambia il livello di fiducia. Le minacce STRIDE si concentrano qui.

## Mitigation strategies

Per ogni minaccia identificata:
1. **Mitigate** — implementare controlli.
2. **Eliminate** — rimuovere la feature/asset.
3. **Transfer** — assicurazione, terze parti.
4. **Accept** — rischio residuo accettabile.

## Quando

Threat modeling è più efficace **early** (design phase) ma va aggiornato a ogni cambio architetturale rilevante. Output tipico: lista di minacce, mitigazioni, requisiti di sicurezza per sviluppo e test.
