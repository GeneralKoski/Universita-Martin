# Canny Edge Detector

Implementazione da zero del Canny Edge Detector per il progetto d'esame di
Fondamenti dell'Intelligenza Artificiale (UniPR, Prof.ssa E. Iotti).

## Pipeline
1. Conversione in scala di grigi (luminanza).
2. Smoothing con filtro gaussiano (separabile, kernel `kernel_size`, varianza `sigma`).
3. Gradiente con filtri di Sobel: magnitudo e direzione.
4. Non-Maximum Suppression sulla direzione del gradiente discretizzata in 4 settori (0°, 45°, 90°, 135°).
5. Double Threshold (`low_ratio`, `high_ratio`) → pixel forti / deboli.
6. Hysteresis: i pixel deboli connessi a pixel forti diventano edge.

## Uso
```bash
pip install -r requirements.txt
python main.py path/to/image.jpg
# parametri opzionali: sigma kernel_size low_ratio high_ratio
python main.py photo.jpg 1.4 5 0.05 0.15
```
Output:
- `edges.png` — mappa binaria dei bordi
- `pipeline.png` — figura con i 6 stadi della pipeline (per il report)

## Struttura
- `canny.py` — implementazione algoritmica (NumPy puro)
- `main.py` — runner di esempio + visualizzazione
- `report/` — report in LaTeX (template IEEE, max 1 pagina)
