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

## Esito

*Nota del 29/09/2026, dal quarto controllo indipendente: le previsioni sopra
sono state committate (`e70769b`) quando le misure di P0 e P2 di
`2026-09-29_profilo-completo`, che ne sono il riferimento, erano già
archiviate. Non le avevo ancora guardate, ma "prima di qualunque misura"
vale solo per le misure di Elasticsearch corretto.*

Misurato il 29/09/2026 fra le 12:51 e le 12:52, Elasticsearch 9.1.0 del
container dell'app, script `1c2f674`, Koskidex `0e914f5` per la valutazione.
Riassunto in `2026-09-29T105143Z_esito.json` (`analizza.py`); rapporti in
`confronto/`, valutazioni in `evaluate/`. I rapporti sulle umane contengono il
testo delle query e restano fuori da git. Il riferimento è
`2026-09-29_profilo-completo` (P0 e P2) e, sulle umane,
`valutazioni-albo/2026-09-29T093306Z_known-item-umane-ku-app-elasticsearch.json`
(Elasticsearch di produzione, 0,3256).

MRR@10, con fra parentesi le ricerche a vuoto:

| | automatiche | umane | date | importi |
|---|---|---|---|---|
| Elasticsearch di produzione | | 0,3256 | | |
| **ESC** | 0,9379 | 0,4490 (29,8%) | 0,3054 (50,7%) | 0,9026 |
| P0 (Koskidex, profilo consigliato) | 0,9498 | 0,4317 (29,8%) | 0,3153 (50,4%) | 0,9167 |
| **ESO** | 0,1311 | 0,5032 (0%) | 0,1231 | 0,3714 |
| P2 (Koskidex, disgiuntivo BM25) | 0,1468 | 0,5024 (0%) | 0,4781 | 0,7007 |

**Cinque previsioni su cinque.**

1. **Confermata.** ESC sulle automatiche 0,9379 contro 0,9498 di P0.
2. **Confermata.** ESC sulle umane 0,4490 contro 0,4317 di P0, con la stessa
   quota di ricerche a vuoto (29,8%).
3. **Confermata.** ESC sulle umane 0,4490 contro 0,3256 di Elasticsearch di
   produzione.
4. **Confermata, quasi identici.** ESO sulle umane 0,5032 contro 0,5024 di
   P2, senza ricerche a vuoto in tutti e due.
5. **Confermata, molto di più.** ESO sulle automatiche 0,1311, contro 0,9379
   di ESC: come P2 sotto P1, il recupero disgiuntivo perde le ricerche per
   numero.

**Cosa dice.** Sulle ricerche per contenuto Elasticsearch, con le stesse
correzioni, arriva dove arriva Koskidex: le umane passano da 0,3256 a 0,4490
con le parole libere di stare in campi diversi, il filtro delle elisioni e i
numeri senza refusi, contro 0,4317 di Koskidex; nel recupero disgiuntivo 0,5032
contro 0,5024. La sezione 8.4 può dire che il vantaggio sulle ricerche per
contenuto sta nelle impostazioni e non nel motore, con questo numero. Quello
che Elasticsearch non ha, in questa prova, sono i vettori: P4 fa 0,6073.

**Limiti.** Le date e gli importi restano come in produzione (ESC 0,3054 sulle
date, contro 0,9789 di P1): normalizzarli in Elasticsearch vuol dire scrivere
char filter a mano per ogni formato, e non l'ho fatto. Le clausole per parola
le ho scelte io prima di misurare (README, "Metodo"), non sono l'unica
traduzione possibile delle impostazioni di Koskidex in Elasticsearch. Il
confronto è sulle stesse 104 query umane, quindi non dice quanto vale su query
diverse.
