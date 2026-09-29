# Apprendimento supervisionato: classificazione

Fonte: `Introduzione alla classificazione.pdf`

## Esempio giocattolo: classificare il genere
- Problema: distinguere esseri umani di sesso maschile e femminile
- In una **società nudista** è banale: basta osservare le caratteristiche sessuali primarie
- **Feature**: aspetto **direttamente osservabile** di un fenomeno di cui si registra una misura:
  - **quantitativa** (valore numerico intero o double)
  - **categoriale** (vero/falso, dolce/salato, festivo/feriale, rosso/verde/giallo, ...)
- Feature possibili: presenza/assenza di seni sviluppati, organi maschili, peluria; ma anche altezza, peso, proporzioni. Se bastano feature semplici, non serve usare quelle complesse da osservare e misurare
- Il classificatore, osservando le feature, **etichetta** (to label) il dato con una categoria più astratta e generale: le **etichette** (o **classi**, popolazioni, gruppi), qui "genere maschile" e "genere femminile"
- La **classe** è un concetto astratto che "spiega" le osservazioni: l'assegnazione a una classe è la **sintesi delle osservazioni**
- Caso realistico (società occidentale): si decide il genere di un passante da feature manifeste (altezza, massa apparente, capelli, abiti, peluria, movimento, timbro vocale), in modo quasi inconscio
- Un uomo con capelli molto lunghi o una donna rasata mettono in crisi l'algoritmo: sono **outlier statistici**

## Definizione formale
Collezione di dati = insieme $P$ di $M$-uple:

$$m_i = (x_{1i}, \dots, x_{Mi}) \in D_1 \times \dots \times D_M$$

- Ogni **feature** $x_{ji}$ appartiene a un **dominio di valori** $D_j$ (insieme numerico o di categorie)
- $P$ è **partizionato** in $k$ classi con etichette $L = (A_1, \dots, A_k)$
- Ogni dato appartiene a **una e una sola classe** (una e una sola etichetta)

**Algoritmo di classificazione**: funzione **computabile** $f : P \mapsto L$

$$f(m \in P) = f(x_1, \dots, x_m) \in L$$

che assegna a ogni dato $m$ un'etichetta $A_i \in L$ cercando di **stimare l'etichetta reale** del dato. (Nella slide gli argomenti sono scritti $x_1, \dots, x_m$ con $m$ minuscola; dalla definizione precedente dovrebbero essere le $M$ feature.)

- **Hit** (successo): $f(m)$ coincide con l'etichetta reale di $m$
- **Miss** (fallimento): $f(m)$ assegna l'etichetta errata
- Uno schema **error free** in generale è impossibile: per ogni schema servono **stime del tasso di hit/miss** (matematiche o sperimentali)
- Il livello di errore tollerabile dipende dalla **criticità dell'applicazione** (soglie indicative):
  - applicazioni **industriali**: errore < **5%**
  - applicazioni **mediche**: errore > **0,5%** inaccettabile

## Esempi di problemi di classificazione
- **Salmoni e sea bass**: attributi lunghezza e colore; tabella con peso in grammi, lunghezza, colore dominante (feature qualitativa da un insieme finito, es. [BLU, AZZURRO, GRIGIO, VERDE]) e ultima colonna "specie" da riempire, senza confondere troppi salmoni (pregiati) con sea bass (meno pregiati)
- **Studenti e carriera**: feature = dati anagrafici, censo della famiglia, voti; classe da predire = reddito dieci anni dopo la laurea (basso/medio/alto). Classificare è a volte una forma di **predizione**. Sul singolo la predizione vale poco (troppi fattori, modello non maneggevole), ma è importante per il futuro **statistico (in aggregato)** della popolazione
- **Iris di Fisher** (1916): 150 iris, 50 per specie (setosa, virginica e "speciosa" secondo il testo; le figure riportano invece **versicolor**, che è la specie effettiva del dataset); 4 feature quantitative (lunghezza e larghezza di petalo e sepalo) più la specie. Domande di Fisher:
  - si può assegnare la specie conoscendo **solo le 4 misure**, senza sapere nulla della pianta?
  - servono **tutte e 4** le misure?
  - le misure sono **indipendenti** (petalo grande implica spesso sepalo grande)?
  - Figura: **scatterplot matrix** delle 4 feature a coppie (rosso = setosa, verde = versicolor, blu = virginica); setosa è ben separata, versicolor e virginica si sovrappongono in parte
  - Dataset piccolo (150 record), gestibile anche a mano: inadeguato per validare schemi complessi, ma di grande valore **didattico**. Fisher lo usò per dare evidenza ad alcune sue idee matematiche
