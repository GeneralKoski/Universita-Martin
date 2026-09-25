# Da fare a mano

Le cose della tesi che non sono sviluppo: servono persone, una decisione o un
incontro. Il piano ([piano.md](piano.md)) resta l'unico elenco completo; qui
c'è solo quello che tocca a Martin, con quello che serve per farlo.

## Persone e raccolta

- [ ] **Known-item umane.** Trovare tre o quattro persone che non sappiano come
      funzionano i motori, un lotto a testa. Mandare in privato la pagina del
      lotto (`risultati/query/known-item-umane/pagine/raccolta-lotto-N.html`,
      si rigenera con `risultati/strumenti/prepara-raccolta.py`), farsi
      rimandare il file `.json`, copiarlo così com'è in
      `risultati/query/known-item-umane/risposte/`, lanciare
      `python3 risultati/strumenti/importa-raccolta.py` e committare. Martin
      non compila le pagine: le sue query misurerebbero lui. Istruzioni per
      chi raccoglie nella parte 1 di [istruzioni-annotazione.md](istruzioni-annotazione.md).
- [ ] **Giudizi del pool** sulle 24 query del confronto (deciso il 25/09/2026
      di non aspettare il relatore). Due passi, in quest'ordine:
      1. scrivere i 24 bisogni in `risultati/query/confronto-24/bisogni.md`,
         una o due frasi dopo ogni `Bisogno:`, **senza guardare risultati**, e
         dirlo: si committa prima di preparare la pagina;
      2. aprire `risultati/query/confronto-24/pagine/giudizi-primo.html` nel
         browser e dare i 905 giudizi (0, 1, 2), in sessioni di un'ora al
         massimo; alla fine scaricare il file e metterlo in
         `risultati/query/confronto-24/risposte/`.
- [ ] **Secondo annotatore** (Leopoldo, o un'altra persona fidata; la pagina
      `giudizi-secondo.html` si prepara dopo il primo) su query intere estratte dal foglio già
      annotato, almeno 150 righe, senza vedere i giudizi del primo (parte 3).

## Decisioni

- [x] **Da dove vengono gli embedding** per i difetti 2 e 3: **modello
      locale**, deciso il 25/09/2026. Riproducibile (pesi e versione fissi), i
      dati non escono dalla macchina, nessun costo, coerente con un motore
      piccolo e autonomo. Niente chiave Gemini; un modello esterno, se mai,
      solo come termine di confronto a capitolo 7 chiuso.
- [ ] **I default** degli interruttori misurati (`BM25Expansion`,
      `DisableOnNumbers`, `Coordination`, `MinimumShouldMatch`...): cambiarli
      cambia il baseline, da decidere con il relatore.

## Relatore

- [ ] **Dicembre 2026**: riproporre la tesi a Bonnici e Dal Palù, a progetti
      d'esame consegnati. Domande: cosa considerano un contributo sufficiente,
      che dimensione si aspettano, se va bene un corpus pubblico, se
      l'impianto di valutazione va bene prima di annotare.
- [ ] **Gennaio 2027**: guardare le tracce ufficiali e chiudere sul relatore.
