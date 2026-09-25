# Perché BM25 perde sulla ricerca per numero

**Domanda.** Sulle 300 known-item `<numero> <comune>` Koskidex piatto con BM25
mette l'atto giusto al primo posto nel 61,7% delle query, contro il 95,7%
dell'euristico, a parità di recupero (`2026-09-25_known-item-auto/`). Lo stesso
segno era uscito su `ordinanza 187` (`2026-09-23_numero-atto/`). Perché?

## Metodo

Stesso impianto delle known-item: Koskidex piatto in memoria con
`scripts/evaluate`, titolo e testo in un campo solo, refusi spenti, `any` +
BM25, sulle stesse 300 query e lo stesso corpus.

1. **Chi passa davanti.** `scripts/evaluate -top 10` salva i primi dieci id di
   ogni query. Per ogni query in cui l'atto giusto non è primo, `analizza.py`
   guarda il primo classificato sul corpus: contiene il numero cercato, o solo
   le parole del comune? E com'è lungo rispetto all'atto giusto? Il corpus si
   legge in locale e non finisce nell'archivio: nell'esito vanno solo id e
   conteggi.
2. **La frequenza del numero.** Per ogni query, in quanti atti compare il
   numero (df), confrontando le query riuscite e quelle fallite. Un numero
   corto compare anche nelle date (`14/05/2014` dà `14`, `05`, `2014`) e negli
   importi, e allora il suo IDF pesa poco.
3. **I controfattuali**, uno alla volta, con i flag `-bm25-b` e `-bm25-k1` di
   `scripts/evaluate`: `b = 0` (niente normalizzazione della lunghezza) e
   `k1` basso (saturazione più forte della frequenza del termine).

**Aggiunto dopo la prima analisi.** Nei fallimenti il primo classificato
risultava non contenere né il numero né il comune. Guardando i termini, spesso
combacia con la query solo per prefisso: `190` con `1900129`, `2` con `2026`.
Koskidex fa ricerca per prefisso anche coi refusi spenti. Da qui due aggiunte:
`analizza.py` conta i fallimenti in cui il primo classificato non ha nessun
termine della query tale e quale, e un quarto controfattuale spegne la ricerca
per prefisso (`-senza-prefisso`, cioè `Settings.DisablePrefixSearch`).

La tokenizzazione in `analizza.py` replica quella predefinita di Koskidex
(minuscolo, via gli accenti, si spezza su tutto ciò che non è lettera o cifra),
e si controlla da sola: l'atto giusto deve contenere tutti i termini della sua
query.

## Prima di misurare

Scritto e committato prima di modificare `scripts/evaluate` e di guardare
qualsiasi ranking.

1. **Nella maggior parte dei fallimenti (più di metà) il primo classificato non
   contiene il numero**: vince su un atto dello stesso comune che ne ripete il
   nome, cioè sulla frequenza delle parole del comune e non sul numero.
2. **I numeri delle query fallite sono più frequenti** di quelli delle query
   riuscite: la mediana della df è più alta.
3. **`b = 0` recupera più di metà del divario**: MRR@10 da 0,709 a oltre 0,84.
   Se è la lunghezza, un atto corto dello stesso comune batte l'atto giusto
   perché la normalizzazione lo premia.
4. **`k1` basso (0,3) aiuta meno di `b = 0`.** Ripetere il nome del comune pesa
   meno con una saturazione forte, ma la previsione è che il fattore principale
   sia la lunghezza.

Le previsioni 3 e 4 sono le meno sicure: se la causa principale è l'IDF basso
del numero (la 2), nessuno dei due parametri la tocca, e la correzione va
cercata altrove.
