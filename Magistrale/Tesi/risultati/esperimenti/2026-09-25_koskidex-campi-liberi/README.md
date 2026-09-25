# Koskidex innestato con le parole libere di stare in campi diversi

**Domanda.** Le known-item `<numero> <comune>` falliscono in Documentale perché
`best_fields` con `operator and` vuole tutte le parole nello stesso campo
(`2026-09-25_known-item-auto/`). Koskidex innestato riproduce quel vincolo con
`all_terms_in_one_field`, acceso per avere gli stessi insiemi di
Elasticsearch. Cosa succede, passando dall'app, se lo si spegne e si lascia il
resto com'è? È il numero che dice cosa guadagna Documentale usando il matching
di Koskidex invece di quello copiato da Elasticsearch.

## Metodo

- In Documentale, `config('services.koskidex.all_terms_in_one_field')`
  (`KOSKIDEX_ALL_TERMS_IN_ONE_FIELD`), **acceso per default**: senza toccare
  l'ambiente l'app si comporta come oggi, e la parità con Elasticsearch resta.
  Tutte le altre impostazioni dell'indice restano quelle di oggi (refusi 3/6,
  niente ricerca per prefisso, `prefix_length` 1, tokenizer standard,
  punteggio euristico).
- Koskidex reindicizzato dall'app con l'interruttore spento, poi le stesse 300
  known-item e le 24 query del confronto con `app:eval-run-queries`.
- Valutazione con `scripts/evaluate -rankings`, lo stesso codice delle altre.
- Sulle 24 query del confronto, confronto degli insiemi con l'ultimo rapporto
  di Elasticsearch.

Elasticsearch non si tocca: `ElasticsearchService` resta il baseline di
produzione, e la sua correzione è già misurata dal controllo diretto
dell'esperimento known-item.

## Prima di misurare

Scritto e committato prima di modificare Documentale.

1. **Known-item: l'atto entro i primi 10 passa dal 2% a più del 90%, e le query
   a vuoto dal 70% a meno del 5%.** È lo stesso vincolo tolto dal controllo su
   Elasticsearch, che è arrivato al 96%.
2. **L'atto è primo in più del 60% delle query**, meglio del 36% del controllo
   su Elasticsearch: il punteggio euristico premia chi ha più parole della query
   senza refusi, e l'atto giusto le ha tutte.
3. **Sulle 24 query del confronto gli insiemi possono solo crescere**: togliere
   un vincolo non toglie documenti. Almeno una query su tre cambia insieme
   rispetto a Elasticsearch, cioè la parità si perde, com'è giusto.

## Esito

`2026-09-25T092008Z_esito.json`, da `analizza.py` al commit `8043f70`, sui
rapporti di Koskidex `9d95eb6` passato dall'app a Documentale `0c6cacf`, alberi
puliti. Dopo la reindicizzazione l'indice aveva `all_terms_in_one_field: false`
e tutte le altre impostazioni invariate.

| known-item, dall'app | MRR@10 | atto primo | atto entro 10 | a vuoto |
|---|---|---|---|---|
| Elasticsearch (produzione) | 0,017 | 1,3% | 2,0% | 70% |
| Koskidex innestato, campo unico | 0,018 | 1,7% | 2,0% | 70% |
| **Koskidex innestato, campi liberi** | **0,548** | **38,3%** | **93,3%** | **0** |
| Elasticsearch, parole in campi diversi (controllo diretto) | 0,534 | 36,3% | 96,0% | 0 |

Le prime due righe e l'ultima vengono da `2026-09-25_known-item-auto/`
(esito `2026-09-25T084208Z`), stesse 300 query e stesso indice.

**Spegnere un solo vincolo porta l'atto giusto fra i primi dieci in 280 query
su 300**, dove prima ce n'erano 6. Ma lo mette primo solo in 115.

**Chi passa davanti**, nelle 185 query in cui l'atto non è primo:

- in **154** il primo classificato ha il numero **con un refuso**: per `1209
  Crispiano` vince un atto con `1109`, per `1172 Crispiano` uno con `1122`
  (verificati a mano). I refusi ammessi sono uno da tre caratteri e due da sei,
  e valgono anche per le cifre. In 70 di questi il numero vicino sta in un
  campo che pesa più di quello in cui l'atto giusto ha il numero esatto, in 84
  no: il peso dei campi aggrava, ma la causa è il refuso sul numero;
- in 29 il primo classificato ha anche il numero esatto;
- in 2 non ha il numero.

È lo stesso difetto di `ordinanza 187` (`2026-09-23_numero-atto/`), che in
produzione mette l'atto giusto al 12° posto perché `187` combacia con `18` e
`17`. Qui, tolto il vincolo del campo unico, diventa il difetto principale.

Sulle 24 query del confronto: **nessun documento perso**, 10 insiemi uguali a
quelli di Elasticsearch, 14 più grandi, 375 documenti in più in tutto.

### Le previsioni

1. Atto entro 10 oltre il 90% e query a vuoto sotto il 5%: **93,3% e zero,
   confermata.**
2. Atto primo oltre il 60%: **smentita**, 38,3%. Il punteggio euristico premia
   chi ha tutte le parole senza refusi, ma un refuso costa solo 3 punti su 12
   per termine, e il peso del campo moltiplica: un numero vicino nel nome o
   nel riassunto può valere più del numero esatto in `additional_data`, che
   pesa 1.
3. Sulle 24 query gli insiemi crescono soltanto, e almeno un terzo cambia:
   **nessun documento perso, 14 su 24 cambiati, confermata.**

### Cosa vuol dire

Il vincolo del campo unico è la ragione per cui la ricerca per numero e comune
non trova niente; i refusi sui numeri sono la ragione per cui, tolto il
vincolo, la trova male. Sono due difetti distinti, e si correggono separatamente.
Il secondo riguarda sia Elasticsearch in produzione sia Koskidex con i refusi
accesi: un numero di protocollo con una cifra sbagliata è un altro atto, non un
refuso. La prossima misura è quindi Koskidex senza refusi sui termini numerici,
dietro un'impostazione, con la sua voce nel diario prima.
