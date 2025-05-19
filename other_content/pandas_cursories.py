#general shape
shape_of_df = df.shape

#size
size_of_df = df.size

#total NaN proportion
df.isna().values.sum() / size_of_df * 100

#obtain column names
cols = df.columns.tolist()

#data characteristics
def analyse_df_characteristics(df):
    cols = df.columns.tolist()
    for col in cols:
        full_count = len(df[col])
        val_counts = df[col].map(type).value_counts()
        nan_count = df[col].isna().sum()
        empty_string_count = (df[col].astype(str).str.strip() == "").sum()
        
        print(f"\n--- Spalte: {col} ---")
        
        print(f"Leerwerte (NaN): {nan_count}")
        print(f"Leere Strings: {empty_string_count}")    

        print("Datentypen und deren Häufigkeit:")
        print(val_counts)

        # Gesamte Einzigartigkeit
        uniques_full = len(df[col].unique())
        uniques_non_null = len(df[col].dropna().unique())

        print(f"Gesamtzahl Werte: {full_count}")
        print(f"Einzigartige Werte (alle): {uniques_full} → {uniques_full / full_count * 100:.2f} %")
        print(f"Einzigartige Werte (ohne NaN): {uniques_non_null} → {uniques_non_null / full_count * 100:.2f} %")

        # Jetzt nach Typ aufteilen:
        for dtype, count in val_counts.items():
            typed_values = df[col][df[col].map(type) == dtype]
            uniques_type = len(typed_values.unique())
            print(f"- Typ {dtype.__name__}: {count} Werte, {uniques_type} einzigartig ({uniques_type / count * 100:.2f} %)")

#statistical parameters
#https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.describe.html
df['col'].describe()

#differentiate database ID vs. other ID (contract number, etc.)
length_of_ids = df['col'].dropna().astype(int).astype(str).str.strip().str.len()   #possibly relevant preparation
length_of_ids.describe()
df['Nr_Arzt'].astype(str).str.len().describe()
#df_adr_full["healthcare_contract_number"].dropna().astype(int).astype(str).str.len().describe()
#df_adr_full["healthcare_contract_number"].dropna().apply(lambda x: len(str(int(x))) if str(x).isdigit() else None).dropna().describe()

#explore duplicates
dupes = df[df.duplicated("col", keep=False)]

