#!/usr/bin/env python3
"""
Classify OxREP shipwrecks into Mediterranean sub-regions using Country, Region,
and Name fields. The Excel export is missing Country for ~860 wrecks, but their
names are identifiable Mediterranean locations.
"""

import pandas as pd
import numpy as np
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

# Known Adriatic place names (Croatian/Montenegrin/Albanian coast, east Italian Adriatic)
ADRIATIC_NAMES = {
    "Baska", "Cavtat", "Cikat", "Ciovo", "Gospa Prizidnica", "Grscica",
    "Ist", "Istria", "Karatunic", "Korcula", "Kornat", "Kurba Vela",
    "Losinj", "Mala Jana", "Mararska", "Molat", "Morovnik", "Murter",
    "Omisalj", "Opat", "Ovrat", "Peljesac", "Povile", "Prasso",
    "Risan", "Rovinj", "Savudrija", "Stanci-Celina", "Susak", "Zapuntel",
    "Zdrijac", "Zirje", "Zut", "Punta Glavina", "Punta Cera",
    "Kornat", "Pag area",
}

ADRIATIC_PREFIXES = [
    "Lastovo", "Mljet", "Nin ", "Olib ", "Vis ", "Premuda", "Pernat",
    "Silba", "Skarda", "Zaton", "Sćedro", "Palagruza",
]

# Known Black Sea place names
BLACK_SEA_NAMES = {
    "Callatis", "Donuzlav", "Soldaya", "Tsikhisdziri",
    "Tcerny Nos", "Varna", "Varvara",
}

BLACK_SEA_PREFIXES = ["Neseber", "Pomorje", "Sozopol"]

# Known Eastern Med: Turkey
TURKEY_NAMES = {
    "Ayitasi Burnu", "Delphinion", "Erdek", "Fethiye", "Gumusluk",
    "Halkoz Adasi", "Hayirsiz Ada", "Iassos", "Kas",
    "Kerme Gulf", "Kotu Burun", "Marmaris", "Sheytan Deresi",
    "Tekmezar Burnu roof tiles", "Tenedos", "Turkey",
}

TURKEY_PREFIXES = [
    "Datca", "Cape Gelidonya", "Iskandil Burnu", "Karaca Adasi",
    "Knidos", "Mandalya Gulf", "Ulu Burun", "Çökertme",
]

# Known Eastern Med: Greece
GREECE_NAMES = {
    "Ayios Ioannis Theologos", "Camirus", "Gaidouromandhra", "Gavrion",
    "Haghiokambos", "Kallithea", "Kastellorizon", "Kavo Vodi", "Kimi",
    "Kimolos", "Kynosoura", "Lemnos", "Methone", "Pelagos", "Pefkos",
    "Philadelphia", "Plitharia", "Poros", "Rhamnous", "Rhodos",
    "Sithonia", "Skopelos", "Tainaron", "Thalassinies Spilies",
}

GREECE_PREFIXES = [
    "Dhia", "Komi ", "Lindos", "Navplion", "Sporades", "Thasos",
    "Voula", "Zakynthos", "Cape Sidero", "Piraeus",
]

# Known Eastern Med: Levant (Israel, Syria, Lebanon)
LEVANT_NAMES = {
    "Ashkelon", "Ashkelon North Byzantine", "Ginosar", "Hishuley Carmel",
    "Israel", "Mikhmoret", "Minat Mishrafa", "Sdot Yam D",
    "Sedot Yam", "Shave Ziyyon", "Syria", "Tartus",
}

LEVANT_PREFIXES = [
    "Arwad", "Caesarea", "Hahotrim", "Hof Hacarmel", "Kefar Shamir",
    "Megadim", "Newe Yam", "Tyre",
]

# Known Eastern Med: Cyprus
CYPRUS_PREFIXES = ["Cape Andreas", "Cape Kiti"]

# Known Western Med: North Africa
N_AFRICA_NAMES = {
    "Baia di Gadir", "Cap Magroua", "Cap Spartel", "Mangub",
    "Marsa Lucch", "Ras Achakkar", "Ras El Basit", "Zembretta",
}

N_AFRICA_PREFIXES = ["Cap Bon", "Cap de Garde", "Cherchel", "Raf Raf", "Tanger"]

# Known Western Med: Spain
SPAIN_NAMES = {
    "Barbate", "Ben-Afeli", "Benicarlo", "Binasafuller", "Castillo",
    "Columbretes", "Denia", "Escombreras", "Formentera",
    "Freu d'en Valento", "Huelva", "Isla Pedrosa", "Mahon", "Majorca",
    "Masa d'Or", "Miramar", "Palamos", "Percheles", "Piedra Negra",
    "Roquetas del Mar", "Sa Nau Perdudo", "Sa Tuna", "Sagunt",
    "Salou", "San Ferreol", "Sancti Petri", "Sant Antoni", "Tagomago",
    "Tarragona", "Valencia",
}

