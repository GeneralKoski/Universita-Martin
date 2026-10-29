# Lezione 9 - 27/10/2026: cut, findall e modelli interpretabili

Fonte: `cut.pl`, `findall.pl` e `Articolo explainable ML.pdf`, caricati su Elly per la lezione (niente slide). Le risposte dei programmi sono state **eseguite** con SWI-Prolog 10.0.2.

## Il cut `!` - `cut.pl`

```prolog
p(1).
p(5).

a(motivo_1) :- p(X), X>2,writeln(X),!, fail.
a(motivo_2) :- p(X), X<2.
a(motivo_3) :- p(X), X=2,!.

b(X):-a(X).
b(X):-p(X).
```

### Cosa fa il cut
- `!` riesce sempre, ma quando viene attraversato **taglia i punti di scelta** creati dalla chiamata del predicato in cui si trova: le alternative per i goal alla sua sinistra nel body (qui `p(X)`) e le **clausole successive** dello stesso predicato. Nell'albero SLD pota i rami a destra.
- Il taglio è **locale** al predicato: non tocca i punti di scelta del chiamante.

### Le query (verificate)
- `?- a(M).`
  - Clausola 1: `p(1)`, `1 > 2` fallisce; backtracking su `p(5)`, `5 > 2`, stampa `5`, poi `!` e `fail`.
  - Il cut ha già scartato le clausole 2 e 3 di `a`, quindi `fail` fa fallire **tutto** `a(M)`: risposta `false`, dopo aver stampato `5`. Senza il cut avrebbe risposto `M = motivo_2`.
- `?- a(motivo_2).` → `true`. La testa della clausola 1 non unifica (`motivo_1 ≠ motivo_2`), quindi il suo cut non viene mai raggiunto; la clausola 2 riesce con `p(1)`, `1 < 2`.
- `?- a(motivo_3).` → `false`. Non esiste `p(2)`, quindi `X = 2` fallisce prima di arrivare al cut. Un cut che non si raggiunge non ha effetto.
- `?- b(X).` → stampa `5`, poi `X = 1 ; X = 5`. La prima clausola di `b` chiama `a(X)`, che fallisce come sopra; il cut era dentro `a` e non impedisce a `b` di provare la sua seconda clausola, `p(X)`.

### Lo schema `!, fail`
- `cond, !, fail` dice "se `cond` è vera, il predicato **fallisce** senza provare alternative". È il modo di esprimere un'**eccezione** a una regola, ed è come si implementa la **negazione per fallimento**:

```prolog
% (aggiunta) \+ G definita con il cut
not(G) :- call(G), !, fail.
not(_).
```

- (Aggiunta) Cut **verdi** e **rossi**: un cut verde toglie solo rami che non darebbero comunque soluzioni (efficienza, il significato non cambia); un cut rosso cambia le risposte, come in `a/1`, dove senza il cut `a(M)` avrebbe soluzione. Con i cut rossi la lettura logica delle clausole non basta più: conta l'ordine.

## Raccogliere tutte le soluzioni - `findall.pl`

```prolog
p(1).
p(2).
p(a).
p(1).

p(X1) :- p(X), X=2, X1 is X+1.

go :- findall(X, p(X), L),
      writeln_rec(L).

writeln_rec([]).
writeln_rec([H|T]) :- writeln(H), writeln_rec(T).
```

- `findall(Template, Goal, Lista)` trova **tutte** le soluzioni di `Goal` (con il backtracking) e raccoglie le istanze di `Template` in `Lista`, nell'ordine in cui le trova e **con i duplicati**. È uno dei predicati extra-logici di "secondo ordine": parla dell'insieme delle soluzioni, non di una sola.
- `writeln_rec` stampa una lista un elemento per riga, per ricorsione.
- La regola `p(X1) :- p(X), X=2, X1 is X+1` aggiunge `3` (da `p(2)`). Il confronto `X = 2` è **unificazione**: con `X = a` semplicemente fallisce, senza errore aritmetico.

