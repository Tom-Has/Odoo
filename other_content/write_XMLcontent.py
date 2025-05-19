for index, row in clean_df.iterrows():
    print('\t<ns1:Sonderausgaben Uebermittlungs_Typ="E">\n')
    print('\t\t<ns1:RefNr>' + str(int(row["EinzahlerID"])) + '</ns1:RefNr>\n')
    print('\t\t<ns1:Betrag>' + str(int(row["Gesamt\nSumme"])) + '</ns1:Betrag>\n')
    print('\t\t<ns1:vbPK>' + row["vbPK"] + '</ns1:vbPK>\n')
    print('\t</ns1:Sonderausgaben>\n')

base_df = pd.read_excel(path)

clean_df = base_df[
    (base_df["Gesamt\nSumme"] > 0) &
    (pd.isna(base_df["übermittelt"])) &
    (pd.notna(base_df["vbPK"]))
]