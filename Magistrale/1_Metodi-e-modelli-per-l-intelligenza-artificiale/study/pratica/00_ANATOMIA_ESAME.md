# 00 - Anatomia dello scritto: cosa chiede davvero Nicolodi

> Ricavato leggendo, il 2026-07-26, tutto il materiale d'esame in `Appunti_colleghi/Zip_appunti/` e i fogli di esercizi 2026 in `Elly/`. Serve a decidere **su cosa fare pratica** e in che ordine.

Fonti lette:

| Fonte | Cosa è | Copertura |
|---|---|---|
| `esami nicolodi risolti.pdf` (48 pp, scansione) | **12 appelli** risolti a mano, dal 28/06/2005 al 20/06/2007 | tutti gli esercizi censiti sotto |
| `parziale/WhatsApp Image 2024-03-28*` | traccia vera del **I Esonero, 3 maggio 2022, versione 1** | 6 esercizi |
| `parziale/WhatsApp Image 2024-05-08*` | svolgimenti di un collega della prova intercorso 2022 | - |
| `NICOLODI REVISIONI 1.pdf` (18 pp) | screenshot di **quiz Elly/Moodle** a scelta multipla e a risposta numerica, con correzioni | ~25 domande |
| `Elly/*/ese_*_2026.pdf` + `sol-*` | **fogli di esercizi assegnati quest'anno** (fogli 1-7) | il programma effettivo 2025/26 |
| `esercizi MMD.pdf` (37 pp, scansione) | svolgimenti a mano dei **fogli 1-7** fatti da un collega | copre anche i fogli 1 e 4, senza soluzione su Elly |

---

## 1. Censimento: quante volte esce ogni esercizio

Su **12 appelli** (2005-2007), ogni appello ha 2-4 esercizi:

| Esercizio | Frequenza | Cosa chiede esattamente |
|---|---|---|
| **Rilassamento e duale lagrangiano** | **7/12** | vedi §2, è il pezzo più pesante dell'esame |
| **Floyd-Warshall da matrici parziali** | **6/12** | "la k-esima iterazione ha prodotto D^(k) e P^(k): completare l'algoritmo, determinare i cammini i→j; in presenza di cicli negativi arrestare l'algoritmo e individuarli" |
| **Dijkstra con tabella λ/p** | 4/12 | tabella iterazione per iterazione, `*` sul nodo che entra in P, poi ricostruzione del cammino a rovescio dai predecessori |
| **Regione ammissibile + conv(X)** | 4/12 | disegnare X, disegnare conv(X), leggere graficamente z\*_PL e z\*_PI |
| **Abbinamento + copertura** | 3/12 | trovare M di cardinalità massima e R di cardinalità minima, **dimostrare** l'ottimalità via \|M\| = \|R\| (dualità forte, König), a volte + formulazione PIB |
| **Zaino: rilassamento lineare** | 3/12 | ordinare per rapporto beneficio/ingombro, riempire, la variabile frazionaria è una sola |
| **Branch and Bound** | 3/12 | ⛔ **fuori programma 6 CFU, da saltare** (vedi §5): non è su Elly, quindi all'esame sarà a scelta o facoltativo |
| **Equazioni di Bellman su DAG** | 2/12 | u_1 = 0, poi u_j = min{u_i + l_ij}, colonna dei predecessori a lato, ricostruzione del cammino |
| **TSP: 1-albero di costo minimo** | 2/12 | cancellare riga/colonna del nodo 1, MST sul resto, riattaccare i 2 archi più corti da 1; giustificare z\*_PCVS ≥ z\*_1-albero |
| **MST (Prim)** | 1/12 | + verifica \|A\| = \|V\| − 1 |
| **BFS a ventaglio** | 1/12 | etichettatura per livelli L_0, L_1, ..., albero BFS, cammino minimo se gli archi hanno peso 1 |

**Lettura del censimento:** il 60% del punteggio di uno scritto tipo sta in **tre** esercizi - Floyd-Warshall parziale, Dijkstra tabellare, duale lagrangiano. Se quelli sono automatici, lo scritto è passato.

---

## 2. Il duale lagrangiano: le due varianti (l'esercizio più importante)

