from nicegui import ui
import asyncio

from backend import utils, generate, builder

# Lade den aktuelle Yaml-Datei
try:
    config = utils.load_config("config/show_config.yaml")
except Exception as e:
    ui.notify(f"Konnte Config nicht laden: {e}", color='negative')
    from backend.models import ShowConfig
    config = ShowConfig()

ui.label('Physikshow Stage Rider Generator').classes('text-3xl font-bold mb-4')

# Modul-Steuerung
with ui.card().classes('w-full'):
    ui.label('Aktive Module').classes('text-lg font-bold')
    with ui.row():
        buehne_checkbox = ui.checkbox('Bühne').bind_value(config.module, 'buehne')
        anreise_checkbox = ui.checkbox('Anreise').bind_value(config.module, 'anreise')
        technik_checkbox = ui.checkbox('Technik').bind_value(config.module, 'technik')
        experimente_checkbox = ui.checkbox('Experimente').bind_value(config.module, 'experimente')

# --- TABS ---
with ui.tabs().classes('w-full') as tabs:
    allgemein_tab = ui.tab('Allgemein') 
    buehne_tab = ui.tab('Bühne').bind_visibility_from(buehne_checkbox, 'value')
    anreise_tab = ui.tab('Anreise').bind_visibility_from(anreise_checkbox, 'value')
    technik_tab = ui.tab('Technik').bind_visibility_from(technik_checkbox, 'value')
    experimente_tab = ui.tab('Experimente').bind_visibility_from(experimente_checkbox, 'value')

# --- TAB PANELS ---
with ui.tab_panels(tabs, value=allgemein_tab).classes('w-full'):
    
    with ui.tab_panel(allgemein_tab):
        ui.label('Metadaten').classes('text-xl font-bold mb-2')
        with ui.row().classes('w-full'):
            ui.input('Show Name').bind_value(config.metadaten, 'show_name').classes('flex-grow')
            ui.input('Veranstaltungsort').bind_value(config.metadaten, 'veranstaltungsort').classes('flex-grow')
        with ui.row().classes('w-full'):   
            ui.input('Datum').bind_value(config.metadaten, 'datum')
            ui.select(['de', 'en'], label='Sprache').classes('flex-grow').bind_value(config.metadaten, 'sprache')
        ui.separator().classes('my-6')
        ui.label('Kontakte & Ansprechpartner').classes('text-xl font-bold mb-2')

        # Hilfsfunktion, um die Kontakt-Reihen schön darzustellen
        def render_kontakte(kontakt_liste, titel):
            ui.label(titel).classes('text-lg mt-2 text-gray-600')
            if not kontakt_liste:
                ui.label('Keine Kontakte hinterlegt.').classes('text-sm italic text-gray-400')
            for kontakt in kontakt_liste:
                with ui.row().classes('w-full items-center gap-4'):
                    ui.input('Name').bind_value(kontakt, 'name').classes('flex-grow')
                    ui.input('Mail').bind_value(kontakt, 'mail').classes('flex-grow')
                    ui.input('Telefon').bind_value(kontakt, 'telefon').classes('flex-grow')

        # Render all three contact lists
        render_kontakte(config.metadaten.kontakte, 'Allgemeine Rückfragen')
        render_kontakte(config.technik.kontakte, 'Technik')
        render_kontakte(config.experimente.kontakte, 'Experimente')

    with ui.tab_panel(buehne_tab):
        with ui.row():
            ui.number('Tische', format='%.0f').bind_value(config.buehne, 'tische')
            ui.number('Stühle', format='%.0f').bind_value(config.buehne, 'stuehle')
        ui.textarea('Sonstiges').bind_value(config.buehne, 'sonstiges').classes('w-full')

    with ui.tab_panel(anreise_tab):
        ui.label('Logistik').classes('text-xl font-bold mb-2')
        with ui.row():
            ui.input('Anreisetag').bind_value(config.anreise, 'anreisetag')
            ui.input('Ankunftszeit').bind_value(config.anreise, 'ankunftszeit')
        ui.number('Crew Größe', format='%.0f').bind_value(config.anreise, 'crew_groesse')
        
        ui.label('Fahrzeuge').classes('text-lg mt-4')
        with ui.row():
            ui.number('Material Transporter', format='%d').bind_value(config.anreise.fahrzeuge, 'material_transporter')
            ui.number('Personen Transporter', format='%d').bind_value(config.anreise.fahrzeuge, 'personen_transporter')

    with ui.tab_panel(technik_tab):
        ui.label('Technik & Medien').classes('text-xl font-bold mb-2')
        ui.label('Bild').classes('text-lg mt-4')
        ui.checkbox('Beamer/Bild benötigt').bind_value(config.technik, 'bild')
        
        ui.label('Licht').classes('text-lg mt-4')
        with ui.row():
            ui.checkbox('Licht bringen wir mit').bind_value(config.technik.licht, 'aktiv')
            ui.checkbox('Verdunkelung nötig').bind_value(config.technik.licht, 'verdunkelung_noetig')
            ui.checkbox('Spot').bind_value(config.technik.licht, 'spot')

        ui.label('Ton').classes('text-lg mt-4')
        ui.checkbox('Brauchen Ton').bind_value(config.technik.ton, 'aktiv')
        ui.checkbox('Bringen Mischpult').bind_value(config.technik.ton, 'mischpult')
        ui.number('Anzahl Mikros', format='%d').bind_value(config.technik.ton, 'anzahl_mikros')


    with ui.tab_panel(experimente_tab):
        ui.label('Spezial-Experimente').classes('text-xl font-bold mb-2')
        
        with ui.card().classes('w-full mb-4'):
            stickstoff_aktiv = ui.checkbox('Flüssigstickstoff').bind_value(config.experimente.fluessigstickstoff, 'aktiv')
            with ui.column().bind_visibility_from(stickstoff_aktiv, 'value').classes('ml-8'):
                ui.number('Liter benötigt', format='%.0f').bind_value(config.experimente.fluessigstickstoff.anforderungen, 'liter_benoetigt')

        with ui.card().classes('w-full'):
            tornado_aktiv = ui.checkbox('Feuertornado').bind_value(config.experimente.feuertornado, 'aktiv')
            with ui.column().bind_visibility_from(tornado_aktiv, 'value').classes('ml-8'):
                ui.label('Bilder werden aus dem Medien-Ordner geladen.')


