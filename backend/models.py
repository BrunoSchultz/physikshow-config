from pydantic import BaseModel, Field
from typing import List, Optional

class Kontakt(BaseModel):
    name: str
    mail: str
    telefon: Optional[str] = None

class Metadaten(BaseModel):
    show_name: str 
    veranstaltungsort: str
    datum: str 
    sprache: str 
    kontakte: List[Kontakt] = []

# --- Module ---
class Module(BaseModel):
    experimente:bool
    technik: bool 
    unterkunft: bool 
    buehne: bool 
    anreise: bool 

# --- Buehne ---
class Buehne(BaseModel):
    tische: int
    stuehle: int 
    sonstiges: str = ""

# --- Anreise --
class Fahrzeuge(BaseModel):
    material_transporter: int = 0
    personen_transporter: int = 0

class Anreise(BaseModel):
    anreisetag: str
    ankunftszeit: str
    crew_groesse: int
    fahrzeuge: Fahrzeuge = Field(default_factory=Fahrzeuge) 
    sonstiges: str = ""

# --- Technik ---
class Licht(BaseModel):
    aktiv: bool = False
    lichtsteuerung_durch_crew: bool = False
    verdunkelung_noetig: bool = False
    spot: bool = False

class Ton(BaseModel):
    aktiv: bool = False
    anzahl_mikros: int = 0
    mischpult: bool = False

class Technik(BaseModel):
    crew: List[str] = []
    kontakte: List[Kontakt] = []
    bild: bool = False
    licht: Licht = Field(default_factory=Licht)
    ton: Ton = Field(default_factory=Ton)
    sonstiges: str = ""

# --- Experimente ---
class StickstoffAnforderungen(BaseModel):
    liter_benoetigt: int = 0

class Fluessigstickstoff(BaseModel):
    aktiv: bool = False
    anforderungen: StickstoffAnforderungen = Field(default_factory=StickstoffAnforderungen)

class Feuertornado(BaseModel):
    aktiv: bool = False
    bilder: List[str] = []

class Experimente(BaseModel):
    kontakte: List[Kontakt] = []
    # Every experiment gets its own slot.
    fluessigstickstoff: Fluessigstickstoff = Field(default_factory=Fluessigstickstoff)
    feuertornado: Feuertornado = Field(default_factory=Feuertornado)

# --- Config ---

class ShowConfig(BaseModel):
    metadaten: Metadaten
    module: Module 
    buehne: Buehne
    anreise: Anreise
    technik: Technik 
    experimente: Experimente