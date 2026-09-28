# Giudizi LLM del pool

`giudizi-llm.tsv` e `qrels/test-llm.tsv` contengono i 905 giudizi del pool delle 24
query dati da un LLM, non da una persona. Sono stati prodotti il 28/09/2026 con
Claude Opus 5.5 (`claude-opus-5-5`), in Claude Code.

- **Bisogni.** Quelli di `bisogni.md`, scritti da Claude prima di vedere i
  risultati e rivisti da Martin (commit afecf63).
- **Scala e regole.** Quelle della parte 2 di `istruzioni-annotazione.md`.
- **Input.** Per ogni atto: titolo, metadati e i primi 2500 caratteri del testo,
  con il testo intero a disposizione quando serviva. Gli atti erano in ordine di
  id e nessun giudice sapeva quale motore li aveva trovati.
- **Esecuzione.** 7 istanze indipendenti, ciascuna su un gruppo di query. Le query
  con un refuso stavano nello stesso gruppo della query giusta (c02/c21,
  c05/c23, c08/c22). I 78 atti in comune fra le coppie hanno ricevuto lo stesso
  grado.
- **Cosa manca.** Niente tempi per giudizio e niente sessioni: non hanno senso
  per un LLM.
- **Distribuzione.** 357 atti a 2, 197 a 1, 351 a 0.

Il prompt usato, parola per parola:

```
Sei un annotatore di pertinenza per una valutazione di motori di ricerca su atti amministrativi di comuni italiani (albo pretorio). Per ogni query hai un file con il bisogno informativo, scritto prima di vedere i risultati, e l'elenco degli atti del pool, in ordine di id (non di ranking; non sai quale motore li ha trovati e non devi cercarlo).

Regole di giudizio: leggi {S}/regole.md (sezioni "La scala" e "Regole per i casi dubbi"). In sintesi:
- 2 = risponde al bisogno per intero: un atto che chi cerca vuole trovare.
- 1 = pertinente ma parziale: tocca il bisogno e chi cerca lo vorrebbe vedere, ma non basta da solo.
- 0 = non risponde, anche se contiene le parole della query.
- Si giudica l'atto, non le parole. Il bisogno scritto è il criterio: dove dice "non lo sono" vale 0, dove dice "parziale" vale 1.
- Un atto e la sua rettifica si giudicano ciascuno per conto proprio.
- Un comune diverso non abbassa il grado, a meno che la query nomini un comune.
- Nel dubbio fra due gradi, il più basso, e scrivilo nella nota.
- Le query con un refuso cercano la stessa cosa della query giusta.

Per ogni atto il file riporta titolo, metadati e i primi 2500 caratteri del testo. Se il testo è troncato e titolo più estratto non bastano per decidere, leggi il testo intero in {S}/atti/<doc_id>.txt. Nel dubbio aprilo. Molti atti hanno testo vuoto: allora si giudica da titolo e oggetto.

Giudica ogni atto indipendentemente, con cura, uno per uno. Non inventare atti e non saltarne.

Per ciascuna delle tue query, scrivi {S}/out/<query_id>.tsv, con intestazione e una riga per atto, nello stesso ordine del file di input:
doc_id<TAB>grado<TAB>nota
La nota è una motivazione breve in italiano (al massimo 15 parole), senza nomi di persone. Usa lettere accentate vere (è, perché), mai trattini lunghi.

Alla fine controlla che ogni file di output abbia esattamente lo stesso numero di atti dell'input (conta le righe "## doc-" nel file di input) e rispondi solo con: query, numero di atti, conteggio per grado.

Le tue query (file di input in {S}/in/<query_id>.md): {Q}
```
