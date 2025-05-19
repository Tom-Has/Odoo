#mapping preparation
product_map = {
    "Artikelnummer": "default_code",
	"Bezeichnung": "name",
	"Preis": "list_price",
	"MWST": "taxes_id",
	#"Positionsnummer2": "suppl_healthcare_tariff_number_ids",
    "Verkaufsinfo": "description_sale",
	"Zusatzinfo": "description",
	"Verpackungsbezeichnung": "uom_id",
	"BestVerpBezeichnung": "uom_po_id",
	"Nr_Warengruppe": "categ_id",
	"SNEingabe": "rent_ok"
}

supplier_price_map = {
    "Beschaffungszeit": "delay",
    "Bestellnummer": "product_code",
    #"EK": "price",
	#"RA": "discount"
}

#column preparation
product_cols = [
    "Nr",
    "Artikelnummer",
	"Bestellnummer",
	"Bezeichnung",
	"Preis",
	"MWST",
	"Positionsnummer2",
    "Verkaufsinfo",
	"Zusatzinfo",
	"Verpackungsbezeichnung",
	"BestVerpBezeichnung",
	"Nr_Lieferant",
	"Nr_Warengruppe",
	"EK",
	"RA",
	"SNEingabe",
	"Beschaffungszeit",
    "Status",
    "Best_EAN",
    "alterEANCode"
]

tarif_cols = [
    "Nr",
    "Nr_Artikel",
    "Nr_KK",
    "Positionsnummer",
    "Tarifpreis",
    "Aufpreis_at",
    "Rehab",
    "RG"
]

supplier_price_cols = [
    "Nr_Lieferant",
    "Beschaffungszeit",
    "Bestellnummer",
    "Nr"
    #"EK",
	#"RA"
]

