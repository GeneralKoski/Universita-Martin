# Riassunto Laboratorio

## Contenuti principali
- Introduzione a Python e Jupyter: script, `import`, `__name__ == "__main__"`, input/output, tipi, casting, operatori e strutture dati di base.
- Uso di `numpy` per lavorare in `R^N`: vettori, `zeros`, `ones`, `linspace`, somma, prodotto per scalare, prodotto scalare e norma euclidea.
- Funzioni `R^N -> R^M`: meshgrid, visualizzazione di superfici, coordinate sferiche, continuita' separata e studio grafico di funzioni in piu' variabili.
- Discesa del gradiente: implementazione numerica, scelta del learning rate, condizioni di arresto, visualizzazione del percorso su superfici e curve di livello.
- Neuroni artificiali, SLP e MLP: pre-attivazione `x·w+b`, funzioni di attivazione, uso di dataset tabellari, limiti della separazione lineare e vantaggio degli strati nascosti.
- Backpropagation da implementare a mano in `07_mlp_vuoto.py`: forward, backward, aggiornamento dei pesi e training mini-batch.
- Visione artificiale di basso livello: conversione RGB -> luminanza, istogrammi, inversione, compressione logaritmica/potenza, contrast stretching, LUT.
- Operatori locali: convoluzione 2D, Sobel, Laplaciano, smoothing con media/Gaussiano, confronto con filtri non lineari come min/max/mediano.
- Convoluzione 1D e PyTorch: classificazione di segnali rumorosi, confronto tra preprocessing con kernel fissi e layer `Conv1d` imparato dalla rete.

## File importanti
- `codice-20260428/`: esercizi incompleti da svolgere.
- `soluzioni-20260428/`: versioni svolte, utili per capire il livello di dettaglio atteso.
- `data-20260428/`: dataset di segnali per il laboratorio sulla convoluzione 1D.
- `img-20260428/`: immagini usate per operatori puntuali e locali.
- I file `.zip` presenti risultano gia' estratti e corrispondono alle cartelle sopra.

## Appunti aggiuntivi
- Qui il filo rosso e': matematica -> implementazione numerica -> rete neurale -> applicazioni su immagini/segnali.
- Conviene saper riscrivere a mano almeno:
  - update della discesa del gradiente;
  - formula della pre-attivazione;
  - pipeline forward/backward di un MLP semplice;
  - formula della convoluzione discreta.
- Nei notebook la parte davvero formativa non e' solo eseguire il codice, ma capire:
  - forma degli array/tensori;
  - significato geometrico del gradiente;
  - differenza tra trasformazioni puntuali e locali;
  - differenza tra feature engineering e feature learning.

## Cosa sapere bene
- Differenza tra SLP e MLP e perche' XOR non e' linearmente separabile.
- Ruolo di loss, gradiente, learning rate e criterio di stop.
- Differenza tra filtro medio, gaussiano, Sobel, Laplaciano, mediano.
- Perche' una `Conv1d` puo' sostituire un preprocessing manuale con kernel fissati.
