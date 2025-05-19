#import Excel files to DataFrames
#df_adr_start = pd.read_excel(input_path + excel_files["res_partner"], usecols=address_cols).query("Nr >= 0 and Branchenkennzeichen != 'Versicherung'")
#df_adr_full = df_adr_start.copy()
#df_countries = pd.read_excel(input_path + "Odoo_Laender.xlsx")
df_countries = pd.read_excel(input_path + "Zuweisung_Land.xlsx", sheet_name='Tabelle1')
df_states = pd.read_excel(input_path + "PLZ_BL_AT_DE.xlsx", usecols=["PLZ_ext", "state_id"])
df_branches = pd.read_excel(input_path + excel_files["res_partner_category"])
df_phone = pd.read_excel(input_path + excel_files["res_partner_phone"], usecols=phone_cols)
df_adr_full = pd.read_excel(input_path + excel_files["res_partner"], usecols=address_cols).query("Nr > 0 and Branchenkennzeichen != 'Versicherung'")
df_docs = pd.read_excel(input_path + excel_files["res_partner_prescriber"])
df_ins = pd.read_excel(input_path + excel_files["res_partner_insurer"], usecols=ins_cols)
df_prime_prescriber = pd.read_excel(input_path + excel_files["res_partner_patient_doctor"], usecols=prime_prescriber_cols).query("Kunde > 0").dropna(subset="Arzt")

#create preliminary import files
df_med_specialties = pd.DataFrame(df_adr_full["Kategorie"].dropna().astype(str).str.strip().loc[lambda x: (~x.isin(suppl_med_specialties)) & (x != "")].unique(), columns=["name"])
df_med_specialties.to_excel(output_path + "suppl_healthcare_medical_specialty.xlsx", index=False)
df_branches = pd.concat([df_branches, pd.DataFrame(df_adr_full["Branchenkennzeichen"].dropna().astype(str).str.strip().loc[lambda x: (~x.isin(df_branches["Text"])) & (x != "")].unique(), columns=["Text"])], ignore_index=True).rename(columns={"Text": "name"})
df_branches.to_excel(output_path + "res_partner_category.xlsx", index=False)

#sort by categories for patients last
cat_list = df_branches["name"].tolist()
cat_list.append(categories.pop(categories.index("Patient")))
df_adr_full["Branchenkennzeichen"] = pd.Categorical(df_adr_full["Branchenkennzeichen"].astype(str).str.strip(), categories=cat_list, ordered=True)
df_adr_full = df_adr_full.sort_values("Branchenkennzeichen")

#prepare dates
df_adr_full["GebDatum"] = pd.to_datetime(df_adr_full["GebDatum"], errors="coerce")
df_adr_full["verstorben_Datum"] = pd.to_datetime(df_adr_full["verstorben_Datum"], errors="coerce")
df_adr_full.loc[df_adr_full["GebDatum"].dt.year < 1900, "GebDatum"] = pd.NaT
df_adr_full.loc[df_adr_full["verstorben_Datum"].dt.year < 1900, "verstorben_Datum"] = pd.NaT

#prepare titles
df_adr_full["Anrede"] = df_adr_full["Anrede"].apply(lambda x: (re.sub(r"[^A-Za-z .\-\(\)]", "", x).strip() if isinstance(x, str) and len(x.strip()) > 1 else ""))
df_adr_full["Titel_hinten"] = df_adr_full["Titel_hinten"].apply(lambda x: (re.sub(r"[^A-Za-z .\-\(\)]", "", x).strip() if isinstance(x, str) and len(x.strip()) > 1 else ""))

#prepare social security number
df_adr_full["healthcare_social_security_number"] = df_adr_full.apply(build_sv_nr, axis=1)

#prepare healthcare_properties
df_adr_full["healthcare_prescriber"] = df_adr_full["Branchenkennzeichen"].isin(["Arzt", "Krankenhaus"])
df_adr_full["healthcare_is_care_home"] = df_adr_full["Branchenkennzeichen"] == "Altenheim"
df_adr_full["healthcare_customer"] = df_adr_full.apply(lambda row: True if row["Branchenkennzeichen"] in ["Patient"] or pd.notnull(row["healthcare_social_security_number"]) else False, axis=1)
df_adr_full["customer_rank"] = df_adr_full["healthcare_customer"].apply(lambda x: 1 if x == True else 0)
df_adr_full["supplier_rank"] = df_adr_full["Branchenkennzeichen"].apply(lambda x: 1 if x in ["Lieferant", "Grosshandel", "Kommissionslager", "DGKP"] else 0)

