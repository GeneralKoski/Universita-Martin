# 5b. Analisi sintattica

Sezione "Analisi sintattica" di Elly (scaricata l'11/08/2026). Il docente non ha slide proprie su questo argomento: usa direttamente quelle tratte da *Engineering a Compiler*, in due formati.

⚠️ **La fonte da leggere per prima non è in questa cartella: è [`../notes/08_parsing.md`](../notes/08_parsing.md)** (~670 righe, italiano). È la sintesi che dà la struttura; queste slide sono il dettaglio in cui si annega se le apri a freddo. Ordine corretto: prima il file di note, poi le slide di questa cartella per riempire i punti in cui esiti.

## Contenuto della cartella

Due serie parallele sullo stesso materiale:

| pptx (con animazioni) | pdf `-1up` (stampabile) | Argomento | Dove sta in `08_parsing.md` |
|---|---|---|---|
| `08-Introduction_to_Parsing` (26) | `L10ParseIntro-1up` (26 pag) | CFG, derivazioni, parse tree, ambiguità | §1 |
| `09-Top_down_Parsing_I` (26) | `L11TopDown-1up` (28 pag) | Parsing top-down, backtracking, ricorsione sinistra | §2, §3 |
| `10-Top_down_Parsing_II...LL_(1)` (23) | `L12TopDownII-1up` (27 pag) | Discesa ricorsiva, FIRST/FOLLOW, tabelle LL(1) | §3 |
| `11-Bottom_up_ParsingI` (41) | `L13Transition-1up` (29 pag) | Passaggio a bottom-up, shift-reduce, handle | §4 |
| `12-LR_Parsers_I` (41) | `L14LRParsers-1up` (55 pag) | Item LR(1), `closure()`/`goto()`, tabelle ACTION/GOTO | §4, §5 |
| `14-Parsing_Wrap_up` (20) | — | Riepilogo e confronto finale LL vs LR | §2, §8 |

Note sulla numerazione:
- La serie EaC salta la **13**: non è un file mancante, su Elly non c'è
- Il **wrap-up esiste solo in pptx**, senza controparte pdf
- I conteggi pagine/slide differiscono fra le due serie perché il pdf è la versione senza build incrementali. Il contenuto è lo stesso: scegli un formato e resta su quello

## Come usare le due serie

- **pdf `-1up`**: da leggere di fila, è il formato giusto per lo studio e per annotare
- **pptx**: utili solo su due cose, dove l'animazione *è* il contenuto - la costruzione passo-passo della tabella LL(1) e l'esecuzione shift-reduce di un parser LR sullo stack. Se ti perdi su quelle, apri il pptx e clicca

## Collegamento con l'esercitazione

La cartella [`../5c_Esercitazione_su_analisi_sintattica/`](../5c_Esercitazione_su_analisi_sintattica/RIASSUNTO.md) contiene `Bison.pdf` e sei parser funzionanti che implementano quello che qui è teoria. Va fatta **dopo** questa, non insieme.

## Punti chiave per l'orale

- **Gerarchia e trade-off LL vs LR**: LL(1) è top-down predittivo, richiede grammatiche senza ricorsione sinistra e fattorizzate; LR(1) è bottom-up shift-reduce e **rinvia la decisione** al momento della riduzione, quindi accetta strettamente più grammatiche. È il punto del wrap-up e la domanda 10 di `04_domande_tipo.md`
- **FIRST e FOLLOW**: saperli calcolare a mano, non solo definire. La grammatica delle espressioni (`E → T E'`, ecc.) è l'esercizio canonico, già svolto nella domanda 14 con la traccia di risposta
- **Item LR(1) e insieme canonico degli stati**: cosa sono `closure()` e `goto()`, e come da lì nascono le tabelle ACTION e GOTO
- **I due conflitti**: shift-reduce (il dangling-else è l'esempio da avere pronto) e reduce-reduce. Cosa significano in termini di stato del parser e come si risolvono - riscrivendo la grammatica oppure con le direttive di precedenza
- **Specifica vs implementazione, di nuovo**: come il lessicale è RE (specifica) + DFA (implementazione), il sintattico è CFG (specifica) + automa a pila (implementazione). È la simmetria che il prof cerca
- ⚠️ **Parse tree ≠ AST**: il parse tree contiene tutti i non-terminali della derivazione, l'AST butta via l'informazione che serviva solo a parsare
