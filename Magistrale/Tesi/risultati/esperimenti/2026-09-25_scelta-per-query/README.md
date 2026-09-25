# Scegliere la configurazione query per query

**Domanda.** Nessuna impostazione unica va bene per le query identificative e
per quelle in lingua naturale (`2026-09-25_recupero-intermedio/`): il recupero
congiuntivo è giusto per `1209 Crispiano` e disastroso per le frasi di SciFact.
Se per ogni query si sceglie fra le due configurazioni, quanto si guadagna al
massimo, e quanto se ne prende con una regola semplice o con un classificatore
addestrato su query già valutate?

## Le due configurazioni

- **A**: BM25, recupero `any`, frequenza mescolata. La migliore su SciFact e
  NFCorpus.
- **B**: BM25, recupero `all`, frequenza mescolata. La migliore sulle known-item.

Tutte e due con Koskidex piatto e `scripts/evaluate`, sugli split di test e di
addestramento di tre collezioni:

| collezione | addestramento | test |
|---|---|---|
| known-item automatiche | 300 (`query/known-item-auto-train/`, seme 20260926, nessun atto in comune col test) | 300 |
| SciFact | 809 (`train`) | 300 |
| NFCorpus | 2.590 (`train`) | 323 |

## Cosa si confronta, sul test

La metrica è nDCG@10 query per query; la scelta di una strategia si valuta
prendendo, per ogni query, il valore della configurazione scelta. Niente
esecuzioni nuove per valutare una strategia: bastano le valutazioni di A e B.

1. **Sempre A** e **sempre B**.
2. **L'oracolo**: per ogni query la migliore delle due, a posteriori. È il tetto:
   nessuna strategia reale lo supera.
3. **La regola della cifra**: B se la query contiene una cifra, altrimenti A.
4. **Il ripiego**: B, e se B non trova niente, A. È quello che si fa con
   Elasticsearch quando `operator and` torna vuoto.
5. **Il classificatore**: una regressione logistica che sceglie B o A.

## Il classificatore, fissato prima di misurare

- **Caratteristiche**, tutte calcolabili dal motore al momento della query, con
  la tokenizzazione di Koskidex replicata e le frequenze documentali della
  collezione della query: logaritmo del numero di termini; se c'è una cifra;
  quota di termini con una cifra; IDF medio, massimo e minimo dei termini,
  divisi per l'IDF di un termine assente, così che stiano fra 0 e 1 in ogni
  collezione; quota di termini assenti dal vocabolario; se B torna vuoto (costa
  una ricerca, la stessa che fa il ripiego).
- **Etichetta**: 1 se B fa meglio di A su quella query, 0 se fa peggio; le query
  in cui fanno uguale non insegnano niente e restano fuori. Ogni query pesa
  quanto la differenza di nDCG@10 fra le due configurazioni, perché sbagliare
  dove la differenza è grande costa di più; e ogni collezione pesa in totale
  quanto le altre, altrimenti NFCorpus (2.590 query) deciderebbe da sola.
- **Addestramento**: caratteristiche standardizzate con medie e deviazioni del
  solo addestramento, discesa del gradiente, passo 0,5, 3.000 iterazioni,
  penalità L2 0,01, soglia 0,5. Scritta a mano in Python, senza librerie.
  Nessun parametro si sceglie guardando il test.

**Il rischio da tenere presente.** Oggi ogni tipo di query sta in una collezione
diversa: le known-item hanno tutte una cifra, e il classificatore può imparare
a riconoscere la collezione invece del tipo di query. Qui non si può escludere;
la prova giusta sono query dei due tipi nella stessa collezione, cioè le
known-item scritte da persone (piano, sezione 2).

Dati guardati prima di scrivere le previsioni, solo sulle query: 114 query di
test di SciFact su 300 contengono una cifra (342 su 809 in addestramento),
NFCorpus 6 su 323.

## Prima di misurare

Scritto e committato prima di lanciare le valutazioni.

1. **Oracolo.** Sulle known-item entro 0,02 da sempre B: lì B è già quasi
   sempre la scelta giusta. Su SciFact e NFCorpus almeno 0,01 sopra sempre A:
   alcune query con pochi termini specifici guadagnano dal recupero congiuntivo.
2. **Regola della cifra.** Sulle known-item uguale a sempre B; su SciFact
   **perde più di 0,05** rispetto a sempre A, perché manda in recupero
   congiuntivo il 38% delle frasi; su NFCorpus entro 0,005 da A.
3. **Ripiego.** Sulle known-item uguale a sempre B; su SciFact e NFCorpus sotto
   sempre A di più di 0,01: quando B trova qualcosa, su una frase trova poco.
