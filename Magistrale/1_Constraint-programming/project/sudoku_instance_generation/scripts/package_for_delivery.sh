#!/usr/bin/env bash
set -euo pipefail

# Costruisce il file zip finale per la consegna del progetto.
# Esegui dalla root del progetto:
#   bash scripts/package_for_delivery.sh

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT"

PROJECT_NAME="sudoku_instance_generation"
ZIP_NAME="${PROJECT_NAME}_delivery.zip"
STAGE_DIR=".package_stage"

rm -rf "$STAGE_DIR" "$ZIP_NAME"
mkdir -p "$STAGE_DIR/$PROJECT_NAME"

# Renderizza il PDF del report se possibile, in modo che lo zip lo contenga.
if python3 scripts/render_report_pdf.py >/dev/null 2>&1; then
  echo "Report PDF rigenerato in report/report.pdf"
else
  rm -f report/report.pdf
  echo "Avviso: rendering PDF non disponibile, lo zip conterrà solo report.md"
fi

# Consegna snella: codice, dataset, risultati e report. Esclusi i documenti
# interni di pianificazione e gli appunti di studio per l'orale.
INCLUDE=(
  "README.md"
  "models"
  "scripts"
  "spec/gecode_local.msc"
  "report/report.pdf"
  "data/solved/sample_solutions.json"
  "data/test"
  "data/generated/final_check_generated.json"
  "data/solved/sample_solutions_500.json"
  "data/solved/augmented_solutions.json"
  "results/full_benchmark.csv"
  "results/full_benchmark.json"
  "results/full_benchmark_1000.csv"
  "results/optimization_benchmark.csv"
  "results/optimization_benchmark.json"
  "results/optimizer_comparison.csv"
  "results/overnight_comparison.csv"
  "results/minizinc_api_comparison.json"
  "results/benchmark_minizinc_timeout300.json"
  "results/final_check_benchmark.json"
  "results/generated_random.json"
  "results/generated_density.json"
  "results/generated_symmetry.json"
)

for item in "${INCLUDE[@]}"; do
  if [ -e "$item" ]; then
    mkdir -p "$STAGE_DIR/$PROJECT_NAME/$(dirname "$item")"
    cp -R "$item" "$STAGE_DIR/$PROJECT_NAME/$item"
  else
    echo "Avviso: '$item' non esiste, saltato."
  fi
done

# Pulizia file rigenerabili
find "$STAGE_DIR" -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find "$STAGE_DIR" -name "*.pyc" -type f -delete 2>/dev/null || true
find "$STAGE_DIR" -name ".DS_Store" -type f -delete 2>/dev/null || true
find "$STAGE_DIR" -name ".gitkeep" -type f -delete 2>/dev/null || true

# Script di build interni: non servono al destinatario della consegna
rm -f "$STAGE_DIR/$PROJECT_NAME/scripts/render_report_pdf.py"
rm -f "$STAGE_DIR/$PROJECT_NAME/scripts/package_for_delivery.sh"

# Crea zip
(cd "$STAGE_DIR" && zip -rq "../$ZIP_NAME" "$PROJECT_NAME")

# Cleanup
rm -rf "$STAGE_DIR"

echo
echo "Zip creato: $PROJECT_ROOT/$ZIP_NAME"
ls -lh "$ZIP_NAME" | awk '{print "  size:", $5}'
echo "  files:"
unzip -l "$ZIP_NAME" | tail -n 1
