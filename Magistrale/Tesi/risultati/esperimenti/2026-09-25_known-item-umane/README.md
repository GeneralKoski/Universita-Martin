# Known-item umane: ritrovare un atto di cui si ricorda il contenuto

**Domanda.** Le 300 known-item automatiche misurano una sola forma di query,
`<numero> <comune>`. Chi cerca un atto visto settimane prima ne ricorda
l'argomento e qualche parola, raramente il numero. Su query scritte da persone
che non conoscono i motori, come se la cavano Elasticsearch di produzione,
Koskidex innestato con il profilo consigliato e le configurazioni di Koskidex
misurate nei capitoli 5 e 7? E cambia qualcosa fra le due fonti, dato che per
Crispiano la persona ha letto il testo intero e l'indice ha la scheda?

Scritto il 25/09/2026, prima che arrivi una sola risposta: nessuna query umana
è stata vista.

## Metodo

**Le query.** La raccolta della parte 1 di `../../../istruzioni-annotazione.md`:
160 atti in quattro lotti, metà per fonte e per genere, una persona per lotto.
`strumenti/importa-raccolta.py` scrive la collezione (`query/known-item-umane/`):
una query per atto, giudizio grado 2 sull'atto mostrato. Le query vuote ("non
saprei") non entrano nella collezione e si contano a parte. Si misura solo a
raccolta chiusa, con tutti i file arrivati.

*Aggiunto il 28/09/2026, dopo l'arrivo dei primi due lotti.* Il file del
lotto 2 si chiama `raccolta-lotto-2-Martin.json`, e con quel nome compare in
`query/known-item-umane/riassunto.json`: il nome è quello che la persona ha
scritto nella pagina di raccolta, ed è un omonimo dell'autore della tesi, non
l'autore. Nessuna query della collezione è scritta dall'autore.

*Aggiunto il 29/09/2026, prima di qualunque misura sulla raccolta completa.*
La raccolta si chiude con tre lotti su quattro: il lotto 3 è arrivato il
29/09 (`raccolta-lotto-3-endri.json`), il quarto non è mai stato assegnato.
Le istruzioni chiedevano tre persone come minimo, e la decisione di chiudere
qui dipende dal tempo, non dai numeri di questo esperimento: le sole
esecuzioni fatte finora sulle query dei primi due lotti sono la prova
generale del 28/09, per provare la procedura, in una cartella temporanea e
non archiviata, e le guardie di altri esperimenti (`date-app`,
`importi-esatti`, `reranker`), che le usano per controllare che un
intervento non cambi niente.

**I motori**, sulle stesse query:

- **dall'app**, con `app:eval-run-queries` sul corpus di Documentale e
  `scripts/evaluate -rankings` per le metriche:
  - **ES**: Elasticsearch come lo usa Documentale in produzione;
  - **KC**: Koskidex innestato con `KOSKIDEX_PROFILO=consigliata`, senza vettori
    (capitolo 6), da un indice ricostruito da zero;
- **Koskidex piatto**, con `scripts/evaluate` sul corpus a schede
  (`beir-metadata`, 10.018 atti, titolo e testo in un campo, refusi spenti):
  - **K0**: il baseline (`all`, punteggio euristico);
  - **LA**: BM25, `any`, frequenza mescolata;
  - **LT**: BM25, `all`, frequenza mescolata;
  - **A**: LA più i vettori, unione, peso 160 (la configurazione per le frasi
    del capitolo 7);
  - **B**: LT più i vettori, unione, peso 10 (quella per gli identificativi);
  - **V**: solo vettori, i 100 più vicini.

  Vettori `bge-m3`, contesto predefinito (le schede sono sotto i 2.048 token,
  `2026-09-25_contesto-ollama/`).

**Le metriche.** Un atto giusto per query: MRR@10 come misura principale, atto
primo, atto entro i primi dieci, query a vuoto. `analizza.py` le riporta su
tutte le query, **per fonte** (Crispiano, Friuli Venezia Giulia) e **per query
con e senza un numero** (una cifra qualsiasi nel testo), da `raccolta.json`.

**Cosa non misura.** L'ordine fra atti tutti pertinenti (ce n'è uno solo), e le
ricerche di chi non sa che l'atto esiste.

## Prima di misurare

1. **Meno del 25% delle query contiene un numero.** Chi ricorda un atto dopo
   settimane ne ricorda l'argomento, non il protocollo.
2. **ES: più del 30% di query a vuoto, atto entro 10 in meno della metà delle
   query.** Tutte le parole devono stare nello stesso campo della scheda, e chi
   scrive aggiunge facilmente il comune, un anno o una parola del testo.
3. **KC fa almeno 0,10 di MRR@10 sopra ES, con almeno 10 punti percentuali di
   query a vuoto in meno.** Le parole possono stare in campi diversi, e
   l'elisione trova *infanzia* in *dell'infanzia*.
4. **Sulle query senza numero LA supera LT di almeno 0,05 di MRR@10; su quelle
   con un numero LT supera LA.** Una parola in più, o scritta diversa, svuota il
   recupero congiuntivo.
5. **A è la migliore configurazione piatta sulle query senza numero, almeno
   0,03 sopra LA.**
6. **Crispiano sotto il Friuli Venezia Giulia: per LA e per KC l'MRR@10 su
   Crispiano è almeno 0,10 più basso.** Su Crispiano la persona ha letto il
   testo intero e scrive parole che nella scheda non ci sono.
