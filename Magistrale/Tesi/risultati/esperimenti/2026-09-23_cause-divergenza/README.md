# Perché Koskidex ed Elasticsearch trovano cose diverse

**Domanda.** Sul corpus di 10.018 atti degli albi pretori, con le stesse 24
query, i due motori restituiscono lo stesso insieme di documenti solo in 8 casi.
Su 14 documenti di prova coincidevano ovunque. Da cosa dipende, e quanto pesa
ogni causa?

**Metodo.** Koskidex riceve esattamente ciò che Elasticsearch ha indicizzato
(copiato dall'indice, nome troncato da `pathinfo()` compreso), con i pesi di
`fuzzySearch`. Poi si aggiunge una correzione alla volta, per imitare il matching
di Elasticsearch, e a ogni passo si contano le query con lo stesso insieme e i
documenti trovati da un motore solo. Le correzioni al motore stanno in una patch
e non entrano mai nel codice di Koskidex.

## Risultato

| Passo | query identiche | documenti solo ES | documenti solo Koskidex |
|---|---|---|---|
| 0. Koskidex com'è | 8 / 24 | 124 | 447 |
| 1. + tutte le parole nello stesso campo | 10 / 24 | 124 | 121 |
| 2. + soglie dei refusi di Elasticsearch | 12 / 24 | 42 | 150 |
| 3. + niente ricerca per prefisso | 13 / 24 | 42 | 112 |
| 4. + prima lettera esatta | 15 / 24 | 42 | 80 |

Eseguito la prima volta il 23/09/2026 e rifatto il 24/09/2026 da questi file,
con numeri identici: `2026-09-24T105605Z_esito.json`. Rifatto da codice
committato, con le impostazioni del Task F7 al posto della patch, di nuovo con
numeri identici: `2026-09-24T112908Z_esito.json` (Koskidex `1549de2`).

1. **Congiunzione per campo.** `best_fields` con `operator: and` vuole tutte le
   parole nello stesso campo; Koskidex le accetta sparse fra campi. Pesa più di
   tutto: 326 dei 447 documenti in più.
2. **Soglie dei refusi.** `AUTO` di Elasticsearch: 1 refuso da 3 caratteri, 2
   da 6. Koskidex: 1 da 4, 2 da 8. Porta via 82 dei 124 "solo ES". Il salto dei
   "solo Koskidex" da 121 a 150 è atteso: soglie più basse danno refusi in più
   anche a Koskidex.
3. **Ricerca per prefisso** (`fuzzy.go:94`): Koskidex accetta qualunque termine
   che *inizia* con la parola cercata, a qualsiasi distanza.
4. **`prefix_length: 1`**: in Documentale la prima lettera deve essere esatta.

## Il resto, spiegato il 25/09/2026

Restavano 9 query diverse, 42 documenti "solo ES" e 80 "solo Koskidex". Le due
ipotesi scritte qui il 23/09 erano **sbagliate** tutte e due:

- **Non era la tokenizzazione dei numeri** a dare i 42 "solo ES" di
  `ordinanza 187`. Era un difetto di Koskidex: i candidati fuzzy erano solo i
  termini con un bigramma in comune con la parola cercata, e `17` non ne ha con
  `187` pur distando un refuso. Una modifica rompe fino a due bigrammi, una
  trasposizione tre: sotto una certa lunghezza la garanzia sparisce. Con le
  soglie predefinite capita a `atre` contro `arte`. Corretto in Koskidex
  (`1902826`, non è un'impostazione: il motore prometteva la distanza di
  Damerau e non la manteneva).
- **Non era `max_expansions`.** La query di produzione rilanciata con
  `max_expansions: 10000` dà esattamente gli stessi insiemi su tutte e 24 le
  query (controllo fatto a mano con uno script nello scratchpad, non archiviato).

**La quinta causa è il tokenizer.** `_explain` su un documento in più ha
mostrato il motivo: il nome dice *"dell'illuminazione pubblica"*, e il
tokenizer standard di Elasticsearch (regole UAX#29) tiene l'apostrofo fra due
lettere dentro la parola. Indicizza `dell'illuminazione` come un termine solo, e
"illuminazione" non lo trova. Le stesse regole uniscono date e decimali
(`14.01.2026`, `3,5`), e per questo in Koskidex `187` raggiungeva anche `18`
dentro le date. Koskidex spezza su ogni carattere che non è lettera o cifra.
Aggiunto come impostazione `tokenizer: "standard"` (`3642dec`).

| Passo | query identiche | documenti solo ES | documenti solo Koskidex |
|---|---|---|---|
| 0-1 | come sopra | | |
| 2. + soglie dei refusi di Elasticsearch | 12 / 24 | 0 | 154 |
| 3. + niente ricerca per prefisso | 13 / 24 | 0 | 116 |
| 4. + prima lettera esatta | 15 / 24 | 0 | 84 |
| **5. + tokenizer standard** | **24 / 24** | **0** | **0** |

Con i difetti corretti (`2026-09-25T070310Z_esito.json`, prima del passo 5) e
poi con il passo 5 (`2026-09-25T070724Z_esito.json`, Koskidex `3642dec`).
**Con le impostazioni di compatibilità, Koskidex restituisce esattamente gli
insiemi di Elasticsearch su tutte e 24 le query.** È la base dell'argomento
"i miglioramenti valgono anche per Documentale": partendo dagli stessi insiemi,
ogni differenza misurata dopo viene dalla modifica, non dal motore.

**Un difetto di Documentale in produzione.** In italiano le elisioni sono
dappertutto (*dell'*, *all'*, *l'*, *un'*): con il tokenizer standard, chi cerca
"illuminazione" non trova gli atti che dicono "dell'illuminazione". Il
tokenizer spiega 84 documenti su 9 query, ma non sono tutti elisioni: i 16 di
`ordinanza 187` vengono dalle date, e lì Elasticsearch fa bene a non trovare
`18` dentro `18.01.2026`. Quanti dei 84 siano elisioni non è ancora contato. Il
comportamento predefinito di Koskidex resta quello di spezzare, che per le
elisioni è quello giusto; per date e decimali andrebbe ripensato a parte.

**Effetto della correzione dei bigrammi sul comportamento predefinito.**
`scripts/compare` sulle 24 query, tre esecuzioni prima (`confronto/2026-09-24T112954Z`,
`112958Z`, `113102Z`, Koskidex `1549de2`) e tre dopo (`confronto/2026-09-25T070255Z`,
`070259Z`, `070303Z`, `1902826`): nessun totale cambia in nessuna delle tre
configurazioni; cambia una sola testa di ranking, `or + BM25` su *"delibera di
giunta sul bilancio di previsione 2026"*, dove `2026` (quattro caratteri) ora
trova anche `2206`, a una trasposizione. Le valutazioni BEIR girano con i
refusi spenti e non ne sono toccate per costruzione.

## Rifarlo

1. `copia-indice-es.py <file fuori dal repo>`: copia l'indice. Il file contiene
   gli oggetti degli atti, quindi non va mai messo qui.
2. Da `~/Desktop/Progetti-personali/Koskidex`:
   `go run ./scripts/esmirror <copia> confronto/2026-09-24T105341Z_albo-metadata-elasticsearch.json query/confronto-24.txt`.

`esmirror.go` e `interruttori-motore.patch` qui accanto sono la versione del
23/09, che girava con una patch al motore: il file d'esito di allora dichiara
`modifiche_non_committate: true` per costruzione. Restano per rifare quel
risultato; da `1549de2` in poi lo script vive in Koskidex e gira da codice
committato.