#prepare BMD debtor no
df_adr_full["bmd_debtor_account_number"] = df_adr_full.apply(lambda row: "2" + str(int(row["Nr"])).zfill(7) if row["Branchenkennzeichen"] == "Patient" else "", axis=1)

#prepare is_company
df_adr_full["is_company"] = ~df_adr_full["healthcare_customer"]

#prepare gender
df_adr_full["Geschlecht20"] = df_adr_full.apply(lambda row: gender_map.get(str(row["Geschlecht20"]).strip().lower(), "") if row["Branchenkennzeichen"] == "Patient" else "", axis=1)

#prepare vat
df_adr_full["UID"] = df_adr_full.apply(validate_and_clean_uid, axis=1)
df_adr_full["UID"] = df_adr_full["UID"].apply(lambda x: "" if x in ["ATU00000000", "I01338390212", "ATU00000000", "AT64995976", "ATU371780004", "CHE104766283", "CHE631457"] else x)

#prepare coutry and language
#df_adr_full["Land"] = df_adr_full["Land"].apply(unify_country_code)
df_countries["Laendername"] = df_countries["Laendername"].apply(lambda x: re.sub(r"^\?$", "", str(x)).strip())
df_countries = df_countries.drop_duplicates(subset="Laendercode_Sansoft")
df_states["PLZ_ext"] = df_states["PLZ_ext"].astype(int).astype(str)
df_adr_full = df_adr_full.merge(
    df_countries[["Laendercode_Sansoft", "Laendername"]],
    left_on=["Land"],
    right_on=["Laendercode_Sansoft"],
    how="left"
)
df_adr_full["lang"] = "en_GB"
df_adr_full.loc[df_adr_full["Laendername"].isin(["Österreich", "Deutschland", "Schweiz"]), "lang"] = "de_DE"
df_adr_full = df_adr_full.merge(
    df_states,
    left_on=["PLZ"],
    right_on=["PLZ_ext"],
    how="left"
)

#prepare healthcare contract number
df_docs_unique = df_docs.drop_duplicates(subset=merge_keys_docs).copy()
df_docs_unique["PLZ"] = df_docs_unique["PLZ"].fillna(0).astype(int).astype(str)
mask_doctor = df_adr_full["Branchenkennzeichen"].isin(["Arzt", "Krankenhaus"])
df_adr_full.loc[mask_doctor, "VPNR"] = df_adr_full[mask_doctor].merge(
    df_docs_unique[merge_keys_docs + ["VPNR"]],
    left_on=merge_keys_df_adr_full,
    right_on=merge_keys_docs,
    how="left"
)["VPNR"].values

#prepare primary prescriber connection
df_prime_prescriber = df_prime_prescriber.sort_values("Arzt").drop_duplicates("Kunde", keep="last")
map_kunde_arzt = df_prime_prescriber.set_index("Kunde")["Arzt"]
mask_patient = df_adr_full["Branchenkennzeichen"] == "Patient"
df_adr_full.loc[mask_patient, "healthcare_default_prescriber_id"] = df_adr_full.loc[mask_patient, "Nr"].map(map_kunde_arzt)

#prepare phone_no
df_phone["AdresseNr"] = df_phone["AdresseNr"].fillna(0).astype(int).astype(str)
df_phone = df_phone.drop_duplicates(subset=["AdresseNr"])
df_adr_full = df_adr_full.merge(
    df_phone[["AdresseNr", "Nummer"]],
    left_on=df_adr_full["Nr"].fillna(0).astype(int).astype(str),
    right_on=["AdresseNr"],
    how="left"
)

#prepare name
df_adr_full["Name2"] = df_adr_full["Name2"].apply(lambda x: (re.sub(r"^[-\.\*\?\+]+", "", str(x)).strip() if pd.notna(x) else x))
df_adr_full["name"] = df_adr_full.apply(generate_company_name, axis=1)
df_adr_full.loc[df_adr_full["is_company"] == True, ["Name", "Name2"]] = ""
    