SPAIN_PREFIXES = [
    "Bajo de", "Cabo de Gata", "Cabrera", "Cadiz", "Cal Cativa",
    "Callela", "Cap de Creus", "Cap Negret", "Cap del Vol",
    "Cartagena", "Colonia de Sant Jordi", "Cueva del Jarro", "Culip",
    "Dragonera", "Dunas del Pinatar", "El Golfet", "El Hornillo",
    "El Sec", "El Toro", "Els Reis", "Guardias Viejas", "Guardis",
    "La Almadraba", "La Malvarrosa", "La Marisma", "Las Amoladeras",
    "Las Encombreras", "Las Hormigas", "Las Marinas", "Las Puntas",
    "Les Medes", "Les Roquetes", "Les Salines", "Les Sorres",
    "Los Escolletes", "Los Esculls", "Los Espines", "Medas",
    "Pudrimel", "Puebla del Rio", "Punta Blanca", "Punta Entina",
    "Punta Javana", "Punta Prima", "Punta de Algas", "Punta de la Mona",
    "Punta del Vapor", "Redona", "Torre Derribada", "Torre La Sal",
    "Porto Christo",
]

# Known Western Med: France (incl. Corsica)
FRANCE_NAMES = {
    "Bandol", "Boulouris", "Bregancon", "Brescou", "Briande",
    "Carqueiranne", "Cassis", "Corsica", "Frontignan",
    "Jarre", "Lazaret", "Nice", "Niolon", "Ratonneau", "Rochelongue",
    "Sausset", "Sete", "Villefranche", "Villepey",
}

FRANCE_PREFIXES = [
    "Arles", "Baie de", "Balise du Pretre", "Bon-Porte", "Bon -Porte",
    "Calanque du", "Calvi", "Cap Bear", "Cap Benat", "Cap Camarat",
    "Cap Couronne", "Cap Croisette", "Cap Gros", "Cap Leucate",
    "Cap Roux", "Cap Sicie", "Cap Taillat", "Cap d'Antibes",
    "Carro ", "Cavaliere", "Cavallo", "Caveaux", "Esteu dou Mieu",
    "Fos ", "Giens", "Grand Bassin", "Grand Grenille",
    "Ilot Barthelemy", "L'Esquillade", "L'Esterel",
    "La Basse du", "La Fourmigue", "La Garoupe", "La Jaumegarde",
    "La Luque", "La Madrague", "La Roche Fouras",
    "Lavezzi", "Le Dattier", "Le Grand Avis", "Le Grand Congloué",
    "Le Grand Radeau", "Le Grand Ribaud", "Le Gros Mur",
    "Le Lion de Mer", "Le Petit Rhone", "Le Titan",
    "Les Catalans", "Les Embiez", "Les Magnons", "Les Negres",
    "Lindons", "Maire ", "Marseillan", "Marseille",
    "Mateille", "Monaco ", "Mont Rose", "Mounine", "Nord-Camarat",
    "Nord-Levant", "Ouest de Plane", "Pierres Plates",
    "Plane ", "Planier", "Pointe Bacon", "Pointe Debie",
    "Pointe Grenier", "Pointe Moussure", "Pointe Pomegues",
    "Pointe de la Galere", "Pointe du Ble", "Pointe du Brouil",
    "Pomegues", "Port-de-Bouc", "Port-la-Nouvelle",
    "Riou ", "Saint Gervais", "Saint Hospice", "Saint Tropez",
    "Sainte Marguerite", "Scole B", "Secanion", "Sud-Camarat",
    "Sud-Perduto", "Toulon", "Tour Sainte Marie",
    "Grazel",
]