- **Passeggeri del Titanic**: 1046 record con classe di imbarco (1, 2, 3), sesso (m=0, f=1), età; da predire la **sopravvivenza** (morto=0, salvato=1). Figura: albero di decisione

```
is sex male?
├─ yes → is age > 9.5?
│        ├─ yes → died      (0.17, 61%)
│        └─ no  → is sibsp > 2.5?
│                 ├─ yes → died      (0.05, 2%)
│                 └─ no  → survived  (0.89, 2%)
└─ no  → survived           (0.73, 36%)
```
(Le slide non spiegano i due numeri sotto le foglie né `sibsp`; per convenzione di questi grafici sono la probabilità di sopravvivenza e la percentuale di passeggeri nella foglia, `sibsp` = numero di fratelli/coniugi a bordo. Le etichette yes/no compaiono solo sulla radice: che il ramo sinistro sia "yes" anche sotto è la lettura consueta.)

## Feature e classe
- In generale la **classe è la causa delle feature** (se un fiore è setosa, sepali e petali rispettano certe proporzioni)
- Classificare = **cercare evidenza di cause nascoste** per fenomeni osservati; ma la classe è solo un attributo assegnato al record
- In teoria **ogni feature non nota può fare da classe**: es. predire la lunghezza del petalo dalle altre informazioni (larghezza petalo, lunghezza e larghezza sepalo, specie)
- Per fenomeni complessi le relazioni causa-effetto non sono chiare: conviene studiare come un attributo varia rispetto agli altri
- **Correlation does not imply causation**: il tempo caldo e soleggiato causa sia il consumo di gelati sia le scottature; gelati e scottature sono correlati ma nessuno causa l'altro

## Costruire un classificatore
- La classificazione basata su **osservazione di dati** è ideale per un computer: esamina enormi quantità di record ed estrae **regolarità**
- Tutti i metodi seguono uno **schema generale**:

```
Example Labeled Data --(Training Dataset)--> Learning Algorithm
                                                   | creates
                                                   v
Online Unlabeled Data --(Data to Predict)--> Model --(Predicted Data)--> Labeled Data
```

## Apprendere dagli esempi
- Molte procedure di decisione/classificazione umane derivano da una fase di **apprendimento (training)**, soprattutto nella fase iniziale della vita; lo stesso vale per altri animali
- Esempio del topino: se la mattonella rossa dà una sensazione sgradevole, apprende la regola "rosso implica dolore" e classifica le celle del labirinto come "sicure" o "pericolose"
- La classificazione automatica simula il training: da un insieme **ben classificato** si deducono **regole** applicabili a record **non ancora classificati** o futuri
- **Universo delle osservazioni**: insieme complessivo dei record di un fenomeno (già osservati e classificati, osservati da classificare, futuri)
- **Training Set (TS)**: sottoinsieme **già classificato** dell'universo, da cui si ricavano le regole
- Le regole possono essere **statistiche, probabilistiche, fuzzy, funzioni discriminanti**, ecc.

## Proprietà di un classificatore
Un buon insieme di regole deve avere:
- **Semplicità**: né troppo grande né troppo complicato (la classificazione futura può avere vincoli di efficienza o **costo computazionale** per record)
- **Correttezza sul TS**: **statisticamente corretto** sul TS da cui è stato creato, cioè il tasso di miss non supera soglie di tolleranza dipendenti dalla criticità dell'applicazione
- **Generalizzabilità**: statisticamente corretto anche sul **resto dell'universo** delle osservazioni (proprietà di **generalizzazione**)

## Il problema dell'overfitting
**Correttezza e generalizzabilità sono spesso in conflitto**: questo apparente paradosso è l'**overfitting**.

