# Il giudice automatico: Claude contro un annotatore umano

**Domanda.** I 905 giudizi del pool delle 24 query del confronto li ha dati un
modello, Claude Opus 5.5 (`query/confronto-24/giudizi-llm.md`: modello,
prompt, input). Il capitolo 8 può reggersi su quei giudizi? Si misura
l'accordo con un annotatore umano, Martin, su un campione estratto a caso.

Scritto il 28/09/2026, prima che Martin dia un solo giudizio sul campione.

**Com'è andata, dichiarato.** Il protocollo della parte 2 e 3 di
`istruzioni-annotazione.md` voleva un annotatore umano su tutto il pool e un
secondo annotatore su un campione. È cambiato così:

- i 24 bisogni li ha scritti Claude, in una sessione separata, prima di aprire
  il foglio del pool (la sessione lo mostra: il foglio è letto la prima volta
  un quarto d'ora dopo la scrittura dei bisogni), e Martin li ha rivisti; due
  riprendono gli esempi che gli erano stati dati (c14 e c19);
- tutti i 905 giudizi li ha dati Claude, con sette istanze indipendenti;
- Martin giudica solo il campione, con la pagina di annotazione, nel ruolo di
  "secondo annotatore": il primo è il modello.

Bisogni e giudice automatico vengono quindi dallo stesso modello: un accordo
alto fra modello e Martin non dice che i bisogni sono buoni, dice che Martin
li applica come il modello. È un limite da scrivere nella tesi.

Scrivendo queste previsioni ho visto, per caso, una decina di giudizi del
modello mentre controllavo le note del file (alcune righe di c03, c15 e c19),
e provando `kappa.py --llm` su un secondo annotatore inventato ho visto quanti
0, 1 e 2 dà il modello sul campione (107 righe a 0). Dei giudizi di Martin non
so niente: non ne ha ancora dato uno. Martin non ha visto il file dei giudizi
del modello.

## Metodo

- **Il campione.** `prepara-giudizi.py --secondo`: query intere, in un ordine
  mescolato con il seme 20260928 fissato il 25/09 (commit `cfa89f0`, prima di
  qualunque giudizio), fino ad almeno 150 righe. Sono c21 (*manutenzone
  strade*), c03 (*concorso*), c19 (*determina 1223*) e c10 (*affidamento
  servizio mensa scolastica*): 178 righe.
- **Martin** giudica con la pagina `giudizi-secondo.html`, che non mostra i
  giudizi del modello né quale motore ha trovato l'atto.
- **L'accordo.** `kappa.py --llm`: accordo semplice, kappa di Cohen sui tre
  gradi, kappa pesato linearmente, matrice di confusione, accordo per query.

## Prima di misurare

1. **Kappa pesato linearmente di almeno 0,60.** Il modello ha i bisogni e le
   stesse regole di Martin, e i bisogni sono stretti, con i casi dubbi già
   decisi; i lavori sui giudici LLM (Thomas et al. 2023, Faggioli et al. 2023)
   trovano accordi con gli annotatori umani che variano molto, spesso
   moderati.
2. **Accordo semplice di almeno il 70%.**
3. **Meno del 10% delle righe con un disaccordo fra 0 e 2**: i disaccordi
   stanno quasi tutti fra gradi vicini.
4. **Il modello è più generoso di Martin**: nel campione dà 2 a più righe di
   lui. È la tendenza più riportata dei giudici LLM.
5. **c19 (determina 1223) ha l'accordo più alto delle quattro query**: il
   bisogno è quasi meccanico (è quella determina o no).

**Regola di decisione, fissata ora.** Con il kappa pesato di almeno 0,60 il
capitolo 8 usa i giudizi del modello, dichiarati come tali, con questo kappa.
Sotto 0,40 non li usa da soli: Martin giudica anche il resto del pool, o il
capitolo 8 si regge sulle known-item umane. Fra 0,40 e 0,60 si usano, ma ogni
risultato del capitolo 8 viene ricalcolato sulle sole query del campione con i
giudizi di Martin, e si riporta se la conclusione cambia.
