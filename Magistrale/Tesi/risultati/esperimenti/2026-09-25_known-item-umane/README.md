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
