# 2. Reliability

## Definizione formale

R(t) = P(nessun failure nell'intervallo [0, t])

Probabilità che il sistema funzioni correttamente fino al tempo t.

## Metriche principali

- **MTTF** (Mean Time To Failure): tempo medio al primo cedimento (sistemi non riparabili).
- **MTBF** (Mean Time Between Failures): tempo medio tra cedimenti (sistemi riparabili). MTBF = MTTF + MTTR.
- **MTTR** (Mean Time To Repair): tempo medio di riparazione.
- **Failure rate** λ(t): tasso istantaneo di failure.
- **Availability** A = MTTF / (MTTF + MTTR).

## Distribuzione esponenziale

Caso più comune con failure rate costante λ:

- R(t) = e^(−λt)
- F(t) = 1 − e^(−λt)
- MTTF = 1/λ

## Curva a vasca da bagno (bathtub)

Tre fasi del failure rate hardware:
1. **Infant mortality** — λ decrescente (difetti di produzione)
2. **Useful life** — λ costante (failure casuali)
3. **Wear-out** — λ crescente (usura)

Il software non ha wear-out fisico ma può degradare per software rot, modifiche, dipendenze obsolete.

## Modelli di reliability del software

- **Jelinski-Moranda**: λ proporzionale al numero di bug residui; ogni fix riduce λ.
- **Goel-Okumoto** (NHPP): processo di Poisson non omogeneo, μ(t) = a(1 − e^(−bt)).
- **Musa basic execution time**: usa tempo di CPU invece del tempo calendario.

## Sistemi serie/parallelo

- **Serie** (n componenti, tutti necessari): R = ∏ Rᵢ
- **Parallelo** (ridondanza, basta uno): R = 1 − ∏(1 − Rᵢ)
- **k-out-of-n**: almeno k componenti su n devono funzionare.

## Fault tolerance

- **Hardware redundancy**: TMR (Triple Modular Redundancy) con voter.
- **Software redundancy**: N-version programming, recovery blocks.
- **Information redundancy**: ECC, checksum, parità.
- **Time redundancy**: rieseguire l'operazione (utile per fault transitori).

### Recovery blocks

```
ensure <test di accettazione>
by <primario>
else by <alternativo 1>
else by <alternativo 2>
else error
```

### N-version programming

N implementazioni indipendenti della stessa specifica, voter sceglie il risultato. Problema: i fault correlati (bug nella spec) non sono mascherati.