Esce in 7 appelli su 12, sempre in una di due forme. Vanno automatizzate entrambe.

### Variante A - zaino (n variabili, un solo vincolo di budget)

Traccia tipo: `max z = 10x₁ + 4x₂ + 14x₃`, `3x₁ + x₂ + 4x₃ ≤ 4`, `x ∈ {0,1}³` (oppure `x ∈ Z₊`).

Procedura meccanica:
1. **Rilassamento lineare**: rapporto beneficio/ingombro per ogni variabile, ordinare, riempire il budget. Una sola variabile resta frazionaria → `z*_PL`.
2. `L(μ) = Σⱼ xⱼ(cⱼ − μ aⱼ) + μ b` - raccogliere ciascuna xⱼ.
3. **Tabella dei segni**: una riga per ogni coefficiente `(cⱼ − μ aⱼ)`, si annulla in `μ = cⱼ/aⱼ`. I punti di rottura sono esattamente i rapporti beneficio/ingombro del punto 1.
4. Per ogni intervallo di μ, `xⱼ = 1` se il coefficiente è positivo, `0` se negativo → `L*(μ)` **lineare a tratti**.
5. Grafico di `L*(μ)`, il minimo è in un punto di rottura → `w*_DL`.
6. Concludere: `w*_DL = z*_PL` → dualità forte (le regioni ammissibili coincidono).

### Variante B - due variabili, rilassamento di un vincolo, soluzione grafica

Traccia tipo: `max z = x₁ + 2x₂` con 3 vincoli, `x` interi; rilassare il vincolo (1).

Procedura meccanica:
1. Disegnare la regione, segnare i **punti interi** ammissibili.
2. `L(μ) = c^T x + μ(b₁ − a₁^T x)`, scrivere il problema lagrangiano (resta con i vincoli non rilassati + interezza).
3. `w*_DL` graficamente: **retta parallela alla funzione obiettivo passante per i due punti interi ottimi**, poi intersecarla col vincolo rilassato preso come uguaglianza. Il sistema 2×2 dà il punto, che valutato in z dà `w*_DL`.
4. Spesso chiede anche `μ*` (il coefficiente angolare della retta) e di verificarlo.

Il passaggio che si sbaglia è il 3: la retta va per i punti **interi**, non per i vertici del poliedro.

---

## 3. Il formato moderno è diverso: ci sono le dimostrazioni SCRITTE

Gli appelli 2005-2007 sono al 100% calcolo. L'**esonero 2022** e i **fogli 2026** aggiungono due tipi di esercizio che negli esami vecchi non ci sono:

### Dimostrazioni da scrivere allo scritto
- Esonero 2022, es. 3: dati due programmi binari, "dopo aver ricordato la definizione di rilassamento, provare che (2) è un rilassamento di (1)".
- Esonero 2022, es. 6 (facoltativo): se `ū ≥ 0`, `x̄` ottima di `P(ū)` è ammissibile per `(P)` e `ū^T(Dx̄ − d) = 0`, allora `x̄` è ottima per `(P)`.
- Foglio 7, es. 2: se `P = Conv(X)` e `x*` è SBA ottima di (PL), allora `x*` è ottima per (PI).
- Foglio 7, es. 3: (a) se `x* ∈ S` allora è ottima per (PI); (b) se `c^T x* = c^T x̂` con `x̂ ∈ S` allora `x̂` è ottima.
- Lezioni 19-20: se `A` è TU allora i vertici di `P*(A,b)` sono interi (si prova passando a `Â = [A | Iₘ]`).

Queste **non** sono materiale da orale soltanto: sono esercizi assegnati come gli altri. Le 4-5 dimostrazioni sopra sono corte e ricorrenti, vanno sapute scrivere.

