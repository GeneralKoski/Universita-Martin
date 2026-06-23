# Cheatsheet — ripasso rapido

## Concetti chiave

| Termine        | Definizione                                              |
|----------------|----------------------------------------------------------|
| Fault          | Causa di un errore (bug, guasto)                         |
| Error          | Stato erroneo del sistema                                |
| Failure        | Servizio devia dalla specifica                           |
| Reliability    | P(funziona correttamente fino a t)                       |
| Availability   | MTTF / (MTTF + MTTR)                                     |
| Safety         | No conseguenze catastrofiche                             |
| Security       | CIA: Confidentiality, Integrity, Availability            |

## Formule reliability

- R(t) = e^(−λt) (esponenziale)
- MTTF = 1/λ
- Serie: R = ∏ Rᵢ
- Parallelo: R = 1 − ∏(1 − Rᵢ)

## Hazard analysis

- **FTA** — top-down, top event → basic events, AND/OR.
- **FMEA** — bottom-up, componente → failure mode → effetto.
- **HAZOP** — guide words su parametri.

## SIL (IEC 61508)

| SIL | PFD low demand     |
|-----|--------------------|
| 1   | 10⁻² – 10⁻¹        |
| 2   | 10⁻³ – 10⁻²        |
| 3   | 10⁻⁴ – 10⁻³        |
| 4   | 10⁻⁵ – 10⁻⁴        |

## Coverage criteria

statement ⊂ branch ⊂ MC/DC ⊂ path

## STRIDE

Spoofing, Tampering, Repudiation, Information disclosure, DoS, Elevation of privilege.

## OWASP Top 10 (2021)

1. Broken Access Control
2. Cryptographic Failures
3. Injection
4. Insecure Design
5. Security Misconfiguration
6. Vulnerable Components
7. Auth Failures
8. Software/Data Integrity
9. Logging Failures
10. SSRF

## Saltzer & Schroeder

Economy, fail-safe defaults, complete mediation, open design, separation of privilege, least privilege, least common mechanism, psychological acceptability.

## Crypto cosa usare

- Cifratura simmetrica → **AES-GCM** o **ChaCha20-Poly1305**
- Hash → **SHA-256** o superiore
- Password → **Argon2id**
- Firma → **Ed25519** o **ECDSA P-256**
- Random → **CSPRNG** (`random_bytes`, `/dev/urandom`)

## Hoare logic

{P} S {Q} — total correctness richiede anche terminazione.

While: trovare invariante I tale che {I ∧ B} S {I}.

## Logiche temporali

- LTL: X (next), F (eventually), G (always), U (until).
- CTL: aggiunge A (∀ path), E (∃ path).
- Safety: G ¬bad. Liveness: F good.

## Sound vs complete

- **Sound** = nessun falso negativo (se dice ok, è ok)
- **Complete** = nessun falso positivo (se trova bug, è vero)
- Per Rice: non si può avere entrambe per proprietà non banali.

## Standard safety per dominio

| Dominio       | Standard       | Livelli      |
|---------------|----------------|--------------|
| Generale      | IEC 61508      | SIL 1–4      |
| Automotive    | ISO 26262      | ASIL A–D     |
| Avionica      | DO-178C        | DAL A–E      |
| Medicale      | IEC 62304      | A/B/C        |
| Ferroviario   | EN 50128       | SIL 1–4      |
