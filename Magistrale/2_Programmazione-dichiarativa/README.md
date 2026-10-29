# Programmazione dichiarativa

**cod. 1009066** - 6 CFU, 48 ore - caratterizzante, monodisciplinare - 2° anno, primo semestre (a.a. 2026/27) - insegnamento in italiano.
**Docente:** Alessandro Dal Palù (alessandro.dalpalu@unipr.it)
**Esame:** **orale sugli argomenti di teoria + discussione del progetto** (programma in **ASP**). Progetto anche in gruppo (max 2 studenti): un problema, tipicamente NP-completo, di cui si curano la modellazione logica, l'implementazione in Answer Set Programming e la valutazione critica delle performance (materiale del docente, confermato da Martin il 19/10/2026). La scheda ufficiale aggiunge che l'orale può riguardare anche la revisione di letteratura scientifica, che si può ripetere più volte e che approfondisce i programmi consegnati.
**Metodi didattici:** lezioni frontali ed esperienze di laboratorio.

Scheda ufficiale: https://corsi.unipr.it/it/ugov/degreecourse/329459

| Edizione | Elly | Corso | Stato |
|---|---|---|---|
| 2026/27 | elly2026 | [id 4403](https://elly2026.didattica.unipr.it/course/view.php?id=4403) | in corso, inizio 21/09/2026 |
| 2025/26 | - | - | non pubblicata |

> Il corso su elly2026 **esiste** (id 4403). Il README diceva "nessun corso Elly
> disponibile": era vero solo per l'edizione 2025/26, che non è mai stata
> pubblicata, e restava falso per quella nuova. Non c'è quindi materiale
> d'archivio: tutto quello che arriva è dell'edizione che seguo.

## Appelli 2026/27

Da Esse3 (via unidesk), letti il 19/10/2026. Tutti in stato "Inserito", iscrizioni non ancora aperte.

- mer 20/01/2027 ore 09:00 - orale - iscrizioni dal 21/12/2026 al 15/01/2027 **(sessione invernale)**
- gio 04/02/2027 ore 09:00 - orale - iscrizioni dal 05/01/2027 al 30/01/2027 **(sessione invernale)**
- gio 18/02/2027 ore 09:00 - orale - iscrizioni dal 19/01/2027 al 13/02/2027 **(sessione invernale)**
- gio 10/06/2027 ore 09:00 - orale - iscrizioni dal 11/05/2027 al 05/06/2027
- gio 24/06/2027 ore 09:00 - orale - iscrizioni dal 25/05/2027 al 19/06/2027
- mar 27/07/2027 ore 09:00 - orale - iscrizioni dal 27/06/2027 al 22/07/2027
- ven 10/09/2027 ore 09:00 - orale - iscrizioni dal 11/08/2027 al 05/09/2027

## Struttura della cartella

- `2026-27/` - materiale Elly, una sottocartella per lezione
- `project/` - il progetto d'esame, una sottocartella per progetto
- `study/` - preparazione dell'orale

Il progetto si può fare in gruppo (max 2 studenti, è una facoltà non un
obbligo). Per ora si sviluppa qui: se servirà condividerlo con un collega si
sposta in un repository a sé, così non gli si passa tutto il percorso
universitario.

Il `.gitignore` del corso tiene fuori da git dataset grezzi, file generati,
risultati, `.venv` e zip di consegna.

## Materiale Elly 2026/27 - corso 4403

Al 16/09/2026 il corso era aperto ma vuoto. Con la prima lezione (21/09/2026)
Dal Palù ha iniziato a caricare: una dispensa di riferimento e una sezione per
ogni lezione con le slide annotate a mano in aula. Aggiornato il 21/09/2026,
ricontrollato il 29/09/2026 e il 18/10/2026: è arrivata la sezione della
lezione 5 con due file Prolog; dispensa e slide della lezione 1 identiche (md5).
Ricontrollato il 29/10/2026: sono arrivate le sezioni delle lezioni 7, 8 e 9
(quattro file Prolog e un articolo), scaricate; il resto identico (md5). Nessun
annuncio sul forum.

### 0 - Introduzione

- [forum] Annunci - https://elly2026.didattica.unipr.it/mod/forum/view.php?id=5755
- `2026-27/0_Introduzione/Dispensa Dovier-Formisano.pdf` (lnc-dovier-3.pdf)

Dovier, Formisano - *Programmazione Dichiarativa in Prolog, CLP e ASP*
(Udine/Perugia, a.a. 16/17, ~230 pagine). È il testo del corso: logica del
prim'ordine, clausole definite, unificazione, SLD-risoluzione, semantica dei
programmi logici, Prolog, CLP, ASP.

### 1 - Lezione 1, 21-09-26

- `2026-27/1_Lezione_1_21-09-26/Slide.pdf` (2026-09-21-Note-10-33_annotato.pdf)

Cinque pagine di appunti scritti a mano in aula (niente testo selezionabile,
sono immagini). Lezione introduttiva, senza contenuto tecnico di Prolog/ASP:

- Curva sforzo/ottimizzazione delle specifiche; LLM che scrivono codice e
  *human over the loop*.
- "Dov'è la comprensione/intelligenza nell'IA?" - dataset + training + rete +
  contesto: **sub-simbolico** (ML generativo) contro **simbolico**.
- Storia dell'IA a due rami: reti neurali bottom-up (potenza di calcolo → GPU →
  LLM, generale) contro dimostratori automatici top-down (theorem proving,
  knowledge representation, automated reasoning, applicazioni specialistiche).
