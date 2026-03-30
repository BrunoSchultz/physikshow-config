# Physikshow Stage Rider Generator

Dieses Projekt bietet eine webbasierte Benutzeroberfläche zur einfachen Erstellung von Stage-Ridern / Bühnenanweisungen für die Physikshow.

## Voraussetzungen

Um dieses Projekt lokal auszuführen, brauchst du:

* **Python 3.x:** Für das Ausführen der Web-App.
* **LaTeX-Distribution** (z. B. TeX Live, MiKTeX oder MacTeX): *Nur erforderlich*, wenn du die fertigen PDF-Dokumente direkt lokal über die App generieren möchtest. Für den Overleaf-Export wird lokal kein LaTeX benötigt.

## Git Installation

Falls du Git noch nicht installiert hast, wähle dein Betriebssystem:

- **Windows:** Lade Git von git-scm.com/download/win herunter und folge dem Installer. Alternativ über das Terminal: `winget install --id Git.Git -e --source winget`.
- **macOS:** Öffne das Terminal und gib `git --version` ein. Falls Git fehlt, bietet macOS automatisch die Installation an. Alternativ via Homebrew: `brew install git`.
- **Linux (Ubuntu/Debian):** Öffne das Terminal und führe `sudo apt update && sudo apt install git` aus.

## Installation

1. **Repository klonen:**
   ```bash
   git clone https://github.com/BrunoSchultz/physikshow-config
   cd physikshow-config
   ```

2. **Python-Packete installieren**
```bash
    pip install -r requirements.txt
```
## Seite starten 

Die gesamte Steuerung erfolgt über die grafische Oberfläche. Starte die Seite einfach über den Terminal von dem `physikshow-config`-Ordner
```bash
python main.py
```
Das Skript startet einen lokalen Webserver und öffnet die Anwendung automatisch in deinem Standard-Webbrowser.

## Bedienung

Die Seite ist in verschiedene Tabsterteilt, in denen du die Anforderungen deiner Show zusammenklicken kannst.

## 1. Aktive Module (Modul-Steuerung)

Ganz oben auf der Seite kannst du per Checkbox auswählen, welche Abschnitte (Bühne, Anreise, Technik, Experimente) im finalen Stage Rider auftauchen sollen.  
Deaktivierte Module werden im finalen Dokument ausgeblendet, und die entsprechenden Tabs in der Benutzeroberfläche verschwinden.

## 2. Dateneingabe über Tabs

### Allgemein
Hier definierst du die Eckdaten der Veranstaltung (Name, Ort, Datum, Sprache).  
Zudem kannst du hier Kontakte und Ansprechpartner für allgemeine Fragen, Technik und Experimente hinzufügen oder löschen.

### Bühne
Definiert die Ausstattung, die direkt auf der Bühne benötigt wird (Anzahl der Tische und Stühle).  
Unter **"Sonstiges"** kannst du freien Text eintragen (z. B. *"Ein Wasseranschluss wird benötigt"*).

### Anreise
Informationen für die Logistik vor Ort.  
Trage Anreisetag, Ankunftszeit und die Größe der Crew ein. Zudem spezifizierst du, wie viele Parkplätze für Material- und Personentransporter freigehalten werden müssen.

### Technik
Detaillierte Steuerung für Bild, Licht und Ton.  
Lege per Checkbox fest, ob ihr eigenes Equipment mitbringt oder die Location Technik (z. B. Mischpult, Mikrofone, Verdunkelung, Beamer) stellen muss.

### Experimente
Besondere Anforderungen und Gefahrenhinweise für spezifische Versuche (aktuell für Flüssigstickstoff und Feuertornado).

## 3. Aktionen & Export

Am unteren Bildschirmrand findest du die Buttons zur Verarbeitung deiner Eingaben:

- **Speichern (YAML)**  
  Speichert deine aktuellen Eingaben im Hintergrund ab. Wenn du die App das nächste Mal öffnest, wird genau dieser Stand wieder geladen.

- **Overleaf ZIP**  
  Generiert den LaTeX-Code und verpackt ihn zusammen mit allen benötigten Medien in eine ZIP-Datei (`overleaf_upload.zip`).  
  Diese wird dir direkt zum Download angeboten und kann in ein neues Overleaf-Projekt hochgeladen werden (*"New Project" → "Upload Project"*).

- **PDF Generieren & Downloaden**  
  Kompiliert den Stage Rider im Hintergrund zu einer fertigen PDF und lädt diese direkt in deinem Browser herunter.  
  *(Achtung: Erfordert eine lokale LaTeX-Installation).*