import asyncio
from nicegui import ui

# Backend imports
from backend.models import Kontakt, ShowConfig
from backend import utils, generate, builder

def load_initial_config() -> ShowConfig:
    """Lädt die Konfiguration oder erstellt einen Fallback."""
    try:
        return utils.load_config("config/show_config.yaml")
    except Exception as e:
        ui.notify(f"Konnte Config nicht laden: {e}", color='negative')
        return ShowConfig()

# Globale State-Instanz für die Session
config = load_initial_config()

@ui.refreshable
def render_kontakt_liste(kontakt_liste: list[Kontakt], titel: str):
    """Rendert eine dynamische Liste von Kontakten."""
    with ui.row().classes('w-full items-center justify-between mt-4 mb-2'):
        ui.label(titel).classes('text-lg font-bold text-gray-700')
        
        def add_kontakt():
            kontakt_liste.append(Kontakt(name="", mail="", telefon=""))
            render_kontakt_liste.refresh()
            
        ui.button('Hinzufügen', icon='add', on_click=add_kontakt).props('outline size=sm')

    if not kontakt_liste:
        ui.label('Keine Kontakte hinterlegt.').classes('text-sm italic text-gray-400 mb-4')
    else:
        with ui.column().classes('w-full gap-2 mb-4'):
            for kontakt in kontakt_liste:
                with ui.row().classes('w-full items-center gap-4'):
                    ui.input('Name').bind_value(kontakt, 'name').classes('flex-grow')
                    ui.input('Mail').bind_value(kontakt, 'mail').classes('flex-grow')
                    ui.input('Telefon').bind_value(kontakt, 'telefon').classes('flex-grow')
                    
                    def remove_kontakt(k=kontakt):
                        kontakt_liste.remove(k)
                        render_kontakt_liste.refresh()
                        
                    ui.button(icon='delete', color='negative', on_click=lambda k=kontakt: remove_kontakt(k)).props('flat round')


# Tabs
def build_allgemein_tab(config: ShowConfig):
    ui.label('Metadaten').classes('text-xl font-bold mb-2')
    with ui.row().classes('w-full gap-4'):
        ui.input('Show Name').bind_value(config.metadaten, 'show_name').classes('flex-grow')
        ui.input('Veranstaltungsort').bind_value(config.metadaten, 'veranstaltungsort').classes('flex-grow')
    
    with ui.row().classes('w-full gap-4 mt-2'):   
        ui.input('Datum').bind_value(config.metadaten, 'datum')
        ui.select(['de', 'en'], label='Sprache').bind_value(config.metadaten, 'sprache').classes('flex-grow')
    
    ui.separator().classes('my-6')
    
    ui.label('Kontakte & Ansprechpartner').classes('text-xl font-bold mb-2')
    render_kontakt_liste(config.metadaten.kontakte, 'Allgemeine Rückfragen')
    ui.separator().classes('my-2')
    render_kontakt_liste(config.technik.kontakte, 'Technik')
    ui.separator().classes('my-2')
    render_kontakt_liste(config.experimente.kontakte, 'Experimente')

def build_buehne_tab(config: ShowConfig):
    with ui.row().classes('gap-4'):
        ui.number('Tische', format='%.0f').bind_value(config.buehne, 'tische')
        ui.number('Stühle', format='%.0f').bind_value(config.buehne, 'stuehle')
    ui.textarea('Sonstiges').bind_value(config.buehne, 'sonstiges').classes('w-full mt-4')

def build_anreise_tab(config: ShowConfig):
    ui.label('Logistik').classes('text-xl font-bold mb-2')
    with ui.row().classes('gap-4'):
        ui.input('Anreisetag').bind_value(config.anreise, 'anreisetag')
        ui.input('Ankunftszeit').bind_value(config.anreise, 'ankunftszeit')
    ui.number('Crew Größe', format='%.0f').bind_value(config.anreise, 'crew_groesse').classes('mt-2')
    
    ui.label('Fahrzeuge').classes('text-lg mt-6')
    with ui.row().classes('gap-4'):
        ui.number('Material Transporter', format='%d').bind_value(config.anreise.fahrzeuge, 'material_transporter')
        ui.number('Personen Transporter', format='%d').bind_value(config.anreise.fahrzeuge, 'personen_transporter')

def build_technik_tab(config: ShowConfig):
    ui.label('Technik & Medien').classes('text-xl font-bold mb-2')
    
    ui.label('Bild').classes('text-lg mt-4')
    ui.checkbox('Beamer/Bild benötigt').bind_value(config.technik, 'bild')
    
    ui.label('Licht').classes('text-lg mt-4')
    with ui.row().classes('gap-4'):
        ui.checkbox('Licht bringen wir mit').bind_value(config.technik.licht, 'aktiv')
        ui.checkbox('Verdunkelung nötig').bind_value(config.technik.licht, 'verdunkelung_noetig')
        ui.checkbox('Spot').bind_value(config.technik.licht, 'spot')

    ui.label('Ton').classes('text-lg mt-4')
    with ui.row().classes('gap-4 items-center'):
        ui.checkbox('Brauchen Ton').bind_value(config.technik.ton, 'aktiv')
        ui.checkbox('Bringen Mischpult').bind_value(config.technik.ton, 'mischpult')
        ui.number('Anzahl Mikros', format='%d').bind_value(config.technik.ton, 'anzahl_mikros')

