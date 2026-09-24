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
con numeri identici: `2026-09-24T105605Z_esito.json`.

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

**Cosa resta, non spiegato.** 9 query ancora diverse. I 42 "solo ES" vengono
tutti da `ordinanza 187`, dove Elasticsearch fa match su `18` e `17`: forse una
differenza di tokenizzazione dei numeri, non verificata. Gli 80 "solo Koskidex"
non sono diagnosticati; un'ipotesi è il tetto di 50 espansioni per termine
(`max_expansions`) delle query fuzzy di Elasticsearch.

## Rifarlo

1. `copia-indice-es.py <file fuori dal repo>`: copia l'indice. Il file contiene
   gli oggetti degli atti, quindi non va mai messo qui.
2. Da `~/Desktop/Progetti-personali/Koskidex`: le istruzioni sono in testa a
   `esmirror.go`. Si applica `interruttori-motore.patch`, si esegue, si annulla.

Il file d'esito dichiara `modifiche_non_committate: true` per costruzione: la
patch è una modifica non committata. Il commit indicato è quello su cui la patch
va applicata.
