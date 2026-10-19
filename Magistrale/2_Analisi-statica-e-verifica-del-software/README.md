# Analisi statica e verifica del software

**cod. 1013066** - 9 CFU, 72 ore - caratterizzante, monodisciplinare - 2° anno, primo semestre (a.a. 2026/27) - insegnamento in italiano.
**Docente:** Vincenzo Arceri (vincenzo.arceri@unipr.it, dalla slide *01 - Introduction*).

**Esame:** **seminario (discussione di almeno un paper) + orale**. Slide 56 di
*01 - Introduction* (2026/27): "Seminar (1+ paper discussion) and oral exam".
Scheda ufficiale (letta il 19/10/2026): "La verifica avviene con la discussione
di un articolo e un esame orale. Lo studente approfondisce un argomento avanzato
partendo da un articolo scientifico tra quelli proposti e prepara una
presentazione da utilizzare il giorno dell'esame." Il seminario quindi si tiene
lo stesso giorno dell'orale, sull'articolo scelto fra quelli del docente. Pesi
non indicati.

> Fino a settembre 2026 la scheda dava il docente come **NON ASSEGNATO** ed era
> vuota. Al 19/10/2026 è compilata, con Arceri docente, obiettivi, contenuti
> (teoria dei reticoli, semantica e fixpoint, dataflow analyses, interpretazione
> astratta, analisi relazionali e non, numeriche e su stringhe) ed esame.

Scheda ufficiale: https://corsi.unipr.it/it/ugov/degreecourse/329458

Il materiale è diviso per edizione: `2026-27/` è il corso che sto seguendo,
`2025-26/` è l'edizione precedente, tenuta come riferimento.

| Edizione | Elly | Corso | Stato |
|---|---|---|---|
| 2026/27 | elly2026 | [id 5198](https://elly2026.didattica.unipr.it/course/view.php?id=5198) | in corso, slide 01-07 |
| 2025/26 | elly2025 | [id 741](https://elly2025.didattica.unipr.it/course/view.php?id=741) | archiviata, materiale completo |

---

## Edizione 2026/27 - Elly 5198

Il 16/09/2026 il corso era vuoto. Ricontrollato il 29/09/2026: sono arrivati il
tutorial di Miné e la prima slide, scaricati in `2026-27/`. Ricontrollato il
18/10/2026: sono arrivate le slide da 02 a 07, scaricate; tutorial e 01 identici
(md5). La scheda ufficiale è ancora priva di programma ed esame (l'esame però
lo dà la slide, vedi sopra).

### 0 - Introduzione

- [forum] Annunci - https://elly2026.didattica.unipr.it/mod/forum/view.php?id=6550

### 1 - Material

- `2026-27/1_Material/Tutorial on Static Inference of Numeric Invariants by Abstract Interpretation (Prof. Antoine Miné).pdf` (article-mine-FTiPL17.pdf) - nel 2025/26 era solo un url, ora è il PDF

### 2 - Slides

- `2026-27/2_Slides/01 - Introduction.pdf` (01.pdf) - rifatta rispetto al 2025/26 (88 pagine contro 89, file diverso)
- `2026-27/2_Slides/02 - Mathematical background.pdf` (02.pdf) - 187 pagine
- `2026-27/2_Slides/03 - Modeling programs.pdf` (03.pdf) - 36 pagine
- `2026-27/2_Slides/04 - Dataflow analyses.pdf` (04.pdf) - 78 pagine
- `2026-27/2_Slides/05 - Meaning of approximation.pdf` (06.pdf) - 85 pagine
- `2026-27/2_Slides/06 - Introduction to abstract interpretation (Galois connections).pdf` (07.pdf) - 58 pagine
- `2026-27/2_Slides/07 - Introduction to abstract interpretation (Abstract semantics).pdf` (08.pdf) - 57 pagine

Dalla quinta slide i nomi originali saltano di uno (`05` è `06.pdf` e così via):
su Elly manca un `05.pdf`, i titoli invece sono consecutivi.

---

## Edizione 2025/26 - Elly 741

Corso in inglese, slide su interpretazione astratta più laboratorio LiSA.
Materiale scaricato, in `2025-26/`.

### 0 - Introduzione

- [forum] Annunci - https://elly2025.didattica.unipr.it/mod/forum/view.php?id=761

### 1 - Material

- [url] Tutorial on Static Inference of Numeric Invariants by Abstract Interpretation (Prof. Antoine Miné) - https://elly2025.didattica.unipr.it/mod/url/view.php?id=33740
- `2025-26/1_Material/Topics for seminars.zip` (Topics.zip)

### 2 - Slide

- `2025-26/2_Slide/01 - Introduction.pdf` (01.pdf)
- `2025-26/2_Slide/02 - Mathematical background.pdf` (02.pdf)
- `2025-26/2_Slide/03 - Modeling programs.pdf` (03.pdf)
- `2025-26/2_Slide/04 - Dataflow analyses.pdf` (04.pdf)
- `2025-26/2_Slide/06 - Meaning of approximation.pdf` (06.pdf)
- `2025-26/2_Slide/07 - Introduction to abstract interpretation (Galois Connection).pdf` (07.pdf)
- `2025-26/2_Slide/08 - Introduction to abstract interpretation (Abstract semantics).pdf` (08.pdf)
- `2025-26/2_Slide/09 - The split operator.pdf` (split-op.pdf)
- `2025-26/2_Slide/10 - Unconstrained variable oracle.pdf` (havoc.pdf)
- `2025-26/2_Slide/12 - Numerical Domains and abstract interpretation.pdf` (parma25a.pdf)
- `2025-26/2_Slide/13 - Convex polyhedra as an abstract domain.pdf` (parma25b.pdf)
- `2025-26/2_Slide/14 - The interval abstract domain.pdf` (11.pdf)
- `2025-26/2_Slide/15 - The finite state automata abstract domain.pdf` (13.pdf)
- `2025-26/2_Slide/16 - Completeness.pdf` (Completeness.pdf)
- `2025-26/2_Slide/17 - Termination static analysis.pdf` (Urban-Part1.pdf)
- `2025-26/2_Slide/18 - Termination static analysis (2).pdf` (Unipr2025-Part2.pdf)
- `2025-26/2_Slide/19 - ML safety.pdf` (Urban-Part3-4.pdf)
- `2025-26/2_Slide/20 - Software quality assurance.pdf` (Lecture1_SoftwareQualityAssurance.pdf)

### 3 - LiSA laboratory sessions

- `2025-26/3_LiSA_laboratory_sessions/05- Introduction to LiSA and dataflow analyses.pdf` (05.pdf)
- `2025-26/3_LiSA_laboratory_sessions/11 - Abstract interpretation in LiSA.pdf` (09.pdf)
