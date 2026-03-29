# Makefile [cite: 1]

PYTHON_SKRIPT = skripte/generiere_rider.py # [cite: 1]
BUILD_ORDNER = build # [cite: 1]
TEX_DATEI = main.tex # [cite: 1]
PDF_DATEI = main.pdf # [cite: 1]
CONFIG_FILE = config/show_config.yaml # [cite: 1]
ZIP_FILE = overleaf_upload.zip # [cite: 1]

.PHONY: all build clean overleaf generate # [cite: 1]

all: build # [cite: 1]

# .tex Datei generieren # [cite: 1]
generate: # [cite: 1]
	@echo "========================================" # [cite: 1]
	@echo "1. Lese Konfiguration und generiere LaTeX..." # [cite: 1]
	@echo "========================================" # [cite: 1]
	@python3 $(PYTHON_SKRIPT) || \
	{ echo "Fehler: Python-Skript fehlgeschlagen."; exit 1; } # [cite: 2]

# Lokal kompilieren # [cite: 2]
build: generate # [cite: 2]
	@echo "" # [cite: 2]
	@echo "========================================" # [cite: 2]
	@echo "2. Kompiliere PDF leise im Hintergrund..." # [cite: 2]
	@echo "========================================" # [cite: 2]
	@if [ ! -f $(BUILD_ORDNER)/$(TEX_DATEI) ]; then \
		echo "Fehler: $(TEX_DATEI) wurde nicht generiert."; exit 1; \
	fi # [cite: 3]
	@if ! command -v pdflatex >/dev/null 2>&1; then \
		echo "Fehler: 'pdflatex' wurde nicht gefunden. Ist LaTeX installiert und im PATH?"; exit 1; \
	fi # [cite: 4] [cite: 5]
	@cd $(BUILD_ORDNER) && pdflatex -interaction=nonstopmode $(TEX_DATEI) > /dev/null 2>&1 || \
	{ echo "Fehler beim Kompilieren. Überprüfe die .log Datei im build/ Ordner."; exit 1; } # [cite: 6] [cite: 7]
	@cd $(BUILD_ORDNER) && pdflatex -interaction=nonstopmode $(TEX_DATEI) > /dev/null 2>&1 || \
	{ echo "Fehler beim zweiten Kompilierdurchlauf. Überprüfe die .log Datei."; exit 1; } # [cite: 8] [cite: 9]
	@echo "ERFOLG! Datei in: $(BUILD_ORDNER)/$(PDF_DATEI)" # [cite: 9]

# Für Overleaf, nur generieren und direkt zippen (ohne pdflatex) # [cite: 9]
overleaf: generate # [cite: 9]
	@echo "" # [cite: 9]
	@echo "========================================" # [cite: 9]
	@echo "2. Erstelle ZIP-Archiv für Overleaf..." # [cite: 9]
	@echo "========================================" # [cite: 9]
	@if ! command -v zip >/dev/null 2>&1; then \
		echo "Fehler: 'zip' Befehl nicht gefunden."; exit 1; \
	fi # [cite: 10]
	@if [ ! -f $(BUILD_ORDNER)/$(TEX_DATEI) ]; then \
		echo "Fehler: $(TEX_DATEI) fehlt für das ZIP-Archiv."; exit 1; \
	fi # [cite: 11]
	@if [ ! -d medien/bilder ]; then \
		echo "Warnung: Ordner 'medien/bilder' nicht gefunden."; \
	fi # [cite: 12]
	@zip -q -r $(ZIP_FILE) $(BUILD_ORDNER)/$(TEX_DATEI) medien/bilder/ || \
	{ echo "Fehler beim Erstellen der ZIP-Datei."; exit 1; } # [cite: 13] [cite: 14]
	@echo "ERFOLG! Overleaf-ZIP erstellt: $(ZIP_FILE)" # [cite: 14]
	@echo "Lade '$(ZIP_FILE)' bei Overleaf hoch (New Project -> Upload Project)." # [cite: 14]

clean: # [cite: 15]
	@echo "Räume Build-Ordner auf..." # [cite: 15]
	@rm -rf $(BUILD_ORDNER)/* # [cite: 15]
	@rm -f $(ZIP_FILE) # [cite: 15]
	@echo "Build-Ordner ist sauber." # [cite: 15]