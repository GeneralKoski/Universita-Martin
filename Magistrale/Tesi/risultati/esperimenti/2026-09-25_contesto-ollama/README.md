# Quanto testo legge bge-m3 attraverso Ollama

**Domanda.** La sezione 7.1 della tesi dà per scontato che il testo intero di
un atto di Crispiano, fra 5 e 13 mila caratteri, stia nel contesto di `bge-m3`,
8.192 token. Ma Koskidex chiede i vettori a Ollama senza dire quanto contesto
usare, e Ollama ha un contesto predefinito suo. Fino a quanti token del testo
arriva davvero il vettore, quanti atti ne restano tagliati, e basta chiedere a
Ollama un contesto più grande?

**Dichiarato.** Preparando le misure sulle known-item umane ho fatto una prova
di sviluppo, non archiviata: testi lunghi con lo stesso inizio e code diverse.
Fino a circa 1.500 token i vettori differiscono; da circa 2.000 token in su
sono identici, e Ollama riporta al più 2.048 token letti. Le previsioni qui
sotto sono scritte dopo quella prova, e quelle sul troncamento a 2.048 ne
dipendono: sono una conferma formale, non un'ipotesi. Le altre (il contesto
più grande, quanti atti superano la soglia) non le ho misurate.

## Metodo

`misura.py`, che parla con Ollama direttamente (non passa da Koskidex), sul
corpus esportato da Documentale (`beir-full`, che per i 563 atti di Crispiano
ha il testo intero e per gli altri la scheda):

1. **Dove taglia.** Un testo lungo fatto dei testi interi di Crispiano uno
   dopo l'altro; per ogni lunghezza del prefisso (da 1.000 a 40.000 caratteri)
   due richieste con lo stesso prefisso e due code diverse. Se i due vettori
   coincidono, la coda non è stata letta. Si registra la differenza massima
   fra le componenti e i token che Ollama dice di aver letto
   (`prompt_eval_count`). Con il contesto predefinito e con `num_ctx` 8.192.
2. **Quanti atti.** Per ciascuno dei 563 testi interi e per ogni scheda, i
   token letti da Ollama con `num_ctx` 8.192, una richiesta per testo: quanti
   superano 2.048 token, quanti arrivano a 8.192 (e quindi sono tagliati anche
   così). Lo stesso per i documenti di SciFact e NFCorpus (aggiunto sotto).

Modello `bge-m3`, con l'impronta registrata nel file di esito.

## Prima di misurare

1. **Con il contesto predefinito Ollama legge al più 2.048 token**: da lì in
   su i due vettori coincidono (differenza massima 0), sotto no.
2. **Con `num_ctx` 8.192 legge fino a 8.192 token**: i vettori differiscono
   fino a quella lunghezza e coincidono oltre.
3. **Fra il 30% e il 70% dei 563 testi interi supera 2.048 token**: 5-13 mila
   caratteri di italiano amministrativo sono dell'ordine di 1.500-4.000 token.
4. **Meno del 5% dei testi interi arriva a 8.192 token.**
5. **Nessuna scheda supera 2.048 token** (la più lunga ha 1.409 caratteri):
   nessun vettore misurato finora nella tesi, tutti su schede o su abstract,
   è stato tagliato. Per SciFact e NFCorpus la misura non si fa qui.

Se la 5 cade, i numeri del capitolo 7 vanno rimisurati.

**Aggiunto dopo le previsioni, prima di misurare.** La guardia della 5 vale
solo se copre tutte le collezioni del capitolo 7: `misura.py` conta i token
anche dei documenti di SciFact e NFCorpus, titolo e testo in un campo come in
valutazione. Previsione, nello stesso spirito:

6. **Meno dell'1% dei documenti di SciFact e di NFCorpus supera 2.048 token**,
   e i numeri del capitolo 7 cambiano al più in modo trascurabile.

**Cambiato prima della misura, dopo una prova su dati inventati.** Nella prova
di `2026-09-25_scheda-testo` su query inventate, A con `-contesto 8192` e A
con il contesto predefinito hanno dato gli stessi numeri query per query.
Chiesto a Ollama 0.34.4 quanti token legge del testo più lungo: 2.048 senza
opzioni, 2.048 con `num_ctx` 4.096 o 8.192, 8.192 con `num_ctx` e
`num_batch` 8.192, 1.024 con `num_ctx` 1.024. Ollama taglia al minimo fra
`num_ctx` e `num_batch`, che vale 2.048. La previsione 2 è quindi già
smentita da quella prova; resta scritta com'era e si misura com'era
registrata. Due modifiche a `misura.py`, dichiarate qui:

