# Template LaTeX tesi magistrale

Scheletro ripreso da `Triennale/Tirocinio/template-tesi-main` (la tesi triennale), ripulito dal contenuto: restano la classe UniPR e l'impianto del documento.

- `theme/uniprthesis.cls` + `theme/logo_unipr.pdf` - classe ufficiale, invariata
- `tesi.tex` - preambolo, metadati del frontespizio e ordine dei capitoli
- `capitoli/` - un file per capitolo, inclusi da `tesi.tex` con `\include`
- `immagini/` - figure

## Da compilare prima di scrivere

In `tesi.tex`: `\title`, `\advisor`, e le due pagine di citazione e dedica. `\degree`, `\degreeyears` (2026--2027) e `\serialNumber` (397464) sono già impostati.

## Compilazione

La classe usa `pdfx` con profilo PDF/A-1b, quindi va compilata con **pdflatex** (Overleaf va bene, come per la triennale). Due passate per indice e riferimenti:

```
pdflatex tesi.tex && pdflatex tesi.tex
```

Con `tectonic` il pacchetto `pdfx` si ferma su `CreationDate is not properly supported`: si compila solo con `tectonic -X compile tesi.tex -Z continue-on-errors`, e il PDF che ne esce non è PDF/A valido. Va bene per un'anteprima veloce, non per la consegna.

## Bibliografia

Come nella triennale è una `thebibliography` scritta a mano in `capitoli/bibliografia.tex`. Per una tesi con parecchi articoli conviene passare a BibTeX (`\bibliography{bibliografia}` + un `.bib`), ma è una scelta da fare una volta, prima di avere 40 voci scritte a mano.
