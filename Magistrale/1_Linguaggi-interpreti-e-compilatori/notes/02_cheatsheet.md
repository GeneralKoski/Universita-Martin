# Cheat-sheet: definizioni, formule, algoritmi

## Linguaggi formali
- Σ alfabeto, Σ\* stringhe finite, ε vuota
- Linguaggio L ⊆ Σ\*
- Linguaggi regolari = riconoscibili da DFA = denotabili da RE
- Linguaggi context-free = riconoscibili da PDA non det. = generabili da CFG

## Espressioni regolari
- Sintassi: ε, a, (e), e\*, e1·e2, e1|e2
- Estese: e+, e?, [a-z], [^a-z]
- Semantica: L: RExpr → ℘(Σ\*)
  - L(e1·e2) = L(e1)·L(e2)
  - L(e1|e2) = L(e1) ∪ L(e2)
  - L(e\*) = ⋃ᵢ₌₀^∞ L(e)ⁱ

## Automi
- **DFA** = `⟨Σ, Q, δ, q0, F⟩` con `δ: Q × Σ → Q`
- **NFA** con ε-mosse = `⟨Σ, Q, δ, q0, F⟩` con `δ: Q × (Σ ∪ {ε}) → ℘(Q)`
- **PDA** = `⟨Σ, Γ, Q, δ, q0, Z0, F⟩` (aggiunge stack)

## Pipeline RE → DFA minimo
1. **Thompson:** RE → ε-NFA (linear time, costruzione strutturale)
2. **Subset construction:** ε-NFA → DFA (stati DFA = sottoinsiemi NFA, ε-closure)
3. **Hopcroft minimization:** DFA → DFA minimo, O(|Σ|·n·log n)

## Grammatiche libere da contesto (CFG)
`G = ⟨S, N, T, P⟩` con `S ∈ N`, `P ⊆ N × (N ∪ T)*`

Forme di parsing:
- **LL(k):** top-down, look-ahead k, predittivo (no left recursion, no ambiguità su k token)
- **LR(k):** bottom-up shift-reduce, più potente (LR(1) ⊃ LL(1))
- **LALR(1):** quello di Yacc/Bison; tabelle più piccole di LR(1) canonico

**Inclusioni:** `LL(1) ⊊ LALR(1) ⊊ LR(1) ⊊ CFG non ambigue ⊊ CFG`

## FIRST e FOLLOW (algoritmo)
`FIRST(α)` = terminali che possono iniziare una derivazione di `α`, più `ε` se `α ⇒* ε`.

```
FIRST(a)     = {a}                          per a terminale
FIRST(ε)     = {ε}
FIRST(X₁…Xₙ) = FIRST(X₁) \ {ε}
               ∪ FIRST(X₂) \ {ε}   se ε ∈ FIRST(X₁)
               ∪ …                  finché ε ∈ FIRST(Xᵢ)
               ∪ {ε}                se ε ∈ FIRST(Xᵢ) per ogni i
```

`FOLLOW(A)` = terminali che possono seguire `A` in una derivazione. Punto fisso su:
```
FOLLOW(S) ⊇ {$}                                     S = simbolo iniziale
A → α B β  ⇒  FOLLOW(B) ⊇ FIRST(β) \ {ε}
A → α B    ⇒  FOLLOW(B) ⊇ FOLLOW(A)
A → α B β  con ε ∈ FIRST(β)  ⇒  FOLLOW(B) ⊇ FOLLOW(A)
```
⚠️ `ε` sta in FIRST, **mai** in FOLLOW. FOLLOW contiene `$`, FIRST no.

## Tabella di parsing LL(1)
Per ogni produzione `A → α`:
- `M[A, a] = A → α` per ogni `a ∈ FIRST(α)`
- se `ε ∈ FIRST(α)`, anche `M[A, b] = A → α` per ogni `b ∈ FOLLOW(A)`

**È LL(1) ⇔ nessuna cella contiene due produzioni**, cioè per ogni `A → α | β`:
`FIRST(α) ∩ FIRST(β) = ∅` e, se `ε ∈ FIRST(α)`, `FIRST(β) ∩ FOLLOW(A) = ∅`.

Prerequisiti sulla grammatica: **eliminare la ricorsione sinistra**, **fattorizzare a sinistra**.