7. **V: sulle query senza numero entro 0,10 da LA; su quelle con un numero
   sotto 0,30.**

Se la 2 e la 3 tengono, il difetto del campo unico del capitolo 6 non riguarda
solo le ricerche per numero ma anche quelle per contenuto.

## Esito

Misurato il 29/09/2026 sulla raccolta chiusa (tre lotti, 120 atti mostrati,
104 query, 16 vuote, 50 di Crispiano e 54 del Friuli Venezia Giulia), Koskidex
`cd86102`. Riassunto in `2026-09-29T094732Z_esito.json` (`analizza.py`), con le
otto valutazioni in `valutazioni-albo/2026-09-29T0930*` e `0933*`; i rapporti
dell'app con il testo delle query restano fuori dal repository, come le
risposte. Gli esiti delle 09:41 e delle 09:42 hanno gli stessi risultati: i
due rilanci aggiungono solo le parole per query e le risposte vuote per lotto
(4, 0 e 12 su 40), che l'Esito e la tesi citano.

**Le valutazioni dall'app sono rifatte.** Il primo giro (09:31) ha lasciato a
ES e KC le metriche di K0: `app:eval-run-queries` colora l'output anche in una
pipe quando `FORCE_COLOR` è impostata, `esegui.sh` non trovava il percorso del
rapporto e `evaluate -rankings` riceveva un argomento vuoto. I due file sono
stati tolti senza essere committati; lo script ora passa `--no-ansi` e si ferma
se non trova il rapporto (`5897f6a`), e il rilancio delle 09:33 è quello usato.

| | MRR@10 | atto primo | entro 10 | a vuoto | Crispiano | FVG | con numero (4) | senza numero (100) |
|---|---|---|---|---|---|---|---|---|
| ES | 0,326 | 27,9% | 42,3% | 46,2% | 0,227 | 0,417 | 0,000 | 0,339 |
| KC | 0,432 | 34,6% | 58,7% | 29,8% | 0,320 | 0,536 | 0,000 | 0,449 |
| K0 | 0,337 | 25,0% | 51,0% | 43,3% | 0,308 | 0,364 | 0,063 | 0,348 |
| LA | 0,559 | 45,2% | 76,0% | 1,0% | 0,477 | 0,635 | 0,750 | 0,552 |
| LT | 0,346 | 28,8% | 47,1% | 43,3% | 0,243 | 0,442 | 0,083 | 0,357 |
| A | **0,613** | 49,0% | 85,6% | 0,0% | 0,557 | 0,665 | 0,778 | **0,606** |
| B | 0,607 | 50,0% | 83,7% | 0,0% | 0,506 | 0,700 | 0,675 | 0,604 |
| V | 0,520 | 39,4% | 75,0% | 0,0% | 0,467 | 0,569 | 0,650 | 0,515 |

**Cinque previsioni confermate, due a metà.** Le due a metà cadono entrambe
sulla metà che riguarda le query con un numero, che sono 4: su 4 query una
sola differenza di posizione sposta l'MRR di 0,25, e quella metà delle due
previsioni non dice molto né in un senso né nell'altro.

1. **Confermata.** Contiene un numero il 3,8% delle query (4 su 104).
2. **Confermata.** ES lascia a vuoto il 46,2% delle query e trova l'atto entro
   i primi dieci nel 42,3%.
3. **Confermata, di poco sul primo numero.** KC fa +0,106 di MRR@10 su ES
   (0,432 contro 0,326) e ha 16,3 punti di query a vuoto in meno (29,8% contro
   46,2%).
4. **A metà.** Sulle query senza numero LA supera LT di 0,195 (0,552 contro
   0,357): confermata. Su quelle con un numero LT non supera LA ma resta molto
   sotto (0,083 contro 0,750): smentita. La previsione immaginava query con il
   numero e poche altre parole, dove il congiuntivo aiuta; le quattro query con
   un numero sono frasi, da 5 a 9 parole (mediana 6,5 contro 3 delle query
   senza numero), e il congiuntivo le svuota come le altre (LT a vuoto su 3
   delle 4).
5. **Confermata.** Sulle query senza numero A è la configurazione piatta
   migliore, 0,606, sopra LA di 0,055. B è a 0,002 da A: sulle frasi scritte da
   persone le due configurazioni ibride del capitolo 7 si equivalgono.
6. **Confermata.** Crispiano sotto il Friuli Venezia Giulia di 0,158 per LA
   (0,477 contro 0,635) e di 0,216 per KC (0,320 contro 0,536).
7. **A metà.** Sulle query senza numero V è a 0,036 da LA (0,515 contro 0,552):
   confermata. Su quelle con un numero V fa 0,650 e non resta sotto 0,30:
   smentita. Come nella 4, le quattro query con un numero sono frasi, e il
   resto della frase basta ai vettori per ritrovarle.

Tengono la 2 e la 3: il difetto del campo unico riguarda anche le ricerche per
contenuto. Resta però un divario grande fra KC e le configurazioni piatte
disgiuntive (0,432 contro 0,559 di LA, 29,8% di query a vuoto contro l'1%):
Koskidex innestato parte dagli stessi insiemi di Elasticsearch, e quindi ne eredita
il recupero congiuntivo sui campi, che sulle frasi è il limite principale. Le
correzioni del profilo consigliato (capitolo 6) ne recuperano una parte, 16
punti di query a vuoto, non tutto.
