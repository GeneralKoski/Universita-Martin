# TODO — Esame Fondamenti IA

Stato aggiornato al 2026-05-04. Esame: progetto + scritto da 3 domande
(Prof.ssa E. Iotti, UniPR). Studente lavoratore, no orale.
Date scritto: 16/30 giugno, 14 luglio, 1/15 settembre 2026.

---

## 1. Progetto — Canny Edge Detector

Concordato implicitamente (è il progetto VA 2 da `progetti.pdf`).
Codice e figure pronti in `Progetto_Canny/`.

- [ ] Compilare `Progetto_Canny/report/report.tex` su Overleaf → PDF
- [ ] Verificare che il report stia in **1 pagina** (max consentito per lavoratori)
- [ ] (opzionale) Aggiungere confronto con `cv2.Canny` per validazione qualitativa
- [ ] (opzionale) Testare su una terza immagine più rumorosa per discutere i limiti

## 2. Scritto — 3 domande dettagliate

**La parte più importante secondo la prof.** Programma in `Esame_-_progetto_report_domande/progetti.pdf`.

### Materiali da recuperare/aspettare
- [ ] Aprire `domande.docx` per capire lo stile delle domande di esempio
- [ ] Aspettare gli **esempi di risposte** che la prof pubblicherà su Elly (~14 maggio)
- [ ] Recuperare le **videoregistrazioni** delle lezioni dal gruppo Teams del corso

### Mappatura programma → lezioni (da completare)
Per ogni macro-area, verificare cosa c'è già nel repo e cosa va recuperato:

- [ ] **Funzioni in più variabili** (Lezioni 1–?)
  - Spazi metrici, norme, gradiente, derivate parziali, Schwartz
  - Discesa del gradiente
- [ ] **Reti Neurali Artificiali** (Lezioni ?–?)
  - Percettrone, SLP, MLP
  - Loss L1/L2, MSE, chain rule
  - Funzioni di attivazione (Heaviside, sigmoide, ReLU, softplus, tanh)
  - Backpropagation, SGD
  - MLP su MNIST, teorema di approssimazione universale
- [ ] **Visione Artificiale** (Lezioni ?–?) — **coperta in parte dal progetto**
  - Digitalizzazione, spazi colore, tensori
  - Operatori puntuali/locali/globali, istogramma
  - Filtri sharpening (Sobel, Laplaciano), smoothing (media, gaussiano)
  - Polinomi di Taylor multivariati
- [ ] **Integrazione + Convoluzione**
  - Integrale in più variabili, cambio di variabile
  - Convoluzione e cross-correlazione (1D e 2D), proprietà
- [ ] **Deep Learning** (Lezione 8 + ?)
  - CNN: layer convolutivi, pooling, dropout, backprop su CNN
  - RNN, variabili latenti, likelihood
  - NLP/LM, cross-entropy, softmax
  - GAN, (Diffusion, RL — solo cenni)

### Riassunti per lezione
Lezione 8 ha già `RIASSUNTO.md`. Replicare per le altre:

- [ ] `Lezione_1/RIASSUNTO.md`
- [ ] `Lezione_2/RIASSUNTO.md`
- [ ] `Lezione_3/RIASSUNTO.md`
- [ ] `Lezione_4/RIASSUNTO.md`
- [ ] `Lezione_5/RIASSUNTO.md`
- [ ] `Lezione_6/RIASSUNTO.md`
- [ ] `Lezione_7/RIASSUNTO.md`

### Auto-test
- [ ] Provare a rispondere alla domanda di esempio in `domande.docx` come se fossi all'esame, cronometrato
- [ ] Confrontare con la risposta-esempio quando pubblicata

## 3. Logistica

- [ ] Iscrizione su Esse3 a una delle date dello scritto (decidere quale in base alla preparazione)
- [ ] Consegna progetto + report PDF alla prof (modalità da chiarire — probabilmente via mail o caricamento Elly)

---

## Risorse utili
- Libro: *Dive into Deep Learning* — https://d2l.ai/ (cap. 7 CNN, cap. 9–10 RNN)
- Template report: IEEE Conference su Overleaf
- Mail prof: eleonora.iotti@unipr.it
