# Snippet 05_method_collision - Claude Opus 4.7

**File testato:** `comparison/snippets_neutral/05_method_collision.cpp`
**Data:** 2026-05-05
**Modello:** Claude Opus 4.7

## Ground truth (clang-tidy)
**2** warning, entrambi sulle chiamate a `::printf` di libc:
- riga 8 (`::printf("[Logger] %s\n", msg);`)
- riga 14 (`::printf("hello from libc\n");`)

**Non** segnala `log.printf("hello from method")` (riga 13): è un `CXXMemberCallExpr` su `Logger::printf`, non `::printf`.

## Risposta integrale dell'LLM (1ª chat fresca)

> ## Riga 1 - `extern "C" int printf(const char *, ...);`
> Ridichiarare manualmente `printf` è cattiva pratica. Fix: `#include <cstdio>`, poi `std::printf`/`::printf`.
>
> ## Righe 4 e 7 - `void printf(const char *msg);` come metodo
> Tecnicamente legale: il metodo `Logger::printf` non è in conflitto con `::printf` globale perché vivono in scope diversi, e la chiamata `::printf(...)` dentro al metodo lo rende esplicito.
>
> Però è una trappola di leggibilità: chi legge `log.printf("...")` si aspetta semantica `printf` variadica. Qui invece accetta una stringa singola.
>
> Fix: rinomina e rendi la firma onesta.
> ```cpp
> struct Logger {
>     void log(std::string_view msg) const;
> };
> void Logger::log(std::string_view msg) const {
>     std::printf("[Logger] %.*s\n", static_cast<int>(msg.size()), msg.data());
> }
> ```
>
> Se vuoi davvero la semantica printf-like:
> ```cpp
> #include <print>
> struct Logger {
>     template <class... Args>
>     void log(std::format_string<Args...> fmt, Args&&... args) const {
>         std::print("[Logger] ");
>         std::println(fmt, std::forward<Args>(args)...);
>     }
> };
> ```
>
> ## Riga 12 - `Logger log;`
> `log` è anche `std::log` (logaritmo naturale) in `<cmath>`. Trappola futura: usa `logger`.
>
> ## Versione corretta complessiva
> ```cpp
> #include <cstdio>
> #include <string_view>
> struct Logger {
>     void log(std::string_view msg) const;
> };
> void Logger::log(std::string_view msg) const {
>     std::printf("[Logger] %.*s\n", static_cast<int>(msg.size()), msg.data());
> }
> int main() {
>     Logger logger;
>     logger.log("hello from method");
>     std::printf("hello from libc\n");
> }
> ```

## Seconda esecuzione (chat fresca, stesso prompt)

> Il codice compila e funziona - non c'è un bug "rotto". Però ci sono problemi di stile/API design.
>
> ## Riga 1 - `extern "C" int printf(const char *, ...);`
> Pessima idea ridichiararlo manualmente. Fix: `#include <cstdio>`.
>
> ## Righe 4 e 8 - metodo `printf`
> Trappola di shadowing. Il fatto che dentro al metodo tu debba scrivere `::printf` per disambiguare è il sintomo. Rinomina:
> ```cpp
> struct Logger { void log(const char* msg); };
> void Logger::log(const char* msg) { std::printf("[Logger] %s\n", msg); }
> ```
>
> ## Riga 4 - il metodo dovrebbe essere `const`
>
> ## Riga 13 - `Logger log;` collide con `std::log` (cmath). Usa `logger`.
>
> ## Cosa NON è un problema
> - `extern "C"` di per sé è corretto per linkare a una funzione C - il problema è solo che ridichiarare `printf` a mano è inutile.
> - `::printf` dentro al metodo è un workaround corretto per lo shadowing - ma la soluzione giusta è **eliminare lo shadowing**, non conviverci.

## Analisi

| Campo | Valore |
|---|---|
| Numero di problemi segnalati | 1ª: 4 (riga 1, righe 4/7 metodo, riga 12 nome var, riga 16 return). 2ª: 4 (riga 1, righe 4/8 metodo, riga 4 const, riga 13 nome var). |
| Ha riconosciuto `Logger::printf` come metodo distinto? | **sì, esplicitamente in entrambe le chat**: "vivono in scope diversi", "::printf dentro al metodo è un workaround corretto". |
| Falsi positivi (es. ha flaggato `log.printf`?) | **NO** - non confonde mai `log.printf("...")` con `::printf` libc. ✓ Passa la trappola. |
| Falsi negativi | 0 sui `::printf` libc. La fix top in entrambe le chat è **`std::printf` qualificato** (mantieni printf, sostituisci solo `extern "C"` con include). |
| Deterministico (1ª = 2ª)? | sì sul nucleo: scope OK, rename suggerito, var `log` segnalata in entrambe. La 1ª preferisce `string_view`, la 2ª resta su `const char*`. La 1ª menziona `std::println` come variante avanzata (template variadic), la 2ª no. |

## Verdetto sintetico

⭐ **Claude passa la trappola di falso positivo.** Esplicitamente riconosce in entrambe le chat che `Logger::printf` non è `::printf` di libc. Determinismo alto.

**Pattern interessante che si rompe:** rispetto agli snippet 01-04, qui Claude **non propone `std::println` come fix primario**: tiene `std::printf` qualificato e rinomina il metodo. La menzione di `std::println` resta come alternativa ("se vuoi davvero la semantica printf-like"). Spiegazione: in questo snippet l'uso di `printf` è già strutturato (formato stringa fisso, non variadic generico), quindi il fix più pragmatico è qualificare `std::printf`, non riscrivere tutto in `std::println`.

Per la slide: il punto è che **Claude trova il falso positivo che un LLM regex-based farebbe**, e propone un fix coerente con la fix-it del check (sostituire `extern "C"` con include) senza forzare riscritture eccessive.