### Modellazione applicata (ricondurre a un problema noto)
Lo schema è sempre "problema industriale in prosa → grafo o programma intero":
- **Piani di rinnovo / sostituzione macchinari** (foglio 3, foglio 4, esonero 2022 es. 4, quiz "bicicletta"): matrice dei costi `c_ij` = compro all'inizio dell'anno i e uso fino alla fine dell'anno j → **DAG con nodi = anni**, cammino minimo da 1 a n+1 con Bellman o Dijkstra. Questo schema esce ovunque, in 4 fonti diverse.
- **Localizzazione supermercati** (foglio 7 es. 1): siti × distretti, ogni distretto servito da al massimo un sito → problema di **impaccamento** (packing), matrice di incidenza, PIB.
- **Clienti e rotte** (esonero 2022 es. 5): ogni cliente coperto da almeno una rotta → **set covering**.
- **Puzzle** (foglio 1): recipienti da 3 e 5 litri, barcaiolo/lupo/capra/cavolo → nodi = stati, archi = mosse ammissibili, BFS.
- **Formulazione pura** (foglio 6): vincoli logici con binarie (implicazione, mutua esclusione, "almeno uno fra... oppure almeno due fra..."), attivazione corsi, cutting-stock, sequenziamento su macchina singola (PIM con tⱼ e wⱼ).

---

## 4. Attenzione: esiste anche un formato a quiz

`NICOLODI REVISIONI 1.pdf` sono screenshot di **quiz Elly/Moodle** dello stesso corso: scelta multipla a 5 alternative (con "nessuna delle altre risposte è corretta" sempre presente) e domande a risposta numerica secca.

Argomenti dei quiz - identici allo scritto, ma valutati in modo diverso:
- grafo dato **per liste** (`V = {...}, A = {(1,5),(1,8),...}`) e non disegnato: cardinalità massima di un abbinamento, cardinalità minima di una copertura, "R = {1,2,3,4} è una copertura di cardinalità minima?"
- 1-albero e albero ricoprente di lunghezza minima: dato un insieme di archi, **è** l'MST o no?
- etichette BFS di un nodo specifico
- Bellman teorico: `u_j ≤ u_i + l_ij` per ogni arco (vero) vs `u_j = u_i + l_ij` solo per i predecessori sul cammino minimo (vero); unicità della soluzione anche in presenza di circuiti (vero, se non negativi); numerabilità progressiva
- Floyd-Warshall: leggere il predecessore corretto da `P^(k)`
- **rilassamento lagrangiano con μ dato**: TSP sui vincoli di grado con `u = (0,0,-6,3,3)` → valore ottimo numerico; UFL sui vincoli di domanda con `u = (5,5,3,2,5,4)` → valore numerico
- zaino: `z*_PL` e `w*_DL` come numero
- TU: condizioni sufficienti, `A` TU ⟺ `A^T` TU, determinante delle sottomatrici quadrate ∈ {0,±1}, la matrice di incidenza di un impaccamento/copertura è sempre TU?
- qualità delle formulazioni: `P ⊆ Conv(X)`, i vertici di `Conv(X)` sono interi, e se `P₂ ⊂ P₁` allora `z*_PL2 ≤ z*_PL1` (per un **minimo**: attenzione al verso)

**Cosa NON so:** se lo scritto del 17 settembre sia su carta (come gli esoneri) o un quiz su Elly. I due formati richiedono preparazioni diverse: sul quiz non c'è punteggio parziale e i distrattori sono costruiti sugli errori di segno/verso, quindi la teoria va saputa **alla lettera**, non a senso. Da chiedere al prof o verificare su Elly.

In ogni caso questi ~25 quiz sono il miglior autotest che hai: le risposte corrette sono già segnate, e le crocette rosse del collega segnano esattamente i punti dove si sbaglia.

---

## 5. Cosa NON serve

Il programma 6 CFU si ferma a *Trasporto generalizzato e problemi facili* incluso, quindi restano fuori: **branch and bound, piani di taglio, programmazione dinamica** (lezioni 23+ dei gestionali).

**Branch and bound: da saltare.** Compare in 3 dei 12 appelli censiti, ma non è nel programma pubblicato su Elly per questo corso, quindi sarà un esercizio a scelta o facoltativo. Se in una traccia d'esame vecchia ne trovi uno, salta l'esercizio e passa al successivo: non è un buco da colmare.

---

## 5-bis. I fogli di esercizi di quest'anno (la fonte più attendibile)

Sono **7 fogli**, uno per modulo, dentro `Elly/`. Non è un file unico. Questi sono gli esercizi che il prof ha effettivamente assegnato nel 2025/26, quindi contano più delle tracce 2005-2007.

