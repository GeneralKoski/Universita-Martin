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
