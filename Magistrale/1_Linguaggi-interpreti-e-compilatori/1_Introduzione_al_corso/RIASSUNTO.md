# 1. Introduzione al corso

## Info generali
- **Docente:** Enea Zaffanella (enea.zaffanella@unipr.it)
- **Crediti:** 9 CFU (72 ore di lezione)
- **Lingua:** italiano (materiale in italiano e inglese)
- **Modalità didattica:** in presenza, lezioni frontali + esercitazioni passive (docente) e guidate (studente)
- **Ricevimento:** su appuntamento

## Materiale didattico
- **Libro di testo:** Keith Cooper, Linda Torczon - *Engineering a Compiler*, 2nd Edition, Morgan Kaufmann, 2011 (EaC)
- Manuali/tutorial degli strumenti: Flex, Bison, Clang, LLVM
- Slide del docente + slide tratte dal libro
- Pagina Elly del corso

## Prerequisiti
- Conoscenza approfondita di un linguaggio imperativo (preferibilmente C++)
- Strutture dati e algoritmi efficienti

## Programma sintetico
1. Introduzione: interpreti e compilatori
2. Struttura di un compilatore
3. Analisi lessicale
4. Analisi sintattica
5. Analisi di semantica statica (context-sensitive)
6. Rappresentazioni intermedie (IR)
7. Generazione del codice
8. Analisi e ottimizzazione della IR (middle end)
9. Introduzione all'interpretazione astratta

## Modalità di esame ⚠️ (sito UniPR + mail del docente)
L'esame è in **due parti separate**:
1. **Seminario (prerequisito):** presentazione con slide ~15 min + Q&A sull'argomento. Argomento + materiale a supporto **concordati col prof almeno 30 gg prima** della data del seminario. **Una volta svolto, dà accesso a tutti gli appelli dell'anno accademico.**
2. **Orale:** domande aperte su tutto il programma, nella data dell'appello.

**Valutazione: 30% seminario + 70% orale.**

- Il docente consiglia di fissare un appuntamento (anche da remoto via Teams) per parlare dell'argomento.
- Riferimento ufficiale: https://corsi.unipr.it/it/ugov/degreecourse/329435

## Note aggiuntive
- Il corso ha forte componente teorica (linguaggi formali, automi, dataflow) e pratica (Flex, Bison, LLVM)
- Le esercitazioni di laboratorio (cartelle 5 e 6) sono parte integrante: il lexer C++ basato su Flex e il mini-linguaggio TinyP coprono praticamente tutto il front end
- Conviene leggere in parallelo la slide del docente (in italiano) e quelle tratte da EaC (in inglese) - coprono lo stesso argomento da angoli leggermente diversi

## Punti chiave per l'orale
Questo capitolo non contiene materia d'esame in senso stretto, ma la **mappa** su cui appoggiare tutto il resto. Serve a due cose concrete durante il colloquio:

- **Saper enunciare la scaletta delle 9 macro-aree in ordine** (interpreti/compilatori → struttura → lessicale → sintattica → semantica statica → IR → generazione codice → middle end → interpretazione astratta). Ti dà un modo per aprire una risposta collocando l'argomento nella pipeline invece di partire a freddo dai dettagli, e ti permette di seguire il prof quando salta da una parte all'altra del programma
- **Sapere quale formalismo abita ogni fase**: RE/automi nel lessicale, CFG/PDA nella sintassi, algoritmi ad-hoc nella semantica statica, punto fisso e approssimazione nel middle end. È la chiave di lettura di tutto il corso: ogni fase è una coppia *specifica dichiarativa* + *implementazione operativa*
- **Citare correttamente il libro di testo**: Cooper & Torczon, *Engineering a Compiler*, 2ª ed., 2011 (EaC). Non è il Dragon Book, che è il riferimento classico ma non quello adottato
- Le parti **teorica** e **pratica** del corso sono pensate in coppia: per ogni tecnica esiste uno strumento visto in esercitazione (Flex, Bison, TinyP, clang-tidy, `opt`). Avere pronto lo strumento corrispondente a ogni argomento è il modo più rapido di dimostrare di aver seguito
