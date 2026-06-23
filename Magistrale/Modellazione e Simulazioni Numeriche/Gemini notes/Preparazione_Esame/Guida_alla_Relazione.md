# Guida Definitiva per la Relazione del Progetto d'Esame

La Redazione Documentale deve essere inviata _rigorosamente ed esplicitamente_ per posta elettronica **entro mezzogiorno del giorno antecedente l'Orale**. Non prendere questa incombenza col contagocce, il professore modulerà e baserà la conversazione partendo dai test su Matlab da voi tracciati qui e su quanto "in ordine" appaiano matematicamente.

## Impaginazione e Punti Chiave da Affrontare

Ciascun capitolo della relazione deve spuntare i seguenti requisiti:

1. **Il Tone-of-Voice Tecnico della Simulazione:**
   Non sminuire né abbozzare i concetti d'introduzione. Assumi che il recensore possa essere chiunque sprovvisto di basi sulla modellazione, perciò spiega fluidamente ed _in modo conciso o chiaro_ cosa stai effettivamente affrontando in simulazione.
   _(E.g., "Il problema delle code per la minimizzazione delle saturazioni tramite processo di markov" -> Breve recap)._

2. **Scritturizzazione dei Codici Sorgente:**
   Verrà specificamente richiesto di incollare ed **illustrare la logica chiave** degli stream di codici (HK implementato per percolazione, oppure Tempi d'Attesa nella coda):
   - Commentali non solo sintatticamente. Aggiungi commenti di modellazione e dimostra l’implementazione matriciale per estrapolare tempi (in loop).

3. **Leggibilità del Concetto (Teoria analitica vs Estrapolazione Sperimentale):**
   Quando argomenti concetti specifici di cui si è trovato base in calcolo algebrico tramite lavagna (v. la stima del tempo teorico d'attesa stazionariato o calcolo dell'autovalore matriciale), devi raffrontare i concetti astratti assieme ai numeri stampati da log sperimentali in simulazione per mostrarne la comparabilità di convergenza. E se c'è "rumore", o difettano, individua e spiega perché (Limite campionamento stocastico, limiti L reticoloc, o errore del Time Autocorrelato).

4. **Regola d'Oro per la Presentazione Visiva (Grafici e Barre):**
   Questo ti vale il completamento netto per punteggio: **nessun Grafico o Plot mostrato su Excel/Matlab non avallato statisticamente viene compreso positivamente**.
   - Ogni Output in andamento tracciato deve disporre delle `ErrorBars`.
   - Tutte le tabelle presentate di corredo alle numeriche per RACS vs p-Colorable o Length Code vs rho dovranno esprimere significati non astratti per entrate tabellari (Scrivi Legend).

5. **Dispersione della Nomenclatura:**
   Mantieni coerenza formale con lo scritto analitico del corso. Ad esempio, non rimescolare l'orientamento teorico usando nomenclature di altre facoltà: Utilizza regolarmente $p_{col}$ per la probabilità percorsi colorati, usa $L$ fisso per reticolo dimensionale base, usa RACS e la formulazione matematica standard come mostrato per $P_{perc}$. La divergenza causa una flessione confusa dell'interazione Orale.

6. **Esame dal Vivo e Pronta Azione (Svolta al Volo):**
   Manteniti reattivo e prepara interfacciamenti diretti al programma durante il Test, per far lanciare simulazioni dinamiche richieste estemporaneamente e mostrare su variata taglia ad es che la Sala d'attesa annulla il fattore di coda infinita ad alte iterazioni o HK mostra efficienza ad ordini ridotti. (Assicurati i Run di controllo corretto fra CercaCluster ed HK e i calcoli $N_{max}$ coda, simulandoli).
