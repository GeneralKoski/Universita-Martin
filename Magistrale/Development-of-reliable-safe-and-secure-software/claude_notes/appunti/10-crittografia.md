# 10. Crittografia applicata

Obiettivi: confidentiality, integrity, authentication, non-repudiation.

## Tipologie

- **Simmetrica** - stessa chiave per cifrare e decifrare.
- **Asimmetrica** (a chiave pubblica) - coppia di chiavi (public, private).
- **Hashing** - funzione one-way, no chiave.
- **MAC / HMAC** - autenticazione con chiave simmetrica.
- **Firma digitale** - autenticazione + non-repudiation con chiave asimmetrica.

## Crittografia simmetrica

- **Block cipher**: AES (128/192/256 bit), 3DES (deprecato), ChaCha20 (stream-like).
- **Modi di operazione**:
  - **ECB** - insicuro (pattern visibili).
  - **CBC** - richiede IV unico, vulnerabile a padding oracle se non autenticato.
  - **CTR** - converte block in stream, parallelizzabile.
  - **GCM**, **CCM** - **AEAD** (Authenticated Encryption with Associated Data): cifratura + integrità in un colpo. **Preferiti**.

Regola: usare **AES-GCM** o **ChaCha20-Poly1305**.

## Crittografia asimmetrica

- **RSA** - basato su fattorizzazione di interi grandi. Chiavi ≥ 2048 bit (3072 raccomandato).
- **ECC** (Elliptic Curve) - chiavi più corte a parità di sicurezza (256 bit ECC ≈ 3072 bit RSA). Curve: P-256, P-384, Curve25519.
- **DH / ECDH** - key exchange.
- **Post-quantum**: Kyber (KEM), Dilithium (signature), standardizzati NIST 2024.

Uso tipico: cifrare una **session key** simmetrica (key encapsulation), poi simmetrica per il bulk.

## Funzioni di hash

Proprietà richieste:
- **Pre-image resistance** - dato h, difficile trovare m tale che H(m)=h.
- **Second pre-image resistance** - dato m, difficile trovare m' ≠ m con H(m)=H(m').
- **Collision resistance** - difficile trovare m, m' con H(m)=H(m').

Stato:
- **MD5, SHA-1** - rotti (collisioni pratiche). Non usare per security.
- **SHA-2** (SHA-256, SHA-512) - sicuri.
- **SHA-3** - Keccak, alternativa strutturalmente diversa.
- **BLAKE2/3** - veloci e sicuri.

## Password hashing

Hash classici sono **troppo veloci** per le password. Usare KDF lente con salt:

- **bcrypt** - costo configurabile.
- **scrypt** - memory-hard.
- **Argon2id** - vincitore PHC 2015, raccomandato. Memory-hard, resistente a GPU/ASIC.
- **PBKDF2** - accettabile se molte iterazioni (≥ 600k SHA-256, OWASP 2023).

Mai usare MD5/SHA-1/SHA-256 plain per le password.

## MAC e firma

- **HMAC-SHA256** - MAC con chiave simmetrica, integrità + autenticazione.
- **Firma digitale** (RSA-PSS, ECDSA, EdDSA): integrità + autenticazione + non-repudiation.
- **Ed25519**: firma EdDSA su Curve25519, deterministica, veloce, raccomandata.

## TLS

Protocollo standard per canale cifrato. Versioni: **TLS 1.3** (raccomandato), TLS 1.2 ok. TLS ≤ 1.1 deprecato.

### Handshake TLS 1.3 (semplificato)

1. Client → ServerHello con `key_share` (ECDHE).
2. Server → ServerHello, certificate, signature, finished.
3. Derivazione delle chiavi con HKDF.
4. Application data cifrate con AEAD.

Forward secrecy garantita da ECDHE: compromettere la chiave privata del server non decifra sessioni passate.

### PKI

- **Certificate** X.509: lega public key a identità, firmato da CA.
- **Chain of trust**: client → intermediate → root CA (trust store).
- **Revocation**: CRL (deprecato), OCSP, OCSP stapling.
- **Certificate Transparency** logs.

## Errori comuni

- Implementare crypto custom.
- Riusare IV/nonce con stream cipher o GCM.
- ECB.
- Hash plain per password.
- Confronto di MAC con `==` (timing attack) → usare `hash_equals`/`constant_time_compare`.
- Random non crittografico (`rand()`) per chiavi/token → usare CSPRNG (`/dev/urandom`, `random_bytes`, `crypto.randomBytes`).
- Hardcoded keys nel codice/repo.

## Dimensioni raccomandate (2025)

| Algoritmo     | Dimensione     |
|---------------|----------------|
| AES           | 256 bit        |
| RSA           | ≥ 3072 bit     |
| ECC           | ≥ 256 bit      |
| Hash          | SHA-256+       |
| HMAC key      | ≥ 256 bit      |
| Password KDF  | Argon2id       |
