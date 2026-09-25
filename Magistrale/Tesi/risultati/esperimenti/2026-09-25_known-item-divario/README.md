# Il divario che resta fra BM25 e l'euristico sulle known-item

**Domanda.** Sulle 300 known-item `<numero> <comune>`, con Koskidex piatto,
BM25 con la frequenza mescolata fa MRR@10 0,833, con la ricerca per prefisso
spenta 0,854, e l'euristico 0,975 (`2026-09-25_bm25-numeri/`). Il piano
prevede di provare due correzioni: una penalità per i match non esatti in BM25,
o il prefisso solo oltre una lunghezza minima. Prima di scriverne una: chi
passa davanti all'atto giusto, una volta corrette le espansioni? Una correzione
scelta senza saperlo sarebbe tarata sulle 300 query e non su una causa.

## Metodo

Solo analisi, su valutazioni già archiviate con i primi dieci id di ogni query:
`valutazioni-albo/2026-09-25T091010Z_known-item-auto-bm25-blended.json`
(frequenza mescolata, Koskidex `f449b02`) e
`2026-09-25T090302Z_known-item-auto-bm25-senza-prefisso.json` (prefisso
spento, `2b3f446`). Stessa tokenizzazione replicata e stesso corpus di
`2026-09-25_bm25-numeri/`.

Per ogni query in cui l'atto giusto non è primo, il primo classificato cade in
una di tre classi:

- **ha il numero esatto**;
- **ha il numero solo per prefisso**: nessun termine uguale al numero, ma uno
  più lungo che comincia con lui (`1900129` per `190`);
- **non ha il numero**: vince con le sole parole del comune.

E per ogni primo classificato: quante volte ripete le parole del comune
rispetto all'atto giusto, e se è più corto.

## Prima di misurare

Scritto e committato prima di guardare i primi dieci id di queste due
valutazioni.

1. **Con la frequenza mescolata, in più di metà dei fallimenti il primo
   classificato ha il numero solo per prefisso.** L'espansione ora pesa quanto
   il numero esatto, e lo spareggio lo decidono le parole del comune e la
   lunghezza: l'euristico invece dà `+2` al match esatto, BM25 niente.
2. **Col prefisso spento, in più di due terzi dei fallimenti il primo
   classificato non ha il numero.** BM25 disgiuntivo non premia chi ha più
   termini diversi della query: un atto che ripete il nome del comune può
   battere uno che ha numero e comune una volta sola.
3. **In quei casi (prefisso spento, primo senza numero) il primo ripete le
   parole del comune più dell'atto giusto in più di due terzi dei casi.**

Se la 1 tiene, la correzione naturale è la penalità per i match non esatti; se
tiene la 2, nessuna delle due correzioni previste tocca quella parte del
divario, e va scritto.

## Aggiunto dopo la prima analisi

L'esito `2026-09-25T094141Z` (sotto) dice che la parte grossa del divario non
viene dalle espansioni: vince un atto senza il numero, che ripete il nome del
comune. È il recupero disgiuntivo: BM25 somma i contributi dei termini, e un
atto che ha solo il comune, più volte, supera uno che ha numero e comune una
volta sola. L'euristico non ci cade perché mette prima chi ha tutti i termini.

Il controfattuale c'è già, senza codice nuovo: **recupero congiuntivo con BM25**
(`-mode all`), con la frequenza mescolata e col prefisso spento. Previsioni,
scritte dopo aver visto l'esito sopra ma prima di lanciare questi due:

4. **Con `all` e la frequenza mescolata l'atto è primo in almeno 255 query su
   300, MRR@10 almeno 0,90.** Spariscono i 36 casi senza numero; restano al più
   i 33 con il numero esatto o per prefisso.
5. **Con `all` e il prefisso spento, almeno 255 e MRR@10 almeno 0,90**, per la
   stessa ragione sui 38 casi senza numero.

