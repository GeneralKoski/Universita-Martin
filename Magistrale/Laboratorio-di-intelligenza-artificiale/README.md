# Laboratorio di intelligenza artificiale

**cod. 1009073** - 6 CFU, 48 ore - caratterizzante, monodisciplinare - 2° anno, primo semestre (a.a. 2026/27) - insegnamento in italiano.
**Docente:** Vincenzo Bonnici (vincenzo.bonnici@unipr.it)
**Esame:** **progetto da presentare** (confermato dal docente il 21/09/2026). Il progetto deve applicare bene tutti i concetti del laboratorio **più qualcosa dal corso teorico di Algoritmi per l'IA**: la teoria va studiata comunque, anche per questo esame.
**Metodi didattici:** lezioni frontali, laboratorio in aula, progetto.

Scheda ufficiale: https://corsi.unipr.it/it/ugov/degreecourse/329454

Il materiale è diviso per edizione: `2026-27/` è il corso che sto seguendo,
`2025-26/` è l'edizione precedente, tenuta come riferimento.

| Edizione | Elly | Corso | Stato |
|---|---|---|---|
| 2026/27 | elly2026 | [id 5197](https://elly2026.didattica.unipr.it/course/view.php?id=5197) | in corso, inizio 23/09/2026 |
| 2025/26 | elly2025 | [id 667](https://elly2025.didattica.unipr.it/course/view.php?id=667) | archiviata, materiale completo |

## Struttura della cartella

- `2026-27/`, `2025-26/` - materiale Elly, un'edizione per cartella
- `project/` - il progetto d'esame, una sottocartella per progetto
- `study/` - preparazione della presentazione

Il progetto deve applicare i concetti del laboratorio **più qualcosa dal corso
teorico di Algoritmi per l'IA**: quella teoria sta in
`../Algoritmi-per-l-intelligenza-artificiale/study/`, va linkata da qui, non
ricopiata.

Il `.gitignore` del corso tiene fuori da git dataset grezzi, file generati,
risultati, `.venv` e zip di consegna: sono tutti rigenerabili e il repository
pesa già parecchio di PDF.

## Contenuti

Basi per modellare, implementare e applicare algoritmi di IA, con taglio pratico su Python e librerie. Complementare ad Algoritmi per l'IA (stesso docente): lì la teoria, qui l'implementazione.

**Programma esteso:** Python per analisi esplorative e apprendimento automatico; feature selection; riduzione della dimensionalità; classificazione e clustering; metodi per lo sbilanciamento dei data set; cenni di regressione; analisi di serie temporali; programmazione dinamica, time warping, allineamento di sequenze; costruzione di data set artificiali; implementazione di algoritmi di ricerca.

**Bibliografia:** Russell, Norvig - *Intelligenza artificiale: un approccio moderno*, Pearson 2016.

---

## Edizione 2026/27 - Elly 5197

Scaricato il 16/09/2026 in `2026-27/`, ricontrollato il 21/09/2026. I nomi
originali del docente portano il prefisso `AILAB_2627_`, che conferma che sono
file rifatti per questa edizione e non copie della precedente.

### 0 - Introduzione

- [forum] Annunci - https://elly2026.didattica.unipr.it/mod/forum/view.php?id=6549
- `2026-27/0_Introduzione/Calendario provvisorio.pdf` (calendario-v0.pdf)
- `2026-27/0_Introduzione/Calendario provvisorio v1.pdf` (calendario-v1.pdf) - **il calendario valido**

#### Calendario v1: cosa cambia rispetto a v0

Il docente ha **aggiunto due lezioni di recupero** a inizio ottobre, in un
giorno e un'aula diversi dal solito:

- lunedì 05-10-2026, 08:30-10:30, **Aula G** - Python 3
- martedì 06-10-2026, 08:30-10:30, **Aula G** - numpy, PLS

Tutto il resto scala indietro di due lezioni: *Pandas e librerie grafiche* passa
dal 14/10 al 07/10, la *programmazione dinamica* dal 18/11 al 05/11, *subgraph
isomorphism* dal 02-03/12 al 25-26/11, i *progetti* dal 09/12 al 02/12 e i tre
laboratori (classificazione, regressione, clustering) dal 16-23/12 al
03-09-16/12. Il corso finisce quindi il **16/12** invece del 23/12, con le
ultime due date (17/12 e 23/12) rimaste libere.

### 1 - Materiale lezioni

- `2026-27/1_Materiale_lezioni/Introduzione al corso.pdf` (AILAB_2627_0-intro.pdf)
- `2026-27/1_Materiale_lezioni/Python 3.pdf` (AILAB_2627_1-python.pdf)
- `2026-27/1_Materiale_lezioni/Esempio Python 3 OOP.py` (Student.py)
- `2026-27/1_Materiale_lezioni/Librerie python.zip` (python-libs.zip)
- `2026-27/1_Materiale_lezioni/Riduzione della dimensionalità.pdf` (AILAB_2627_3-dim-red.pdf)
- `2026-27/1_Materiale_lezioni/Notebook - riduzione della dimensionalità.ipynb` (dimred.ipynb)
- `2026-27/1_Materiale_lezioni/Sbilanciamento del dataset.pdf` (AILAB_2627_4-sbilanciamento.pdf)
- `2026-27/1_Materiale_lezioni/Benchmarking.pdf` (AILAB_2627_5-benchmark.pdf)
- `2026-27/1_Materiale_lezioni/Serie temporali.pdf` (AILAB_2627_6-serie-temporali.pdf)
- `2026-27/1_Materiale_lezioni/Programmazione dinamica.pdf` (AILAB_2627_7-programmazione-dinamica.pdf)
- `2026-27/1_Materiale_lezioni/Teoria dei grafi e algoritmi su grafi.pdf` (AILAB_2627_8-grafi.pdf)
- `2026-27/1_Materiale_lezioni/Subgraph isomorphism.pdf` (SubGI.pdf)
- `2026-27/1_Materiale_lezioni/Notebook - Classificazione.ipynb` (lab-classificazione.ipynb)
- `2026-27/1_Materiale_lezioni/Notebook - Clustering.ipynb` (lab-clustering.ipynb)

### Cosa cambia rispetto al 2025/26

**Nuovo:**
- *Teoria dei grafi e algoritmi su grafi* - arriva da Algoritmi per l'IA, che
  nell'edizione 2026/27 non ha più `8-grafi.pdf`. Stesso docente, argomento
  spostato dal corso teorico a quello di laboratorio.
- *Riduzione della dimensionalità* come voce a sé, slide più notebook. Nel
  2025/26 stava dentro `3 - Preprocessing.pdf`.

**Tolto (per ora):**
- *Preprocessing* come slide unica.
- I cinque seminari (Avesani, Viesi, Maresi, Bellingeri, Mensi): si aggiungono
  durante l'anno, non a calendario.
- Le sezioni *Esami*, *Registrazioni* e *Progetti*, che nel 2025/26 si sono
  riempite a corso avviato.

---

## Edizione 2025/26 - Elly 667

Materiale scaricato, in `2025-26/`.

### 0 - Introduzione

- [forum] Annunci - https://elly2025.didattica.unipr.it/mod/forum/view.php?id=687
- `2025-26/0_Introduzione/Calendario.pdf` (calendario-ailab-2526.pdf)
- `2025-26/0_Introduzione/Calendario v2.pdf` (calendario-ailab-2526-v2.pdf)
- `2025-26/0_Introduzione/Calendario v3.pdf` (calendario-ailab-2526-v3.pdf)
- `2025-26/0_Introduzione/Calendario v4.pdf` (calendario-ailab-2526-v4.pdf)

### 1 - Esami

- [url] Foglio prenotazione slot esami - https://elly2025.didattica.unipr.it/mod/url/view.php?id=75521
- [label] Modalità di esame

### 2 - Materiale lezioni

- `2025-26/2_Materiale_lezioni/0 - Introduzione al corso.pdf` (0-intro.pdf)
- `2025-26/2_Materiale_lezioni/1 - Python3.pdf` (1-python.pdf)
- `2025-26/2_Materiale_lezioni/1 - Python 3 - Esempio OOP (Student.py).py` (Student.py)
- `2025-26/2_Materiale_lezioni/2 - Librerie Python.zip` (2-python-libs.zip)
- `2025-26/2_Materiale_lezioni/3 - Preprocessing.pdf` (3-preprocessing.pdf)
- `2025-26/2_Materiale_lezioni/4 - Sbilanciamento delle classi.pdf` (4-imbalance.pdf)
- `2025-26/2_Materiale_lezioni/5 - Benchmark sintetici.pdf` (5-benchmarking.pdf)
- `2025-26/2_Materiale_lezioni/6 - Classificazione.ipynb` (6-classificazione.ipynb)
- `2025-26/2_Materiale_lezioni/7 - Apprendimento non supervisionato.ipynb` (7-clustering.ipynb)
- `2025-26/2_Materiale_lezioni/8 - Analisi di serie temporali.pdf` (8-serie-temporali.pdf)
- `2025-26/2_Materiale_lezioni/9 - Programmazione dinamica.pdf` (9-programmazione-dinamica.pdf)
- `2025-26/2_Materiale_lezioni/10 - SubGI.pdf` (SubGI.pdf)
- `2025-26/2_Materiale_lezioni/Slide seminario Simone Avesani - Trascittomica spaziale.pdf` (Presentazione_SimoneAvesani.pdf)
- `2025-26/2_Materiale_lezioni/Slide seminario Eva Viesi - Chemioinformatica.pdf` (Presentazione_EvaViesi.pdf)
- `2025-26/2_Materiale_lezioni/Slide Seminario Maresi - Predizione di bioattività.pdf` (Seminario_20nov.pdf)
- `2025-26/2_Materiale_lezioni/Slide seminario Bellingeri - Computaitonal Gastronomy.pdf` (Computational Gastronomy, Corso AI, UNIPR 2025_ITA.pdf)
- `2025-26/2_Materiale_lezioni/Slide seminario Mensi - Anomaly detection.pdf` (Seminario0312_V2.pdf)

### 3 - Registrazioni

- [url] Lezione  0 - Introduzione al corso e accenni di Python3 - https://elly2025.didattica.unipr.it/mod/url/view.php?id=35049
- [url] Lezione 1 - Python3 (parte 2) - https://elly2025.didattica.unipr.it/mod/url/view.php?id=35512
- [url] Lezione 2 - Python3 (parte 3) - https://elly2025.didattica.unipr.it/mod/url/view.php?id=42849
- [url] Lezione 3 - Analisi dei dati esplorativa (parte 1) - https://elly2025.didattica.unipr.it/mod/url/view.php?id=45080
- [url] Lezione 4 - Analisi dei dati esplorativa (parte 2) - https://elly2025.didattica.unipr.it/mod/url/view.php?id=45077
- [url] Lezione 6 - Preprocessing e Feature selection - https://elly2025.didattica.unipr.it/mod/url/view.php?id=48018
- [url] Lezione 7 -  Riduzione della dimensionalità - https://elly2025.didattica.unipr.it/mod/url/view.php?id=48330
- [url] Lezione 8 - Sbilanciamento (parte 1) - https://elly2025.didattica.unipr.it/mod/url/view.php?id=50350
- [url] Lezione 9 - Alberi di decisione e Kaggle - https://elly2025.didattica.unipr.it/mod/url/view.php?id=50822
- [url] Lezione 10 - Sbilaciamento (parte 2); Benchmarking (parte 1) - https://elly2025.didattica.unipr.it/mod/url/view.php?id=53560
- [url] Lezione 12  - Benchmarkign (parte 2); Regressione. - https://elly2025.didattica.unipr.it/mod/url/view.php?id=53816
- [url] Lezione 13 - Analisi di serie temporali. - https://elly2025.didattica.unipr.it/mod/url/view.php?id=56305
- [url] Lezione 14 - Classificazione - https://elly2025.didattica.unipr.it/mod/url/view.php?id=56588
- [url] Lezione 15 - Progetti; Dynamic Time Warping - https://elly2025.didattica.unipr.it/mod/url/view.php?id=59231
- [url] Lezione 16 - Seminario "Subgraph Isomorphism" - https://elly2025.didattica.unipr.it/mod/url/view.php?id=59788
- [url] Lezione 17 - Seminari Trascrittomica spaziale e chemioinformatica - https://elly2025.didattica.unipr.it/mod/url/view.php?id=60684
- [url] Lezione 18 - Programmazione dinamica (parte 1) - https://elly2025.didattica.unipr.it/mod/url/view.php?id=62581
- [url] Lezione 19 - Seminario Maresi - https://elly2025.didattica.unipr.it/mod/url/view.php?id=62580
- [url] Lezione 20 - Seminario Bellingeri - https://elly2025.didattica.unipr.it/mod/url/view.php?id=67764
- [url] Lezione 20 - Seminario Mensi - https://elly2025.didattica.unipr.it/mod/url/view.php?id=67765
- [url] Seminari Baruzzo e Cesaro - https://elly2025.didattica.unipr.it/mod/url/view.php?id=71960
- [url] Lezione 21 - Presentazione progetti finale - https://elly2025.didattica.unipr.it/mod/url/view.php?id=73118

### 4 - Progetti

- [url] Tabella di scelta del progetto - https://elly2025.didattica.unipr.it/mod/url/view.php?id=59240
- [label] Lista progetti
