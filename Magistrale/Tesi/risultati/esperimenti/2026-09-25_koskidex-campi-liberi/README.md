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
