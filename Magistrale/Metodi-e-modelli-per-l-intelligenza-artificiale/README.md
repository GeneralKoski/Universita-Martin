# Metodi e modelli per l'intelligenza artificiale

Appunti, esercizi e materiale di studio per il corso **Metodi e modelli per l'intelligenza artificiale** - Laurea Magistrale in Scienze Informatiche, Università di Parma.

> **SCRITTO: giovedì 17 settembre 2026**, poi orale. Da verificare su Esse3 se l'orale è nella stessa giornata o in data successiva. Sette giorni prima (10 settembre) c'è l'orale di LIC, quindi il grosso di questo esame va chiuso **prima** di quella data: piano in [`study/README.md`](study/README.md).

## Informazioni corso (A.A. 2025/2026)

| Campo | Valore |
|---|---|
| Codice | 334989 |
| Corso di laurea | Scienze Informatiche (LM) |
| Mutuato da | Ingegneria Gestionale - Metodi e modelli per le decisioni (9 CFU, DISTI) |
| Programma 6 CFU | fino a *Trasporto generalizzato e problemi facili* incluso |
| Anno / Semestre | 1° anno - 2° semestre |
| CFU | 6 |
| Ore | 48 (lezioni frontali) |
| SSD | MAT/03 - Geometria |
| Tipologia | Affine / Integrativa |
| Lingua | Italiano |
| Docente | Prof. Lorenzo Nicolodi |
| Dipartimento | Scienze Matematiche, Fisiche e Informatiche (SMFI) |

Pagina ufficiale: <https://corsi.unipr.it/it/ugov/degreecourse/334989>

## Obiettivi formativi

Introduzione ai principali algoritmi e tecniche di **programmazione intera e combinatoria**, con applicazioni industriali e gestionali. Lo studente impara a formulare e risolvere problemi di programmazione intera/combinatoria e ad analizzarne le soluzioni.

## Prerequisiti

- Programmazione Lineare

## Programma

### 1. Teoria
- Richiami di programmazione lineare
- Introduzione alla teoria dei giochi
- Ottimizzazione su grafi e reti, tecniche di esplorazione
- Criteri di interezza: **totale unimodularità**
- Programmazione lineare intera (PI): tecniche di formulazione e qualità delle formulazioni
- Metodi esatti: enumerazione implicita, **piani di taglio**, **branch and bound**, programmazione dinamica
- Qualità delle soluzioni: rilassamenti e dualità; **rilassamenti lagrangiani** e dualità lagrangiana
- Cenni di programmazione non lineare
- Metodi euristici: greedy, ricerca locale, costruttive, in due fasi

### 2. Applicazioni
- Problemi e modelli di **localizzazione** (impianti, nodi logistici)
- Logistica distributiva: trasporto, distribuzione
- **Problema del commesso viaggiatore (TSP)**
- Instradamento di veicoli (VRP) in reti di trasporto
- Schedulazione di attività
- Modelli di Input-Output
- Modelli di Produzione

## Metodi didattici

Lezioni frontali con esempi, applicazioni ed esercizi assegnati e discussi a lezione.

## Modalità d'esame

Entrambe le prove sono obbligatorie (non è stato sostenuto il parziale).

- Prova **scritta** (17 settembre 2026): risoluzione di esercizi, 90-120 min. Due macro-blocchi: (1) algoritmi sui grafi - BFS/DFS, Bellman, Dijkstra, Floyd-Warshall, MST; (2) programmazione intera e ottimizzazione combinatoria - formulazioni, TSP, localizzazione, rilassamenti, TU.
- Prova **orale**: argomenti teorici e applicazioni, cioè definizioni e **dimostrazioni** (elenco in `study/pratica/13_simulazione_esame.md`).

**Specificità del caso 6 CFU** (corso mutuato dai gestionali, 9 CFU):

- Il programma si ferma a *Trasporto generalizzato e problemi facili* incluso: fuori branch and bound completo, piani di taglio, programmazione dinamica.
- Allo scritto dovrebbe toccare **un esercizio in meno** rispetto ai gestionali. Conviene ricordarlo al prof Nicolodi in apertura: gli appunti dei colleghi dicono "se il prof si ricorda".

**Due cose che la scheda non dice** (emerse dal censimento in `study/pratica/00_ANATOMIA_ESAME.md`):

- Lo scritto nel formato recente (esonero 2022, fogli di esercizi 2026) chiede anche **dimostrazioni scritte** e **modellazione applicata**, non solo esecuzione di algoritmi.
- Il prof usa anche **quiz Elly/Moodle** a scelta multipla e a risposta numerica sugli stessi argomenti (`Appunti_colleghi/Zip_appunti/NICOLODI REVISIONI 1.pdf`). Non è chiaro se rientrino nello scritto del 17 settembre: **da verificare**.

Fonti: scheda ufficiale del corso + `Appunti_colleghi/Modalità_esame.txt` + censimento del materiale d'esame.

## Bibliografia

- Note a cura del docente
- L. A. Wolsey, *Integer Programming*, Wiley-Interscience, New York, 1998
- F. Maffioli, *Elementi di programmazione matematica*, 2ª ed., Casa Editrice Ambrosiana, Milano, 2000
- G. Ghiani, R. Musmanno, *Modelli e metodi per l'organizzazione dei sistemi logistici*, Pitagora, Bologna, 2000
- F. S. Hillier, G. J. Lieberman, *Introduzione alla ricerca operativa*, 8ª ed., McGraw-Hill, Milano, 2006

## Link utili

- [Pagina del corso (UniPR)](https://corsi.unipr.it/it/ugov/degreecourse/334989)
- [Corso di laurea - Scienze Informatiche](https://corsi.unipr.it/it/scheda/cdlm-info)
- [Materiale didattico - Elly2025](https://elly2025.didattica.unipr.it/course/index.php?categoryid=2)
- [Calendario esami](https://corsi.unipr.it/it/ugov/degreecourse/334989)

## Contatti

- **Docente:** Prof. Lorenzo Nicolodi
- **Presidente CdS:** Prof. Vincenzo Bonnici - <vincenzo.bonnici@unipr.it>
- **Manager didattica:** Dott.ssa Claudia Buga - <claudia.buga@unipr.it>
- **Segreteria studenti:** <segreteria.scienze@unipr.it>
