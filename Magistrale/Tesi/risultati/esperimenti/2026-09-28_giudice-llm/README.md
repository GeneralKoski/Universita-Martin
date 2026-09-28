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

## Esito

Da `query/confronto-24/accordo/2026-09-28T100644Z_kappa-llm.json`
(`kappa.py --llm`, strumenti da `3092571`). Il primo annotatore è il modello
(`giudizi-llm.tsv`), il secondo Martin (`giudizi-secondo.tsv`, importato con
`importa-giudizi.py` dal file scaricato dalla pagina alle 10:04 UTC del
28/09/2026). Il file di Martin è completo: 178 righe su 178, nessuna mancante,
nessuna in più, nessun valore nullo, impronta uguale a quella del foglio. Una
sola sessione, dalle 09:49 alle 10:04 UTC: un quarto d'ora, mediana 2,6 s a
giudizio, 10 giudizi cambiati.

| | valore |
|---|---|
| righe | 178 |
| accordo semplice | 54,5% (97 righe) |
| kappa di Cohen | 0,262 |
| kappa pesato linearmente | **0,370** |
| disaccordi fra 0 e 2 | 20 righe, 11,2% |

**Matrice di confusione** (righe: modello; colonne: Martin):

| | Martin 0 | Martin 1 | Martin 2 | totale modello |
|---|---|---|---|---|
| modello 0 | **68** | 29 | 10 | 107 |
| modello 1 | 3 | **6** | 17 | 26 |
| modello 2 | 10 | 12 | **23** | 45 |
| totale Martin | 81 | 47 | 50 | 178 |

**Accordo per query:**

| query | righe | uguali | accordo | modello sopra Martin | modello sotto Martin | fra 0 e 2 |
|---|---|---|---|---|---|---|
| c03 | 44 | 24 | 54,5% | 15 | 5 | 11 |
| c10 | 30 | 18 | 60,0% | 4 | 8 | 4 |
| c19 | 50 | 40 | **80,0%** | 0 | 10 | 0 |
| c21 | 54 | 15 | 27,8% | 6 | 33 | 5 |

Previsione per previsione:

1. **Smentita.** Kappa pesato 0,370, non almeno 0,60: sotto anche la soglia
   di 0,40. Il kappa di Cohen sui tre gradi è 0,262.
2. **Smentita.** Accordo semplice del 54,5%, non almeno il 70%.
3. **Smentita, di poco.** 20 righe su 178 con un disaccordo fra 0 e 2
   (11,2%), non meno del 10%; 11 di queste sono in c03.
4. **Smentita, al contrario.** Il modello è più severo di Martin: dà 2 a 45
   righe contro 50, e 0 a 107 contro 81. Delle 81 righe in disaccordo, in 56
   il modello dà un grado più basso di Martin e solo in 25 uno più alto.
   L'unica query dove il modello è più generoso è c03 (2 a 26 righe contro
   14).
5. **Confermata.** c19 ha l'accordo più alto, 80%, contro il 60% di c10 e
   meno del 55% delle altre due. Ma l'accordo viene quasi tutto dal grado 0:
   il modello dà 0 a 49 righe su 50, e i 10 disaccordi sono tutti righe a cui
   il modello dà 0 e Martin 1. Corretto per il caso, sulla sola c19 il kappa
   di Cohen è 0,15 e quello pesato 0,26 (calcolati a parte da
   `giudizi-llm.tsv` e `giudizi-secondo.tsv`, non sono nel file archiviato).

**Decisione.** Il kappa pesato è 0,370, sotto 0,40: per la regola fissata
prima di misurare il capitolo 8 non usa i giudizi del modello da soli.
Restano le due strade che la regola prevede: Martin giudica anche il resto del
pool, o il capitolo 8 si regge sulle known-item umane. **Il 28/09/2026 Martin
ha scelto la seconda**: il resto del pool non si giudica, e il pool con i
giudizi del modello resta al più un confronto secondario, dichiarato come tale
e con questo kappa accanto.

**Dove stanno i disaccordi.**

- **Sul grado 1.** Martin dà 1 a 47 righe, il modello a 26, e sono d'accordo
  su 6 soltanto. Il grado intermedio è quello che i due applicano in modo più
  diverso: dove Martin vede un atto parzialmente utile il modello dice quasi
  sempre 0 (29 righe) o 2 (12 righe).
- **In c21**, che da sola fa 39 degli 81 disaccordi. Qui il modello è
  sistematicamente più severo di un grado: 16 righe con 1 dal modello e 2 da
  Martin, 13 con 0 dal modello e 1 da Martin.
- **In c03**, dove la tendenza è opposta: il modello dà 2 a righe che Martin
  giudica 1 (7) o 0 (8), e c'è più della metà dei disaccordi fra 0 e 2.
- **In c19**, dove l'unico disaccordo è fra 0 e 1: Martin riconosce come
  parzialmente utili 10 atti che il modello scarta.

I disaccordi non vanno quindi in una sola direzione: dipendono dalla query,
cioè da come ciascuno legge il bisogno. Questo è coerente con il limite
dichiarato all'inizio (bisogni e giudice vengono dallo stesso modello, e
Martin li applica a modo suo).

**Limiti.** Martin ha giudicato 178 righe in un quarto d'ora, con una mediana
di 2,6 s a giudizio e 24 giudizi sotto il secondo: un ritmo da lettura del
titolo più che dell'estratto. La mediana è la stessa sulle righe in accordo e
su quelle in disaccordo (2,5 e 2,6 s), quindi la fretta non spiega da sola i
disaccordi, ma un secondo passaggio più lento potrebbe spostare parte dei
giudizi di grado 1. Le quattro query del campione sono poche per dire quanto
il disaccordo dipenda dalla query e quanto dal giudice.