# Known Western Med: Italy (non-Adriatic)
ITALY_NAMES = {
    "Ardenza", "Arenella", "Argentario", "Basiluzzo", "Borgo Caprile",
    "Brida Marina", "Capel Rosso", "Caprera", "Cattolica", "Cavoli",
    "Cecina", "Cervia", "Cervo", "Chia", "Cirella di Diamante",
    "Civitavecchia", "Corte Cavanella", "Dattilo", "Domu de S'Orku",
    "Empoli", "Fano", "Filicudi Porto", "Galbucina", "Galli",
    "Gallinaria", "Gandolfo", "Gavetti", "Genoa", "Gravisca",
    "Imperia", "Is Arenas", "Is Mortorius", "Isola Rossa",
    "Isola delle Femmine", "La Ciaccia", "La Frasca",
    "La Macchi Tonda", "La Paolina", "Lago di Monate",
    "Le Murelle", "Logonovo", "Maddalena", "Maestro-Maria",
    "Malamocco", "Maraone", "Margarida", "Marina Porto", "Marritza",
    "Milazzo", "Mola", "Molara", "Monfalcone", "Naregno",
    "Nicotera", "Noce, Fiume", "Nora", "Oristano", "Osellucia",
    "Ostia", "Ostuni", "Palese", "Palinuro", "Palizi Marina",
    "Panarelli", "Pegli", "Pesaro", "Populonia",
    "Posillipo", "Praiano", "Procida", "Pomposa",
    "Pontelagoscuro", "Portomaggiore", "Salerno",
    "San Bartolomeo", "San Nicola", "San Vito",
    "Santa Cesarea", "Santa Severa", "Santo Ianni", "Sardinia",
    "Sciacca", "Scoglietto", "Scoglitti", "Scopello",
    "Sulcis", "Terracina", "Teulada", "Trapani",
    "Varazze", "Vendicari", "Vieste", "Vignale", "Vulcano", "Zanca",
}

ITALY_PREFIXES = [
    "Averno", "Bacoli", "Baratti", "Bari", "Brindisi", "Cabras",
    "Cagliari", "Cala Bona", "Cala Cupa", "Cala Gadir", "Cala Grande",
    "Cala Levante", "Cala Mindola", "Cala Portalo", "Cala Scirocco",
    "Cala Ustina", "Cala Vellana", "Cala del Piccione",
    "Cala di Li Francesi", "Camarina", "Capo Ali", "Capo Bellavista",
    "Capo Carbonara", "Capo Colonna", "Capo Enfola", "Capo Ferrato",
    "Capo Granitola", "Capo Graziano", "Capo Mele", "Capo Passero",
    "Capo Plaia", "Capo Rasocolmo", "Capo Rizzuto",
    "Capo San", "Capo Sant", "Capo Testa", "Capo Vite",
    "Capo Zafferano", "Capo della Frasca", "Capo di Muro",
    "Capraia", "Castellammare", "Castellare", "Castelsardo",
    "Circeo", "Coltellazzo", "Eloro", "Fiumicino", "Fontanamare",
    "Giglio", "Golfo della Stella", "Golo", "Gorgona",
    "Lampedusa", "Lampione", "Le Formiche di Grosseto",
    "Marsala", "Marzamemi", "Montecristo", "Nemi",
    "Ognina", "Olbia", "Palazzo di Stella", "Panarea",
    "Pantelleria", "Pian di Spille", "Pianosa", "Pignato di Fuori",
    "Plemmirio", "Pomonte", "Ponte d'Oro", "Ponza",
    "Porto Azzurro", "Porto Badisco", "Porto Cesareo", "Porto Ercole",
    "Porto Longo", "Porto Paglia", "Porto Palo", "Porto Pistis",
    "Porto Santo Stefano", "Porto Venere", "Portolafia",
    "Punta Altarella", "Punta Chiappa", "Punta Crapazza",
    "Punta Falcon", "Punta Lazzaretto", "Punta Leona",
    "Punta Nera", "Punta Palom", "Punta Patedda", "Punta Penne",
    "Punta Perla", "Punta Polveraia", "Punta Pozzolana",
    "Punta Raisi", "Punta Salina", "Punta Sardegna",
    "Punta Scario", "Punta Scifo", "Punta Secca", "Punta Sottile",
    "Punta Stilo", "Punta dei Mangani", "Punta dei Ripalti",
    "Punta del Fenaio", "Punta del Morto", "Punta dell'Arco",
    "Punta della Contessa", "Punta della Madonna",
    "Punta di San Francesco", "Punta le Tombe",
    "Rocca di San Nicola", "San Vincenzo", "Sant'Antioco",
    "Saturo", "Scialandro", "Scoglio Businco", "Scoglio della Formica",
    "Secca del", "Secche Di Ugento", "Sinuessa", "Siracusa",
    "Taranto", "Taravo", "Terrasini", "Torre Castellucia",
    "Torre Flavia", "Torre San Gennaro", "Torre Testa",
    "Torre Valdaliga", "Torre dell'Orso", "Torre dell'Ovo",
    "Triscina", "Ustica", "Vachetta", "Vada ", "Valle Isola",
    "Ventotene", "Comino",
]

