#mapping preparation
supply_order_map = {
    #"auto": "client_order_ref",
    #"Datum": "date_order",
    #"Nr_Betreuer": "user_id"
}

supply_order_line_map = {
    #"Anz": "product_uom_qty,
    #"Positionsnummer": ,
    #"KK_Tarifbezeichnung": 
}

#column preparation
sale_order_cols = [
    #"Nr",
    #"Nr_Kassa",
    "Nr_Adresse",
    "Nr_Arzt",
    #"fortlfdNr",
    "Datum",
    #"Buchung_SB",
    #"Nr_Art",
    "Nr_Betreuer",
    "Anz",
    #"Nr_Artikel",
    #"Positionsnummer",
    #"KK_Tarifbezeichnung",
    "Preis",
    #"Umsatz_SB",
    #"mwstJN",
    #"MWST",
    #"Nr_KK",
    #"Nr_Filiale",
    #"Nr_Warengruppe",
    #"Netto",
    #"Artikelbrutto",
    #"KK_geprüft_am",
    #"KK_geprüft_durch",
    #"KK_Ausstellungsdatum",
    #"KK_bewilligt",
    #"KK_KundenUnterschrift",
    #"KK_Nr_Abrechnungsgruppe",
    #"KK_Info",
    #"KK_verbucht_am",
    #"Zusatztext",
    #"Kennzeichen",
    #"Storno",
    #"Nr_Behelfsgruppe",
    "auto",
    #"Nr_KK_Abrechnung",
    #"SBH_Rechnung",
    #"Nr_Wg",
    #"rehab",
    #"VO_Nummer",
    #"VOE",
    #"VOUebernahme_Datum",
    #"ausblenden",
    #"RG",
    #"BewNr",
    #"Beharrung",
    #"Nr_kk_ereignis",
    #"Nr_Vermittler",
    #"UnfallNummer",
    #"Rabatt",
    #"aufzahlung",
    #"UNDAT",
    #"Region",
    #"INKO_Ausnahme",
]

document_cols = [
    "Nr",
    #"Nr_Adresse",
    "Datum",
    "Bemerkung",
    "Text",
    #"Nr_Versorgung",
    "Dateiname"
]

sale_order_group_key = ["Nr_Adresse", "date_order"]
