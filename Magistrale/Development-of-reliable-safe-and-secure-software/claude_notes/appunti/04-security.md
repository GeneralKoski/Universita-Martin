# 4. Security

## Triade CIA

- **Confidentiality** - solo soggetti autorizzati accedono all'informazione.
- **Integrity** - l'informazione non viene alterata in modo non autorizzato.
- **Availability** - il servizio è disponibile quando richiesto.

Estensioni: **Authenticity**, **Non-repudiation**, **Accountability** (modello Parkerian Hexad aggiunge possesso, utilità).

## AAA

- **Authentication** - verificare l'identità (chi sei).
- **Authorization** - verificare i permessi (cosa puoi fare).
- **Accounting/Auditing** - tracciare le azioni (cosa hai fatto).

## Fattori di autenticazione

1. Qualcosa che **sai** (password, PIN)
2. Qualcosa che **hai** (token, smartcard)
3. Qualcosa che **sei** (biometria)
4. Qualcosa che **fai** (pattern comportamentali)
5. **Dove** sei (geolocalizzazione)

MFA = combinazione di almeno due fattori distinti.

## Modelli di controllo degli accessi

- **DAC** (Discretionary): il proprietario decide (file system Unix).
- **MAC** (Mandatory): policy centrale, etichette di sicurezza (Bell-LaPadula, Biba).
- **RBAC** (Role-Based): permessi associati a ruoli, ruoli agli utenti.
- **ABAC** (Attribute-Based): policy in base ad attributi di soggetto, oggetto, ambiente.

### Bell-LaPadula (confidentiality)

- **No read up**: un soggetto non può leggere oggetti a livello superiore.
- **No write down**: un soggetto non può scrivere a livello inferiore.

### Biba (integrity)

Duale di Bell-LaPadula:
- **No read down**, **No write up**.

## Threat agent / asset / vulnerability

- **Asset**: ciò che ha valore e va protetto (dati, sistemi, reputazione).
- **Threat**: potenziale evento avverso.
- **Threat agent**: chi potrebbe causare la minaccia.
- **Vulnerability**: debolezza sfruttabile.
- **Exploit**: tecnica concreta per sfruttare la vulnerabilità.
- **Attack**: tentativo effettivo di sfruttare.
- **Risk** = Threat × Vulnerability × Impact.

## Principi di Saltzer & Schroeder (1975)

1. **Economy of mechanism** - semplicità.
2. **Fail-safe defaults** - negato di default.
3. **Complete mediation** - controllare ogni accesso.
4. **Open design** - non security through obscurity.
5. **Separation of privilege** - più condizioni per accedere.
6. **Least privilege** - minimi permessi necessari.
7. **Least common mechanism** - minimizzare componenti condivisi.
8. **Psychological acceptability** - usabilità.

Aggiunti più tardi: **defense in depth**, **fail securely**, **don't trust services**, **secure the weakest link**.
