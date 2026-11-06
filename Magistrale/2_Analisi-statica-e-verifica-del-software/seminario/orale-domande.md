# Orale: domande probabili sul corso

Servono per i 10 minuti di orale dopo il seminario. Non sono dettagli: sono le domande principali per ogni lezione, con una risposta corta (quella che diresti a voce in 20-30 secondi). Fonte: le slide del corso in `2026-27/2_Slides/` (le lezioni 01-11 in `.md`, la 12 sul PDF). Le domande le ho scelte io pensando a cosa chiederebbe un docente: non so cosa chiederà davvero.

**Come usarlo:** copri la risposta, rispondi a voce, poi controlla. Prima fai le "10 più probabili", poi il resto.

## Le 10 più probabili

1. Che cos'è l'abstract interpretation e perché serve? (01, 05)
2. Perché non si può avere un'analisi automatica, sound e completa? (01)
3. Che cos'è una connessione di Galois, e che cosa sono α e γ? (06)
4. Cosa vuol dire che un'analisi è sound? (05, 06, 07)
5. Perché serve il widening e come funziona sugli intervalli? (12)
6. Differenza tra dataflow analysis e abstract interpretation. (04)
7. Cos'è un reticolo completo e perché i punti fissi (Kleene, Knaster-Tarski) servono? (02)
8. Perché l'analisi dei segni perde precisione? Fai un esempio. (05, 06)
9. Che cos'è un dominio relazionale? Intervalli, octagon, poliedri. (05, 08)
10. Perché per i poliedri non esiste la connessione di Galois? (06) Aggancio diretto al seminario TVL.

---

## 01 - Introduzione

**Che differenza c'è tra validation e verification?**
Validation: stiamo costruendo il software giusto? (requisiti informali → specifiche). Verification: stiamo costruendo il software nel modo giusto? (specifiche → sistema). L'analisi statica è verification.

**Perché non esiste un verificatore perfetto?**
Teorema di Rice: ogni proprietà non banale del comportamento di programmi in un linguaggio Turing-completo è indecidibile. Quindi non si può avere un metodo insieme automatico, sound e complete.

**A cosa si rinuncia nel corso?**
Mai alla soundness. Si rinuncia alla completeness: l'analisi può dire "forse" (falsi allarmi), ma non dice mai "corretto" per un programma sbagliato. Si cerca di mantenere automazione e potenza.

**Analisi statica contro dinamica?**
Dinamica (testing, fuzzing): esegue il programma su un insieme finito di input, risponde sì/no. Statica: ragiona su tutti gli input, risponde sì/no/forse e può perdere precisione.

**Un esempio di bug reale?**
Ariane 5 (1996): overflow nella conversione da float a 64 bit a intero a 16 bit, con il controllo numerico disattivato. Costo di circa 370 milioni di dollari.

---

## 02 - Background matematico

**Cos'è un ordine parziale?**
Una relazione riflessiva, antisimmetrica e transitiva. Esempio: ⊆ sull'insieme delle parti.

**Che differenza c'è tra lattice e complete lattice?**
Lattice: ogni coppia di elementi ha lub (join) e glb (meet). Complete lattice: ogni sottoinsieme, anche infinito, ha lub (quindi ha sempre ⊥ e ⊤). I lattice finiti sono completi. ℤ con ≤ è un lattice ma non completo; ℤ ∪ {±∞} sì.

**Cos'è una funzione monotona?**
Se x ⊑ y allora f(x) ⊑ f(y). Le funzioni che preservano join o meet sono monotone, non vale il viceversa.

**Cos'è un punto fisso? Cosa dicono Kleene e Knaster-Tarski?**
Punto fisso: f(x) = x. Knaster-Tarski: f monotona su complete lattice → i punti fissi formano un complete lattice, lfp = glb dei pre-punti fissi. Kleene: f continua → lfp = lub delle iterate f^n(⊥), che si calcola iterando da ⊥.

**Cos'è la condizione di catena ascendente (ACC)?**
Ogni catena ascendente si stabilizza in un numero finito di passi. Garantisce che l'iterazione di Kleene termini. I poset finiti la soddisfano; (ℕ, ≤) e (ℤ, ≤) no.

---

## 03 - Modellare i programmi

**Qual è il dominio concreto di un'analisi sui valori?**
Insiemi di valori possibili per ogni variabile in ogni punto del programma, nel reticolo (℘(ℤ), ⊆, ∪, ∩). Join = ∪ dove i cammini si uniscono, filtro = ∩ sulle guardie.

**Perché con i cicli serve un punto fisso?**
Un ciclo genera equazioni ricorsive: lo stato in testa al ciclo dipende da sé stesso. La soluzione è il least fixpoint. Su ℘(ℤ) l'iterazione da ∅ può non terminare (catena infinita).