## Item LR(1) e costruzione degli stati
Item = `[A → α · β, a]`: ho già riconosciuto `α`, mi aspetto `β`, con lookahead `a`.

```
closure(I): finché cambia, per ogni [A → α·Bβ, a] ∈ I e ogni B → γ
              aggiungi [B → ·γ, b] per ogni b ∈ FIRST(βa)
goto(I, X) = closure({ [A → αX·β, a] | [A → α·Xβ, a] ∈ I })
```
Stato iniziale: `closure({[S' → ·S, $]})`. **ACTION**: shift su terminale, reduce quando il dot è in fondo e il lookahead corrisponde, accept su `[S' → S·, $]`. **GOTO**: transizioni su non-terminali.

**Handle** = sottostringa riducibile nella derivazione rightmost al contrario. Il parser LR riconosce handle.

## Conflitti
| Conflitto | Significato | Rimedio |
|---|---|---|
| shift-reduce | lo stato ammette sia shift sia reduce sullo stesso lookahead | riscrivere la grammatica, o direttive di precedenza (convenzione: **vince lo shift**) |
| reduce-reduce | due riduzioni possibili nello stesso stato | quasi sempre difetto strutturale: riscrivere |

Esempio canonico di shift-reduce: **dangling else**. LALR(1) può introdurre nuovi reduce-reduce rispetto a LR(1), **mai** nuovi shift-reduce.

## Bison: precedenza e associatività
Dichiarate dopo `%token`, **precedenza crescente dall'alto in basso**:
```
%left  '+' '-'
%left  '*' '/'
%right '^'
%nonassoc UMINUS       // token fittizio, mai prodotto dal lexer
...
expr: '-' expr %prec UMINUS   // forza qui la precedenza di UMINUS
```
Risoluzione: precedenza produzione > lookahead → **reduce**; minore → **shift**; uguale → decide l'associatività.

**Due strade per la precedenza**, da saper confrontare:
| | Grammatica stratificata (`expr`/`term`/`factor`) | Grammatica piatta + direttive |
|---|---|---|
| Ambiguità | non ambigua per costruzione | ambigua, conflitti risolti fuori dalla grammatica |
| Conflitti Bison | zero | shift-reduce risolti da `%left`/`%right` |
| Costo | un non-terminale per livello, albero più profondo | leggibile, facile da estendere |

Esempi eseguibili: `5c_Esercitazione_su_analisi_sintattica/calc-2` (stratificata) vs `calc-2-prec` (piatta).

## Disambiguazione lessicale
1. **Lessema più lungo**
2. **Priorità per ordine** delle regole

## Three-address code
`x ← y op z` con singolo operatore. Rappresentazioni: quadruples, triples, indirect triples.

## SSA (Static Single Assignment)
- Ogni nome ha **una sola definizione**
- Funzioni `φ` ai punti di confluenza: `x3 ← φ(x1, x2)`
- Permette analisi efficienti (sparsa)

## CFG (Control Flow Graph)
- Nodi = basic block (sequenza max single-entry/single-exit)
- Archi = branch/fall-through
- Entry, exit nodes

## Dominators
- `d dom n` se ogni cammino entry→n passa per d
- `idom(n)` = dominator immediato (esiste unico)
- Dominator tree: padre di n = idom(n)
- Equazioni: `DOM(n0) = {n0}`, `DOM(n) = {n} ∪ ⋂_{p ∈ pred(n)} DOM(p)` per `n ≠ n0`
- **Init algoritmo iterativo:** `DOM(n) = N` (tutti i nodi) per `n ≠ n0`, poi convergenza per intersezione (max fixed point). Se inizializzi a ∅ l'algoritmo non converge correttamente.

## Live Variables (DFA backward)
```
LiveOut(exit) = ∅
LiveOut(n) = ⋃_{m ∈ succ(n)} ( UEVar(m) ∪ (LiveOut(m) \ VarKill(m)) )
```

## Reaching Definitions (DFA forward)
```
ReachIn(entry) = ∅
ReachOut(n) = Gen(n) ∪ (ReachIn(n) \ Kill(n))
ReachIn(n) = ⋃_{p ∈ pred(n)} ReachOut(p)
```

