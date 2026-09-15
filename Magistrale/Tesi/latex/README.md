# Template LaTeX tesi magistrale

Scheletro ripreso da `Triennale/Tirocinio/template-tesi-main` (la tesi triennale), ripulito dal contenuto: restano la classe UniPR e l'impianto del documento.

- `theme/uniprthesis.cls` + `theme/logo_unipr.pdf` - classe ufficiale, invariata
- `tesi.tex` - preambolo, metadati del frontespizio e ordine dei capitoli
- `capitoli/` - un file per capitolo, inclusi da `tesi.tex` con `\include`
- `bibliografia.bib` - le fonti, in BibTeX
- `immagini/` - figure

## Da compilare prima di scrivere

In `tesi.tex`: `\title`, `\advisor`, e le due pagine di citazione e dedica. `\degree`, `\degreeyears` (2026--2027) e `\serialNumber` (397464) sono già impostati.

## Compilazione

Toolchain installata via Homebrew: `brew install texlive biber` (`biber` è a parte, la formula texlive non lo include). La classe usa `pdfx` con profilo PDF/A-1b: serve **pdflatex**, non tectonic.

I binari stanno in `/opt/homebrew/opt/texlive/bin`: se `pdflatex` non si trova, aggiungilo al PATH.

```
latexmk -pdf tesi.tex
```

`latexmk` gestisce da solo le passate e la chiamata a `biber`. A mano sarebbe:

```
pdflatex tesi.tex && biber tesi && pdflatex tesi.tex && pdflatex tesi.tex
```

Per ripulire gli ausiliari: `latexmk -C`.

## Bibliografia

`biblatex` con backend `biber`, stile numerico. Le fonti stanno in `bibliografia.bib`, si citano con `\cite{chiave}` e compaiono in bibliografia **solo se citate** (per forzarne una non citata: `\nocite{chiave}`).

Lo stile si cambia in un punto solo, nell'opzione `style=` di `\usepackage{biblatex}` in `tesi.tex`: `numeric-comp` (attuale, `[1,3-5]`), `alphabetic` (`[Rob09]`), `authoryear`. Se il relatore chiede un formato preciso, si decide lì.