Esempio: pesci con dimensione e tono medio di grigio; nei grafici asse y = **width** (circa 14-22), asse x = **lightness** (0-10). Il testo parla di "lunghezza" ma l'asse è etichettato width, etichettati da un pescatore esperto (TS). Salmoni (neri) a sinistra, sea bass (rossi) a destra.
1. **Retta** di separazione: regola semplice e immediata, abbastanza corretta, ma lascia errori (salmoni nella zona sea bass e viceversa)
2. **Frontiera frastagliata** che separa quasi perfettamente il TS: più corretta ma **non preferibile**, per due motivi:
   - è più complicata
   - (più importante) si **adatta** al TS, che è un **campione piccolo e casuale** dell'universo: nuovi salmoni cadranno nelle "penisole" della zona sea bass e viceversa. Spiega "troppo bene" il TS e **non generalizza**
3. Soluzione intermedia: una **conica (iperbole)**, equazione di secondo grado invece che di primo: regola un po' più complessa, **meno errori** e migliori prospettive di generalizzazione

## Validazione
- Per convalidare la generalizzazione si usa, oltre al TS, un altro insieme già etichettato: **insieme di controllo** o di **verifica** (**Control Set** o **Test Set**, **CS**)
- Schema: Training set → "train and tune your model"; Test set → "evaluate the model's performance"
- Il CS **non si usa nella sintesi delle regole**, solo dopo che sono state definite sul TS
- Se le regole hanno sul CS lo **stesso tasso d'errore** che sul TS, sono **generalizzabili**
- Esistono molte strategie e varianti

## Quali e quante feature?
- Domande: le feature sono tutte utili, sovrabbondanti o dannose? Alcune sono più importanti? Combinare più feature conviene sempre?
- **Non esiste una risposta valida per tutti i casi**
- Esempio: istogrammi di salmoni e sea bass sulle singole feature
  - **lunghezza** (length) con soglia $l^*$: le due distribuzioni si **sovrappongono molto**
  - **luminosità** (lightness) con soglia $x^*$: separazione **molto migliore**, sovrapposizione ridotta
  - Una singola feature con soglia separa male o parzialmente; da qui l'utilità (non garantita) di combinarle

## Il rumore e le eccezioni
- Nel mondo reale non si controllano tutti i fattori sperimentali: il **rumore** complica la ricerca delle regole
- Rumore = serie di **perturbazioni** dei dati dovute a fenomeni non controllabili o non noti. Un salmone "ideale" starebbe sempre dal lato giusto della frontiera
- Cause dello "spostamento" di un salmone nella regione sea bass:
  - **endogene** al fenomeno: il pesce ha avuto dieta o storia diversa e somiglia di più a un sea bass; cause varie, non note, impredicibili
  - **esogene**, dovute all'**osservatore**: strumento starato (**errore sistematico**), etichettatore distratto
- **Outlier** ("fuori livello"): dato molto fuori norma rispetto ai valori tipici della classe; nel TS può rendere inefficace l'apprendimento. Alcuni algoritmi ne riducono l'influenza, altri ne sono molto sensibili
- Ogni algoritmo su dati reali deve essere **robusto alle perturbazioni**
- Il rumore è **amplificato da troppe feature**, soprattutto se **irrilevanti** (figura: caco, "cacomela", mela)

## Contare gli errori
- Stima grezza con un CS: **percentuale di record classificati male**. Rilevante ma **non completamente descrittiva**
- **Non tutti gli errori sono uguali**: i costi degli errori **non sono uniformi / non sono simmetrici**
  - salmone scambiato per sea bass: perdita economica; sea bass nella scatoletta di salmone: il cliente può chiudere un occhio
  - diagnosi medica: sano classificato malato → un secondo controllo lo scopre (solo paura immotivata); **malato classificato sano** → ritardo di diagnosi, errore gravissimo

### Matrice di confusione
- Griglia **quadrata**: secondo il testo della slide, sulle **righe** la classe reale, e riporta (in percentuale) a quali classi sono stati assegnati gli elementi di quella classe
- Esempio della figura (valori assoluti, righe = **Predicted**, colonne = **Real**):

| | Real: calcio | Real: basket |
|---|---|---|
| **Predicted: calcio** | 1 | 2 |
| **Predicted: basket** | 0 | 7 |