#fill empty names
mask_name = (
    (df_adr_full["Name"].fillna("").str.strip().eq("")) &
    (df_adr_full["Name2"].fillna("").str.strip().eq("")) &
    (df_adr_full["is_company"].eq(False))
)
df_adr_full.loc[mask_name, "Name"] = "SUPPL_Anonym"

#prepare ref
df_adr_full["Nr"] = df_adr_full["Nr"].apply(lambda x: str(int(x)).zfill(6))

#prepare excess_prescribers
merged = df_docs.merge(
    df_adr_full["VPNR"],
    left_on=["VPNR"],
    right_on=["VPNR"],
    how='left',
    indicator=True
)
df_docs_excess = merged[merged["_merge"] == "left_only"].copy()
df_docs_excess['healthcare_prescriber'] = True
df_docs_excess['is_company'] = True
df_docs_excess['ref'] = "SUPPL_excess_prescriber"
df_docs_excess["lang"] = "de_DE"
df_docs_excess["country_id"] = "Österreich"
#df_docs_excess['akadGrad'] = df_docs_excess['akadGrad'].fillna("")
#df_docs_excess['Vorname'] = df_docs_excess['Vorname'].fillna("")
df_docs_excess["Zuname"] = df_docs_excess.apply(lambda row: ("SUPPL_Arztname_Unbekannt" if pd.isna(row["Zuname"]) and pd.isna(row["Vorname"]) and pd.isna(row["akadGrad"]) else row["Zuname"]), axis=1)
df_docs_excess["name"] = df_docs_excess[["akadGrad", "Vorname", "Zuname"]].apply(lambda row: " ".join([str(x).strip() for x in row if pd.notna(x) and str(x).strip() != ""]), axis=1)
df_docs_excess = df_docs_excess.merge(
    df_states,
    left_on=["PLZ"],
    right_on=["PLZ_Post"],
    how="left"
)

#prepare insurances
df_ins["KK_string"] = df_ins["Nr_VERSICHERUNGSTRAEGER"].apply(lambda x: str(int(x)).zfill(2) if pd.notnull(x) and x < 100 else pd.NA)
df_ins_codes = df_ins[~df_ins["KK_string"].isin(suppl_insurance_codes)].dropna(axis=0, subset=['KK_string']).drop_duplicates(subset=['KK_string'])
df_ins = df_ins_codes.copy()
df_ins["ref"] = df_ins["KrankenkassenNr"].apply(lambda x: "KK" + str(int(x)).zfill(5))
df_ins["healthcare_insurer"] = True
df_ins["is_company"] = True

#drop excess columns
df_adr_full = df_adr_full.drop(columns=["SozVersNr", "privat", "SVNr2", "Land", "Laendercode_Sansoft", "AdresseNr", "PLZ_ext"]).copy()
df_docs_excess = df_docs_excess.drop(columns=["Sortierkriterium", "_merge", "Zuname", "Vorname", "akadGrad", "PLZ_Post"]).copy()
#df_ins = df_ins.drop(columns=["KK_string"]).copy()

#rename columns
df_adr_full = df_adr_full.rename(columns=address_map)
df_docs_excess = df_docs_excess.rename(columns=doc_map)
df_ins_codes = df_ins_codes.rename(columns={"KK_string": "code", "Kurzbezeichnung": "name", "Krankenkasse": "description"})
df_ins = df_ins.rename(columns={"Kurzbezeichnung": "healthcare_svt_code_id", "Krankenkasse": "name"})

#export results
df_docs_excess.to_excel(output_path + "res_partner_prescriber(excess).xlsx", index=False)
df_ins_codes.to_excel(output_path + "suppl_healthcare_insurance_agency_code.xlsx", index=False)
df_ins.to_excel(output_path + "res_partner_insurance(excess).xlsx", index=False)
#df_adr_full.to_excel(output_path + "res_partner.xlsx", index=False)

#export large results in chunks
total_rows = len(df_adr_full)
if total_rows > chunk_size:
    for i in range(0, total_rows, chunk_size):
        chunk = df_adr_full.iloc[i:i + chunk_size]
        chunk.to_excel(output_path + f"res_partner_chunk_{i // chunk_size + 1}.xlsx", index=False)
else:
    df_adr_full.to_excel(output_path + "res_partner.xlsx", index=False)


