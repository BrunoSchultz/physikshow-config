# Physikshow made easy

Dieses Projekt ist eine automatisierte Pipeline zur Erstellung von Stage-Ridern / Bühnenanweisungen für die Physikshow. Es nutzt Python und Jinja2, um Konfigurationsdaten (YAML) in LaTeX-Templates einzufügen, und kompiliert diese anschließend zu einem fertigen PDF-Dokument.

Die Vorlagen sind modular aufgebaut und unterstützen sowohl Deutsch (`de`) und Englisch (`en`).

## Voraussetzungen

Um dieses Projekt lokal auszuführen, benötigst du Folgendes:

* **Python 3.x:** Für das Ausführen des Generierungs-Skripts (`generiere_rider.py`).
* **LaTeX-Distribution:** (z. B. TeX Live, MiKTeX oder MacTeX), falls du die PDF-Dokumente lokal generieren möchtest.
* **Make:** Zum Ausführen der vordefinierten Build-Befehle (auf den meisten Linux/macOS-Systemen vorinstalliert).

Falls du keine lokale Latex-Installation hast, kannst du einen zip-Ordner für Overleaf erstellen (siehe Anwendung).

## Installation

1. **Repository klonen:**
   ```bash
   git clone [https://github.com/BrunoSchultz/physikshow-config](https://github.com/BrunoSchultz/physikshow-config)
   cd physikshow-config
   ```

2. **Python-Abhängigkeiten installieren:**
    ```bash
    pip install -r requirements.txt
    ```

## Anwendung

#### Konfiguration 

Die Inhalte werden über eine YAML-Konfigurationsdatei in `config/show_config.yaml` gesteuert. Hier definierst du alle Parameter (Metadaten, benötigte Technik, Logistik und Experimente), ohne den zugrunde liegenden LaTeX-Code manuell bearbeiten zu müssen.

#### Lokale PDF-Generierung

Wenn du LaTeX lokal installiert hast, kannst du den gesamten Prozess (Generierung der .tex-Datei und Kompilierung zur .pdf ) mit einem einzigen Befehl starten:

```bash
make
```

Die fertige PDF-Datei sowie die LaTeX-Quelldatei findest du anschließend im Verzeichnis `build/`.

#### Nutzung mit Overleaf

Falls du keine lokale LaTeX-Installation hast oder das Projekt auf Overleaf bearbeiten möchtest, kannst du die .tex-Dateien generieren und direkt verpacken lassen:

```bash
make overleaf
```

Dieser Befehl generiert den LaTeX-Code und erstellt automatisch die Datei `overleaf_upload.zip`. Diese ZIP-Datei enthält alles (inklusive des Ordners medien/bilder/) und kann direkt in ein neues Overleaf-Projekt hochgeladen werden ("New Project" -> "Upload Project").

#### Aufräumen 

Um alle generierten Dateien, temporären LaTeX-Dateien und den build/-Ordner zu entfernen, nutze

```bash
make clean
```

Oft können kompiliere Probleme entstehen, die dadurch behoben werden, indem man davor `make clean` ausführt.

### Config Datei
Die Datei ist im YAML-Format geschrieben. Achte beim Bearbeiten darauf, die Einrückungen (Leerzeichen, keine Tabs) beizubehalten. Werte können als Text (in Anführungszeichen "..."), als Zahlen oder als Wahrheitswerte (true / false) angegeben werden.

1. **Metadaten**

Hier definierst du die allgemeinen Eckdaten der Veranstaltung.


2. **Module**

Hier entscheidest du, welche Abschnitte im finalen Stage Rider auftauchen sollen. Setze den Wert auf true, wenn du das entsprechende Template benötigst (z. B. `technik: true`). Die folgenden Blöcke werden nur dann im Stage Rider verarbeitet, wenn das entsprechende Modul oben auf `true` gesetzt wurde.

3. **Bühne (buehne)**

Definiert die Ausstattung, die direkt auf der Bühne benötigt wird. Gib die genaue Anzahl an Tischen (tische) und Stühlen (stuehle) an. Unter `sonstiges` kannst du zusätzlichen Text eintragen (z. B. "Ein Wasseranschluss wird benötigt"). Bleibt das Feld leer (""), wird kein Text generiert.

4. **Anreise und Logistik (anreise)**

Informationen für die Planung vor Ort. Trage den Anreisetag (z. B. "31.03." oder "Showtag"), die genaue Uhrzeit und die Größe der Crew ein. Unter fahrzeuge spezifizierst du, wie viele Parkplätze für Material- und Personentransporter freigehalten werden müssen.

5. **Technik (technik)**

Alles rund um Licht, Ton und Medien. Crew & Kontakte: Du kannst spezifische Ansprechpartner nur für die Technik benennen.

- Bild: Auf true setzen, falls Beamer/Leinwände für Bilder oder Videos gebraucht werden.

- Licht & Ton: Hier kannst du sehr granular einstellen, was ihr selbst mitbringt (aktiv: true) und was die Location leisten muss.

6. **Experimente (experimente)**

Besondere Anforderungen und Gefahrenhinweise für die üblichen, "gefährlichen" Versuche. Zurzeit nur für flüssigen Stickstoff und Feuertornado, kann aber leicht ergänzt werden.