# Malta -> western_med
MALTA_NAMES = {
    "Filfla", "Malta", "Mellieha", "Munxar", "Qawra",
    "Saint George's Bay", "Saint Paul's Bay",
}
MALTA_PREFIXES = ["Xlendi", "Imera"]

# Misc unclassifiable
OTHER_NAMES = {"Mediterranean", "Sicilian Channel", "Graham Bank", "Perduto", "Corbella", "Pa"}


def classify_by_name(name: str) -> str:
    if pd.isna(name):
        return "unclassified"

    n = str(name).strip()

    if n in OTHER_NAMES:
        return "unclassified"

    # Black Sea
    if n in BLACK_SEA_NAMES:
        return "black_sea"
    for p in BLACK_SEA_PREFIXES:
        if n.startswith(p):
            return "black_sea"

    # Adriatic
    if n in ADRIATIC_NAMES:
        return "adriatic"
    for p in ADRIATIC_PREFIXES:
        if n.startswith(p):
            return "adriatic"

    # Eastern Med: Turkey
    if n in TURKEY_NAMES:
        return "eastern_med"
    for p in TURKEY_PREFIXES:
        if n.startswith(p):
            return "eastern_med"

    # Eastern Med: Greece
    if n in GREECE_NAMES:
        return "eastern_med"
    for p in GREECE_PREFIXES:
        if n.startswith(p):
            return "eastern_med"

    # Eastern Med: Levant
    if n in LEVANT_NAMES:
        return "eastern_med"
    for p in LEVANT_PREFIXES:
        if n.startswith(p):
            return "eastern_med"

    # Eastern Med: Cyprus
    for p in CYPRUS_PREFIXES:
        if n.startswith(p):
            return "eastern_med"

    # Western Med: N. Africa
    if n in N_AFRICA_NAMES:
        return "western_med"
    for p in N_AFRICA_PREFIXES:
        if n.startswith(p):
            return "western_med"

    # Western Med: Spain
    if n in SPAIN_NAMES:
        return "western_med"
    for p in SPAIN_PREFIXES:
        if n.startswith(p):
            return "western_med"

    # Western Med: France
    if n in FRANCE_NAMES:
        return "western_med"
    for p in FRANCE_PREFIXES:
        if n.startswith(p):
            return "western_med"

    # Western Med: Italy
    if n in ITALY_NAMES:
        return "western_med"
    for p in ITALY_PREFIXES:
        if n.startswith(p):
            return "western_med"

    # Malta
    if n in MALTA_NAMES:
        return "western_med"
    for p in MALTA_PREFIXES:
        if n.startswith(p):
            return "western_med"

    return "unclassified"


