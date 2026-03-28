# Makefile für die Bühnenmeister Pipeline

PYTHON_SKRIPT = skripte/generiere_rider.py
BUILD_ORDNER = build
TEX_DATEI = main.tex
PDF_DATEI = main.pdf
CONFIG_FILE = show_config.yaml


.PHONY: all build clean overleaf generate

all: build

# .tex Datei generieren
generate:
	@echo "========================================"
	@echo "1. Lese $(CONFIG_FILE) und generiere LaTeX..."
	@echo "========================================"
	python3 $(PYTHON_SKRIPT) $(CONFIG_FILE)

# Lokal kompilieren
build: generate
	@echo ""
	@echo "========================================"
	@echo "2. Kompiliere PDF leise im Hintergrund..."
	@echo "========================================"
	@cd $(BUILD_ORDNER) && pdflatex -interaction=nonstopmode $(TEX_DATEI) > /dev/null 2>&1
	@cd $(BUILD_ORDNER) && pdflatex -interaction=nonstopmode $(TEX_DATEI) > /dev/null 2>&1
	@echo "✅ ERFOLG! Datei in: $(BUILD_ORDNER)/$(PDF_DATEI)"

# Für Overleaf, nur generieren und direkt zippen (ohne pdflatex)
overleaf: generate
	@echo ""
	@echo "========================================"
	@echo "2. Erstelle ZIP-Archiv für Overleaf..."
	@echo "========================================"
	@zip -q -r overleaf_upload.zip $(BUILD_ORDNER)/$(TEX_DATEI) medien/bilder/
	@echo "✅ ERFOLG! Overleaf-ZIP erstellt: overleaf_upload.zip"
	@echo "Lade 'overleaf_upload.zip' bei Overleaf hoch (New Project -> Upload Project)."

clean:
	@echo "Räume Build-Ordner auf..."
	rm -rf $(BUILD_ORDNER)/*
	rm -f overleaf_upload.zip
	@echo "Build-Ordner ist sauber."