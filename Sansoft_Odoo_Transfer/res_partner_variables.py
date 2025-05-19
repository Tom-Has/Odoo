#mapping dict preparation
address_map = {
    "Nr": "ref",
    "Anrede": "suppl_academic_title_pre",
    "Titel_hinten": "suppl_academic_title_post",
    "Name": "lastname",
    "Name2": "firstname",
    "Strasse": "street",
    "PLZ": "zip",
    "Ort": "city",
    "Branchenkennzeichen": "category_id",
    "UID": "vat",
    "Kategorie": "healthcare_prescriber_specialty",
    "Bemerkung": "comment",
    "GebDatum": "suppl_day_of_birth",
    "verstorben_Datum": "suppl_day_of_death",
    "VPNR": "healthcare_contract_number",
    "Geschlecht20": "suppl_gender",
    "Laendername": "country_id",
    "Nummer": "phone"
}

gender_map = {
    "m": "male",
    "w": "female",
    "d": "other",
    "o": "open",
    "u": "diverse"
}

doc_map = {
    "VPNR": "healthcare_contract_number",
    "akadGrad": "suppl_academic_title_pre",
    "Zuname": "lastname",
    "Vorname": "firstname",
    "Adresse": "street",
    "PLZ": "zip",
    "Ort": "city"
}

#Excel read column preparation
address_cols = [
    "Nr",
	"Anrede",
	"Name",
	"Name2",
	"Strasse",
	"Land",
	"PLZ",
	"Ort",
	"Kategorie",
	"Branchenkennzeichen",
	"SozVersNr",
	"GebDatum",
	"privat",
	"SVNr2",
	"Geschlecht20",
	"verstorben_Datum",
	"Bemerkung",
	"UID",
	"Titel_hinten"
]
    
ins_cols = [
    "Nr_VERSICHERUNGSTRAEGER",
	"KrankenkassenNr",
	"Kurzbezeichnung",
	"Krankenkasse"
]
    
phone_cols = [
    "AdresseNr",
	"Nummer"
]

prime_prescriber_cols = [
    "Kunde",
    "Arzt"
]

#merge key columns
merge_keys_df_adr_full = [
    "Anrede",
	"Name",
	"Name2",
	"Strasse",
	"PLZ",
	"Ort"
]

merge_keys_docs = [
    "akadGrad",
	"Zuname",
	"Vorname",
	"Adresse",
	"PLZ",
	"Ort"
]

#constant data columns
suppl_med_specialties = [
	'Allgemeinmedizin',
	'Chirurgie',
	'DGKP',
	'Dermatologie',
	'FA Haut- und Geschlechtskrankheiten',
	'Facharzt für physikalische Medizin',
	'Gynäkologie',
	'Internist',
	'Kardiologie',
	'Kinder- und Jugendheilkunde',
	'Lungenheilkunde',
	'Neurologie',
	'Orthopädie und Traumatologie',
	'Orthopädie und Unfallchirurgie',
	'Orthopädie und orthopädische Chirurgie',
	'Unfall- und Handchirurgie',
	'Urologie'
]

suppl_insurance_codes = [
    "03",
	"05",
	"07",
	"08",
	"09",
	"1A",
	"4B",
	"5A",
	"4C",
	"4A",
	"4D",
	"7A",
	"4E",
	"8B",
	"8C",
	"8D",
	"6A",
	"4F",
	"40",
	"50",
	"13",
	"16",
	"12",
	"14",
	"17",
	"15",
	"18",
	"19",
	"11"
]
