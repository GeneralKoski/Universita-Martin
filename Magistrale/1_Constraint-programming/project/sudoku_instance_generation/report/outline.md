# Struttura del Report

## 1. Introduzione

- Obiettivo del progetto
- Requisiti principali
- Perché il problema è interessante in CP

## 2. Modellazione del Sudoku

- Variabili
- Domini
- Vincoli di riga, colonna e blocco
- Uso di `alldifferent`

## 3. Controllo di Unicità

- Strategia solve-and-block
- Strategia di conteggio delle soluzioni
- Gestione dei timeout

## 4. Generazione dei Puzzle

- Sorgente delle griglie complete
- Strategia di rimozione degli indizi
- Criterio di accettazione o rollback

## 5. Architettura della Pipeline

- Ruolo di MiniZinc
- Ruolo dello script di orchestrazione
- Formati dei dati

## 6. Esperimenti

- Setup sperimentale
- Timeout
- Confronto tra strategie
- Analisi tempo vs numero di indizi

## 7. Conclusioni

- Risultati principali
- Limiti
- Possibili estensioni
