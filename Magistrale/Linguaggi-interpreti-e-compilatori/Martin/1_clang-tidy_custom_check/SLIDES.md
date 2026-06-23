---
marp: true
theme: default
paginate: true
size: 16:9
header: 'clang-tidy custom check · misc-no-printf'
footer: 'Martin Trajkovski · Linguaggi, Interpreti e Compilatori · A.A. 2025/26'
style: |
  :root {
    --blu-scuro: #14365c;
    --blu: #2e6da4;
    --blu-chiaro: #cfe2f3;
    --rosso: #d9534f;
    --verde: #4a9d5b;
    --grigio-testo: #3a4654;
    --grigio-soft: #6b7785;
  }
  section {
    font-family: "Helvetica Neue", "Arial", sans-serif;
    font-size: 22px;
    color: var(--grigio-testo);
    padding: 48px 60px 56px 60px;
    background: #ffffff;
  }
  h1 {
    color: var(--blu-scuro);
    font-weight: 700;
    margin-bottom: 0.15em;
    letter-spacing: -0.01em;
  }
  h1::after {
    content: "";
    display: block;
    width: 56px;
    height: 4px;
    background: var(--rosso);
    border-radius: 2px;
    margin-top: 10px;
  }
  h2 { color: var(--blu); font-weight: 600; margin-bottom: 0.3em; }
  h3 { color: var(--blu); margin-bottom: 0.2em; font-weight: 600; }
  ul, ol { margin: 0.35em 0; }
  li { margin: 0.22em 0; }
  p { margin: 0.45em 0; }
  strong { color: var(--blu-scuro); }
  em { color: var(--grigio-soft); }
  .lead {
    font-size: 0.92em;
    color: var(--grigio-soft);
    font-style: italic;
    margin: 0.1em 0 0.7em 0;
    border-left: 3px solid var(--blu-chiaro);
    padding-left: 0.7em;
  }
  code, pre {
    font-family: "JetBrains Mono", "Fira Code", "Menlo", monospace;
  }
  pre {
    font-size: 0.7em;
    line-height: 1.4;
    background: #f7f9fb;
    border: 1px solid #e3e9f0;
    border-left: 3px solid var(--blu);
    padding: 0.6em 1em;
    border-radius: 6px;
    margin: 0.45em 0;
  }
  code {
    background: #eef2f7;
    color: var(--blu-scuro);
    padding: 0.1em 0.35em;
    border-radius: 4px;
    font-size: 0.92em;
  }
  blockquote {
    border-left: 4px solid var(--rosso);
    background: #fdf6f5;
    color: #4a3a3a;
    font-style: italic;
    padding: 0.5em 0.9em;
    margin: 0.5em 0;
    border-radius: 0 6px 6px 0;
  }
  table {
    font-size: 0.76em;
    border-collapse: collapse;
    margin: 0.5em 0;
    width: 100%;
  }
  th { background: var(--blu); color: white; padding: 0.4em 0.7em; text-align: left; }
  td { border: 1px solid #e3e9f0; padding: 0.3em 0.6em; }
  tr:nth-child(even) td { background: #f7f9fb; }
  .ok { color: var(--verde); font-weight: 700; }
  .no { color: var(--rosso); font-weight: 700; }
  section.cover {
    background: linear-gradient(135deg, #0e2842 0%, #2e6da4 100%);
    color: white;
    text-align: center;
    justify-content: center;
  }
  section.cover h1 { color: white; font-size: 2em; }
  section.cover h1::after { margin: 14px auto 0 auto; background: var(--blu-chiaro); }
  section.cover h2 { color: var(--blu-chiaro); font-weight: 400; font-size: 1.05em; }
  section.cover code {
    background: rgba(255, 255, 255, 0.16);
    color: white;
  }
  section.cover p { color: #e8f1fa; }
  section.cover header, section.cover footer { color: #9db8d0; }
  section.divider {
    background: linear-gradient(135deg, #14365c 0%, #2e6da4 100%);
    color: white;
    justify-content: center;
  }
  section.divider h1 { color: white; font-size: 1.7em; }
  section.divider h1::after { background: var(--blu-chiaro); }
  section.divider p { color: var(--blu-chiaro); }
  header { font-size: 0.52em; color: #aab4c0; }
  footer { font-size: 0.52em; color: #aab4c0; }
  .flow {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 9px;
    font-family: "JetBrains Mono", "Fira Code", "Menlo", monospace;
    font-size: 14px;
    margin: 22px 0 8px 0;
    flex-wrap: nowrap;
  }
  .flow .box {
    border: 2px solid #9aa6b3;
    background: #f7f9fb;
    padding: 9px 11px;
    border-radius: 8px;
    text-align: center;
    line-height: 1.25;
    white-space: nowrap;
    box-shadow: 0 1px 2px rgba(0,0,0,0.04);
  }
  .flow .box.ours {
    border-color: var(--rosso);
    background: #fdf2f2;
    font-weight: 600;
    color: var(--blu-scuro);
  }
  .flow .box.out {
    border-color: var(--verde);
    background: #f1f8f3;
  }
  .flow .arr { color: var(--blu); font-size: 1.4em; font-weight: 700; }
  .flow-caption {
    text-align: center;
    font-size: 0.78em;
    color: var(--grigio-soft);
    margin: 0 0 12px 0;
  }
  .pill {
    display: inline-block;
    background: var(--blu-chiaro);
    color: var(--blu-scuro);
    font-size: 0.72em;
    font-weight: 600;
    padding: 0.15em 0.6em;
    border-radius: 999px;
    margin-bottom: 0.4em;
  }
---

<!-- _class: cover -->

# Un check `clang-tidy` da zero

## Costruzione, test e integrazione di un linter C++ che capisce il codice, non solo il testo

Martin Trajkovski
*Linguaggi, Interpreti e Compilatori · A.A. 2025/26*

---

## Il problema

<p class="lead">Tutto nasce da un fastidio concreto in code review.</p>

> "Continuo a vedere `printf` in C++ moderno. Vorrei che il CI me lo segnali da solo, con il fix già pronto."

- I pattern che si ripetono andrebbero **controllati dalla macchina**, non dall'occhio umano
- Ma gli strumenti testuali (`grep`, espressioni regolari) leggono **caratteri**, non significato: si perdono o sbagliano appena entrano in gioco **scope, template, macro**
- Serve uno strumento che ragioni su **tipi e contesto**, come fa il compilatore

<p class="lead">Lo strumento esiste già: si chiama clang-tidy. Vediamo com'è fatto dentro.</p>

---

## Architettura di clang-tidy

<p class="lead">Il compilatore non è una scatola chiusa: è una libreria su cui possiamo agganciarci.</p>

<div class="flow"><div class="box">codice.cpp</div><div class="arr">→</div><div class="box">clang<br>frontend</div><div class="arr">→</div><div class="box">AST<br>+ semantica</div><div class="arr">→</div><div class="box ours">AST<br>matchers</div><div class="arr">→</div><div class="box ours">check</div><div class="arr">→</div><div class="box out">diagnostica<br>+ fix-it</div></div>

<div class="flow-caption">in <span style="color:#d9534f"><b>rosso</b></span>: gli unici due pezzi che scrivo io · tutto il resto è infrastruttura Clang</div>

- Il **frontend** di Clang trasforma il sorgente in un **AST** (l'albero della struttura del programma) già arricchito di **semantica**: tipi risolti, overload scelti, template istanziati
- Io scrivo solo i **matcher** (quali nodi cercare) e il **check** (cosa fare quando li trovi)

---

## Cos'è l'AST, in 4 righe

<p class="lead">AST = Abstract Syntax Tree, l'albero che rappresenta la struttura del programma.</p>

```bash
echo 'int x = (int)3.14;' | clang -x c++ -Xclang -ast-dump -fsyntax-only -
```

```
TranslationUnitDecl
└── VarDecl 'x' 'int'                        ← dichiarazione di variabile
    └── CStyleCastExpr 'int' <FloatingToIntegral>   ← il cast, con tipo
        └── FloatingLiteral 'double' 3.14    ← il valore 3.14
```

Il cast non è la stringa `"(int)"`: è un **nodo tipato** che sa di trasformare un `double` in un `int`. È su questo livello, non sul testo, che ragionano i check.

---

## Gli AST Matchers: un piccolo linguaggio per cercare nodi

<p class="lead">DSL = Domain-Specific Language, un mini-linguaggio dedicato a un solo compito.</p>

```cpp
// "ogni chiamata a una funzione il cui nome è ::printf"
callExpr(callee(functionDecl(hasName("::printf"))))

// "ogni metodo virtuale che non è un override"
cxxMethodDecl(isVirtual(), unless(isOverride()))
```

Si legge come una frase, dall'esterno verso l'interno, e si compone come un albero. È **dichiarativo**: descrivi *cosa* cercare, non *come* visitare l'albero. Molto più conciso che scrivere a mano un visitatore ricorsivo.

---

## Anatomia di un check

<p class="lead">Ogni check è una classe C++ con due soli "agganci".</p>

```cpp
class NoPrintfCheck : public ClangTidyCheck {
public:
  NoPrintfCheck(StringRef N, ClangTidyContext *C)
    : ClangTidyCheck(N, C) {}
  void registerMatchers(MatchFinder *F) override;   // QUALI nodi cerco
  void check(const MatchFinder::MatchResult &R) override;  // COSA faccio
};
```

È piccola di proposito: tutta la complessità (parsing, type checking, name resolution) la gestisce il driver di Clang. Io mi concentro solo sulla regola.

---

## Il nostro check: `misc-no-printf`

<p class="lead">Una regola minimale ma non banale, scelta apposta per toccare i casi difficili.</p>

**Cosa fa:**
- segnala le chiamate a `::printf` di libc (la `printf` "vera", del C)
- **non** segnala `mylib::printf`: è un'altra funzione, sta in un altro **scope**
- emette un **fix-it**: sostituisce il nome con `std::print` (il rimpiazzo type-safe di C++23)

**Perché è un buon esempio didattico:**
- il matcher è di poche righe, ma deve gestire **scope, macro, template**
- il fix-it è chirurgico: tocca solo il nome, non l'intera chiamata

---

## `registerMatchers`: dichiaro cosa cercare

<p class="lead">Il cuore del check sta tutto in questo singolo matcher.</p>

```cpp
void NoPrintfCheck::registerMatchers(MatchFinder *F) {
  F->addMatcher(
    callExpr(
      callee(functionDecl(hasName("::printf"))),
      unless(isExpansionInSystemHeader())   // ignora gli header di sistema
    ).bind("printfCall"),
    this);
}
```

- `hasName("::printf")` aggancia il nome **globale e qualificato** → nessuna collisione con `printf` definite dall'utente
- `unless(isExpansionInSystemHeader())` evita di segnalare codice che non è nostro (es. dentro `<cstdio>`)

---

## `check`: produco diagnostica e fix-it

<p class="lead">Quando un nodo matcha, questa funzione viene chiamata e genera l'avviso.</p>

```cpp
void NoPrintfCheck::check(const MatchFinder::MatchResult &R) {
  const auto *Call = R.Nodes.getNodeAs<CallExpr>("printfCall");
  const Expr *Callee = Call->getCallee()->IgnoreImpCasts();
  diag(Callee->getBeginLoc(),
       "uso di 'printf' sconsigliato; usare 'std::print'")
    << FixItHint::CreateReplacement(
         SourceRange(Callee->getBeginLoc(), Callee->getEndLoc()),
         "std::print");
}
```

`FixItHint::CreateReplacement` sostituisce **solo** il token `printf` con `std::print`: il fix è applicabile in automatico, su mille file, a ogni PR.

---

<!-- _class: divider -->

# Demo

## Dagli esempi piccoli al progetto reale, e il confronto con gli LLM

---

## Demo 1: esempi mirati + confronto con gli LLM

<p class="lead">Prima dimostro che il check "capisce" davvero scope e overload, poi lo metto contro due LLM.</p>

```bash
clang-tidy -checks='-*,misc-no-printf' snippets/02_namespace_collision.cpp
# → 1 hit: SOLO ::printf, ignora mylib::printf

clang-tidy -checks='-*,misc-no-printf' snippets/06_using_template_alias.cpp
# → 1 hit: l'overload resolution dirotta ::printf("...", int) al template
```

Confronto: **6 snippet × {Claude Opus 4.7, ChatGPT 5.5} × 2 chat fresche = 24 run**

| | clang-tidy | Claude | ChatGPT |
|---|---|---|---|
| Determinismo | <span class="ok">100%</span> | alto su 5/6 | medio |
| Fix primario = `std::print` | sì | 4/6 | <span class="no">0/6</span> |
| Snippet 06 (overload res.) | sempre 1 hit | 1ª ✓ / 2ª ✗ | 1ª ✗ / 2ª ✓ |
| Bug fuori scope (`2.5→2`) | non visto | trovato ⭐ | trovato ⭐ |

> **Il risultato più netto:** stesso modello, due chat identiche → interpretazioni **opposte** dello stesso codice.

---

## Demo 2: su progetti veri

<p class="lead">Gli esempi piccoli convincono poco: ecco lo stesso check su codebase reali.</p>

**Caso A · `bear_demo` (build con Make):**
```bash
bear -- make            # "registra" la build e produce compile_commands.json
clang-tidy -p . main.cpp logger.cpp net.cpp util.cpp
# → 5/5 hit, 0 falsi positivi
```

**Caso B · `tinyxml2` (libreria reale da GitHub, build CMake):**
```bash
cmake -B build -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
clang-tidy -p build --extra-arg=-isysroot $(xcrun --show-sdk-path) \
  tinyxml2.cpp xmltest.cpp
# → 28 hit in 0.2s
```

> **Il numero da ricordare:** `grep printf` → **42** match · clang-tidy → **28**.
> I 14 di scarto sono commenti, stringhe, `vfprintf`/`snprintf`, macro. *Quello* è il valore dell'AST.

---

## Test, documentazione, integrazione

<p class="lead">Un check serio non è solo codice: è anche test riproducibili e integrazione in CI.</p>

- **Test in stile lit** (il framework di test di LLVM): `RUN: %check_clang_tidy %s misc-no-printf %t`, gira dentro la build farm ufficiale, verifica messaggi *e* fix applicato
- **Documentazione** in `.rst`, come tutti i check ufficiali di LLVM
- **Integrazione CI** (Continuous Integration): `clang-tidy --warnings-as-errors='*'` blocca il merge se il check trova qualcosa
- **Distribuzione**: si compila dentro `clang-tools-extra` → può essere proposto upstream

---

## Take-away

<p class="lead">La domanda finale non è "chi vince", ma "che tipo di domanda si fa al codice".</p>

**Quando scrivere un check custom:** pattern interno ricorrente · vincolo deterministico · fix riapplicabile in CI
**Quando NO:** regola sfumata (meglio review umana o LLM) · stile generico (esiste già un check ufficiale)

**clang-tidy e LLM sono complementari, non sostituti:**
- **clang-tidy** → deterministico e preciso sul suo mandato (scope, tipi, overload)
- **LLM** → trovano bug fuori dal mandato (`static_cast<int>(2.5) → 2`), ma sulla precisione dell'AST **fluttuano tra un'esecuzione e l'altra**

> Se la domanda ha una risposta deterministica → vince clang-tidy.
> Se richiede comprensione del contesto → vince l'LLM.

<p class="lead">Risorse: clang-tidy/Contributing.html · LibASTMatchersReference.html · repo: Martin/1_clang-tidy_custom_check/</p>
