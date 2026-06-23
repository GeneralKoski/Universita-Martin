# Snippet prompts - pronti da rilanciare

Regole (da `llm_responses/_PROMPT.md`):
- Chat nuova ogni volta, anche per la 2a run dello stesso snippet.
- Incolla esattamente il blocco (prompt + codice).
- Per ogni run annota: righe segnalate, fix primario, e se le 2 run divergono.

Prompt identico per tutti, cambia solo il codice. Ogni blocco va lanciato in 2 chat fresche.

---

## Snippet 01

```
Trova problemi in questo C++ moderno e suggerisci fix.
Sii specifico: cita il numero di riga, descrivi il problema,
e proponi il codice corretto.

extern "C" int printf(const char *, ...);

int main() {
  printf("hello\n");
  return 0;
}
```

---

## Snippet 02

```
Trova problemi in questo C++ moderno e suggerisci fix.
Sii specifico: cita il numero di riga, descrivi il problema,
e proponi il codice corretto.

namespace mylib {
int printf(const char *);
}

extern "C" int printf(const char *, ...);

int caller() {
  mylib::printf("greeting from mylib");
  ::printf("hello from libc\n");
  return 0;
}
```

---

## Snippet 03

```
Trova problemi in questo C++ moderno e suggerisci fix.
Sii specifico: cita il numero di riga, descrivi il problema,
e proponi il codice corretto.

extern "C" int printf(const char *, ...);

#define LOG(x) printf("[LOG] " x "\n")

int main() {
  LOG("avvio");
  LOG("fine");
  return 0;
}
```

---

## Snippet 04

```
Trova problemi in questo C++ moderno e suggerisci fix.
Sii specifico: cita il numero di riga, descrivi il problema,
e proponi il codice corretto.

extern "C" int printf(const char *, ...);

template <typename T>
void log_value(T value) {
  printf("v=%d\n", static_cast<int>(value));
}

int main() {
  log_value(1);
  log_value(2.5);
  return 0;
}
```

---

## Snippet 05

```
Trova problemi in questo C++ moderno e suggerisci fix.
Sii specifico: cita il numero di riga, descrivi il problema,
e proponi il codice corretto.

extern "C" int printf(const char *, ...);

struct Logger {
  void printf(const char *msg);
};

void Logger::printf(const char *msg) {
  ::printf("[Logger] %s\n", msg);
}

int main() {
  Logger log;
  log.printf("hello from method");
  ::printf("hello from libc\n");
  return 0;
}
```

---

## Snippet 06

```
Trova problemi in questo C++ moderno e suggerisci fix.
Sii specifico: cita il numero di riga, descrivi il problema,
e proponi il codice corretto.

#include <cstdio>

namespace logging {
template <typename... Args>
int printf(const char *fmt, Args... args) {
  return std::printf(fmt, args...);
}
}

using logging::printf;

namespace detail {
typedef int (*PrintfPtr)(const char *, ...);
static PrintfPtr kPrintfPtr = &std::printf;
}

#define TRACE(...) ::printf(__VA_ARGS__)

template <typename T>
void emit(T value) {
  printf("v=%d\n", static_cast<int>(value));
}

int main() {
  printf("via using: %d\n", 42);
  ::printf("direct libc: %d\n", 1);
  detail::kPrintfPtr("via pointer: %d\n", 2);
  TRACE("via macro: %d\n", 3);
  emit(7);
  emit(2.5);
  return 0;
}
```
