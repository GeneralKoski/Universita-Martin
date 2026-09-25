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