**Cos'è la trace semantics?**
La semantica che descrive un programma come l'insieme delle sue tracce di esecuzione. Da essa si ricavano per astrazione semantiche più semplici (per esempio i valori per program point).

**Perché il join dev'essere il minimo maggiorante?**
Per non perdere precisione inutilmente: [−5,5] ⊔ [0,0] = [−5,5], non [−10,5].

---

## 04 - Dataflow analysis

**Cos'è un CFG?**
Grafo di flusso di controllo: nodi = statement, archi = possibili passaggi da uno statement al successivo.

**Come funziona una dataflow analysis?**
Si scrivono equazioni tra stato di entrata e di uscita di ogni blocco (entry = join delle uscite dei predecessori, exit = funzione di trasferimento gen/kill) e si risolvono per iterazione (worklist) fino al punto fisso.

**Le quattro analisi classiche?**
Reaching definitions (forward, may), available expressions (forward, must), live variables (backward, may), very busy expressions (backward, must). May usa ∪, must usa ∩.

**Perché la constant propagation non è distributiva?**
Perché f(x ⊔ y) ≠ f(x) ⊔ f(y): unire gli stati prima di applicare la funzione perde precisione (per esempio z = x + y con x e y costanti diverse nei due rami). Le analisi gen/kill sono distributive; le numeriche no.

**Quando serve l'abstract interpretation invece della dataflow?**
Per le analisi non distributive e per domini non banali (intervalli, relazionali), cioè quando non basta un'analisi gen/kill.

---

## 05 - Significato dell'approssimazione

**Qual è lo schema generale di un'analisi sound?**
Si vuole verificare [[P]] ⊆ Q, ma è indecidibile. Si calcola una sovra-approssimazione [[P]]♯ con [[P]] ⊆ [[P]]♯ e si controlla [[P]]♯ ⊆ Q (decidibile). Se vale, il programma è corretto; altrimenti "non so" (possibile falso allarme).

**Sotto-approssimazione contro sovra-approssimazione?**
Sotto: si calcolano meno comportamenti, i "sì" sono certi (testing). Sovra: si calcolano più comportamenti, i "no" sono certi (analisi statica sound). Il corso usa la sovra.

**Il dominio dei segni: esempio di perdita di precisione?**
Elementi: ⊤, +, 0, −, ⊥. Somma + ⊕ − = ⊤: non si sa il segno del risultato.

**I domini numerici in ordine di precisione?**
Intervalli (non relazionali) < octagon (±x ± y ≤ c) < poliedri (vincoli lineari qualsiasi). Più preciso = più costoso. Le congruenze catturano le regolarità (x = a mod m).

**Cos'è la collecting semantics?**
La semantica che associa a ogni program point l'insieme degli stati raggiungibili. È ancora indecidibile, quindi si astrae.

---

## 06 - Interpretazione astratta: connessioni di Galois

**Cos'è una connessione di Galois?**
Una coppia di funzioni α: C → A (astrazione) e γ: A → C (concretizzazione) tali che α(c) ⊑ a ⟺ c ⊆ γ(a). Da "⇒" viene la soundness, da "⇐" il fatto che α dà la migliore astrazione.

**Che cos'è la soundness in termini di α e γ?**
c ⊆ γ(α(c)): l'astrazione contiene almeno ciò che rappresenta. Nell'altra direzione α(γ(a)) ⊑ a.

**Che differenza c'è tra connessione e inserzione di Galois?**
Nell'inserzione α∘γ = id: α suriettiva e γ iniettiva, cioè nessun elemento astratto è ridondante. Ogni connessione si riduce a un'inserzione eliminando gli elementi ridondanti.

**Perché γ∘α = id non è quello che vogliamo?**
Vorrebbe dire nessuna astrazione (isomorfismo): si tornerebbe al concreto, senza perdita ma anche senza guadagno.

**Esempio di dominio senza connessione di Galois?**
I poliedri convessi con il disco x² + y² ≤ 1: non c'è una migliore approssimazione poligonale. È lo stesso argomento usato nel paper TVL.

---

## 07 - Interpretazione astratta: semantica astratta

**Come si costruisce l'analisi astratta partendo da quella concreta?**
Si scrive la semantica concreta come sistema di equazioni sul CFG, poi si sostituisce ∪ con ⊔, gli stati iniziali con α(I) e le operazioni con le loro versioni astratte.

**Quando un operatore astratto è sound?**
f♯ è sound se α∘f ⊑ f♯∘α, equivalentemente f∘γ ⊑ γ∘f♯.

**Cos'è la best correct approximation?**
f^bca = α∘f∘γ: la migliore tra le approssimazioni sound. Spesso non è calcolabile (γ(a) è infinito).