## Available Expressions (DFA forward, ⋂)
```
AvailIn(entry) = ∅
AvailOut(n)    = U  per ogni n ≠ entry  (init = universo, perché meet è ⋂)
AvailOut(n) = Expr(n) ∪ (AvailIn(n) \ Kill(n))
AvailIn(n)  = ⋂_{p ∈ pred(n)} AvailOut(p)
```
**Nota init:** con meet ⋂, l'identità del lattice (top) è l'**universo U** delle espressioni; entry parte da ∅ perché niente è "available" prima del programma. Si converge al **massimo punto fisso** rispetto a ⊑ = ⊇ (più espressioni = più informazione utile).

## Very Busy Expressions (DFA backward, ⋂)
Espressione `e` è "very busy" all'uscita di n se sarà valutata su **ogni** cammino fino all'uso (senza essere ridefinita). Usata per **code hoisting** (anticipare valutazioni → registro liberato prima).
```
VBOut(exit) = ∅;  VBIn(n) = U per n ≠ exit
VBIn(n)  = Expr(n) ∪ (VBOut(n) \ Kill(n))
VBOut(n) = ⋂_{s ∈ succ(n)} VBIn(s)
```

## Riepilogo direzione/meet delle 4 DFA classiche
| Analisi | Direz. | Meet | Init non-boundary | Punto fisso |
|---|---|---|---|---|
| Live Variables | back | ∪ | ∅ | min |
| Reaching Defs | fwd | ∪ | ∅ | min |
| Available Expr | fwd | ⋂ | U | max |
| Very Busy Expr | back | ⋂ | U | max |

## Convergenza dataflow
- Lattice `(L, ⊑)` finito + funzione di trasferimento monotona ⇒ punto fisso esiste
- **Knaster-Tarski:** monotonia su lattice completo ⇒ esistenza min/max punto fisso
- **Kleene:** se F continua, lfp(F) = ⊔ Fⁿ(⊥)

## Local Value Numbering
```
per ogni o = <op, o1, o2> in BB:
   vn1 = lookup(o1); vn2 = lookup(o2)
   h = hash(<op, vn1, vn2>)
   se h già presente: o ← reference
   se costanti: fold + replace con loadI
```

## Calling convention (System V AMD64 - esempio)
- Arg interi: rdi, rsi, rdx, rcx, r8, r9, poi stack
- Float: xmm0..xmm7
- Return: rax (e rdx per long long)
- Callee-saved: rbx, rbp, r12-r15
- Caller-saved: rax, rcx, rdx, rsi, rdi, r8-r11, xmm0-xmm15

## Activation Record (frame)
Tipico layout (cresce verso il basso):
1. Parametri (passati o salvati)
2. Return address
3. Old base pointer (saved frame ptr)
4. Saved registers (callee-saved usati)
5. Local variables
6. Temporary expression slots / spill area

## vtable (single inheritance)
- Ogni oggetto: `[ vtable_ptr | data members ]`
- vtable: array di puntatori a funzione, indicizzato per nome metodo
- Call: `obj->vtable[i](obj, args...)` (passaggio implicito di `this`)

## Domini astratti (interpretazione astratta)
| Dominio | Elementi | Costo | Precisione |
|---|---|---|---|
| Sign | {⊥, –, 0, +, ⊤} | bassissimo | bassa |
| Constant | {⊥} ∪ ℤ ∪ {⊤} | basso | media (per costanti) |
| Interval | `[a,b]` | basso | media |
| Octagon | `±x ± y ≤ c` | medio (O(n²)) | medio-alta |
| Polyhedra | `Σaᵢxᵢ ≤ b` | alto (esponenziale) | alta |

## Galois connection
`α: P → A` (astrazione), `γ: A → P` (concretizzazione)
`α(p) ⊑_A a ⇔ p ⊑_P γ(a)`
Implica: α monotona, γ monotona, α∘γ ⊑ id, id ⊑ γ∘α.

## Widening operator ∇
- `a ⊔ b ⊑ a ∇ b` (sovrapprossimazione)
- Ogni catena ascendente diventa stazionaria in tempo finito
- Esempio intervals: `[1,5] ∇ [1,7] = [1,+∞]`
