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
