df = pd.read_excel('C:\\Users\ThomasHabenschuss\Documents\Datenimports\Schaper\Datenbank20250303\ADRESSEN.xlsx')
df = pd.read_excel('C:\\Users\ThomasHabenschuss\Documents\Datenimports\Schaper\Datenbank20250303\ADRESSEN.xlsx').loc[lambda df: df['Nr'] > 0]
df = pd.read_excel('C:\\Users\ThomasHabenschuss\Documents\Datenimports\Schaper\Datenbank20250303\ADRESSEN.xlsx', usecols=address_cols).query("Nr > 0")

df_doc_patient_connector = pd.read_excel(input_path + excel_files["res_partner_patient_doctor"]).query("Kunde > 0")
df_patients_odoo = pd.read_excel()
df_doctor_map = df_doc_patient_connector.groupby("Kunde")["Arzt"].max().reset_index()
df_patients_odoo = df_patients_odoo.merge(df_doctor_map, how="left", left_on="external_id", right_on="Kunde")

count = 0
temp=iter(grouped_df)
while count <= 10:
   count, frame = next(temp)
   print(frame["Name", "Name2", "Branchenkennzeichen"])

grouped_df = df[
    (df['Branchenkennzeichen'] != "Patient") &
    (df['Branchenkennzeichen'] != "Versicherung") &
    (df["privat"] != "False")
].groupby(by=['Name', 'Branchenkennzeichen'])



str(math.floor(df.at[10000, "SozVersNr"])) + df.at[10000, "GebDatum"].strftime("%d") + df.at[10000, "GebDatum"].strftime("%m") + df.at[10000, "GebDatum"].strftime("%y")


df_patient = df[df['Branchenkennzeichen'].isin(["Patient", "Zustelladresse"])]
df_patient["GebDatum"] = pd.to_datetime(df["GebDatum"], errors="coerce")
df_patient = df[
    df["GebDatum"].notnull() &
    df["SozVersNr"].apply(lambda x: pd.notnull(x) and len(str(int(x))) in [3, 4])
].copy()
df_patient["SV_Nr"] = df_patient.apply(
    lambda row: (
        ("0" + str(int(row["SozVersNr"]))) if len(str(int(row["SozVersNr"]))) == 3
        else str(int(row["SozVersNr"]))
    ) +
    f"{row['GebDatum'].day:02d}{row['GebDatum'].month:02d}{row['GebDatum'].year % 100:02d}",
    axis=1
)

#grouped_patient = df[df['Branchenkennzeichen'].isin(["Patient", "Zustelladresse"])].groupby(by=['Name', 'Name2'])
grouped_patient = df_patient.groupby(by=["SV_Nr"])

patient_group = df[df['category_id'].isin(["Patient", "Zustelladresse"])].groupby(by=["healthcare_social_security_number"])

for name, group in patient_group:
    if (group["category_id"] == "Zustelladresse").any() and (group["category_id"] == "Patient").any():
        #print(f"\nName: {name}")
        print(group[["firstname", "lastname", "category_id", "healthcare_social_security_number"]])

df_country_code["Land"] = df_country_code_single["Land"].apply(
    lambda x: "AT" if x == "A" else
              "DE" if x == "D" else
              "CH" if x == "C" else
              "IT" if x == "I" else
              "ES" if x == "E" else
              "JP" if x == "J" else
              "BE" if x == "B" else
              "FR" if x == "F" else
              "HU" if x == "G" else
              "HU" if x == "H" else
              "GB" if x == "K" else
              "HU" if x == "H" else
              "LU" if x == "L" else
              "MT" if x == "M" else
              "NO" if x == "N" else
              "PO" if x == "P" else
              "RO" if x == "R" else
              "SE" if x == "S" else
              "TH" if x == "T" else
              "HU" if x == "U" else
              x
)

def check_column_types(df, columns=None, sample_rows=5):
    """
    Zeigt pro Spalte die enthaltenen Typen und Beispielwerte.
    
    Args:
        df: Der DataFrame.
        columns: Liste von Spalten, falls nur bestimmte geprüft werden sollen.
        sample_rows: Anzahl Beispielwerte pro Spalte.
    """
    cols = columns if columns else df.columns
    report = {}

    for col in cols:
        col_data = df[col]
        types = col_data.map(type).value_counts()
        samples = col_data.dropna().unique()[:sample_rows]
        report[col] = {
            "dtype": col_data.dtype,
            "value_types": types.to_dict(),
            "sample_values": list(samples)
        }

    return report

def print_wrong_uid(row):
    original_uid = str(row.get("UID", "")).strip()
    name = str(row.get("Name", "")).strip()
    name2 = str(row.get("Name2", "")).strip()
    ref = str(int(row.get("Nr", ""))).strip().zfill(6)
    cleaned_uid = re.sub(r"[^A-Z0-9]", "", original_uid.upper())
    
    if cleaned_uid == "NAN" or cleaned_uid == "":
        return ""
    
    if not re.fullmatch(r"^[A-Z]{2}[A-Z0-9]{6,12}$", cleaned_uid):
        print(ref + " / " + name + " " + name2 + " / " + cleaned_uid)
        return ""

    if re.search(r"(\d)\1{5}", cleaned_uid):
        print(ref + " / " + name + " " + name2 + " / " + cleaned_uid)
        return ""

    return cleaned_uid
