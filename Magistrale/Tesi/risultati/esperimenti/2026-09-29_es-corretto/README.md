# Elasticsearch con le stesse correzioni

**Domanda.** La sezione 8.4 della tesi sostiene che quasi tutto il guadagno di
pertinenza di Koskidex innestato viene da impostazioni che Elasticsearch ha già
o può avere: le parole libere di stare in campi diversi, il filtro delle
elisioni, i numeri senza refusi. È un'affermazione, non una misura. Con le
stesse correzioni, Elasticsearch fa quello che fa Koskidex, sulle stesse query?

Scritto il 29/09/2026, prima di scrivere lo script e prima di qualunque misura.

## Metodo

`ElasticsearchService` non si tocca. `es-corretto.py` crea nel container di
Elasticsearch dell'app (`localhost:9201`) un indice `es-corretto` con il
mapping di `search-documents-local` e un analizzatore predefinito con il filtro
`elision` e gli articoli di Lucene, come l'indice di controllo di
`2026-09-25_elisioni`, e ci copia i documenti con `_reindex`. Poi interroga
l'indice con due query riscritte, sulle stesse collezioni di
`2026-09-29_profilo-completo` (known-item automatiche, umane, date, importi),
e scrive rapporti nel formato di `app:eval-run-queries`, valutati con
`scripts/evaluate -rankings -top 10`:

- **ESC**, come KC (P0 di `profilo-completo`): un `bool` con un `must` per
  parola, ciascuno un `multi_match` `best_fields` sui sei campi con i pesi,
  `prefix_length: 1`, `tie_breaker: 0.3` e `fuzziness: AUTO`, tranne le
  parole fatte di sole cifre, cercate con `fuzziness: 0`;
- **ESO**, come P2: le stesse clausole in `should`, con
  `minimum_should_match: 1`. Elasticsearch ha già BM25.

Date e importi restano come in produzione: normalizzarli in Elasticsearch
vuol dire scrivere char filter a mano per ogni formato, e sulle query umane
non cambiano niente (`2026-09-28_date-app`). Il confronto con Koskidex è quindi
con P0 e con P2, non con P1.

## Prima di misurare

1. **ESC come KC sulle automatiche**: MRR@10 entro 0,02 da P0.
2. **ESC come KC sulle umane**: MRR@10 entro 0,03 da P0.
3. **ESC sopra Elasticsearch di produzione sulle umane** di almeno 0,08 (KC
   ne fa +0,106).
4. **ESO come P2 sulle umane**: MRR@10 entro 0,05. Il BM25 di Elasticsearch
   è per campo, con `best_fields` che prende il migliore; Koskidex combina i
   campi a modo suo: l'ordine può cambiare, i candidati sono quasi gli stessi.
5. **ESO sotto ESC sulle automatiche** di almeno 0,03, come P2 sotto P1.

Se tengono la 1, la 2 e la 4, il vantaggio di Koskidex innestato sulle ricerche
per contenuto sta nelle impostazioni e non nel motore, e la sezione 8.4 lo può
dire con un numero.
