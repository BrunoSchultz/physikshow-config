import os
import shutil
import subprocess
import zipfile
from typing import Tuple

def compile_pdf(tex_path: str) -> Tuple[bool, str]:
    """
    Kompiliert die angegebene .tex Datei zu einer PDF.
    Gibt (Erfolg, Nachricht) zurück.
    """
    if not os.path.exists(tex_path):
        return False, f"Fehler: Die Datei {tex_path} wurde nicht gefunden."

    build_dir = os.path.dirname(tex_path)
    tex_file = os.path.basename(tex_path)
    
    try:
        # pdflatex muss zweimal laufen, damit Inhaltsverzeichnis/Referenzen stimmen
        for _ in range(2):
            subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", tex_file],
                cwd=build_dir,
                stdout=subprocess.PIPE, # Fängt den Output ab, damit die Konsole nicht vollgemüllt wird
                stderr=subprocess.PIPE,
                check=True,
                text=True
            )
            
        pdf_path = tex_path.replace('.tex', '.pdf')
        return True, f"PDF erfolgreich erstellt: {pdf_path}"
        
    except FileNotFoundError:
        return False, "Fehler: 'pdflatex' nicht gefunden. Ist LaTeX installiert und im PATH?"
    except subprocess.CalledProcessError:
        return False, "Fehler beim Kompilieren. Bitte überprüfe den LaTeX-Code oder die .log Datei."
    except Exception as e:
        return False, f"Unerwarteter Fehler: {str(e)}"


def create_overleaf_zip(tex_path: str, zip_path: str = "overleaf_upload.zip") -> Tuple[bool, str]:
    """
    Erstellt ein ZIP-Archiv für Overleaf mit der .tex Datei und den Medien.
    """
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            
            # LaTeX Datei hinzufügen
            if os.path.exists(tex_path):
                build_dir = os.path.dirname(tex_path)
                tex_file = os.path.basename(tex_path)
                # Behält die alte Struktur bei (z.B. build/main.tex)
                zipf.write(tex_path, arcname=f"{build_dir}/{tex_file}")
            else:
                return False, f"Fehler: {tex_path} nicht gefunden. Bitte erst generieren!"
                
            # Medienordner hinzufügen
            medien_dir = os.path.join("medien", "bilder")
            if os.path.exists(medien_dir):
                for root, _, files in os.walk(medien_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zipf.write(file_path, arcname=file_path)
            else:
                # Falls keine Bilder da sind, blockieren wir das Zippen nicht, warnen aber
                pass 
                
        return True, f"Overleaf-ZIP erfolgreich erstellt: {zip_path}"
    except Exception as e:
        return False, f"Fehler beim Erstellen der ZIP: {str(e)}"


def clean_build(build_dir: str = "build", zip_path: str = "overleaf_upload.zip") -> Tuple[bool, str]:
    """Räumt den Build-Ordner und die ZIP-Datei auf."""
    try:
        if os.path.exists(build_dir):
            for filename in os.listdir(build_dir):
                file_path = os.path.join(build_dir, filename)
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
        
        if os.path.exists(zip_path):
            os.remove(zip_path)
            
        return True, "Build-Ordner und ZIP wurden erfolgreich bereinigt."
    except Exception as e:
        return False, f"Fehler beim Aufräumen: {str(e)}"