**Cosa garantisce il fixpoint transfer?**
Se f♯ è sound, α(lfp(F)) ⊑ lfp(F♯): calcolando nel dominio astratto si ottiene una sovra-approssimazione della soluzione concreta. Con f♯ = bca vale l'uguaglianza.

**Che differenza c'è tra il teorema di Kleene e quello di Tarski in questo contesto?**
Kleene: iterando da ⊥ in A si arriva a un x con lfp(f) ⊑ γ(x) (serve la continuità). Tarski: basta trovare un a con f♯(a) ⊑ a (post-punto fisso) per avere lfp(f) ⊑ γ(a). Entrambi danno soundness, non ottimalità.

---

## 08 - L'operatore split

**Qual è il problema?**
Un if genera due rami e ogni guardia chiede un filter sullo stato astratto (c, poi ¬c). Con i poliedri questo costa due volte e richiede due copie dello stato.

**Cos'è l'operatore split?**
split(A, c) = (filter(A, c), filter(A, ¬c)): calcola i due rami in una sola chiamata e senza copie.

**Perché è più veloce?**
Condivide il lavoro sui generatori del poliedro (la classificazione dei vertici rispetto all'iperpiano, i nuovi vertici sul bordo).

**Che risultati ha?**
Speed-up fino a 4,35 (firewire), qualche rallentamento (0,76 e 0,87) e memoria molto minore, senza perdita di precisione.

---

## 09 - Unconstrained variable oracles

**Che idea c'è dietro?**
"Abstract compilation": riscrivere il programma prima dell'analisi per renderla più veloce, accettando di perdere un po' di precisione. Le variabili probabilmente senza vincoli (likely unconstrained, LU) su cui l'analisi non saprebbe nulla vengono sostituite da un valore non deterministico (x ← ?).

**Perché la trasformazione è sound?**
Sostituire un assegnamento con un valore qualunque aggiunge comportamenti, non ne toglie: è una sovra-approssimazione, qualunque cosa dica l'oracolo.

**Che differenza c'è tra oracolo non relazionale e relazionale?**
Non relazionale: aggressivo, guarda solo le singole variabili. Relazionale: conservativo, perché un assegnamento lineare crea una relazione e toglie dall'insieme LU tutte le variabili coinvolte.

**Che risultati ha?**
Con i poliedri speed-up medio di 2,61 (massimo 8,23), con circa il 90% dei vincoli conservato; con gli intervalli circa il 99%.

---

## 10 - Analisi statica dei vettori R

**Perché R è difficile da analizzare?**
Tutto è un vettore, NA è diverso da NULL, i tipi si promuovono in silenzio, le operazioni riciclano il vettore più corto e l'indicizzazione ha tre modalità. Lunghezza e contenuto dipendono dal ramo eseguito.

**Com'è fatto il dominio astratto?**
Un elemento è un intervallo di lunghezza [l, u], un prefisso di posizioni esplicite, un sommario per il resto e un insieme di attributi. È parametrico nel dominio dei valori (per esempio gli intervalli).

**Perché non c'è la connessione di Galois?**
Una catena di elementi con sempre più posizioni esatte non ha estremo inferiore, quindi non esiste α. L'analisi usa solo γ (è concretization-based), come nel paper TVL.

**Che limiti ha?**
Non relazionale, niente relazioni fra lunghezze, niente analisi interprocedurale, niente disgiunzioni ai punti di unione.

---

## 11 - LiSA

**Cos'è LiSA?**
Una libreria Java open source (Parma e Venezia) per costruire analizzatori basati su abstract interpretation. Non è un analizzatore completo: il frontend che traduce il sorgente in CFG lo scrive l'utente.

**Com'è fatta la pipeline?**
Programma → frontend (dipendente dal linguaggio) → CFG → LiSA (analisi interprocedurale, fixpoint sui CFG, semantica degli statement, stato astratto) → warning.

**Cos'è lo stato astratto?**
Un heap domain (riscrive gli accessi in memoria in variabili simboliche) più un value domain (vede solo variabili e costanti).

**Cosa deve implementare un dominio?**
`Lattice` (lessOrEqual, lub, widening, top, bottom) e `SemanticDomain` (assign, smallStepSemantics, satisfies, assume).

**Esempi di applicazione?**
GoLiSA (non-determinismo negli smart contract Go) ed EVMLiSA (CFG sound per bytecode EVM).

---

## 12 - Dominio degli intervalli, widening e narrowing

**Cos'è un widening?**
Un operatore ∇ che calcola un maggiorante (x ⊑ x∇y e y ⊑ x∇y) e garantisce che ogni sequenza x_{i+1} = x_i ∇ y_{i+1} si stabilizzi in tempo finito. Sovra-approssima l'lfp ma assicura la convergenza.

**Qual è il widening sugli intervalli?**
[a,b] ∇ [c,d] = [a se a ≤ c, altrimenti −∞ ; b se b ≥ d, altrimenti +∞]. Esempio: [0,1] ∇ [0,2] = [0, +∞).

**Il widening è commutativo o monotono?**
Né l'uno né l'altro: [2,3] ∇ [1,4] = [−∞,+∞] ma [1,4] ∇ [2,3] = [1,4]. Non è nemmeno monotono (esempio dalla slide: [0,1] ⊑ [0,3] ma [0,1] ∇ [0,2] = [0,+∞] ⋢ [0,3] ∇ [0,2] = [0,3]).

**Dove si applica?**
Basta applicarlo in un nodo per ogni ciclo del CFG (di solito la testa del ciclo): applicarlo ovunque darebbe un'approssimazione troppo grossolana (Bourdoncle).

**Cos'è il narrowing e quando si usa?**
Un operatore △ che recupera precisione dopo il widening, partendo dal post-punto fisso: x ⊓ y ⊑ x △ y ⊑ x, con convergenza garantita. Sugli intervalli [a,b] △ [c,d] sostituisce con c, d solo i limiti infiniti. Si usa nei widening points, in una seconda fase discendente.

**Esempio completo (mio)?**
`i = 0; while (i < 100) i = i + 1`. Con il widening la testa del ciclo diventa [0, +∞). Il narrowing applica di nuovo la funzione: [0,0] ⊔ ([0,99] + 1) = [0,100], e [0,+∞) △ [0,100] = [0,100]: il limite superiore torna finito.

**Perché gli intervalli non sono relazionali?**
Tengono un intervallo per variabile e perdono le relazioni: dopo `x = y` non sanno che x e y sono uguali.

---

## Domande trasversali (agganci tra le lezioni e il TVL)

**Cosa c'entra il tuo paper con il corso?**
È un dominio numerico relazionale tra gli octagon (slide 05) e i poliedri (slide 05, 08). Usa un reticolo non completo e senza α (slide 02, 06); per terminare serve un widening (slide 12); e il join è il punto costoso, come per lo split dei poliedri (slide 08).

**Perché α non esiste nel TVL?**
Per lo stesso motivo del disco e dei poliedri (slide 06): nessuna migliore approssimazione con un numero finito di disuguaglianze. Si lavora con la sola γ, come per i vettori R (slide 10).

**Dove si vede il compromesso precisione/costo?**
In tutto il corso: dominio dei segni contro intervalli, intervalli contro octagon contro poliedri, widening (convergenza contro precisione), split e oracoli LU (velocità contro precisione).

**Perché il widening in TVL è delicato?**
Per la completion: dopo il widening può reintrodurre disuguaglianze appena tolte e rompere la terminazione (slide 12 e paper).

---

## Mini-glossario (una riga a testa)

- **Sound:** non dice mai "corretto" per un programma sbagliato (nessun falso negativo).
- **Complete:** dice sempre "corretto" per un programma corretto (nessun falso allarme). Si sacrifica.
- **Over-approximation:** include almeno tutti i comportamenti reali.
- **α / γ:** astrazione (migliore approssimazione astratta) e concretizzazione (significato concreto di un elemento astratto).
- **lfp:** il minimo punto fisso; è la semantica di un ciclo.
- **Widening / narrowing:** forzano la convergenza (salendo) e recuperano precisione (scendendo).
- **Relazionale:** ricorda relazioni tra variabili (x − y ≤ c). Non relazionale: un valore per variabile.
- **Must / may:** vale su tutti i cammini (∩) / su almeno un cammino (∪).
- **Forward / backward:** analisi nel verso dell'esecuzione / contrario.
- **Flow-sensitive:** tiene conto dell'ordine degli statement.
- **Distributiva:** f(x ⊔ y) = f(x) ⊔ f(y); se vale, la dataflow è esatta.
- **Falso allarme:** l'analisi dice "forse errore" ma il programma è corretto.

---

## Cose da non dire

- Che l'analisi statica "dimostra la correttezza" in generale: dimostra una proprietà, o dice "non so".
- Che una sovra-approssimazione può dare falsi negativi: no, può dare solo falsi positivi.
- Che il widening è monotono o commutativo.
- Che Kleene o Tarski garantiscono l'ottimalità: garantiscono la soundness.
- Che le slide 08 e 09 sono dello stesso tipo di quelle teoriche: sono seminari su articoli (split, oracoli), se ti chiedono dettagli di numeri meglio dire "approssimativamente" e non inventare.