### Il file così com'è non termina (verificato)
- `?- p(X).` dà `1 ; 2 ; a ; 1 ; 3`, poi **va in loop**. Finiti i fatti, la regola chiama di nuovo `p(X)`, che finiti i fatti richiama la regola, e così via: è **ricorsione a sinistra**, come la versione 3 della chiusura transitiva della lezione 5. Ogni livello ritrova solo `3`, che non passa `X = 2`, e scende ancora.
- Quindi `?- go.` **non stampa niente e non termina**: `findall` deve esaurire tutte le soluzioni prima di restituire la lista, e qui non le esaurisce mai.
- Togliendo la regola (verificato), `?- go.` stampa `1`, `2`, `a`, `1`.

### `findall`, `bagof`, `setof` (aggiunta, verificata sui soli fatti)
| Chiamata | Risultato |
|---|---|
| `findall(X, p(X), L)` | `L = [1,2,a,1]` (ordine di ritrovamento, duplicati) |
| `bagof(X, p(X), L)` | `L = [1,2,a,1]` |
| `setof(X, p(X), L)` | `L = [1,2,a]` (ordinata nell'ordine standard dei termini, numeri prima degli atomi, senza duplicati) |
| `findall(X, p(zzz), L)` | `L = []` |
| `bagof(X, p(zzz), L)` | fallisce |

- Differenze: senza soluzioni `findall` dà la lista vuota, `bagof` e `setof` **falliscono**; con variabili libere nel goal che non stanno nel template, `bagof`/`setof` fanno backtracking su di esse (un gruppo di soluzioni per ogni loro valore) a meno di quantificarle con `Var^Goal`, mentre `findall` le tratta come esistenziali.

## L'articolo: Rudin, *Stop explaining black box machine learning models for high stakes decisions and use interpretable models instead*

Cynthia Rudin (Duke University), *Nature Machine Intelligence* 1, 206-215, maggio 2019 (Perspective). Collegato alla lezione 1: il confronto sub-simbolico/simbolico, interpretabile no/sì, black box sì/no.

### La tesi
- Per le decisioni **ad alto rischio** (giustizia penale, sanità, finanza) non bisogna usare modelli **black box** accompagnati da **spiegazioni post hoc** ("explainable ML", un secondo modello che spiega il primo), ma modelli **intrinsecamente interpretabili**, che forniscono spiegazioni **fedeli** a quello che calcolano.
- Black box di due tipi: funzione **troppo complicata** per un essere umano (deep learning) oppure **proprietaria** (segreto commerciale).
- L'interpretabilità dipende dal dominio, non ha una definizione unica: di solito è un **vincolo sulla forma del modello** (sparsità, monotonia, additività, vincoli fisici o causali, ragionamento per casi). Per i dati strutturati la **sparsità** è una buona misura: le persone gestiscono al più 7 ± 2 entità cognitive alla volta.

### Problemi della explainable ML
1. **Il trade-off accuratezza/interpretabilità è un mito.** Con dati strutturati e feature significative non c'è di solito differenza significativa fra modelli complessi (reti profonde, boosting, random forest) e modelli semplici (regressione logistica, liste di decisione) dopo il preprocessing. La figura del programma XAI della DARPA non viene da dati reali. Nel processo iterativo di data science (KDD, CRISP-DM) poter interpretare i risultati fa migliorare i dati, e il trade-off si **ribalta**. Esempio: predizione dei guasti della rete elettrica di New York, dove gli algoritmi differivano al massimo dell'1% e i predittori migliori erano modelli sparsi.
2. **Le spiegazioni non sono fedeli.** Se fossero fedeli al 100% sarebbero il modello stesso. Una spiegazione corretta al 90% è sbagliata il 10% delle volte, e allora non ci si può fidare né di lei né della black box.
3. **"Spiegazione" è un termine fuorviante.** Un modello che imita le predizioni può usare feature diverse. Caso **COMPAS**: ProPublica ha costruito un modello lineare che dipendeva dalla razza e ha concluso che COMPAS fosse razzista, ma COMPAS sembra non lineare e potrebbe non dipendere dalla razza oltre alla correlazione con età e precedenti. Meglio chiamarle "sintesi delle predizioni" o "trend".
4. **Spiegazioni incomplete.** Le **saliency map** dicono dove guarda la rete, non cosa fa con quella parte: per "husky" e per "flauto traverso" la mappa può essere la stessa. Mostrare solo la spiegazione della classe corretta dà falsa fiducia.
5. **Informazione esterna al database.** Con una black box non si sa come combinare il rischio stimato con circostanze non nel modello: COMPAS non considera la gravità del reato attuale, e il giudice potrebbe non saperlo.
6. **Percorso decisionale troppo complicato.** COMPAS usa 130+ fattori: con un errore di battitura dell'1% per campo, più di un questionario su due ne contiene almeno uno (1 - 0,99¹³⁰ ≈ 0,73). Errori che hanno deciso cauzioni.

### Perché le black box vengono comunque preferite
- **Profitto**: un modello proprietario si vende per predizione. Il modello **CORELS** (Certifiably Optimal Rule Lists) ha la stessa accuratezza di COMPAS con tre regole:

| | |
|---|---|
| IF età 18-20 e sesso maschile | THEN predice arresto (entro 2 anni) |
| ELSE IF età 21-23 e 2-3 precedenti | THEN predice arresto |
| ELSE IF più di tre precedenti | THEN predice arresto |
| ELSE | predice nessun arresto |

  COMPAS è costoso e proprietario, CORELS gratuito e trasparente. Altri casi: **BreezoMeter** (usato da Google negli incendi in California del 2018) dava aria "buona" quando era pericolosa; una rete neurale su radiografie che riconosceva la parola "portable" (il tipo di macchinario) invece del contenuto medico, un problema di **confounding**.
- **Conflitto di responsabilità**: chi vende il modello non risponde delle singole predizioni (paragone con le agenzie di rating della crisi del 2008).
- **"Nasconderlo impedisce di aggirarlo"**: se un sistema trasparente si può aggirare, era progettato male (legge di Goodhart); se misura davvero la qualità, migliorarne il punteggio significa migliorare davvero.
- **Spiegazioni controfattuali** ("con 1000 $ di debito in meno avresti avuto il prestito"): non bastano, il cambiamento minimo è diverso per ogni persona.
- **Costruire modelli interpretabili è difficile**: servono esperti di dominio e problemi di ottimizzazione vincolata, computazionalmente duri; le spiegazioni si basano su derivate e ottimizzazione a gradiente, più facili.
- **"Le black box trovano pattern nascosti"**: se il pattern è abbastanza importante, un modello interpretabile ben costruito lo può trovare lo stesso.

### Governance
- Il GDPR (art. 22) dà un "diritto alla spiegazione", ma non richiede che sia accurata, completa o fedele.
- Proposte: vietare black box per decisioni ad alto rischio quando esiste un modello interpretabile con le stesse prestazioni; più debole, obbligare chi introduce una black box a riportare l'accuratezza dei metodi interpretabili.

### Tre sfide algoritmiche
1. **Modelli logici ottimi** (liste di regole, alberi di decisione, OR di AND). Problema di ottimizzazione:

$$\min_{f \in \mathcal{F}} \; \frac{1}{n}\sum_{i=1}^{n} \mathbb{1}[\text{osservazione } i \text{ classificata male da } f] + \lambda \cdot \text{size}(f)$$

   con $\lambda$ = errore che si accetta per avere un termine in meno ($\lambda = 0{,}01$: si aggiunge un termine solo se riduce l'errore di almeno l'1%). È **computazionalmente duro**. Le euristiche greedy (CART, C4.5) non sono ottime né sparse. CORELS lo risolve **all'ottimo** sulle liste di regole in meno di un minuto sui dati di Broward County, grazie a teoremi che riducono lo spazio di ricerca, una libreria di bit-vector veloce e strutture dati per simmetrie e calcoli intermedi.
2. **Scoring system sparsi ottimi**: modelli lineari sparsi con **coefficienti interi** (i punti), molto usati in medicina. Problema: perdita logistica + $\lambda \sum_j \mathbb{1}[b_j \neq 0]$ con $b_j \in \{-10, \dots, 10\}$, un programma **misto intero non lineare**. Arrotondare una regressione logistica non funziona bene. **RiskSLIM** lo risolve con un metodo a piani di taglio. Esempio per la recidiva entro tre anni: arresti precedenti ≥ 2 (+1), ≥ 5 (+1), arresti per violazioni di ordinanze locali (+1), età al rilascio 18-24 (+1), età ≥ 40 (-1); punteggio da -1 a 4 → rischio 11,9%, 26,9%, 50,0%, 73,1%, 88,1%, 95,3%.
3. **Interpretabilità specifica per dominio, anche nella computer vision**, dove la sparsità sui pixel non ha senso. Reti con un **livello di prototipi** (*This looks like that*): in addestramento impara parti prototipiche delle immagini di ogni classe (la testa tipica di una ghiandaia azzurra), in test confronta le parti dell'immagine con i prototipi e decide con una somma pesata delle similarità. La spiegazione **è** il calcolo del modello, non post hoc, con accuratezza vicina alla rete originale.

- Altri esempi: la FICO Explainable ML Challenge 2018 chiedeva una black box più spiegazione, ma un modello **additivo** globalmente interpretabile ha vinto il premio di riconoscimento.

### Perché modelli interpretabili accurati esistono spesso: il Rashomon set
- **Rashomon set**: l'insieme dei modelli ragionevolmente accurati (entro una certa distanza dal migliore). Con dati finiti è spesso **grande**, come mostra il fatto che algoritmi diversi danno prestazioni simili sugli stessi dati; se è grande e vario, contiene probabilmente anche un modello **semplice**, quindi interpretabile e accurato.
- Conseguenza: gli algoritmi possono essere instabili (piccoli cambiamenti, modelli diversi ma ugualmente buoni), e gli esperti hanno più libertà di scegliere il modello che trovano interpretabile.

### Collegamento con il corso (aggiunta)
- Le liste di regole IF-THEN di CORELS sono programmi logici: in Prolog sono clausole in ordine con il cut, ed è il cut a dare la semantica "ELSE IF" (la prima regola che si applica decide).

```prolog
predice(arresto, Eta, Sesso, _)  :- Eta >= 18, Eta =< 20, Sesso = m, !.
predice(arresto, Eta, _, Prec)   :- Eta >= 21, Eta =< 23, Prec >= 2, Prec =< 3, !.
predice(arresto, _, _, Prec)     :- Prec > 3, !.
predice(nessun_arresto, _, _, _).
```

- I problemi di ottimizzazione delle sfide 1 e 2 sono combinatori e NP-difficili, il tipo di problema che il corso affronta con CLP e ASP.

## Da ricordare per l'orale
- Il cut taglia i punti di scelta del predicato in cui si trova: goal alla sua sinistra e clausole successive; non quelli del chiamante
- `!, fail` = eccezione / negazione per fallimento; cut verdi (efficienza) contro rossi (cambiano le risposte)
- `findall` raccoglie tutte le soluzioni con duplicati e dà `[]` se non ce ne sono; `bagof` fallisce, `setof` ordina ed elimina i duplicati
- `findall` termina solo se il goal ha un albero SLD finito: in `findall.pl` la regola ricorsiva a sinistra lo impedisce
- Rudin: per decisioni ad alto rischio modelli interpretabili, non black box spiegate; il trade-off accuratezza/interpretabilità è spesso un mito; CORELS, RiskSLIM, reti a prototipi, Rashomon set
