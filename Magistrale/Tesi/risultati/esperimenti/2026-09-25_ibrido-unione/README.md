# Difetto 2: dal re-ranking al recupero ibrido

**Domanda.** In Koskidex il vettore della query si usa solo per riordinare:
`SearchScored` aggiunge `sim * 20` ai documenti che il lessicale ha già
trovato, e un documento semanticamente pertinente che non condivide parole con
la query non entra mai. È il difetto 2, e si vede anche dal vivo: con
l'embedder acceso, "traffico" non trova l'ordinanza di chiusura di una strada,
né da sola né in ibrido. Quanto costa questo difetto, in pertinenza e in
tempo, e quanto vale il modello da solo?

## Metodo

- **Embedding**: `bge-m3` via Ollama 0.34.4, digest `790764642607`, 1024
  dimensioni, vettori già normalizzati, calcolati una volta e letti dalla cache
  di `scripts/evaluate -embedder bge-m3` (Koskidex `4b7b97b`). Il testo
  embeddato è quello indicizzato: titolo e testo in un campo.
- **`Settings.HybridMode`** in Koskidex, con il comportamento di oggi come
  default:
  - vuoto (**R**, re-ranking, oggi): il vettore riordina i candidati lessicali;
  - `union` (**U**): i primi `VectorTopK` documenti per similarità coseno
    entrano fra i candidati, accanto a quelli lessicali;
  - `vector` (**V**): solo i primi `VectorTopK` per similarità, il lessicale
    ignorato. È il riferimento: quanto vale il modello da solo.
  - `Settings.VectorTopK`, **100**, fissato prima di misurare: è la profondità
    di Recall@100, e nessun documento oltre il centesimo per similarità può
    contare nelle metriche se il lessicale non lo trova.
- **La fusione non cambia**: in tutti e tre i rami il punteggio di un
  documento è lessicale + `sim * 20`, e un documento trovato solo dal vettore
  ha `sim * 20`, come oggi nella ricerca solo vettoriale. È il difetto 3, e si
  misura dopo, a parte: qui cambia solo chi entra fra i candidati.
- **Scansione esaustiva** di tutti i vettori (O(n·d)), senza indice
  approssimato: il costo si misura, non si presume.
- **Base lessicale**, la stessa in tutte le configurazioni (**L**, senza
  vettori): BM25, recupero `any`, frequenza mescolata, nessuna analisi.
  Numeri già archiviati: SciFact 0,6694, NFCorpus 0,3049, known-item MRR@10
  0,833.
- **Collezioni**: SciFact e NFCorpus (test), le 300 known-item automatiche
  degli albi (test). Refusi spenti, come in ogni valutazione piatta. Quattro
  configurazioni per collezione (L, R, U, V), con `scripts/evaluate`, i primi
  dieci id salvati.
- **Prima del codice**, un test che oggi fallisce: un documento pertinente solo
  semanticamente deve comparire con `union` e non con il re-ranking.

**Dichiarato.** La cache dei vettori è stata riempita con tre esecuzioni di
sviluppo di `evaluate -embedder bge-m3` in re-ranking, cioè la configurazione
R, prima di questo README. Le metriche di quelle esecuzioni non le ho lette:
ho letto solo la configurazione registrata (modello, digest, tempi, vettori
calcolati).

## Prima di misurare

Scritto e committato prima di scrivere il codice.

1. **Il re-ranking migliora le collezioni pubbliche**: R supera L di almeno
   0,02 di nDCG@10 su SciFact e di almeno 0,01 su NFCorpus. `bge-m3` è un
   modello forte, e `sim * 20` sposta i punteggi di diversi punti, quanto le
   differenze di BM25.
2. **Il re-ranking peggiora le known-item**: R perde almeno 0,05 di MRR@10
   rispetto a L. Il modello non distingue `1209` da `1109`, e fra gli atti dello
   stesso comune riordina per somiglianza di contenuto.
3. **L'unione porta richiamo, poco ordine**: U supera R di almeno 0,01 di
   Recall@100 su SciFact e su NFCorpus, mentre nDCG@10 cambia di meno di 0,01.
   Un documento trovato solo dal vettore ha al più 20 punti e sta sotto i
   lessicali forti: entra in coda, non in testa.
4. **Sulle known-item l'unione non cambia niente che conti**: MRR@10 di U entro
   0,01 da R. L'atto giusto il lessicale lo trova già.
5. **Il modello da solo** (V): nDCG@10 fra 0,55 e 0,72 su SciFact, fra 0,28 e
   0,37 su NFCorpus; sulle known-item MRR@10 sotto 0,2.
6. **Il costo**: la mediana del tempo per query di U supera quella di R di meno
   di 10 ms su SciFact e NFCorpus (5.183 e 3.633 documenti) e di meno di 20 ms
   sulle known-item (10.018).

Se la 3 cade perché nDCG@10 cambia molto, i documenti del vettore arrivano in
testa, e la scala della fusione (difetto 3) pesa già qui: va scritto così,
senza anticipare la correzione.

## Esito
