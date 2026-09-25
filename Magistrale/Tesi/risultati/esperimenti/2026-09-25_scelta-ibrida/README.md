# Scegliere per query con l'unione e il peso del vettore

**Domanda.** `2026-09-25_scelta-per-query/` sceglieva fra BM25 `any` e `all`
senza vettori, e l'oracolo coincideva con la scelta per collezione: `all`
tornava vuoto sulle frasi e non poteva vincere. Due esperimenti dopo le cose
sono cambiate:

- con l'unione `all` non torna più vuoto (`2026-09-25_ibrido-congiuntivo/`:
  zero query a vuoto, known-item a 0,9579);
- il peso del vettore giusto dipende dal tipo di query: 160 sulle frasi, 10
  sugli identificativi (`2026-09-25_fusione/`).

Se per ogni query si sceglie fra una configurazione per le frasi e una per gli
identificativi, quanto si guadagna sulla migliore configurazione fissa, e
adesso che le due configurazioni competono davvero anche sulle frasi, c'è
spazio per scegliere oltre il tipo di query?

## Le due configurazioni

Tutte e due BM25, frequenza mescolata, `bge-m3` digest `790764642607` dalla
cache, unione con i 100 più vicini, somma lessicale più `sim * peso`:

- **A**: recupero `any`, peso **160**, il migliore su SciFact train e NFCorpus
  dev.
- **B**: recupero `all`, peso **10**, il migliore sulle known-item train.

I pesi vengono dalla calibrazione del difetto 3 (`131533Z_calibrazione.json`),
fatta con `any`; per B non si ricalibra con `all`, per non scegliere niente
guardando altro che gli split di calibrazione.

Più **L**, BM25 `all` senza vettori, che serve solo per una caratteristica: se
il recupero lessicale congiuntivo trova qualcosa. Sul test si riusano le L del
difetto 2 congiuntivo (13:20-13:21 UTC, stesso codice); sull'addestramento si
eseguono. E come riferimento le U del difetto 2 congiuntivo (`all`, unione,
peso 20), la migliore configurazione fissa trovata finora che regge i due tipi
di query.

Stessi split della scelta per query: known-item automatiche 300 + 300,
SciFact 809 + 300, NFCorpus 2.590 + 323. Metrica nDCG@10 query per query,
anche sulle known-item, come nella scelta per query.

## Le strategie

Le stesse della scelta per query, con una differenza: "B vuoto" diventa "L
vuoto", perché B con l'unione non è mai vuoto.

1. **Sempre A**, **sempre B**, e il riferimento **sempre U a 20**.
2. **Oracolo**: la migliore fra A e B, query per query.
3. **Regola della cifra**: B se la query ha una cifra.
4. **Ripiego**: B se L trova qualcosa, altrimenti A.
5. **Cifra e L non vuoto**: la regola a due condizioni della scelta per query.
6. **Classificatore**: la stessa regressione logistica, con le stesse otto
   caratteristiche (l'ultima è "L vuoto") e gli stessi parametri (passo 0,5,
   3.000 iterazioni, L2 0,01, soglia 0,5), addestrata sulle query di
   addestramento in cui A e B differiscono, pesate per la differenza, ogni
   collezione con peso totale 1.

Dati guardati prima di scrivere le previsioni: la media di U a 20 in nDCG@10
(0,6483, 0,3333 e 0,9675 sulle known-item, 0,6497), calcolata dalle
valutazioni già archiviate del difetto 2 congiuntivo.

## Prima di misurare

Scritto e committato prima di lanciare le valutazioni.

1. **Il guadagno del peso per tipo.** La regola a due condizioni fa almeno
   0,665 di media sulle tre collezioni, cioè almeno 0,015 sopra sia la
   migliore configurazione fissa (U a 20, 0,6497 in nDCG@10) sia il
   classificatore della scelta per query senza vettori (0,6473).
2. **Sempre A sulle known-item** crolla sotto 0,65: 160 sugli identificativi
   fa quello che faceva in calibrazione (0,50 di MRR sul train).
3. **Sempre B sulle frasi**: su SciFact entro 0,02 dal solo vettore (0,6436),
   perché L risponde a 10 query su 300 e il resto lo ordina il vettore; su
   NFCorpus fra 0,30 e 0,34.
4. **L'oracolo ha spazio oltre il tipo di query**: su SciFact almeno 0,03 sopra
   sempre A, dove nella scelta per query faceva zero. A e B adesso sono due
   ordinamenti diversi della stessa query (lessicale più vettore forte contro
   quasi solo vettore), e ciascuno vince su una parte delle frasi.
5. **Il classificatore non prende quello spazio**: sta entro 0,005 dalla regola
   a due condizioni sulla media. Le caratteristiche descrivono la forma della
   query, non dicono quale dei due ordinamenti sarà migliore su una frase.