4. **Classificatore.** Sulle known-item entro 0,01 da sempre B; su SciFact e
   NFCorpus entro 0,005 da sempre A; quindi **batte la regola della cifra su
   SciFact**, dove la cifra da sola sbaglia.

Se la 4 tiene, la scelta per query funziona almeno fra collezioni diverse, e va
messa alla prova sulle known-item umane prima di portarla nel motore. Se non
tiene, si scrive perché.

## Aggiunto dopo una prova

Lo script, prima di archiviare, è stato provato una volta senza scrivere
nell'archivio. I pesi del modello dicevano: B se ci sono cifre e la query è
corta, ma non se B torna vuoto. Da lì una sesta strategia, scelta **dopo** aver
visto quella prova e quindi senza previsione: **B se la query contiene una
cifra e B trova qualcosa, altrimenti A**. Serve a una domanda sola: il
classificatore fa più di questa regola scritta a mano?

## Esito

`2026-09-25T100505Z_esito.json`, da `analizza.py` al commit `cec00e1`, sulle dodici valutazioni di
Koskidex `1588695`, albero pulito. Il classificatore ha imparato da 1.673
query di addestramento in cui A e B differiscono (994 NFCorpus, 635 SciFact, 44
known-item: sulle altre 256 known-item A e B fanno uguale); 2.026 pari escluse.

nDCG@10 sul test:

| strategia | known-item | SciFact | NFCorpus | media |
|---|---|---|---|---|
| sempre A (`any`) | 0,8629 | **0,6694** | **0,3049** | 0,6124 |
| sempre B (`all`) | **0,9687** | 0,0246 | 0,1939 | 0,3957 |
| oracolo | 0,9687 | 0,6694 | 0,3056 | 0,6479 |
| regola della cifra | 0,9687 | 0,4105 | 0,3009 | 0,5600 |
| ripiego (B, se vuoto A) | 0,9687 | 0,6663 | 0,2877 | 0,6409 |
| **classificatore** | **0,9687** | **0,6694** | 0,3038 | **0,6473** |
| cifra e B non vuoto (aggiunta dopo) | 0,9687 | 0,6694 | 0,3038 | 0,6473 |

**Il classificatore arriva a 0,0006 dall'oracolo**, e sulle 114 query di
SciFact con una cifra ne manda a B solo 2. I pesi (standardizzati) dicono cosa
ha imparato: B vuoto -1,68, c'è una cifra +1,02, quota di cifre +0,96,
lunghezza della query -0,46; le caratteristiche sull'IDF pesano poco.

**Ma l'oracolo stesso non va oltre la scelta per collezione.** Su SciFact il
recupero congiuntivo non è strettamente meglio su nessuna query di test; su
NFCorpus lo è su 6, per 0,0007 in tutto. Scegliere per query, su questi dati,
vuol dire soltanto riconoscere il tipo di query: e per riconoscerlo basta la
regola a due condizioni aggiunta dopo, che fa esattamente quanto il
classificatore.

### Le previsioni

1. Oracolo: sulle known-item entro 0,02 da sempre B, **confermata** (uguale);
   su SciFact e NFCorpus almeno 0,01 sopra sempre A, **smentita** (0 e
   0,0007). Il recupero congiuntivo non aiuta mai le frasi.
2. Regola della cifra: uguale a B sulle known-item, oltre 0,05 sotto A su
   SciFact, entro 0,005 da A su NFCorpus: **confermata** (-0,259 su SciFact,
   -0,004 su NFCorpus).
3. Ripiego: uguale a B sulle known-item, sotto A di più di 0,01 su SciFact e
   NFCorpus: **smentita a metà**. Su NFCorpus -0,017, ma su SciFact solo
   -0,003: B lì torna quasi sempre vuoto (290 query su 300), e il ripiego
   diventa A.
4. Classificatore: entro 0,01 da B sulle known-item, entro 0,005 da A su
   SciFact e NFCorpus, e meglio della regola della cifra su SciFact:
   **confermata**.

### Cosa vuol dire

Il classificatore funziona, ma su questi dati non serve: il problema che
risolve è riconoscere a quale famiglia appartiene una query, e le famiglie
stanno in collezioni diverse con segni evidenti (le cifre, la lunghezza, B
vuoto). Una regola scritta a mano fa lo stesso ed è spiegabile in una riga.
È il rischio dichiarato nel metodo: qui non si distingue "tipo di query" da
"collezione".

Il machine learning avrà qualcosa da dire solo con query dei due tipi nella
stessa collezione, dove le cifre non bastano: una known-item umana come
"ordinanza chiusura via Roma luglio" non ha numeri, e una frase può averne.
La prova si rifà, con lo stesso script, quando ci sono le known-item umane
(piano, sezione 2). Nel motore non entra niente finché quella prova non dice
che il classificatore batte la regola.
