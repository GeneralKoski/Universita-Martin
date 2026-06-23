# 8. Secure coding

## OWASP Top 10 (2021)

1. **A01 Broken Access Control** — controlli di autorizzazione mancanti/aggirabili.
2. **A02 Cryptographic Failures** — dati sensibili non protetti, algoritmi obsoleti.
3. **A03 Injection** — SQL, NoSQL, OS command, LDAP.
4. **A04 Insecure Design** — difetti architetturali.
5. **A05 Security Misconfiguration** — default insicuri, header mancanti.
6. **A06 Vulnerable and Outdated Components** — dipendenze con CVE note.
7. **A07 Identification and Authentication Failures** — gestione credenziali debole.
8. **A08 Software and Data Integrity Failures** — supply chain, deserializzazione insicura.
9. **A09 Security Logging and Monitoring Failures**.
10. **A10 Server-Side Request Forgery (SSRF)**.

## Vulnerabilità classiche

### Buffer overflow (C/C++)

Esempio tipico: copia di un input dell'utente in un buffer fisso senza controllo della dimensione → sovrascrittura dello stack.

Mitigazioni: bounds checking (strncpy, snprintf), stack canaries, ASLR, DEP/NX, linguaggi memory-safe (Rust, Go).

### Integer overflow

Moltiplicare due interi senza controllo può causare wrap-around e portare ad allocare un buffer più piccolo del previsto, da cui out-of-bounds write successivo.

Mitigazione: controlli espliciti, builtin `__builtin_*_overflow` di GCC/Clang.

### Format string

Passare input dell'utente come format string (es. `printf(user_input)`) permette all'attaccante di leggere/scrivere memoria con `%s`, `%n`.

Mitigazione: passare sempre un format costante (`printf("%s", user_input)`).

### SQL Injection

Concatenare input nelle query SQL permette di iniettare clausole arbitrarie (es. `' OR 1=1 --`).

Mitigazione: **prepared statements** con bind parameters.

```php
$stmt = $pdo->prepare("SELECT * FROM users WHERE name = ?");
$stmt->execute([$name]);
```

### XSS (Cross-Site Scripting)

- **Reflected**: input riflesso nella response senza escape.
- **Stored**: payload memorizzato (commenti, profili).
- **DOM-based**: manipolazione del DOM lato client.

Mitigazione: escape contestuale (HTML, attribute, JS, URL), CSP, framework che fanno escape automatico.

### CSRF (Cross-Site Request Forgery)

Sito malevolo induce il browser della vittima a fare richieste autenticate al sito target.

Mitigazione: CSRF token, SameSite cookie, controllo Origin/Referer.

### Command injection

Interpolare input dell'utente dentro un comando shell consente di iniettare separatori e comandi aggiuntivi.

Mitigazione: API che separano comando e argomenti senza shell (`subprocess.run([...], shell=False)`), whitelist, escape.

### Path traversal

Concatenare input dell'utente in un path consente sequenze `../` per uscire dalla directory consentita.

Mitigazione: normalizzazione, controllo che il path risolto sia dentro la directory consentita.

### Deserializzazione insicura

Deserializzare oggetti non fidati può portare a RCE in linguaggi con serializzatori che istanziano classi arbitrarie (es. `unserialize` in PHP, ObjectInputStream in Java, alcuni serializzatori binari di Python).

Mitigazione: usare formati dati senza esecuzione di codice (JSON), firmare i payload, sandbox.

### SSRF

Server fa richieste a URL controllati dall'attaccante (servizi interni, metadata cloud su 169.254.169.254).

Mitigazione: whitelist di URL/IP, blocco di IP privati e link-local.

### Race conditions / TOCTOU

Tra il momento del check (es. controllo permessi su un path) e il momento dell'uso (apertura del file), un attaccante può cambiare il target tramite link simbolici.

Mitigazione: usare file descriptor invece di path, lock, operazioni atomiche.

## Principi di secure coding

- **Validate input** (whitelist > blacklist).
- **Encode output** in base al contesto.
- **Prepared statements** sempre.
- **Least privilege** per processi e DB user.
- **Fail securely** (default deny).
- **Don't roll your own crypto**.
- **Keep dependencies updated**.
- **Secrets** fuori dal codice (env var, secret manager).
- **Logging** senza dati sensibili.

## Memory safety

Linguaggi memory-safe (Rust, Go, Java, C#, Python) eliminano per costruzione molte classi di bug C/C++. Microsoft e Google riportano che ~70% delle CVE sono memory-safety bug.

## SAST / DAST / IAST

- **SAST** (Static): analizza il codice sorgente.
- **DAST** (Dynamic): testa l'applicazione runtime (web scanner).
- **IAST** (Interactive): agente runtime che combina i due.
- **SCA** (Software Composition Analysis): vulnerabilità nelle dipendenze.