- Ragionamento ad alto livello: dal problema si deducono passi fino alla
  soluzione; la conoscenza (common knowledge, specifica, mancanza di conoscenza)
  è **esplicita**.
- Confronto sub-simbolico / simbolico: tanti dati con poco significato contro
  pochi dati ad alto significato; semantica dei dati no/sì; velocità alta/bassa;
  affidabilità ~95% contro 100% (solver, SAT solver); interpretabile no/sì;
  black box sì/no.
- Imperativo contro dichiarativo: specifiche informali con pre/post condizioni,
  modello algoritmico, implementazione, manutenzione e bug fixing - contro
  specifiche + knowledge representation direttamente **eseguibili** (contratto
  matematico), goal dato a un **solver** di automated reasoning che restituisce
  la risposta. Nel dichiarativo il bug fixing torna sulle specifiche.

### 5 - Lezione 5, 13-10-26

- `2026-27/5_Lezione_5_13-10-26/mdt.pl` (mdt.pl) - simulatore di **macchina di
  Turing** in Prolog: `delta/5` come tabella di transizione, il nastro come
  `nastro(ListaSinistra, Corrente, ListaDestra)`, `passo/4` e `calcolo/4`
  ricorsivi fino a `statoFinale/1`, `updateNastro/4` per gli spostamenti `l`/`r`
  con `elementoVuoto` ai bordi
- `2026-27/5_Lezione_5_13-10-26/test.pl` (test.pl) - esempi base: chiusura
  transitiva `q/2` in tre versioni (la terza, ricorsiva a sinistra, va in loop per
  l'ordine di selezione SLD: prima regola del listato, atomo più a sinistra),
  numeri di Peano `num/1`, liste, `somma/2` e `len/2` con `is`

### 7 - Lezione 7, 20-10-26

- `2026-27/7_Lezione_7_20-10-26/struct.pl` (struct.pl) - termini composti come
  struttura dati: fatti `struct/3` e `struct/4` con argomenti funtore `f(_, _)`

### 8 - Lezione 8, 26-10-26

- `2026-27/8_Lezione_8_26-10-26/generate.pl` (generate.pl) - schema
  *generate and test*: `genera/4` e `test/4` combinati in `soluzione/4`, poi
  `genera/2` che alloca una lista di N variabili su una lista di valori ammessi

### 9 - Lezione 9, 27-10-26

- `2026-27/9_Lezione_9_27-10-26/Articolo explainable ML.pdf` (s42256-019-0048-x-1-1.pdf) -
  Cynthia Rudin, *Stop explaining black box machine learning models for high
  stakes decisions and use interpretable models instead*, Nature Machine
  Intelligence 2019, 10 pagine
- `2026-27/9_Lezione_9_27-10-26/cut.pl` (cut.pl) - effetto del cut `!` e di
  `!, fail` sul backtracking
- `2026-27/9_Lezione_9_27-10-26/findall.pl` (findall.pl) - `findall/3` e stampa
  ricorsiva di una lista

Su Elly non ci sono sezioni per le lezioni 2, 3, 4 e 6: il docente non ha caricato
niente. Lo schema resta una sezione Elly per data, ma non per ogni lezione.

## Contenuti

Modello di programmazione dichiarativa, logica computazionale e pratica su problemi complessi. Linguaggi trattati: **Prolog** e **Answer Set Programming**.

**Programma esteso:** introduzione al logic programming e alle basi teoriche; logica del primo ordine, semantica, stable model semantics (Gelfond-Lifschitz); modellazione in ASP; linguaggio e grounding; tecniche di codifica avanzate; programmazione in Answer Set Programming.

**Bibliografia:** dispense fornite nel materiale didattico (italiano e inglese).

**Risultati attesi:** modellare un problema in specifiche formali, implementare il codice di logica computazionale discendente dal modello, saper modellare problemi anche fuori dall'informatica.
