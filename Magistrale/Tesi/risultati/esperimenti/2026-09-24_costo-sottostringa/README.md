# Quanto costa la ricerca per sottostringa

**Domanda.** Documentale cerca le cartelle con un match fuzzy unito a un
wildcard `*termine*` (Task F6 del piano). Koskidex lo fa con `substring_match`,
che scandisce tutto il vocabolario a ogni ricerca. Basta la scansione, o serve
un indice di n-grammi?

**Metodo.** `scripts/compare -sottostringa` sul corpus albo, metadati e testo
integrale, con 20 frammenti di parola (`query/sottostringhe-20.txt`), tre
esecuzioni per corpus da codice committato (Koskidex `ff465b6`, albero pulito).
Si confronta, query per query, `or + euristico` con la stessa configurazione più
la sottostringa: stesso indice e stesse impostazioni, l'unica differenza è la
scansione. Mediana delle tre esecuzioni. Script: `costo.py`.

## Risultato

| Corpus | Termini | Ms in più per query, mediana | Minimo | Massimo |
|---|---|---|---|---|
| metadati | 23.551 | **0,73** | 0,41 | 5,89 |
| testo integrale | 33.434 | **1,02** | 0,74 | 8,93 |

**La scansione basta.** Costa meno di un millisecondo a query su 23-33 mila
termini, circa 30 nanosecondi a termine, e cresce col vocabolario. Un indice di
cartelle ha qualche migliaio di percorsi e un vocabolario molto più piccolo di
questi: la scansione ci costa decimi di millisecondo. Un indice di n-grammi
sarebbe memoria e codice in più per risparmiare meno di un millisecondo.

**Il massimo non è la scansione.** `zione` passa da 29 a 8.134 documenti
trovati (da 281 a 8.210 sul testo integrale): il tempo in più va a valutare e
ordinare migliaia di documenti, non a scorrere il vocabolario. Su un indice di
cartelle un frammento così comune trova tante cartelle quante ne trova
Elasticsearch, che fa la stessa cosa.

**Cosa aggiunge.** Sulle altre query la sottostringa trova da 0 a 108 documenti
in più (109 sul testo integrale; il massimo è `determ`, che dentro altri
termini compare spesso). Sono i documenti che
il wildcard di Elasticsearch trova e il match fuzzy no.

Limiti: i tempi valgono sulla macchina di `macchina.md`. Il corpus albo non ha
cartelle (l'import degli albi non ne crea), quindi la misura è sul vocabolario
dei documenti, che per le cartelle è un limite superiore.

File d'esito: `2026-09-24T112315Z_esito.json`. Rapporti letti:
`confronto/2026-09-24T112207Z`, `112211Z`, `112215Z` (metadati) e `112224Z`,
`112234Z`, `112243Z` (testo integrale).
