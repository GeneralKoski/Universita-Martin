# Mappa Concettuale: Modellazione e Simulazioni Numeriche

I pilastri teorici attorno a cui ruota l'intero corso e l'esame finale:

## 1. Probabilità e Statistica di Base

- **Distribuzioni Fondamentali:** Binomiale, Poisson, Gaussiana, Esponenziale.
- **Applicazioni Pratiche:** Estrazioni ripetute (giochi ad urne), tempi di intercorrenza per gli arrivi/servizi.
- **Teoremi Fondanti:** Legge dei Grandi Numeri (convergenza concettuale dei campionati nel limite di $N \to \infty$) e Teorema Limite Centrale (sulle distribuzioni delle medie).

## 2. Processi ed Equazioni di Markov

- **Dinamica:** Sistemi in cui il futuro dipende esclusivamente dallo stato presente.
- **Componenti Matematici:** Matrici di transizione stocastiche, distribuzione asintotica stazionaria.
- **Concetti Avanzati:** Reversibilità, tempo di ritorno, modelli termodinamici semplificati (come il modello di Ehrenfest termodinamico).

## 3. Teoria delle Code (Il primo Progetto)

- **Modellizzazione come Processo di Markov:** Lo stato del sistema corrisponde in ogni momento alla _lunghezza_ della coda.
- **Dinamiche Analizzate:** Coda infinita vs Coda con Sala d'Attesa (limite massimo di posti).
- **Elementi Critici:** Tempi di attesa dell'utente, ricerca della distribuzione p_stazionaria, studio dell'impatto dell'**autocorrelazione** per estrarre la statistica e la varianza in tempi d'estrazione finiti.

## 4. Teoria della Percolazione (Il secondo Progetto)

- **Inquadramento Geometrico:** Modelli per la propagazione di interazioni spaziali (solitamente trattati su un reticolo quadrato $L \times L$).
- **Obiettivo Formale:** Analizzare l'insorgenza (o l'assenza) del cluster infinito basandosi sulla probabilità base di colorazione $p_{col}$ di un singolo sito, localizzando criticamente la "Soglia di Percolazione" $p_c$.
- **Ricerca Algoritmica:** Algoritmi _flood-fill/ricorsivi_ di base (stack) a confronto con i più evoluti algoritmi che non rivisitano il passato (come l'algoritmo di Hoshen-Kopelman).