- Classificatore **perfetto** → matrice di confusione = **matrice identità**; un buon classificatore non ha percentuali eccessive **fuori dalla diagonale principale**. Figura 3×3 (true × predicted: basket, calcio, football americano) con la sola diagonale verde
- Non basta stimare l'errore su **un unico CS** (è un campione casuale): ripetere con **CS diversi** dà una stima più precisa
- Buoni TS e CS sono spesso costosi o impossibili da ottenere → **strategie di randomizzazione con ripetizione** nella selezione di TS e CS dall'universo

## Fasi di un sistema di classificazione automatica
1. **Sensing** (o **sampling**): raccolta dei dati dal mondo fisico e traduzione in informazioni digitali
2. **Segmentazione**: partizione in unità significative, eliminazione dei particolari irrilevanti, miglioramento della qualità, isolamento delle informazioni che generano un "data item"
3. **Estrazione delle feature**: misure quantitative o qualitative per ogni caratteristica (le colonne della tabella). Le feature sono molto variabili: sceglierle **INVARIANTI alle trasformazioni** tipiche della situazione sperimentale
   - es. pesci fotografati su nastro alla luce naturale: la **luminanza** non è invariante all'illuminazione (esiti diversi sera/mattina, sole/nuvole); il **peso** sì, quindi è più affidabile
   - deve esserci una probabile **relazione tra classi e feature**: classificare la carriera di uno studente sul "colore degli occhi" non ha senso
4. **Classificazione**: esecuzione dell'algoritmo di assegnazione delle label
5. **Post-processing**: valutazione della qualità della classificazione e dei **costi dell'errore**
6. **Decisione**: uso del classificatore per risolvere un problema reale

## Ciclo di costruzione di un sistema di classificazione
Il designer lavora **per cicli** (prototipo → valutazione → riprogettazione). In ogni ciclo, in ordine:
1. **Raccolta dati**: scelta dei dati per allenare e conoscenza dei dati su cui il classificatore dovrà generalizzare
2. **Selezione delle feature**: troppo poche? troppe? tutte rilevanti? si possono ottenere feature più significative **combinando matematicamente** quelle osservate?
3. **Scelta del modello matematico**: ipotesi su come le feature interagiscono tra loro e con l'esito, e su come si **distribuiscono statisticamente**; molto legato al punto 2
4. **Training**: su osservazioni ben comprese e ben classificate si "accorda" l'algoritmo per minimizzare errori (e costi)
5. **Valutazione**: il problema è risolto o si poteva fare meglio? Lo dice solo un esperimento su un **dataset di valutazione**

## Da ricordare per lo scritto
- Definizione: dati $m_i = (x_{1i}, \dots, x_{Mi}) \in D_1 \times \dots \times D_M$, $P$ partizionato in $k$ classi $L = (A_1, \dots, A_k)$, ogni dato in **una sola** classe; classificatore = funzione **computabile** $f: P \mapsto L$ che **stima** l'etichetta reale
- **Hit/miss**; error free impossibile; soglie indicative: industria < 5%, medicina > 0,5% inaccettabile
- Feature **quantitative** vs **categoriali**; la classe è vista come **causa** delle feature, ma correlazione non implica causalità
- Tre proprietà di un buon classificatore: **semplicità**, **correttezza sul TS**, **generalizzabilità**; correttezza e generalizzabilità sono in conflitto → **overfitting**
- Esempio salmoni/sea bass: retta (semplice, qualche errore) vs frontiera frastagliata (overfitting sul TS piccolo e casuale) vs iperbole (compromesso)
- **Training Set** per costruire le regole, **Control/Test Set** mai usato nella sintesi; regole generalizzabili se l'errore sul CS è uguale a quello sul TS; ripetere con più CS e usare randomizzazione con ripetizione
- Rumore: cause **endogene** vs **esogene** (osservatore, errore sistematico); **outlier**; algoritmi **robusti**; troppe feature irrilevanti amplificano il rumore
- Costi degli errori **non simmetrici** (falso sano in medicina gravissimo) → **matrice di confusione**: perfetta = identità, fuori diagonale = errori
- Feature buone: **invarianti** alle trasformazioni sperimentali (peso sì, luminanza no) e **correlate** alla classe
- Fasi: sensing → segmentazione → estrazione feature → classificazione → post-processing → decisione. Ciclo di progetto: raccolta dati → selezione feature → modello → training → valutazione
