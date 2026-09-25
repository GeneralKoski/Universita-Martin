# Le stopword o le loro espansioni?

**Domanda.** Nella voce E1 del diario di Koskidex (23/09/2026) le stopword
inglesi portano SciFact da 0,6197 a 0,6641 di nDCG@10 con BM25, e la
spiegazione era: le parole funzionali pesano troppo. Due giorni dopo la
frequenza mescolata (`Settings.BM25Expansion = "blended"`) ha mostrato che una
stopword di due o tre lettere è anche un prefisso larghissimo (`the` combacia
con `theory`, `in` con `insulin`), e che BM25 pesava quelle espansioni con il
loro IDF, alto. Quanto del guadagno delle stopword veniva dalle parole
funzionali, e quanto dalle loro espansioni per prefisso?

**Cosa si sa già, dai file in archivio** (`koskidex-beir/2026-09-25T0910*`, Koskidex
`f449b02`), e quindi non è una previsione:

| SciFact, nDCG@10 | senza analisi | con le stopword | guadagno |
|---|---|---|---|
| espansioni pesate col termine trovato (di serie) | 0,6197 | 0,6641 | +0,044 |
| frequenza mescolata | 0,6694 | 0,6757 | +0,006 |

Con le espansioni corrette il guadagno delle stopword scende di sette volte. È
un indizio, non una prova: la frequenza mescolata cambia il peso di tutte le
espansioni, non solo di quelle delle stopword.

## Metodo

1. **Il controfattuale diretto.** SciFact e NFCorpus con `scripts/evaluate`,
   recupero `any`, BM25 di serie, **ricerca per prefisso spenta**
   (`-senza-prefisso`), senza analisi e con le stopword. Se il guadagno veniva
   dalle espansioni, senza prefisso sparisce.
2. **Il conto sulle query** (`analizza.py`). Sulle query di test di SciFact,
   con la tokenizzazione di Koskidex replicata e il vocabolario del corpus
   (titolo e testo in un campo, come in valutazione): quante query contengono
   una stopword di almeno due lettere, quindi espandibile (sotto le due lettere
   Koskidex non espande), quante espansioni porta ciascuna, e con che
   frequenza documentale rispetto alla stopword.
3. **Dove sta il guadagno.** Dalle due valutazioni già archiviate col prefisso
   acceso (`091020Z` e `091036Z`), la differenza di nDCG@10 query per query,
   divisa fra le query con e senza una stopword espandibile.

Nessuna modifica al codice di Koskidex: si misura con impostazioni che
esistono già.

## Prima di misurare

Scritto e committato prima di lanciare le valutazioni e lo script.

1. **Senza ricerca per prefisso, le stopword portano SciFact meno di 0,01**,
   contro lo 0,044 col prefisso acceso. BM25 pesa già poco una parola
   frequente: senza espansioni, toglierla cambia poco.
2. **Più di metà delle query di test di SciFact contiene almeno una stopword
   espandibile.** Sono domande in inglese (`the`, `of`, `in` ricorrono
   ovunque).
3. **Il guadagno col prefisso acceso sta nelle query con una stopword
   espandibile**: quelle senza portano meno del 10% del guadagno totale. Una
   query senza stopword non cambia; cambiano solo le lunghezze dei documenti.

Su NFCorpus le stopword portavano solo +0,009 anche col prefisso acceso
(0,2810 contro 0,2900): la misura si fa, ma non è abbastanza grande da
confermare o smentire qualcosa, e non ha una previsione.

## Esito

`2026-09-25T093916Z_esito.json`, da `analizza.py` al commit `f668ea3`. Le
valutazioni col prefisso spento vengono da Koskidex `ca2aed3`, albero pulito;
i file si chiamano `*_scifact-scifact-*` e `*_nfcorpus-nfcorpus-*` perché
`scripts/evaluate` antepone già la collezione al nome del run. Quelle col
prefisso acceso vengono da `f449b02`: rifatte su `ca2aed3` come controllo di
sviluppo (non archiviato) danno gli stessi 0,6197 e 0,6641.

| SciFact, BM25, nDCG@10 | senza analisi | con le stopword | guadagno |
|---|---|---|---|
| prefisso acceso, espansioni col termine trovato | 0,6197 | 0,6641 | +0,044 |
| prefisso acceso, frequenza mescolata | 0,6694 | 0,6757 | +0,006 |
| **prefisso spento** | **0,6634** | **0,6664** | **+0,003** |

NFCorpus col prefisso spento: 0,3062 senza analisi e 0,3072 con le stopword.

**Il guadagno delle stopword su SciFact veniva quasi tutto dalle loro
espansioni.** Spenta la ricerca per prefisso, toglierle porta 0,003: le parole
funzionali in sé BM25 le pesava già poco. Senza prefisso e senza stopword
SciFact fa 0,6634, quanto le stopword col prefisso acceso: le stopword
funzionavano perché spegnevano la ricerca per prefisso proprio sulle parole
che la usavano peggio.

**Il meccanismo, contato.** 271 query di test su 300 contengono almeno una
stopword espandibile. `of` compare in 173 query e sta in 5.173 documenti su
5.183, ma porta 26 espansioni con una frequenza mediana di 2 documenti; `in`
ne porta 933, di cui 332 in un documento solo. BM25 pesava ogni espansione con
il suo IDF: chiedere `of` voleva dire premiare chi contiene `offspring`.

**Dove sta il guadagno.** Le 271 query con una stopword espandibile guadagnano
in media 0,049; le 29 senza 0,003, e ne cambiano solo 4 (per le lunghezze dei
documenti, che senza stopword si accorciano). Le query senza portano lo 0,7%
del guadagno totale.

### Le previsioni

1. Senza prefisso le stopword portano meno di 0,01: **+0,003, confermata.**
2. Più di metà delle query contiene una stopword espandibile: **271 su 300,
   confermata.**
3. Le query senza portano meno del 10% del guadagno: **0,7%, confermata.**

### Cosa cambia

La spiegazione della voce E1, "le parole funzionali pesano troppo", è
sbagliata: le stopword su SciFact correggevano un difetto delle espansioni per
prefisso, lo stesso che la frequenza mescolata corregge per tutti i termini. In
tesi il guadagno delle stopword non va presentato come un effetto dell'analisi
lessicale. E il confronto giusto con i riferimenti BEIR, che sono senza
prefisso, è con la frequenza mescolata: 0,6694 senza analisi, 0,6757 con le
stopword.