| Foglio | Percorso | Contenuto | Soluzioni |
|---|---|---|---|
| 1 | `2_Procedure_BFS_e_DFS/ese_1_2026.pdf` | 2 puzzle da ricondurre a esplorazione su grafo: recipienti da 3 e 5 litri (raccogliere 4 litri), barcaiolo/lupo/capra/cavolo | - |
| 2 | `3_Cammini_Minimi_Equazioni_di_Bellman/ese_2_2026.pdf` | (a) cammino minimo 1→13 su un DAG di 13 nodi con Bellman; (b) risolvere le equazioni di Bellman su un grafo piccolo **con un circuito** (3→4→2→3) | `6_Albero_Ricoprente_Minimo_(MST)/sol_esercizi_(3.4bisese_2).pdf` |
| 3 | `3_Cammini_Minimi_Equazioni_di_Bellman/ese_3_2026.pdf` | **piano di rinnovo ottimale** macchinario da 12.000 €, 5 anni, tabella manutenzione + ricavato → DAG + Bellman | `4_Cammini_Minimi_Dijkstra/Sol-piano-rinn-ott.pdf` |
| 3.1 | `4_Cammini_Minimi_Dijkstra/ese_3.1_2026.pdf` | stesse equazioni di Bellman del foglio 2 + Dijkstra da 1=A a tutti gli altri su un grafo di 8 nodi (A-H) | `6_Albero_Ricoprente_Minimo_(MST)/sol-ese-dijkstra(ese3.1).pdf` |
| 4 | `5_Cammini_Minimi_Floyd_Warshall/ese_4_2026.pdf` | (a) matrice costi `c_ij` acquisto macchinari anno i → fine anno j, come cammino minimo risolto con Dijkstra; (b) completare Floyd-Warshall da `D^(0)`/`P^(0)` su 4 nodi con pesi negativi | - |
| 5 | `7_Programmazione_Lineare_&_Ottimizzazione_Combinatoria/ese_5_2026.pdf` | 6 città con distanze stradali, centro servizi installabile in ogni nodo, copertura entro 11 km → formulare il PI che minimizza le installazioni (**set covering**) | `7_Programmazione_Lineare_&_Ottimizzazione_Combinatoria/sol-ese-cop-seq-stsp.pdf` |
| 6 | `7_Programmazione_Lineare_&_Ottimizzazione_Combinatoria/ese_6_2026.pdf` | 5 esercizi di **sola formulazione**: vincoli logici con binarie, attivazione corsi, scelta corsi, cutting-stock, sequenziamento su macchina singola (PIM) | `ese_6_2026_sol.pdf` |
| 7 | `8_Rilassamenti_e_Dualità/ese_7_2026.pdf` | (1) localizzazione supermercati, siti × distretti → **impaccamento**; (2) **dimostrazione**: `P = Conv(X)` + SBA ottima di (PL) ⟹ ottima per (PI); (3) **dimostrazione**: `x* ∈ S` ⟹ ottima, e `c^T x* = c^T x̂` ⟹ `x̂` ottima | `sol-ese-7.pdf` |
| — | `9_Matrici_TU_e_Teorema_di_Interezza/` | solo la soluzione: **dimostrazione** `A` TU ⟹ vertici di `P*(A,b)` interi (via `Â = [A \| Iₘ]`) | `sol_es_Lez_19_20.pdf` |

Nota: i fogli 2, 3.1 e 5 sono scansioni manoscritte senza testo estraibile, gli altri sono PDF LaTeX.

**Dove Elly non dà la soluzione, ce l'hai altrove:** `Appunti_colleghi/Zip_appunti/esercizi MMD.pdf` (37 pp) sono gli svolgimenti a mano dei fogli 1-7 fatti da un collega. Sono gli stessi fogli, quindi coprono anche i **fogli 1 e 4**, per cui su Elly manca il `sol-*`.

Due letture utili di questa tabella:

- **6 fogli su 8 sono modellazione o dimostrazione, non esecuzione di algoritmi.** Gli algoritmi (Bellman, Dijkstra, Floyd-Warshall) escono nei fogli 2-4, ma sempre agganciati a un problema industriale da tradurre prima in grafo. La pura esecuzione su un grafo già dato la trovi solo nel foglio 4b.
- **Manca completamente un foglio sul duale lagrangiano numerico** (tabella dei segni, `L*(μ)` a tratti), che invece è l'esercizio più frequente negli appelli vecchi. Il foglio 7 sui rilassamenti va sulla teoria e sulle formulazioni. Per la pratica su quello i tuoi materiali sono gli appelli risolti, non i fogli.

## 6. Piano di pratica, in ordine

### Priorità 1 - da rendere automatici (nessun ragionamento, solo esecuzione)
1. **Floyd-Warshall a partire da D^(k)/P^(k)** - la regola di aggiornamento di `P`, che è il punto dove si sbaglia: `p^(k)_ij = p^(k-1)_kj` quando il cammino passa per k. E lo stop: `d_ii < 0` per qualche i ⟹ ciclo negativo, si arresta e si esibisce il ciclo risalendo i predecessori. → `05_esercizi_floyd_warshall.md`
2. **Dijkstra tabellare** λ/p, con `*` sul nodo che entra. → `04_esercizi_dijkstra.md`
3. **Duale lagrangiano, entrambe le varianti** di §2. → `09_esercizi_rilassamenti_dualita.md`

Target: ognuno risolto in meno di 10 minuti senza guardare niente. Verifica: 3 istanze diverse di fila, tutte giuste.

### Priorità 2 - da saper fare senza esitare
4. Regione ammissibile + `conv(X)` disegnati, `z*_PL` vs `z*_PI` letti dal grafico
5. Abbinamento max + copertura min + `|M| = |R|` ⟹ ottimalità (e la formulazione PIB di entrambi)
6. Equazioni di Bellman su DAG, con la colonna dei predecessori
7. Piani di rinnovo/sostituzione → DAG (lo schema di §3, il più ricorrente fra le applicazioni)
8. TSP: 1-albero come limitazione inferiore
9. Le 5 dimostrazioni brevi di §3

### Priorità 3 - una passata sola
10. MST (Prim), BFS a livelli, riduzione di puzzle a esplorazione su grafo
11. Formulazioni del foglio 6 (vincoli logici, cutting-stock, sequenziamento)
12. TU: condizioni sufficienti e il teorema di interezza

Il branch and bound **non** è in lista: fuori programma, vedi §5.

### Simulazioni
Tracce complete stampabili da `esami nicolodi risolti.pdf` coprendo le soluzioni. Le più rappresentative del formato moderno sono l'**esonero 2022** (mix calcolo + dimostrazione + modellazione) e gli appelli **13 luglio 2005** e **9 febbraio 2006** (grafi + zaino + lagrangiano completo). Vedi `13_simulazione_esame.md`.

---

## 7. Errori ricorrenti visibili negli svolgimenti

Dai passaggi corretti in rosso negli esami risolti e dalle crocette nei quiz:

- **Floyd-Warshall, matrice dei predecessori**: si aggiorna `D` e si dimentica `P`, o si copia il predecessore sbagliato. Negli svolgimenti il collega scrive esplicitamente `p^(3)_14 = p^(2)_34 = 3` riga per riga: conviene fare lo stesso.
- **Cicli negativi**: la condizione è `d_ii < 0`, sulla **diagonale**. Va poi esibito il ciclo, non solo dichiarato.
- **Duale lagrangiano variante B**: la retta va per i punti **interi**, non per i vertici del poliedro.
- **Dualità forte vs debole** in abbinamento/copertura: in generale `|M| ≤ |R|` (debole); l'uguaglianza vale perché il grafo è **bipartito**, e va detto.
- **Verso delle disuguaglianze** nel confronto fra formulazioni: per un problema di minimo, `P₂ ⊂ P₁` ⟹ `z*_PL2 ≥ z*_PL1`. È il distrattore più usato nei quiz.
- **Bellman**: `u_j ≤ u_i + l_ij` vale per **ogni** arco; l'uguaglianza solo se `i` è predecessore di `j` su un cammino minimo. Confonderli è l'errore segnato due volte nei quiz.
