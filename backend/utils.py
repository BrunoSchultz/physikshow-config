import os
import yaml
from models import ShowConfig

def load_config(filepath: str = "config/show_config.yaml") -> ShowConfig:
    """
    Liest die YAML-Datei und wandelt sie in das Pydantic-Objekt um.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Die Konfigurationsdatei '{filepath}' wurde nicht gefunden.")
        
    with open(filepath, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f) or {}
        
    return ShowConfig(**data)

def save_config(config: ShowConfig, filepath: str = "config/show_config.yaml") -> bool:
    """
    Speichert das Pydantic-Objekt zurück in die YAML-Datei, filtert aber
    inaktive Experimente heraus, um die Datei sauber zu halten.
    """
    try:
       # zu dict konvertieren
        data = config.model_dump(exclude_unset=True)
        
        # Cleanup Experiments
        if 'experimente' in data:
            experiments_to_keep = {}
            for key, value in data['experimente'].items():
                # kontakte behalten
                if key == 'kontakte' or (isinstance(value, dict) and value.get('aktiv') is True):
                    experiments_to_keep[key] = value
            
            # Replace the full list with our cleaned-up list
            data['experimente'] = experiments_to_keep

        # Auf yaml schreiben
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)
            
        return True
        
    except Exception as e:
        print(f"Fehler beim Speichern der Config: {e}")
        return False