# Ricettario delle Formule (Semplificato)

Questo file contiene le formule principali che devi conoscere per l'esame, spiegate in modo semplice.

---

## 1. Trasformare un numero a caso in un tempo (MATLAB)

Per simulare quando arrivano i clienti (tempi di arrivo) o quanto tempo ci mettono a essere serviti, usiamo questa formula. Trasforma un numero casuale tra 0 e 1 (rand()) in un tempo che segue la distribuzione Esponenziale:

t_a = -1/lambda * ln(rand())

(Dove lambda è la frequenza con cui arrivano i clienti).

---

## 2. Formule per le Code

- Rapporto di Traffico (rho):
  rho = lambda * s
  (Dove lambda è quanto spesso arrivano e s è quanto tempo ci mette il servizio).
  Attenzione: Se rho >= 1, arrivano clienti più velocemente di quanto riesci a servirli, quindi la coda cresce all'infinito.

- Probabilità di avere 1 cliente in coda (Pi_1):
  Pi_1 = [Pi_0 * (1 - K_0)] / K_0
  (Dove Pi_0 è la probabilità che la coda sia vuota e K_0 è la probabilità che non arrivi nessuno durante un servizio).

- Trovare media e varianza della coda:
  In uno stato stabile (stazionario), usiamo queste uguaglianze per trovare i valori medi:
  - Media: E(Q_n^2) = E(Q_{n+1}^2)
  - Varianza: E(Q_n^3) = E(Q_{n+1}^3)

---

## 3. Formule per la Percolazione

- Grandezza del cluster gigante (P1):
  Ci dice quanta parte della griglia è occupata dal cluster più grande:
  P1 = s_max / L^2
  (Dove s_max è il cluster più grande e L^2 è la grandezza totale della griglia).

- RACS (Taglia Media dei Cluster):
  È la media della grandezza di tutti i cluster, senza contare quello più grande (s_max).

  RACS = [somma di s * (s * n_s)] / [somma di (s * n_s)]
  (Nota: la somma al numeratore esclude s_max).

  Vicino alla soglia di percolazione, questa formula "esplode" (il valore diventa altissimo), indicando che i cluster si stanno unendo.
