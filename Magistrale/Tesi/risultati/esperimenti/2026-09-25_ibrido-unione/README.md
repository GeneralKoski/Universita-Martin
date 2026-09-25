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

`2026-09-25T124914Z_esito.json`, da `analizza.py` al commit `1821e35` (albero
pulito), sulle dodici valutazioni di Koskidex `f5ce77f` delle 12:47-12:49 UTC
(`koskidex-beir/2026-09-25T124733Z`-`124838Z`,
`valutazioni-albo/2026-09-25T124841Z`-`124904Z`). Vettori `bge-m3`, digest
`790764642607`, dalla cache: calcolarli la prima volta ha richiesto 11 minuti
per SciFact, 8 per NFCorpus e 9 per gli albi.

| | L lessicale | R re-ranking (oggi) | U unione | V solo vettori |
|---|---|---|---|---|
| SciFact nDCG@10 | 0,6694 | **0,6913** | 0,6913 | 0,6436 |
| SciFact Recall@100 | 0,8859 | 0,9116 | 0,9116 | 0,9037 |
| NFCorpus nDCG@10 | 0,3049 | 0,3284 | **0,3340** | 0,3149 |
| NFCorpus Recall@100 | 0,2391 | 0,2499 | **0,2809** | 0,2830 |
| NFCorpus query a vuoto | 24 | 24 | **0** | 0 |
| known-item MRR@10 | 0,8331 | **0,8464** | 0,8464 | 0,1837 |
| ms per query, mediana (SciFact / NFCorpus / known-item) | 25,8 / 2,2 / 1,4 | 34,0 / 3,2 / 1,9 | 40,4 / 8,3 / 17,2 | 30,8 / 7,5 / 16,6 |

**Il re-ranking vale più di due punti su entrambe le collezioni pubbliche.
L'unione aggiunge qualcosa solo dove il lessicale lascia buchi**, e con il
recupero disgiuntivo di questa base i buchi sono pochi.

**Perché su SciFact l'unione non cambia niente.** Con `any` e nessuna stopword,
il lessicale trova in mediana 5.182 documenti su 5.183: i cento più vicini per
similarità sono già fra i candidati, e il vettore non ne porta nessuno
(mediana 0, al più 60). Il difetto 2 lì non si vede, perché il difetto 0 è
stato corretto dalla parte opposta: quando il lessicale prende tutto, non c'è
niente da recuperare. Su NFCorpus, query corte, il lessicale trova in mediana
560 documenti e ne lascia 24 query senza risultati: il vettore porta in mediana
44 candidati nuovi, Recall@100 sale di 0,031 e le 24 query a vuoto spariscono.
Sulle known-item ne porta 12 in mediana, ma finiscono tutti sotto l'atto
giusto: le 300 query danno le stesse metriche.

**Quello che non si è misurato qui, e conta per Documentale.** In produzione la
ricerca è congiuntiva (`operator and`, campo unico): lì il lessicale trova
pochi documenti o nessuno, e l'unione dovrebbe pesare molto di più. Va misurata
sulla configurazione dell'innesto, non su questa base.

### Le previsioni

1. Il re-ranking migliora di almeno 0,02 SciFact e 0,01 NFCorpus: **+0,0219 e
   +0,0235, confermata.** Su SciFact 43 query migliorano e 9 peggiorano, su
   NFCorpus 118 e 34 (contate a mano sulle valutazioni archiviate, non dallo
   script).
2. Il re-ranking perde almeno 0,05 sulle known-item: **+0,0133, smentita.** Il
   modello non distingue i numeri, ma fra gli atti che il lessicale ha già messo
   alla pari riordina meglio di quanto credessi: 33 query migliorano, 22
   peggiorano (contate a mano).
3. L'unione porta almeno 0,01 di Recall@100 su SciFact e NFCorpus, con nDCG@10
   entro 0,01: **smentita su SciFact** (nessun cambiamento, per la ragione
   sopra), **confermata su NFCorpus** (+0,031 di Recall@100, +0,0056 di
   nDCG@10, 8 query migliorano e nessuna peggiora).
4. Sulle known-item l'unione entro 0,01 dal re-ranking: **identica, confermata.**
5. Il modello da solo: **SciFact 0,6436, NFCorpus 0,3149, known-item 0,1837,
   confermata** in tutti e tre gli intervalli. Da solo il modello batte il
   lessicale su NFCorpus e in Recall@100, e perde in testa su SciFact.
6. Il costo dell'unione, meno di 10 ms su SciFact e NFCorpus e di 20 sulle
   known-item: **+6,5, +5,1 e +15,3 ms, confermata.** È la scansione di tutti i
   vettori, lineare nel numero di documenti: 10.018 atti costano poco più del
   doppio dei 5.183 abstract. I vettori qui arrivano già come `[]float64`; dal
   server arrivano come `[]interface{}` e si convertono a ogni query, un costo
   in più da misurare quando Documentale indicizzerà con i vettori.

### Cosa vuol dire per la tesi

Il difetto 2 è reale ma il suo peso dipende dal recupero lessicale: con `any`
su documenti lunghi è nullo, con query corte vale tre punti di richiamo e
toglie le risposte vuote, con il recupero congiuntivo di Documentale va ancora
misurato. Il guadagno grosso di questo capitolo lo dà il vettore anche solo
come re-ranking (+0,022 e +0,024 di nDCG@10), cioè con la fusione `sim * 20`
che è il difetto 3: la prossima misura dice se una fusione fatta bene
guadagna ancora, e se il `20` era stato fortunato.