def classify_wreck(row: pd.Series) -> str:
    """Classify using Country first, then Region, then Name."""
    country = row.get("country", "")
    sea_area = row.get("sea_area", "")
    region_db = row.get("region_db", "")
    name = row.get("name", "")

    if pd.isna(country):
        country = ""
    if pd.isna(sea_area):
        sea_area = ""
    if pd.isna(region_db):
        region_db = ""

    country = str(country).strip()
    sea_area = str(sea_area).strip()
    region_db = str(region_db).strip()

    # --- Priority 1: Country ---
    if country:
        if "Black Sea" in sea_area:
            return "black_sea"
        if country in ("Bulgaria", "Romania"):
            return "black_sea"
        if country in ("Croatia", "Albania", "Montenegro") or "Adriatic" in sea_area:
            return "adriatic"
        if country == "Italy" and "Adriatic" in sea_area:
            return "adriatic"
        if country in ("Britain", "United Kingdom", "UK", "Belgium", "Netherlands"):
            return "atlantic"
        if country == "France" and any(x in sea_area for x in ("Atlantic", "Channel")):
            return "atlantic"
        if country in ("Spain", "France", "Minorca", "Malta", "Tunisia", "Algeria",
                        "Morocco", "Libya"):
            return "western_med"
        if country in ("Italy", "Italy - Sicily"):
            return "western_med"
        if country in ("Greece", "Turkey", "Cyprus", "Syria", "Lebanon", "Israel",
                        "Egypt", "Sudan"):
            return "eastern_med"
        if country in ("ZZ-Non-Mediterranean", "India"):
            return "other"
        if country == "International waters":
            return "unclassified"

    # --- Priority 2: Region (subnational) ---
    if region_db:
        french_regions = {"Bouches-du-Rhône", "Var", "Languedoc-Roussillon",
                         "Alpes-Maritimes", "Corsica", "Bouches-du Rhône",
                         "Languedoc-Rousillon"}
        italian_west = {"Sicily", "Sardinia", "Tuscany", "Campania", "Calabria",
                       "Liguria", "Lazio", "Latium", "Elba, Tuscany",
                       "Southern Sicily", "North east Sicily", "Western Sicily",
                       "Bay of Naples", "Capri", "Capri, Campania",
                       "Capraia Island, Liguria", "Golfo dell'Asinara, N Sardinia",
                       "Veneto", "Between Sicily, Sardinia and Tunisia",
                       "Between Sicily and Carthage"}
        italian_adriatic = {"Puglia", "Brindisi", "Marche",
                           "South east of Taranto, Puglia"}
        adriatic_regions = {"central Dalmatia", "southern Dalmatia",
                           "northern Dalmatia", "west side of Istria", "Kvarner",
                           "Mljet island", "Lastovo Island", "Mjlet Island"}
        turkey_regions = {"Marmaris Peninsula", "Marmara", "Marmara islands",
                         "North of Bodrum", "Northern Turkey", "Antalya",
                         "Western tip of Datça Peninsula",
                         "South west of Marmaris", "East of Bodrum",
                         "between Turkish mainland and Kos"}
        greece_regions = {"Chios", "Paros, Cyclades", "Argolic Gulf",
                         "Astypalaea, Dodecanese", "Laconia",
                         "Kalymnos, Dodecanese", "South west Messinia, Peloponnese",
                         "Rhodes", "Between Ithaki and Cephalonia", "Lesbos",
                         "Euboia", "Kyra-Panagia Island, Northern Sporades",
                         "Argolid", "Attica",
                         "Off southern tip of Peloponnese",
                         "In the harbour of Apollonia"}
        israel_regions = {"Dor", "Gaza", "On the south side of Tyre",
                         "north of Akko", "West coast", "South coast"}
        spain_regions = {"Majorca", "Minorca", "Catalonia", "Cartagena",
                        "near Cartagena"}
        nafr_regions = {"Gulf of Sirte"}

        if region_db in french_regions:
            return "western_med"
        if region_db in italian_west:
            return "western_med"
        if region_db in italian_adriatic:
            return "adriatic"
        if region_db in adriatic_regions:
            return "adriatic"
        if region_db in turkey_regions:
            return "eastern_med"
        if region_db in greece_regions:
            return "eastern_med"
        if region_db in israel_regions:
            return "eastern_med"
        if region_db in spain_regions:
            return "western_med"
        if region_db in nafr_regions:
            return "western_med"

    # --- Priority 3: Name-based classification ---
    result = classify_by_name(name)
    if result != "unclassified":
        return result

    return "unclassified"


def main():
    df = pd.read_csv(PROCESSED_DIR / "shipwrecks_clean.csv")
    print(f"Total wrecks: {len(df)}")
    print(f"Currently classified: {(df.region != 'other').sum()}")

    df["region"] = df.apply(classify_wreck, axis=1)

    print(f"\nAfter reclassification:")
    print(df.region.value_counts())
    print(f"\nUnclassified: {(df.region == 'unclassified').sum()}")

    unclassified = df[df.region == "unclassified"]
    if len(unclassified) > 0:
        print(f"\nUnclassified wreck names:")
        for _, row in unclassified.iterrows():
            print(f"  {row['name']} (country={row.get('country')}, region_db={row.get('region_db')})")

    df.to_csv(PROCESSED_DIR / "shipwrecks_clean.csv", index=False)
    print(f"\nSaved updated shipwrecks_clean.csv")

    # Now re-run the binning with updated regions
    from ingest_shipwrecks import apply_equal_probability_dating, BIN_START_YEAR, BIN_END_YEAR

    df_dated = df[
        df["date_start"].notna()
        & df["date_end"].notna()
        & (df["date_start"] <= df["date_end"])
    ].copy()

    binned_50 = apply_equal_probability_dating(df_dated, 50)
    binned_25 = apply_equal_probability_dating(df_dated, 25)

    binned_50.to_csv(PROCESSED_DIR / "shipwrecks_binned_50yr.csv", index=False)
    binned_25.to_csv(PROCESSED_DIR / "shipwrecks_binned_25yr.csv", index=False)
    print("Updated binned CSVs")

    # Print regional totals for sanity check
    print("\n50yr bin regional totals:")
    for col in ["total_count", "western_med", "eastern_med", "adriatic", "black_sea", "atlantic"]:
        print(f"  {col}: {binned_50[col].sum():.1f}")
    unclassified_total = binned_50.total_count.sum() - sum(
        binned_50[c].sum() for c in ["western_med", "eastern_med", "adriatic", "black_sea", "atlantic"]
    )
    print(f"  unclassified: {unclassified_total:.1f}")


if __name__ == "__main__":
    main()