- il punto 1 del metodo misura anche una terza variante, `num_ctx` e
  `num_batch` 8.192;
- il punto 2 conta i token con `num_ctx` e `num_batch` 8.192: con il solo
  `num_ctx` ogni conteggio si fermerebbe a 2.048 e non direbbe niente.

La prima esecuzione, partita con il codice di prima, è stata fermata a metà
del conteggio senza archiviare niente. Koskidex manda `num_batch` insieme a
`num_ctx` da `ffa38ab`.

## Esito

Da `2026-09-25T194540Z_esito.json` (commit `822c97e`, albero pulito, Ollama
0.34.4, `bge-m3` con impronta `790764642607`).

**Dove taglia.** Due richieste con lo stesso prefisso e due code diverse:

| prefisso (caratteri) | predefinito | `num_ctx` 8.192 | `num_ctx` e `num_batch` 8.192 |
|---|---|---|---|
| 6.000 | 1.832 token, vettori diversi | uguale al predefinito | 1.832, diversi |
| 8.000 | 2.048, diversi | uguale | 2.286, diversi |
| 10.000 | 2.048, **identici** | uguale | 2.850, diversi |
| 25.000 | 2.048, identici | uguale | 6.823, diversi |
| 30.000 | 2.048, identici | uguale | 8.117, diversi |
| 35.000 | 2.048, identici | uguale | 8.192, **identici** |

A 8.000 caratteri i vettori differiscono ancora anche con 2.048 token letti:
il prefisso da solo ne occupa circa 1.960, e i primi token delle code
rientrano. Il taglio tiene l'inizio del testo.

**Quanti documenti**, token letti con `num_ctx` e `num_batch` 8.192:

| | documenti | oltre 2.048 | a 8.192 | mediana | massimo |
|---|---|---|---|---|---|
| testi interi di Crispiano | 563 | 334 (59%) | 3 | 2.168 | 8.192 |
| schede (atti del Friuli Venezia Giulia) | 9.455 | 0 | 0 | 88 | 486 |
| SciFact | 5.183 | 3 (0,06%) | 0 | 356 | 2.256 |
| NFCorpus | 3.633 | 2 (0,06%) | 0 | 393 | 2.610 |

Previsione per previsione:

1. **Confermata.** Con il contesto predefinito Ollama legge al più 2.048
   token; da 10.000 caratteri in su i vettori coincidono, sotto no.
2. **Smentita**, come la prova dichiarata sopra aveva già mostrato: con il
   solo `num_ctx` 8.192 ogni riga è identica al predefinito. Servono
   `num_ctx` e `num_batch` insieme, e allora legge fino a 8.192 token.
3. **Confermata.** Il 59% dei testi interi (334 su 563) supera 2.048 token:
   più della metà del testo di un atto su due non arrivava al vettore.
4. **Confermata.** Solo 3 testi interi (0,5%) arrivano a 8.192 token.
5. **Confermata.** Nessuna scheda supera 2.048 token, la più lunga ne ha 486.
   Le schede dei 563 atti di Crispiano non sono contate a parte (nel corpus
   `beir-full` quegli atti hanno il testo intero), ma la più lunga delle
   schede di `beir-metadata` ha 1.409 caratteri e resta lontana dalla soglia.
   I vettori delle misure di Documentale e dell'albo nel capitolo 7 non sono
   stati tagliati.
6. **Confermata.** 3 documenti di SciFact e 2 di NFCorpus superano 2.048
   token, di al più 208 e 562 token: lo 0,06% di ciascun corpus, troppo poco
   per spostare i numeri del capitolo 7.

**Cosa ne segue.** I numeri del capitolo 7 restano validi. La sezione 7.1,
che dava il testo intero sotto il contesto di `bge-m3`, è sbagliata e va
corretta: attraverso Ollama il limite era 2.048 token, e più della metà dei
testi interi lo supera. `embedder.context` in Koskidex (con `num_batch`, da
`ffa38ab`) lo alza fino agli 8.192 del modello; quanto questo conti per la
pertinenza lo dice la previsione 4 di `2026-09-25_scheda-testo`.
