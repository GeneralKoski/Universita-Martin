# Programmazione dichiarativa

**cod. 1009066** - 6 CFU, 48 ore - caratterizzante, monodisciplinare - 2° anno, primo semestre (a.a. 2026/27) - insegnamento in italiano.
**Docente:** Alessandro Dal Palù (alessandro.dalpalu@unipr.it)
**Esame:** prova orale (teoria e/o revisione di letteratura scientifica) + discussione di un progetto (anche in gruppo, max 2 studenti). L'orale si può ripetere più volte e approfondisce i programmi consegnati.
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

## Materiale Elly 2026/27 - corso 4403

Al 16/09/2026 il corso era aperto ma vuoto. Con la prima lezione (21/09/2026)
Dal Palù ha iniziato a caricare: una dispensa di riferimento e una sezione per
ogni lezione con le slide annotate a mano in aula. Aggiornato il 21/09/2026.

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

Le lezioni successive dovrebbero seguire lo stesso schema: una sezione Elly per
data, con le slide annotate.

## Contenuti

Modello di programmazione dichiarativa, logica computazionale e pratica su problemi complessi. Linguaggi trattati: **Prolog** e **Answer Set Programming**.

**Programma esteso:** introduzione al logic programming e alle basi teoriche; logica del primo ordine, semantica, stable model semantics (Gelfond-Lifschitz); modellazione in ASP; linguaggio e grounding; tecniche di codifica avanzate; programmazione in Answer Set Programming.

**Bibliografia:** dispense fornite nel materiale didattico (italiano e inglese).

**Risultati attesi:** modellare un problema in specifiche formali, implementare il codice di logica computazionale discendente dal modello, saper modellare problemi anche fuori dall'informatica.