Se la 1 tiene, il peso per tipo di query entra nel piano come la correzione del
difetto 3, e la regola va messa alla prova sulle known-item umane. Se tiene la
4 e non la 5, c'è un problema di scelta per query che la forma della query non
risolve, e va scritto come limite.

## Esito

`2026-09-25T133033Z_esito.json`, da `analizza.py` al commit `9799277` (albero
pulito), sulle quindici valutazioni delle 13:25-13:30 UTC più le tre L e le tre
U del difetto 2 congiuntivo, tutte Koskidex `f16b4c9`. Il classificatore ha
imparato da 1.839 query di addestramento in cui A e B differiscono (1.438
NFCorpus, 226 SciFact, 175 known-item); 1.860 pari escluse.

nDCG@10 sul test:

| strategia | known-item | SciFact | NFCorpus | media |
|---|---|---|---|---|
| sempre A (`any`, 160) | 0,5589 | **0,7067** | **0,3441** | 0,5366 |
| sempre B (`all`, 10) | **0,9680** | 0,6483 | 0,3325 | 0,6496 |
| sempre U (`all`, 20), riferimento | 0,9675 | 0,6483 | 0,3333 | 0,6497 |
| oracolo | 0,9731 | 0,7280 | 0,3655 | 0,6889 |
| regola della cifra | 0,9680 | 0,6881 | 0,3438 | 0,6666 |
| ripiego (B, se L vuoto A) | 0,9680 | 0,7072 | 0,3433 | **0,6728** |
| **cifra e L non vuoto** | **0,9680** | 0,7067 | 0,3438 | **0,6728** |
| classificatore | 0,9680 | 0,7036 | 0,3432 | 0,6716 |
| classificatore senza vettori (`scelta-per-query`) | 0,9687 | 0,6694 | 0,3038 | 0,6473 |

**Il peso del vettore scelto per tipo di query vale +0,023 di nDCG@10 medio
sulla migliore configurazione fissa**, e +0,026 sulla scelta per query senza
vettori. Per prenderlo basta ancora la regola a due condizioni: la query ha una
cifra e il recupero lessicale congiuntivo trova qualcosa. Anche il ripiego fa
lo stesso in media.

**E adesso l'oracolo ha spazio oltre il tipo di query**: 0,016 sopra la regola,
quasi tutto sulle frasi (+0,021 su SciFact, +0,021 su NFCorpus), dove nella
scelta per query senza vettori faceva zero. A e B sono ormai due ordinamenti
diversi della stessa frase, lessicale con vettore forte contro quasi solo
vettore, e B vince su 29 query di SciFact su 300 e su 82 di NFCorpus su 323. Ma
nessuno lo sa riconoscere dalla forma della query: il classificatore manda a B
21 query di SciFact e ci perde (0,7036 contro 0,7067 di sempre A), e su NFCorpus
ne manda 156 e perde 0,001. I pesi dicono che ha imparato la stessa regola di prima
(quota di cifre +0,98, L vuoto -0,64) e poco altro.

### Le previsioni

1. La regola a due condizioni almeno 0,665 di media, almeno 0,015 sopra U a 20
   e sopra il classificatore senza vettori: **0,6728, +0,023 e +0,026,
   confermata.**
2. Sempre A sulle known-item sotto 0,65: **0,5589, confermata.**
3. Sempre B su SciFact entro 0,02 dal solo vettore, su NFCorpus fra 0,30 e
   0,34: **0,6483 (+0,005) e 0,3325, confermata.** Su SciFact B e U a 20
   coincidono: quando il lessicale è vuoto il peso non cambia l'ordine.
4. L'oracolo almeno 0,03 sopra sempre A su SciFact: **+0,021, smentita** nella
   misura, non nel verso: lo spazio c'è, più piccolo di come lo davo.
5. Il classificatore entro 0,005 dalla regola: **-0,0012, confermata.**

### Cosa vuol dire per la tesi

La correzione del difetto 3 ha una forma precisa: due configurazioni, una per
le frasi (`any`, peso 160) e una per gli identificativi (`all`, peso 10), e una
regola di una riga per scegliere. Vale +0,023 sulla migliore configurazione
fissa, e resta il rischio già dichiarato nella scelta per query: qui ogni tipo
di query sta in una collezione diversa, e la regola può riconoscere la
collezione più che il tipo. La prova sono le known-item umane.

Resta un limite da scrivere: 0,016 di nDCG@10 medio che un oracolo prende e
nessuna caratteristica della query sa prendere. Sono query in cui il vettore da
solo ordina meglio del lessicale col vettore, e per saperlo bisognerebbe
guardare i risultati, non la query.

