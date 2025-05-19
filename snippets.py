columns = firstline.strip().split(",")
for value in parts:
    create_base = {}
    create_base[columns[parts.index(value)]] = value
    model.create(create_base)

df_test_original = df_so[["auto", "Nr_Adresse", "Datum"]].merge(
    df_link["Nr_fremd"],
    indicator=True,
    how="inner",
    left_on="auto",
    right_on="Nr_fremd"
)

df_conclusion = df_test_grouped_unique_auto[["auto", "Nr_Adresse", "Datum"]].rename(columns={"auto": "auto_left", "Nr_Adresse": "Nr_Adresse_left", "Datum": "Datum_left"}).merge(
    df_test_original_unique_auto[["auto", "Nr_Adresse", "Datum"]].rename(columns={"auto": "auto_right", "Nr_Adresse": "Nr_Adresse_right", "Datum": "Datum_right"}),
    indicator=True,
    how="left",
    left_on="auto_left",
    right_on="auto_right"
)

"""
Gruppierung df_so als neuer df, dessen Verknüpfung mit df_link, Eliminierung Duplikate von auto
Verknüpfung df_so mit df_link, Eliminierung Duplikate von auto
left merge gruppierter df mit df_so, jeweils als Versionen ohne Duplikate
_merge in allen Fällen both
-> alle auto-Werte des gruppierten df werden im original df gefunden, d.h. auto via first aggregieren scheint sinnvoll
-> Caveat: duplikatfreie Werte von auto sind im original df_so ein paar tausend mehr, d.h. die Gruppierung nach Kunde und ganzem Tag lässt Fälle aus, bei denen z.B. ein Kunde am gleichen Tag mehrmals kauft oder während eines Kaufs mehrere Aufträge erfasst werden
"""
