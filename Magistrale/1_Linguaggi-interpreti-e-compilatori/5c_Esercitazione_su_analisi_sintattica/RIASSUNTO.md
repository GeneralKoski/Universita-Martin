# 5c. Esercitazione su analisi sintattica (Bison)

Sezione "Esercitazione su analisi sintattica" di Elly (scaricata l'11/08/2026). È il gemello dell'esercitazione sul lexer: là Flex, qui Bison.

- `Bison.pdf` - slide del docente (Beamer): token, attributi, `%union`, associatività e precedenza, produzioni e azioni semantiche
- Sei progetti compilabili, estratti da `bison.zip`

## I sei esempi, in ordine

Non sono sei esempi indipendenti: sono **una progressione**, ognuno aggiunge una cosa al precedente. Va seguita in quest'ordine.

| # | Cartella | Cosa aggiunge |
|---|---|---|
| 1 | `calc-1/` | Solo il **riconoscitore**: la grammatica delle espressioni infisse senza azioni semantiche. Accetta o rifiuta, non calcola |
| 2 | `calc-2/` | **Interprete**: aggiunge `%union`, attributi tipizzati (`%token <d> NUMBER`, `%type <d> expr`) e azioni `{ $$ = $1 + $3; }`. La precedenza è codificata nella **struttura della grammatica**, stratificata in `expr` / `term` / `factor` |
| 3 | `calc-2-prec/` | Stesso interprete, **grammatica piatta e ambigua** (`expr: expr '+' expr \| expr '*' expr \| ...`) più le direttive `%left '+' '-'`, `%left '*' '/'`, `%right '^'`, `%nonassoc UMINUS`. Aggiunge `^` e l'unario con `%prec UMINUS` |
| 4 | `calc-3/` | **Compilatore**: traduce da infissa a RPN invece di valutare. Stessa grammatica, azioni semantiche diverse |
| 5 | `calc-3-rpn/` | **Interprete del linguaggio target**: valuta espressioni RPN |
| 6 | `Wait/` | Grammatica minimale artificiale, senza azioni: `S → A \| B`, `A → a \| ( A )`, `B → b \| ( B >` |

### I tre confronti che valgono l'esame

**`calc-2` vs `calc-2-prec`** è il confronto più importante di tutta l'esercitazione, ed è una domanda d'orale quasi obbligata. Due modi di ottenere lo stesso risultato:

- *Grammatica stratificata* (`calc-2`): la precedenza è una proprietà **strutturale**, la grammatica è non ambigua per costruzione, Bison non segnala conflitti. Costo: un livello di non-terminali per ogni livello di precedenza, quindi grammatica più grossa e parse tree più profondo
- *Grammatica piatta + direttive* (`calc-2-prec`): la grammatica **è ambigua** e genera conflitti shift-reduce, che `%left`/`%right`/`%nonassoc` risolvono dichiarativamente. Più leggibile e più facile da estendere (`^` e l'unario sono due righe), ma dipende da una risoluzione esterna alla grammatica

`%prec UMINUS` è il trucco del token fittizio: la produzione `'-' expr` erediterebbe la precedenza di `'-'` binario, che è troppo bassa; `%prec` gliene assegna un'altra senza che quel token compaia mai nell'input.

**`calc-3` + `calc-3-rpn`** insieme sono la dualità interprete/compilatore del capitolo 2 resa concreta e piccola: `calc-3` traduce L → M, `calc-3-rpn` è l'interprete di M. Esempio da citare quando il prof chiede "perché alla fine serve sempre un interprete".

**`Wait/`** è costruita ad arte per mostrare l'espressività di LR contro LL, che sul programma ufficiale è la voce "confronto top-down vs bottom-up". Per decidere se sta parsando una `A` o una `B` il parser deve superare un prefisso di `(` **di lunghezza arbitraria** e arrivare al `)` o al `>`: nessun LL(k) ce la fa con lookahead fisso, mentre LR rinvia la scelta al momento della riduzione. Di qui il nome.

⚠️ Non ho potuto verificare il report di Bison su questa grammatica (bison non è installato sulla macchina Windows): **fallo durante il laboratorio** con `bison --report=all`, guarda `parser.output` e verifica se ci sono conflitti e di che tipo. È esattamente il genere di osservazione concreta che vale all'orale.

## Build

Serve **flex + bison + g++** (sulla macchina Windows bison manca).

```bash
cd calc-2 && make        # produce ./calc
echo "2+3*4" | ./calc    # eval: 14
make clean
```

Il `Makefile` di ogni `calc-*` passa `--report=all` a Bison: dopo il build guarda **`calc.output`**, che contiene gli stati LR, gli item, le tabelle e l'elenco dei conflitti. È il modo più diretto per vedere in concreto la teoria di `5b_`.

`Wait/` ha un Makefile diverso (`lexer.ll` + `parser.yy` → `./parser`) perché usa l'interfaccia yacc classica senza attributi.

## Punti chiave per l'orale

- **Struttura di un file Bison**: prologo `%{ %}`, dichiarazioni (`%union`, `%token`, `%type`, precedenze), `%%`, regole con azioni, `%%`, epilogo. Sapere cosa sono `$$`, `$1`, `$3` e da dove vengono i tipi
- **Le due strade per la precedenza** (grammatica stratificata vs direttive) con i rispettivi costi - vedi sopra, è il confronto `calc-2`/`calc-2-prec`
- **`%prec` e i token fittizi**: a cosa servono, con l'unario meno come esempio
- **Chi fa cosa nella coppia Flex/Bison**: il lexer restituisce il codice del token e riempie `yylval`, il parser consuma la sequenza di token e costruisce/valuta. `calc.hh` è l'interfaccia condivisa
- **`calc.output` esiste**: sapere che Bison sa mostrarti stati e conflitti, e averlo guardato, distingue chi ha fatto l'esercitazione da chi l'ha letta
- **Stessa grammatica, azioni diverse = interprete o compilatore** (`calc-2` vs `calc-3`): la grammatica descrive la sintassi, la semantica sta nelle azioni
