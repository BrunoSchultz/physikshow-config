#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import yaml
from jinja2 import Environment, FileSystemLoader

def lade_konfiguration(config_pfad="config/show_config.yaml"):
    with open(config_pfad, 'r', encoding='utf-8') as datei:
        return yaml.safe_load(datei)

def konfiguriere_jinja_umgebung(template_ordner):
    return Environment(
        block_start_string='<%', block_end_string='%>',
        variable_start_string='<<', variable_end_string='>>',
        comment_start_string='<#', comment_end_string='#>',
        trim_blocks=True, lstrip_blocks=True,
        loader=FileSystemLoader(os.path.abspath(template_ordner))
    )

def generiere_rider():
    print("Starte Bühnenmeister Pipeline...")
    config = lade_konfiguration()
    
    # Zugriff auf templates
    sprache = config.get('metadaten', {}).get('sprache', 'de').lower()
    template_ordner = f"templates/{sprache}"
    
    if not os.path.exists(template_ordner):
        print(f"Fehler: Template-Ordner '{template_ordner}' existiert nicht!")
        sys.exit(1)
        
    env = konfiguriere_jinja_umgebung(template_ordner)
    template = env.get_template('base.tex.j2')
    gerendertes_latex = template.render(config=config)
    
    os.makedirs("build", exist_ok=True)
    ausgabe_pfad = "build/main.tex"
    with open(ausgabe_pfad, 'w', encoding='utf-8') as f:
        f.write(gerendertes_latex)
        
    print(f"Erfolgreich generiert aus: {template_ordner}/base.tex.j2")

if __name__ == "__main__":
    generiere_rider()
