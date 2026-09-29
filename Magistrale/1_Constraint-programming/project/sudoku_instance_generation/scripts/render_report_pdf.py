#!/usr/bin/env python3

"""Renderizza report/report.md in report/report.pdf.

Dipendenze esterne:
- pandoc (per la conversione markdown -> HTML)
- weasyprint (per la conversione HTML -> PDF)

Su macOS le librerie native richieste da weasyprint (gobject, pango) si trovano
sotto /opt/homebrew/lib quando vengono installate via Homebrew. Lo script aggiunge
quel percorso a DYLD_FALLBACK_LIBRARY_PATH se necessario.
"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


def ensure_lib_path() -> None:
    if sys.platform != "darwin":
        return
    brew_lib = "/opt/homebrew/lib"
    if not Path(brew_lib).is_dir():
        return
    current = os.environ.get("DYLD_FALLBACK_LIBRARY_PATH", "")
    if brew_lib in current.split(":"):
        return
    new_value = brew_lib if not current else f"{brew_lib}:{current}"
    os.environ["DYLD_FALLBACK_LIBRARY_PATH"] = new_value


def find_chrome() -> str:
    candidates = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
    ]
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
        found = shutil.which(name)
        if found:
            candidates.insert(0, found)
    for candidate in candidates:
        if Path(candidate).exists():
            return candidate
    return ""


def render_pdf(html_path: Path, output_path: Path, base_dir: Path) -> bool:
    """Renderizza l'HTML in PDF: preferisce weasyprint, ripiega su Chrome headless."""
    ensure_lib_path()
    try:
        from weasyprint import HTML

        HTML(filename=str(html_path), base_url=str(base_dir)).write_pdf(str(output_path))
        return True
    except (ImportError, OSError):
        pass

    chrome = find_chrome()
    if not chrome:
        print("Errore: né weasyprint né Chrome disponibili per generare il PDF", file=sys.stderr)
        return False
    subprocess.run(
        [
            chrome,
            "--headless",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={output_path}",
            f"file://{html_path}",
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return output_path.exists()


def main() -> int:
    parser = argparse.ArgumentParser(description="Renderizza il report markdown in PDF")
    parser.add_argument("--input", default="report/report.md")
    parser.add_argument("--output", default="report/report.pdf")
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parents[1]
    input_path = project_root / args.input
    output_path = project_root / args.output
    base_dir = input_path.parent

    if shutil.which("pandoc") is None:
        print("Errore: pandoc non disponibile nel PATH", file=sys.stderr)
        return 1

    html_path = output_path.with_suffix(".html")
    subprocess.run(
        [
            "pandoc",
            str(input_path),
            "-o",
            str(html_path),
            "--standalone",
            "--metadata",
            "pagetitle=Sudoku Instance Generation",
            f"--resource-path={base_dir}",
        ],
        check=True,
    )

    if not render_pdf(html_path, output_path, base_dir):
        html_path.unlink(missing_ok=True)
        return 1
    html_path.unlink(missing_ok=True)

    try:
        from pypdf import PdfReader

        pages = len(PdfReader(str(output_path)).pages)
        print(f"Generato {output_path} ({pages} pagine)")
    except ImportError:
        print(f"Generato {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