def build_experimente_tab(config: ShowConfig):
    ui.label('Spezial-Experimente').classes('text-xl font-bold mb-2')
    
    with ui.card().classes('w-full mb-4'):
        stickstoff_aktiv = ui.checkbox('Flüssigstickstoff').bind_value(config.experimente.fluessigstickstoff, 'aktiv')
        with ui.column().bind_visibility_from(stickstoff_aktiv, 'value').classes('ml-8 mt-2'):
            ui.number('Liter benötigt', format='%.0f').bind_value(config.experimente.fluessigstickstoff.anforderungen, 'liter_benoetigt')

    with ui.card().classes('w-full'):
        tornado_aktiv = ui.checkbox('Feuertornado').bind_value(config.experimente.feuertornado, 'aktiv')
        with ui.column().bind_visibility_from(tornado_aktiv, 'value').classes('ml-8 mt-2'):
            ui.label('Bilder werden aus dem Medien-Ordner geladen.').classes('text-gray-600 italic')


# Aktionen
def speichere_yaml():
    if utils.save_config(config, "config/show_config.yaml"):
        ui.notify("Konfiguration in YAML gespeichert!", color="positive")
    else:
        ui.notify("Fehler beim Speichern.", color="negative")

async def baue_pdf():
    ui.notify("Kompiliere PDF...", type="info")
    try:
        builder.clean_build()
        tex_pfad = generate.generiere_rider(config)
        
        # Auslagern des pdflatex-Befehls
        erfolg, nachricht = await asyncio.to_thread(builder.compile_pdf, tex_pfad)
        
        if erfolg:
            ui.notify("PDF erfolgreich erstellt!", color="positive")
            ui.download(tex_pfad.replace('.tex', '.pdf'))
        else:
            ui.notify(nachricht, color="negative", timeout=10000)
    except Exception as e:
        ui.notify(f"Fehler: {str(e)}", color="negative")

def baue_zip():
    ui.notify("Erstelle Overleaf ZIP...", type="info")
    try:
        builder.clean_build()
        tex_pfad = generate.generiere_rider(config)
        erfolg, nachricht = builder.create_overleaf_zip(tex_pfad)
        
        if erfolg:
            ui.notify(nachricht, color="positive")
            ui.download("overleaf_upload.zip")
        else:
            ui.notify(nachricht, color="negative")
    except Exception as e:
        ui.notify(f"Fehler: {str(e)}", color="negative")


# ==========================================
# UI
# ==========================================

def build_ui():
    ui.label('Physikshow Stage Rider Generator').classes('text-3xl font-bold mb-4')

    # Modul-Steuerung
    with ui.card().classes('w-full mb-4'):
        ui.label('Aktive Module').classes('text-lg font-bold')
        with ui.row().classes('gap-4'):
            buehne_checkbox = ui.checkbox('Bühne').bind_value(config.module, 'buehne')
            anreise_checkbox = ui.checkbox('Anreise').bind_value(config.module, 'anreise')
            technik_checkbox = ui.checkbox('Technik').bind_value(config.module, 'technik')
            experimente_checkbox = ui.checkbox('Experimente').bind_value(config.module, 'experimente')

    # Tabs initialisieren
    with ui.tabs().classes('w-full') as tabs:
        allgemein_tab = ui.tab('Allgemein') 
        buehne_tab = ui.tab('Bühne').bind_visibility_from(buehne_checkbox, 'value')
        anreise_tab = ui.tab('Anreise').bind_visibility_from(anreise_checkbox, 'value')
        technik_tab = ui.tab('Technik').bind_visibility_from(technik_checkbox, 'value')
        experimente_tab = ui.tab('Experimente').bind_visibility_from(experimente_checkbox, 'value')

    # Tab Panels befüllen
    with ui.tab_panels(tabs, value=allgemein_tab).classes('w-full'):
        with ui.tab_panel(allgemein_tab):
            build_allgemein_tab(config)
        with ui.tab_panel(buehne_tab):
            build_buehne_tab(config)
        with ui.tab_panel(anreise_tab):
            build_anreise_tab(config)
        with ui.tab_panel(technik_tab):
            build_technik_tab(config)
        with ui.tab_panel(experimente_tab):
            build_experimente_tab(config)

    # Buttons
    ui.separator().classes('my-6')
    with ui.row().classes('w-full justify-between items-center'):
        with ui.row().classes('gap-4'):
            ui.button('Speichern (YAML)', on_click=speichere_yaml, color='secondary')
            ui.button('Overleaf ZIP', on_click=baue_zip, color='accent')
        ui.button('PDF Generieren & Downloaden', on_click=baue_pdf, color='primary').classes('font-bold')

build_ui()
ui.run(title="Stage Rider Builder", favicon="🎭")