#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os 
import sys
from jinja2 import Environment, FileSystemLoader
import utils
from models import ShowConfig

def konfiguriere_jinja_umgebung(template_ordner):
    return Environment(
        block_start_string='<%', block_end_string='%>',
        variable_start_string='<<', variable_end_string='>>',
        comment_start_string='<#', comment_end_string='#>',
        trim_blocks=True, lstrip_blocks=True,
        loader=FileSystemLoader(os.path.abspath(template_ordner))
    )

def generiere_rider(config: ShowConfig) -> str:
    data = config.model_dump()

    sprache = data['metadaten']['sprache']
    template_ordner = f"templates/{sprache}"

    if not os.path.exists(template_ordner):
        raise FileNotFoundError(f"Fehler: Template-Ordner '{template_ordner}' existiert nicht")
    
    env = konfiguriere_jinja_umgebung(template_ordner)
    template = env.get_template('base.tex.j2')
    gerendertes_latex = template.render(config=data)

    os.makedirs("build", exist_ok=True)
    ausgabe_pfad = "build_test/main.tex"

    with open(ausgabe_pfad, 'w', encoding='utf-8') as f:
        f.write(gerendertes_latex)
        
    print(f"Erfolgreich generiert aus: {template_ordner}/base.tex.j2")

    return ausgabe_pfad

if __name__ == '__main__':
    test_config = utils.load_config()
    generiere_rider(test_config)