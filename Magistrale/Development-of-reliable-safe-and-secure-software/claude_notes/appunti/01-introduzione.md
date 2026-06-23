# 1. Introduzione e definizioni

## Dependability

Capacità di un sistema di erogare un servizio di cui ci si possa giustificatamente fidare. Concetto ombrello (Laprie, Avizienis) che include:

- **Availability** — disponibilità del servizio quando richiesto
- **Reliability** — continuità del servizio corretto
- **Safety** — assenza di conseguenze catastrofiche per utenti e ambiente
- **Confidentiality** — assenza di divulgazione non autorizzata
- **Integrity** — assenza di alterazioni improprie dello stato
- **Maintainability** — capacità di subire modifiche e riparazioni

**Security** = confidentiality + integrity + availability (CIA).

## Catena Fault → Error → Failure

- **Fault** (guasto/difetto): causa adjudicata o ipotizzata di un errore. Es. bug nel codice, componente HW rotto.
- **Error** (errore): parte dello stato del sistema che può portare a un failure. Manifestazione del fault.
- **Failure** (cedimento): evento che si verifica quando il servizio erogato devia dal servizio corretto.

```
Fault --(attivazione)--> Error --(propagazione)--> Failure
```

## Classificazione dei fault

- **Origine**: fisici / sviluppo / interazione
- **Persistenza**: permanenti / transitori
- **Intenzionalità**: malicious (attacchi) / non-malicious (bug)
- **Fase**: design-time / operational

## Mezzi per la dependability

1. **Fault prevention** — evitare l'introduzione di fault (processo, metodologia)
2. **Fault tolerance** — erogare servizio corretto in presenza di fault (ridondanza, recovery)
3. **Fault removal** — ridurre numero/severità dei fault (testing, verifica)
4. **Fault forecasting** — stimare presenza, incidenza e conseguenze (analisi, modelli)

## Reliable vs Safe vs Secure

- **Reliable**: funziona come specificato in condizioni nominali.
- **Safe**: non causa danni anche quando fallisce.
- **Secure**: resiste ad attacchi intenzionali.

Un sistema può essere reliable ma non safe (fa esattamente ciò che la spec richiede, ma la spec è pericolosa) e viceversa.
