# Makefile 

PYTHON_SKRIPT = skripte/generiere_rider.py
BUILD_ORDNER = build
TEX_DATEI = main.tex
PDF_DATEI = main.pdf
CONFIG_FILE = config/show_config.yaml
ZIP_FILE = overleaf_upload.zip

.PHONY: all build clean overleaf generate

all: build

# .tex Datei generieren
generate:
	@echo "========================================"
	@echo "1. Lese Konfiguration und generiere LaTeX..."
	@echo "========================================"
	@python3 $(PYTHON_SKRIPT) || { echo "❌ Fehler: Python-Skript fehlgeschlagen."; exit 1; }

# Lokal kompilieren
build: generate
	@echo ""
	@echo "========================================"
	@echo "2. Kompiliere PDF leise im Hintergrund..."
	@echo "========================================"
	@if [ ! -f $(BUILD_ORDNER)/$(TEX_DATEI) ]; then \
		echo "❌ Fehler: $(TEX_DATEI) wurde nicht generiert."; exit 1; \
	fi
	@if ! command -v pdflatex >/dev/null 2>&1; then \
		echo "❌ Fehler: 'pdflatex' wurde nicht gefunden. Ist LaTeX installiert und im PATH?"; exit 1; \
	fi
	@cd $(BUILD_ORDNER) && pdflatex -interaction=nonstopmode $(TEX_DATEI) > /dev/null 2>&1 || { echo "❌ Fehler beim Kompilieren. Überprüfe die .log Datei im build/ Ordner."; exit 1; }
	@cd $(BUILD_ORDNER) && pdflatex -interaction=nonstopmode $(TEX_DATEI) > /dev/null 2>&1 || { echo "❌ Fehler beim zweiten Kompilierdurchlauf. Überprüfe die .log Datei."; exit 1; }
	@echo "✅ ERFOLG! Datei in: $(BUILD_ORDNER)/$(PDF_DATEI)"

# Für Overleaf, nur generieren und direkt zippen (ohne pdflatex)
overleaf: generate
	@echo ""
	@echo "========================================"
	@echo "2. Erstelle ZIP-Archiv für Overleaf..."
	@echo "========================================"
	@if ! command -v zip >/dev/null 2>&1; then \
		echo "❌ Fehler: 'zip' Befehl nicht gefunden."; exit 1; \
	fi
	@if [ ! -f $(BUILD_ORDNER)/$(TEX_DATEI) ]; then \
		echo "❌ Fehler: $(TEX_DATEI) fehlt für das ZIP-Archiv."; exit 1; \
	fi
	@if [ ! -d medien/bilder ]; then \
		echo "⚠️ Warnung: Ordner 'medien/bilder' nicht gefunden."; \
	fi
	@zip -q -r $(ZIP_FILE) $(BUILD_ORDNER)/$(TEX_DATEI) medien/bilder/ || { echo "❌ Fehler beim Erstellen der ZIP-Datei."; exit 1; }
	@echo "✅ ERFOLG! Overleaf-ZIP erstellt: $(ZIP_FILE)"
	@echo "Lade '$(ZIP_FILE)' bei Overleaf hoch (New Project -> Upload Project)."

clean:
	@echo "Räume Build-Ordner auf..."
	@rm -rf $(BUILD_ORDNER)/*
	@rm -f $(ZIP_FILE)
	@echo "✅ Build-Ordner ist sauber."