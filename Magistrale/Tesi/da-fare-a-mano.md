# Da fare a mano

Le cose della tesi che non sono sviluppo: servono persone, una decisione o un
incontro. Il piano ([piano.md](piano.md)) resta l'unico elenco completo; qui
c'è solo quello che tocca a Martin, con quello che serve per farlo.

**Da dove ripartire** (aggiornato il 25/09/2026): i lotti alle persone e i 24
bisogni si possono fare subito e in parallelo; i giudizi vengono dopo i
bisogni, il secondo annotatore dopo i giudizi. Importazioni, commit e misure li
fa Claude: basta mettere i file nelle cartelle indicate e dirlo.

## Persone e raccolta

- [ ] **Known-item umane.** Quattro persone che non sappiano come funzionano i
      motori (non informatici), **un lotto diverso a testa**: i quattro file
      `risultati/query/known-item-umane/pagine/raccolta-lotto-1.html` ... `-4`
      hanno 40 atti diversi ciascuno, stessa pagina. Bastano tre persone.
      Mandarli **in privato** (contengono il testo degli atti, con nomi di
      persone), farsi rimandare il `.json` che la pagina scarica alla fine,
      copiarlo così com'è in `risultati/query/known-item-umane/risposte/` e
      dirlo a Claude. Martin non compila le pagine: le sue query misurerebbero
      lui. Istruzioni per chi raccoglie nella parte 1 di
      [istruzioni-annotazione.md](istruzioni-annotazione.md).
- [ ] **Giudizi del pool** sulle 24 query del confronto (deciso il 25/09/2026
      di non aspettare il relatore). Due passi, in quest'ordine:
      1. scrivere i 24 bisogni in `risultati/query/confronto-24/bisogni.md`,
         una o due frasi dopo ogni `Bisogno:` (cosa cerca chi digita quella
         query nel documentale di un comune, e se serve cosa no), **senza
         guardare risultati**. I refusi: `come «manutenzione strade»`. Le
         query con un numero: cosa conta come quell'atto. Circa un'ora. Poi
         dirlo a Claude, che committa e genera la pagina;
      2. aprire `risultati/query/confronto-24/pagine/giudizi-primo.html` nel
         browser e dare i 905 giudizi: tasti 0 (non risponde), 1 (parziale),
         2 (risponde), T per il testo intero, freccia a sinistra per tornare
         indietro. Sessioni di un'ora al massimo, con Pausa quando si smette;
         4-5 ore in tutto. Alla fine "Scarica il file", metterlo in
         `risultati/query/confronto-24/risposte/` e dirlo a Claude.
- [ ] **Secondo annotatore** (Leopoldo, o un'altra persona fidata; la pagina
      `giudizi-secondo.html` si prepara dopo il primo) su query intere estratte dal foglio già
      annotato, almeno 150 righe, senza vedere i giudizi del primo (parte 3).

## Decisioni

- [x] **Da dove vengono gli embedding** per i difetti 2 e 3: **modello
      locale**, deciso il 25/09/2026. Riproducibile (pesi e versione fissi), i
      dati non escono dalla macchina, nessun costo, coerente con un motore
      piccolo e autonomo. Niente chiave Gemini; un modello esterno, se mai,
      solo come termine di confronto a capitolo 7 chiuso.
- [ ] **I default** degli interruttori misurati: proposta del 25/09/2026 di non
      cambiarne nessuno (il baseline resta intatto) e di definire una
      **configurazione consigliata** con nome, che prepara Claude. A Martin e
      al relatore resta solo confermarla.

## Relatore

- [ ] **Dicembre 2026**: riproporre la tesi a Bonnici e Dal Palù, a progetti
      d'esame consegnati. Domande: cosa considerano un contributo sufficiente,
      che dimensione si aspettano, se va bene un corpus pubblico, se
      l'impianto di valutazione va bene prima di annotare.
- [ ] **Gennaio 2027**: guardare le tracce ufficiali e chiudere sul relatore.
