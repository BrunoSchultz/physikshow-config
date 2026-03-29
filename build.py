#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import shutil
import subprocess
import zipfile

BUILD_DIR = "build"
TEX_FILE = "main.tex"
PDF_FILE = "main.pdf"
ZIP_FILE = "overleaf_upload.zip"

def generate():
    print("========================================")
    print("1. Lese Konfiguration und generiere LaTeX...")
    print("========================================")
    # Uses the same Python interpreter currently running this script
    script_path = os.path.join("skripte", "generiere_rider.py")
    subprocess.run([sys.executable, script_path], check=True)

def build():
    generate()
    print("\n========================================")
    print("2. Kompiliere PDF leise im Hintergrund...")
    print("========================================")
    
    tex_path = os.path.join(BUILD_DIR, TEX_FILE)
    if not os.path.exists(tex_path):
        print(f"Fehler: {tex_path} wurde nicht generiert.")
        return

    try:
        # pdflatex needs to run from within the build directory to keep root clean
        for _ in range(2):
            subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", TEX_FILE],
                cwd=BUILD_DIR,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True
            )
        print(f"✅ ERFOLG! Datei in: {BUILD_DIR}/{PDF_FILE}")
    except FileNotFoundError:
        print("Fehler: 'pdflatex' wurde nicht gefunden. Ist LaTeX installiert und in den System-Umgebungsvariablen (PATH)?")
    except subprocess.CalledProcessError:
        print("Fehler beim Kompilieren der LaTeX-Datei. Überprüfe die .log Datei im build/ Ordner.")

def overleaf():
    generate()
    print("\n========================================")
    print("2. Erstelle ZIP-Archiv für Overleaf...")
    print("========================================")
    
    with zipfile.ZipFile(ZIP_FILE, 'w', zipfile.ZIP_DEFLATED) as zipf:
        tex_path = os.path.join(BUILD_DIR, TEX_FILE)
        if os.path.exists(tex_path):
            zipf.write(tex_path, arcname=f"{BUILD_DIR}/{TEX_FILE}")
        else:
            print(f"Warnung: {tex_path} nicht gefunden.")
            
        medien_dir = os.path.join("medien", "bilder")
        if os.path.exists(medien_dir):
            for root, _, files in os.walk(medien_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, arcname=file_path)
        else:
            print(f"Warnung: Ordner {medien_dir} nicht gefunden.")
            
    print(f"✅ ERFOLG! Overleaf-ZIP erstellt: {ZIP_FILE}")
    print("Lade 'overleaf_upload.zip' bei Overleaf hoch (New Project -> Upload Project).")

def clean():
    print("Räume Build-Ordner auf...")
    if os.path.exists(BUILD_DIR):
        for filename in os.listdir(BUILD_DIR):
            file_path = os.path.join(BUILD_DIR, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Fehler beim Löschen von {file_path}: {e}")
                
    if os.path.exists(ZIP_FILE):
        os.remove(ZIP_FILE)
    print("Build-Ordner ist sauber.")

if __name__ == "__main__":

    target = sys.argv[1].lower() if len(sys.argv) > 1 else "build"
    
    if target == "generate":
        generate()
    elif target in ["build", "all"]:
        build()
    elif target == "overleaf":
        overleaf()
    elif target == "clean":
        clean()
    else:
        print(f"Unbekanntes Ziel: {target}")
        print("Verwendung: python build.py [generate|build|overleaf|clean]")