Non è una correzione da adottare così: il recupero congiuntivo è il difetto 0,
e su SciFact lascia a vuoto 290 query su 300. Se la 4 tiene, il risultato è che
la configurazione giusta dipende dal tipo di query, identificativa o in lingua
naturale: è l'argomento della fusione dipendente dalla query (piano, sezione 5).

## Esito

Due file, entrambi da `analizza.py` su valutazioni archiviate da alberi puliti:
`2026-09-25T094141Z_esito.json` (commit `6ba70f4`, le due valutazioni di
partenza) e `2026-09-25T094258Z_esito.json` (commit `4e23f3d`, le due col
recupero congiuntivo, Koskidex `4ee872c`). La tokenizzazione replicata passa il
suo controllo su tutte le query.

**Chi passa davanti all'atto giusto**, primo classificato delle query sbagliate:

| BM25, recupero `any` | MRR@10 | falliti | senza numero | numero esatto | numero solo per prefisso |
|---|---|---|---|---|---|
| frequenza mescolata | 0,833 | 69 | **36** | 22 | 11 |
| prefisso spento | 0,854 | 60 | **38** | 22 | - |

Dei 36 primi classificati senza numero, 35 ripetono le parole del comune più
dell'atto giusto; dei 38, 37. È il recupero disgiuntivo: un atto con il solo
nome del comune, ripetuto, somma più di uno che ha numero e comune una volta.

**Col recupero congiuntivo il divario si chiude:**

| known-item, Koskidex piatto | MRR@10 | atto primo | entro 10 |
|---|---|---|---|
| euristico (`all` o `any`, uguali) | 0,975 | 287 | 299 |
| BM25 `any`, frequenza mescolata | 0,833 | 231 | 287 |
| BM25 `all`, frequenza mescolata | 0,960 | 281 | 299 |
| **BM25 `all`, prefisso spento** | **0,976** | **288** | **299** |

Restano 12 fallimenti in cui vince un altro atto con lo stesso numero esatto,
e con la frequenza mescolata 7 in cui vince un numero trovato per prefisso.

### Le previsioni

1. Con la frequenza mescolata più di metà dei fallimenti perde contro un numero
   trovato per prefisso: **smentita**, 11 su 69. La frequenza mescolata aveva
   già tolto quasi tutto il danno del prefisso.
2. Col prefisso spento più di due terzi dei fallimenti perde contro un atto
   senza numero: **smentita di poco**, 38 su 60 (63%). Nel verso previsto, sotto
   la soglia scritta.
3. In quei casi il primo ripete il comune più dell'atto in più di due terzi:
   **confermata**, 37 su 38.
4. `all` con la frequenza mescolata, almeno 255 primi e MRR@10 almeno 0,90:
   **confermata**, 281 e 0,960.
5. `all` col prefisso spento, almeno 255 e 0,90: **confermata**, 288 e 0,976.

### Cosa vuol dire

**Sulle known-item BM25 non è peggio dell'euristico: lo è il recupero
disgiuntivo.** A parità di recupero congiuntivo BM25 fa quanto l'euristico
(288 primi contro 287). Il confronto del 25/09 (0,709 contro 0,975) metteva
BM25 in `any` contro l'euristico, che in `any` resta forte perché ordina prima
chi ha tutti i termini: di fatto era un confronto fra un recupero disgiuntivo e
uno congiuntivo.

Le due correzioni previste nel piano (penalità per i match non esatti, prefisso
oltre una lunghezza minima) toccherebbero al più i 7-11 casi del prefisso, non
i 36-38 senza numero: non si fanno.

Il recupero congiuntivo non è la risposta generale: su SciFact è il difetto 0,
290 query su 300 a vuoto. La configurazione giusta dipende dal tipo di query,
identificativa o in lingua naturale. Due strade, da decidere con la loro voce
di diario prima di misurare: un recupero intermedio come `minimum_should_match`
di Elasticsearch, o la scelta per tipo di query della sezione 5 del piano.
