# 01 - Introduction

Fonte: `01 - Introduction.pdf`

## Il docente e il corso
- Corso: **Static analysis and software verification**, Vincenzo Arceri (UniPR).
- Percorso del docente, tutto sulla **static analysis** (analisi statica): JavaScript (triennale, Verona), PHP (magistrale, Verona), codice self-modifying in JavaScript (PhD, Verona), string static analysis per linguaggi dinamici e smart contract blockchain (post-doc, Ca' Foscari), poi a Parma (2021-2026) analisi statica di software blockchain, linguaggi dinamici e software di data science.
- Word cloud delle keyword di ricerca: dominano **Analysis**, **Static**, **Abstract**, **String**, **Domain**, **Dynamic**, **Interpreter**, **Blockchain**, Smart Contracts, Program, Code.

## Libri di riferimento
- **Principles of Program Analysis** - F. Nielson, H. R. Nielson, C. Hankin (Springer 2004). Panoramica dei quattro approcci principali alla program analysis:
  - **data flow analysis**
  - **constraint-based analysis**
  - **abstract interpretation** (interpretazione astratta)
  - **type and effect systems**
- **Introduction to Static Analysis: An Abstract Interpretation Perspective** - X. Rival, K. Yi (MIT Press 2020). Introduzione autocontenuta all'analisi statica basata su abstract interpretation.
- **Principles of Abstract Interpretation** - P. Cousot (MIT Press 2021). "La bibbia": tutti i concetti informatici e matematici dell'abstract interpretation, con applicazioni a semantica, specifica, verifica e analisi statica.

## Software reliability
- **Reliability** (IEEE 610.12-1990): "the **ability** of a system or component to perform its required functions under stated conditions for a specified **period of time**".
- **Software Reliability Management** (IEEE 982.1-1988): processo di **ottimizzazione dell'affidabilità** del software tramite un programma che enfatizza prevenzione degli errori, individuazione e **rimozione** dei fault e uso di misure per massimizzare l'affidabilità, compatibilmente con i vincoli di progetto (risorse, tempi, prestazioni).
- Da queste definizioni, la software reliability consiste di tre attività:
  1. **Error prevention**
  2. **Fault detection and removal**
  3. **Measurements** per massimizzare l'affidabilità, in particolare misure a supporto delle prime due

## Perché la software verification è importante
- I bug software costano all'economia USA circa **60 miliardi $ l'anno** (0,6% del PIL).
- **La sicurezza è una necessità**: la perdita economica mondiale dovuta a tutte le forme di attacco è circa **250 miliardi $**.
- I difetti software rendono la programmazione "so painful".

### Casi storici
**Ariane 5 Flight 501 (1996)**
- Esploso 37 secondi dopo il decollo, autodistrutto a causa di un bug. Costo: 370.000.000 $.
- Il codice mostrato (sintassi Ada):

```ada
horizontal_veloc_bias: integer;
horizontal_veloc_sensor: float;
-- ...
pragma suppress(numeric_error, horizontal_veloc_bias);
sensor_get(horizontal_veloc_sensor);
horizontal_veloc_bias := integer(horizontal_veloc_sensor);
-- ...
```

- Causa: **overflow** nella conversione da float a 64 bit a intero con segno a 16 bit. Il `pragma suppress(numeric_error, ...)` disattiva il controllo dell'errore numerico su quella variabile.

**Pentium FDIV bug (1994)**
- Divisione floating-point sbagliata nell'hardware. Costo: 475.000.000 $.
- Esempio: $\frac{4195835}{3145727} = 1.333739$ (risultato riportato nella slide), con errore dello 0,006%.

**CrowdStrike Faulty Update (2024)**
- Oltre 5000 voli cancellati, impatto su banche, governi, sanità. Costo stimato: 5.400.000.000 $.
- La slide mostra un crash dump: `Access violation`, tentativo di lettura dall'indirizzo `0x000000000000009c` (evidenziato anche come `READ_ADDRESS`), cioè un accesso a memoria non valida.

### Vulnerabilità di sicurezza ("A lot more!")
Collage di articoli, ognuno associato a una classe di vulnerabilità:
- **Equifax** (2017, "worst hacks of 2017" secondo Wired): dati personali di 145,5 milioni di persone esposti. Causa: **out-of-date vulnerable dependency** (dipendenza obsoleta e vulnerabile).
- **eBay** (2014): richiesta a tutti gli utenti di cambiare password. Causa: **cross-site scripting (XSS) vulnerability**.
- **TalkTalk** (2015-2016): costo 42 milioni £, multa record di 400k £. Causa: **SQL injection**, tecnica nota da quasi 20 anni.
- Hack da oltre 50 milioni $ nel mondo delle valute virtuali (NYT DealBook). Causa: **reentrancy vulnerability**.

### Trend
- **Nuovi CVE per anno** (fonte: CVE program): crescita da circa 1.500 nel 1999 a quasi 29.000 nel 2023; il 2024 è a circa 26.000 (barra in rosso).
- **Vulnerabilità open-source per linguaggio** (2009-2018 vs 2019): C 47% / 30%, C++ 6% / 9%, Java 11% / 15%, JavaScript 10% / 10%, PHP 15% / 27%, Python 6% / 5%, Ruby 5% / 4%. C ha ancora il primato per l'enorme volume di codice scritto in C.

## Validation vs Verification
- **Validation**: il sistema soddisfa i bisogni reali dell'utente? *"Are we building the right software?"*
- **Verification**: il sistema soddisfa le specifiche dei requisiti? *"Are we building the software right?"*
- Schema:

```
Collected requirements (informal) → SW specs → System
|------------ Validation -----------|
                                    |---- Verification ----|
```

- **Validation** copre il passaggio requisiti informali → specifiche (es. usability testing, user feedback, requirement engineering).
- **Verification** copre il passaggio specifiche → sistema (es. testing, inspections, **static analysis**).

### Esempio: risposta dell'ascensore
- Specifica **validabile ma non verificabile**: se un utente preme il pulsante al piano $i$, un ascensore disponibile deve arrivare al piano $i$ **in un tempo ragionevole**.
- Specifica **verificabile**: se un utente preme il pulsante al piano $i$, un ascensore disponibile deve arrivare al piano $i$ **entro 30 secondi**.
- Morale: per verificare serve una specifica precisa, non vaga.

## Software verification
Il compito è verificare un'affermazione di correttezza su un programma:
- **Functional correctness**: il programma offre esattamente i servizi descritti nel documento di specifica.
- **Absence of non-functional errors** (non *cosa* fa il programma, ma *come*):
  - rispetto dei vincoli di spazio/tempo
  - assenza di **run-time errors**
  - rispetto dei vincoli di sicurezza
- Nel corso "verifica" si intende in **senso forte**: si cercano **garanzie**.

## Bad news: there's no silver bullet
Non ci si può aspettare un metodo di verifica che sia contemporaneamente:
- **Automatic**: non richiede interazione umana
- **Powerful**: capace di dimostrare proprietà non banali
- **Sound** (corretto): non dimostra mai la proprietà se questa non vale
- **Complete** (completo): dimostra sempre la proprietà se vale, cioè non manca mai di dichiarare corretto un programma corretto

**Teorema di Rice**: tutte le proprietà non banali del comportamento dei programmi in un linguaggio **Turing-completo** sono **indecidibili**.

**Undecidability** di una proprietà significa che **non esiste un metodo di verifica automatico che sia sia sound sia complete**.

### "You can't always (ever) get what you want"
```
Program  ─┐
          ├─→ [Decision procedure] ─→ Yes / No
Property ─┘
```
- Una procedura di decisione che, dati programma e proprietà, risponda sempre Yes/No non esiste.
- Le proprietà comportamentali sono indecidibili: **l'halting problem può essere incorporato in quasi ogni proprietà di interesse**.

### A cosa rinunciare?
| Proprietà | Scelta |
|---|---|
| **Soundness** | mai ("no way!") |
| **Powerful** | il più possibile |
| **Automatic** | vi rinunciano deductive verification / interactive theorem proving (fuori dal corso) |
| **Completeness** | difficile o addirittura impossibile da ottenere (ripresa più avanti nel corso) |

Quindi l'approccio del corso: analisi **automatiche e sound**, il più potenti possibile, accettando di perdere **completeness**.

## Dynamic analysis vs Static analysis
**Dynamic analysis**
- Il programma $P$ viene eseguito su un sottoinsieme finito di input (nella figura: 1, 2, 3 su $0, 1, 2, 3, 4, \dots$); il dynamic analyzer risponde **Yes / No**.
- Corretta rispetto a un **insieme finito e concreto di input** e a un programma (es. **testing**, **fuzzing**).

**Static analysis**
- Il programma $P$ viene considerato su **tutti** gli input $0, 1, 2, 3, 4, \dots$; lo static analyzer risponde **Yes / No / Maybe**.
- Corretta rispetto a **tutti gli input** e a un programma, ma **può perdere precisione**: la risposta "Maybe" è dove si vede la rinuncia alla completeness.

## Obiettivi e organizzazione
- **Course goal**: capire le tecniche di base per sviluppare analisi statiche di programmi.
- **Seminari** di ospiti: Greta Dolcetti (IBM), Isabella Mastroeni (UniVR), Caterina Urban (INRIA), Roberto Bagnara (UniPR), Pietro Ferrara (ex IBM, UniVE), altri da definire.
- Contatti: e-mail `vincenzo.arceri@unipr.it`, ricevimento su appuntamento via email, materiale e avvisi sulla pagina Elly del corso.
- **Exam** (come scritto nella slide): "Seminar (1+ paper discussion) and oral exam", cioè un seminario con discussione di almeno un paper e un esame orale. Dettagli (pesi, modalità) non indicati.

## Da ricordare
- **Validation** = "building the right software" (requisiti → specifiche); **Verification** = "building the software right" (specifiche → sistema). La static analysis è una tecnica di verification.
- Una specifica verificabile deve essere precisa (ascensore: "tempo ragionevole" vs "entro 30 secondi").
- Software verification = functional correctness + assenza di errori non funzionali (spazio/tempo, run-time errors, sicurezza); nel corso si cercano **garanzie**.
- Le quattro qualità desiderate: **automatic**, **powerful**, **sound** (mai dimostrare il falso), **complete** (dimostrare sempre il vero).
- **Teorema di Rice**: ogni proprietà non banale del comportamento dei programmi in un linguaggio Turing-completo è indecidibile; quindi nessun metodo automatico è sia sound sia complete (l'halting problem si "annida" in quasi ogni proprietà).
- Scelta del corso: la **soundness non si sacrifica mai**, si sacrifica la **completeness**; l'automazione la si abbandona solo in deductive verification/theorem proving (fuori corso).
- **Dynamic analysis**: insieme finito di input, risposte Yes/No (testing, fuzzing). **Static analysis**: tutti gli input, risposte Yes/No/**Maybe** (perdita di precisione).
- I quattro approcci classici alla program analysis: data flow analysis, constraint-based analysis, abstract interpretation, type and effect systems.
- Esempi-simbolo: Ariane 5 (overflow float 64 bit → int 16 bit), Pentium FDIV, CrowdStrike (lettura da indirizzo non valido), vulnerabilità come dipendenze obsolete, XSS, SQL injection, reentrancy.
