# Protocollo Ufficiale dell'Analisi Dati

Studiato analizzando precisamente le dispense e le richieste per la redazione del file finale (Valido per entrambi i Progetti d'Esame).

## 1. Gestione dello Standard Error (SE)

- **Errore su Misurazioni Standard:**
  L'errore associabile su un valor medio estrapolato da misurazioni puramente incorrelate ($N$ variabili identiche indipendenti):
  ```matlab
  Errore = std(dati) / sqrt(length(dati));
  ```
- **L'insidia dell'Autocorrelazione (Fondamentale!):**
  Quando generi la simulazione temporale di una coda e misuri lo stato della coda consecutivamente (stato n+1 fortemente condizionato da stato n), calcolare $N$ dalla formula di cui sopra ti restituirà un **errore falsamente ottimistico**.
  - Devi tener conto del "Tempo Esteso/Integrato di Autocorrelazione" (Tau).
  - Assicurati di usare o mostrare gli algoritmi come `MYautocorr.m` visti a lezione per determinare la VERA valenza e indipendenza dei tuoi frame di osservazione.

## 2. Plottare con Errorbar (Rigore di Output)

Nessun output analitico simulato è considerato tollerabile per la votazione olistica senza un errore associato visivamente.
Occorre implementare grafici tramite `errorbar`:

```matlab
% Plotto l'andamento della percolazione o delle tempistiche
% rispetto alla probabilita' p
plot(p, risultati_analitici, 'r-');           % Grafico atteso
hold on;
errorbar(p, media_simulazioni, errore_sim, 'bo'); % Punti misurati con baffi
```

La lunghezza dei "baffi" visivi sui punti mostrati convaliderà (se la linea teorica ci passa in mezzo) il teorema limite assieme ai limiti d'osservazione.

## 3. Strategia di Campionamento ("Non farti prendere la mano")

Quando stai scansionando una probabilità che definisce una tendenza logistica ($p_{col}$ per individuare una soglia, ad es $P \in [0, 1]$):

1. **Evita la densità dove il caso è lineare o banale:** Eseguire 50 campionamenti tra $p=0.0$ e $p=0.4$ è inutile e computazionalmente dispendioso.
2. **Alta Risoluzione in Transizione:** Aumenta prepotentemente le ripetizioni e la densità dei punti misurati ai ridosso della supposta soglia di percolazione (attorno a $p_{col} \approx 0.59$ in forma bidimensionale, ovvero dove scattano pendenze di rialzo drastiche).