# --- ACTIONS / BUTTONS ---
ui.separator().classes('my-4')

with ui.row().classes('w-full justify-between'):
    
    def speichere_yaml():
        # JETZT erst schreiben wir das config-Objekt auf die Festplatte
        erfolg = utils.save_config(config, "config/show_config.yaml")
        if erfolg:
            ui.notify("Konfiguration in YAML gespeichert!", color="positive")
        else:
            ui.notify("Fehler beim Speichern.", color="negative")

    async def baue_pdf():
        ui.notify("Generiere LaTeX...", type="info")
        try:
            tex_pfad = generate.generiere_rider(config)
            ui.notify("Kompiliere PDF...", type="ongoing")
            
            # Auslagern des pdflatex-Befehls, damit die GUI nicht einfriert
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
            # 1. Wir müssen die .tex Datei frisch generieren, bevor wir sie zippen!
            tex_pfad = generate.generiere_rider(config)
            
            # 2. ZIP packen
            erfolg, nachricht = builder.create_overleaf_zip(tex_pfad)
            
            if erfolg:
                ui.notify(nachricht, color="positive")
                # Bietet die fertige ZIP direkt zum Download an
                ui.download("overleaf_upload.zip")
            else:
                ui.notify(nachricht, color="negative")
                
        except Exception as e:
            ui.notify(f"Fehler: {str(e)}", color="negative")

    with ui.row().classes('gap-4'):
        ui.button('Speichern (YAML)', on_click=speichere_yaml, color='secondary')
        ui.button('Overleaf ZIP', on_click=baue_zip, color='accent')
    ui.button('PDF Generieren & Downloaden', on_click=baue_pdf, color='primary').classes('font-bold')


ui.run(title="Stage Rider Builder", favicon="🎭")