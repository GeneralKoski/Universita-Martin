# 11. Processi e standard

## Secure Development Lifecycle (SDL)

Microsoft SDL, BSIMM, OWASP SAMM. Idea: integrare la sicurezza in **ogni fase** dello sviluppo, non solo a fine progetto.

Fasi tipiche:

1. **Training** - formazione del team.
2. **Requirements** - requisiti di sicurezza, privacy, compliance.
3. **Design** - threat modeling, attack surface analysis.
4. **Implementation** - secure coding standards, SAST, code review.
5. **Verification** - DAST, fuzzing, penetration testing.
6. **Release** - incident response plan, final security review.
7. **Response** - gestione vulnerabilità post-release, patch.

### Shift-left

Spostare attività di security il più presto possibile: il costo di un bug cresce esponenzialmente con la fase in cui viene scoperto.

## DevSecOps

Integrazione di security nel ciclo CI/CD:
- SAST in pipeline (pre-merge).
- SCA per dipendenze (Dependabot, Snyk).
- Container scanning (Trivy, Grype).
- Secret scanning (gitleaks, trufflehog).
- DAST in staging.
- Policy as code (OPA, Conftest).
- Runtime security (Falco).

## Standard rilevanti

### Generali

- **ISO/IEC 27001** - sistema di gestione della sicurezza delle informazioni (ISMS).
- **ISO/IEC 27002** - controlli di sicurezza.
- **NIST SP 800-53** - controlli per sistemi federali USA.
- **NIST CSF** - Cybersecurity Framework (Identify, Protect, Detect, Respond, Recover).
- **Common Criteria (ISO/IEC 15408)** - valutazione prodotti, livelli **EAL1–EAL7**.

### Safety

- **IEC 61508** - funzionale base, livelli SIL 1–4.
- **ISO 26262** - automotive, ASIL A–D.
- **DO-178C** - software avionico, DAL A–E.
- **IEC 62304** - software dispositivi medici, classi A/B/C.
- **EN 50128** - software ferroviario.
- **IEC 61511** - process industry.

### Privacy/legali

- **GDPR** (UE 2016/679) - protezione dati personali.
- **NIS2** - sicurezza reti e sistemi informativi UE.
- **Cyber Resilience Act** (UE) - requisiti per prodotti con elementi digitali.

## CWE / CVE / CVSS

- **CWE** (Common Weakness Enumeration) - tassonomia di tipi di debolezze (es. CWE-79 XSS).
- **CVE** (Common Vulnerabilities and Exposures) - identificatori univoci di vulnerabilità specifiche.
- **CVSS** - score numerico di severità (vedi cap. 9).
- **NVD** - database NIST che arricchisce CVE con metadati e CVSS.

## Code review

Pratica chiave per qualità e sicurezza. Linee guida:
- PR piccole (< 400 LoC).
- Checklist (input validation, auth, error handling, log, crypto).
- Almeno un reviewer indipendente.
- Tool-assisted: SAST integrato in PR, suggerimenti automatici.

## Maturity models

- **OWASP SAMM** - Software Assurance Maturity Model.
- **BSIMM** - Building Security In Maturity Model (descrittivo, basato su survey).
- **CMMI** - generale per processi software.

## Supply chain security

Crescente importanza dopo SolarWinds, Log4Shell, xz backdoor (2024).

- **SBOM** (Software Bill of Materials) - lista dipendenze (formato SPDX, CycloneDX).
- **SLSA** - framework per integrità della supply chain.
- **Sigstore / cosign** - firma e verifica artefatti.
- **Reproducible builds**.

## Vulnerability management

1. **Discovery** - scanner, bug bounty, disclosure responsabile.
2. **Triage** - CVSS, exploitability, contesto.
3. **Remediation** - patch, mitigation, workaround.
4. **Verification** - retest.
5. **Disclosure** - coordinated (CVD).
