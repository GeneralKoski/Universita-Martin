# Niente refusi sui numeri

**Domanda.** Con le parole libere di stare in campi diversi, Koskidex innestato
trova l'atto giusto entro i primi dieci nel 93% delle known-item `<numero>
<comune>`, ma lo mette primo solo nel 38%. In 154 dei 185 casi in cui non è
primo lo scavalca un atto con il numero a un refuso, `1109` per `1209`
(`2026-09-25_koskidex-campi-liberi/`). Lo stesso difetto mette `ordinanza 187`
al 12° posto in produzione (`2026-09-23_numero-atto/`). Cosa succede se un
numero deve combaciare esattamente?

## Metodo

- In Koskidex, `Settings.TypoTolerance.DisableOnNumbers`
  (`typo_tolerance.disable_on_numbers`), **spento per default**. Acceso, un
  termine della query fatto di sole cifre non ammette refusi. È la stessa
  impostazione, con lo stesso nome e la stessa definizione, che Meilisearch ha
  aggiunto nella v1.15 (`typoTolerance.disableOnNumbers`), spenta anche lì per
  default. I codici misti restano con i refusi: `a651` ne ammette uno come
  oggi. Una `fuzziness` esplicita nella richiesta vince sull'impostazione, come
  vince oggi su `enabled`.
- In Documentale, `config('services.koskidex.typos_on_numbers')`
  (`KOSKIDEX_TYPOS_ON_NUMBERS`), **acceso per default**: senza toccare
  l'ambiente l'app si comporta come oggi.
- Koskidex reindicizzato dall'app, poi le 300 known-item e le 24 query del
  confronto con `app:eval-run-queries`, in due configurazioni: con le parole
  in campi diversi (quella che interessa) e con il vincolo del campo unico
  (per chiudere il quadrato due per due con le misure già fatte).
- Valutazione con `scripts/evaluate -rankings -top 10`, lo stesso codice delle
  altre. Le posizioni di `doc-0001` per `ordinanza 187` e di `doc-0002` per
  `determina 1223` si leggono dai rapporti del confronto.

**Cosa non si misura, e perché.** Sulle collezioni pubbliche (SciFact,
NFCorpus) e sulle known-item con Koskidex piatto la valutazione gira con i
refusi spenti, per essere confrontabile con i BM25 pubblicati
(`internal/eval/koskidex.go`). Lì l'impostazione non agisce per costruzione, e
una misura darebbe numeri identici senza dire niente.

## Prima di misurare

Scritto e committato prima di toccare il codice di Koskidex e di Documentale.

1. **Parole in campi diversi, known-item: l'atto è primo in più dell'80% delle
   query** (dal 38,3%), MRR@10 oltre 0,85. Dei 185 casi in cui oggi non è primo,
   154 perdono contro un numero a un refuso, che non combacia più. Non si
   arriva oltre il 92%: nei 29 casi in cui vince un atto con il numero esatto
   l'impostazione non cambia niente.
2. **Atto entro 10 non sotto il 93,3%, nessuna query a vuoto, Recall@100
   almeno 0,99.** L'atto giusto contiene il numero tale e quale, quindi
   togliere i refusi toglie concorrenti e non l'atto.
3. **Sulle 24 query del confronto cambiano solo le tre con un numero**
   (`delibera di giunta sul bilancio di previsione 2026`, `determina 1223`,
   `ordinanza 187`), e i loro insiemi si restringono soltanto. Le altre 21
   sono identiche a quelle con i refusi sui numeri. `doc-0001` è primo per
   `ordinanza 187` e `doc-0002` per `determina 1223`.
4. **Con il vincolo del campo unico non cambia quasi niente**: atto entro 10
   non oltre il 3%, query a vuoto almeno il 70%. Il vincolo è la causa delle
   query a vuoto, e togliere i refusi può solo restringere gli insiemi.

## Esito

`2026-09-25T093350Z_esito.json`, da `analizza.py` al commit `757163e`, sui
rapporti di Koskidex `ae1c4b9` passato dall'app a Documentale `ab52f4f`, alberi
puliti. Dopo ogni reindicizzazione le impostazioni dell'indice sono state
rilette: `disable_on_numbers: true`, `all_terms_in_one_field` come voluto, il
resto invariato.

| known-item, dall'app | MRR@10 | atto primo | atto entro 10 | a vuoto | ms, mediana |
|---|---|---|---|---|---|
| campo unico, refusi sui numeri (oggi) | 0,018 | 1,7% | 2,0% | 70% | 5,4 |
| campo unico, numeri esatti | 0,020 | 2,0% | 2,0% | **95%** | 4,6 |
| parole libere, refusi sui numeri | 0,548 | 38,3% | 93,3% | 0 | 5,0 |
| **parole libere, numeri esatti** | **0,950** | **91,7%** | **99,7%** | **0** | **4,3** |

Le righe con i refusi sui numeri vengono dalle misure precedenti, con Koskidex
`f6810d0` e `9d95eb6`: fra quei commit e `ae1c4b9` cambiano solo impostazioni
spente per default e gli strumenti di valutazione, e `TestBaselineRankingIsFrozen`
passa a ogni commit. I tempi sono di esecuzioni diverse sulla stessa macchina,
da leggere come ordine di grandezza.

**Le due correzioni insieme portano l'atto giusto al primo posto in 275 query
su 300**, da 5. Nessuna delle due basta da sola: il vincolo del campo unico
decide se l'atto si trova, i refusi sui numeri decidono se è primo.

**Chi resta davanti**, nelle 25 query in cui l'atto non è primo:

- in 21 il primo classificato ha lo stesso numero, esatto, in un campo che pesa
  di più (il numero dell'atto giusto sta in `additional_data`, che pesa 1);
- in 3 lo ha esatto in un campo che non pesa di più;
- in 1 non lo ha esatto: `A647/2026 GORIZIA`, vinta da un atto con `a649`. È
  l'unico codice misto fra i perdenti, e tiene i refusi per scelta.

L'unico atto oltre il decimo posto è quello di `3 UDINE`: un numero di una
cifra, che già prima non ammetteva refusi.

**Con il vincolo del campo unico le query a vuoto salgono dal 70% al 95%.** Il
30% che prima rispondeva qualcosa rispondeva per lo più grazie a un refuso sul
numero: degli 89 insiemi non vuoti, 74 si svuotano, e nessuna query vuota
comincia a rispondere.

Sulle 24 query del confronto cambiano solo `ordinanza 187` e `determina 1223`,
a parità di vincolo, e si restringono soltanto: con le parole libere da 124 e
10 risultati a uno solo ciascuna, l'atto giusto. La terza query con un numero,
`delibera di giunta sul bilancio di previsione 2026`, non restituisce niente in
nessuna configurazione, e non poteva cambiare. Le altre 21 sono identiche.

| posizione dell'atto giusto | `ordinanza 187` | `determina 1223` |
|---|---|---|
| Elasticsearch, produzione | 12° su 85 | 5° su 8 |
| Koskidex, campo unico, refusi sui numeri | 47° su 85 | 1° su 8 |
| Koskidex, parole libere, refusi sui numeri | 63° su 124 | 1° su 10 |
| **Koskidex, numeri esatti (tutti e due i vincoli)** | **1° su 1** | **1° su 1** |

### Le previsioni

1. Con le parole libere l'atto è primo in più dell'80% delle query ma non oltre
   il 92%, MRR@10 oltre 0,85: **91,7% e 0,950, confermata.** Il tetto teneva
   per la ragione prevista: davanti restano atti con il numero esatto.
2. Atto entro 10 non sotto il 93,3%, nessuna query a vuoto, Recall@100 almeno
   0,99: **99,7%, zero, 1,0, confermata.**
3. Delle 24 cambiano solo le query con un numero, e si restringono; `doc-0001`
   e `doc-0002` primi: **confermata**, con una precisazione. Le query cambiate
   sono due e non tre, perché la terza è vuota comunque.
4. Con il campo unico non cambia quasi niente, entro 10 non oltre il 3% e a
   vuoto almeno il 70%: **confermata nei numeri (2% e 95%), ma "quasi niente"
   era sbagliato.** Le query a vuoto crescono di 25 punti: con quel vincolo, a
   rispondere erano per lo più i numeri sbagliati.

### Cosa vuol dire

La ricerca per numero e comune, che in produzione trova l'atto entro i primi
dieci nel 2% dei casi, con Koskidex e due impostazioni lo mette primo nel 92%.
Sono due difetti distinti del matching copiato da Elasticsearch, e la parità
fra i due motori li eredita entrambi. Elasticsearch in produzione ha ancora
tutti e due: `ElasticsearchService` resta com'è, per restare il baseline.
