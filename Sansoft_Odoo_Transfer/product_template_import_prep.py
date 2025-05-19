#import product file to DataFrames
df_product = pd.read_excel(input_path + excel_files["product_templates"], usecols=product_cols).query("Nr > 0 and Status == 3")

#category procedure
df_parent_cat = pd.read_excel(input_path + excel_files["product_parent_cat"])
df_child_cat = pd.read_excel(input_path + excel_files["product_sub_cat"])
df_child_cat = df_child_cat.merge(
    df_parent_cat,
    how="left",
    left_on=["Nr_Geschäftsbereich"],
    right_on=["Nr"]
)
df_child_cat = df_child_cat.rename(columns={"Text_x": "pos_categ_ids", "Text_y": "parent_id", "Nr_x": "cat_nr"})
df_child_cat[["name", "parent_id"]].to_excel(output_path + "product_category.xlsx", index=False)
df_child_cat["categ_id"] = df_child_cat.apply(lambda row: " / ".join([cat.strip() for cat in [row["parent_id"], row["pos_categ_ids"]]]), axis=1)

#uom procedure
df_uom = pd.concat([
    df_product[["Verpackungsbezeichnung"]].rename(columns={"Verpackungsbezeichnung": "name"}),
    df_product[["BestVerpBezeichnung"]].rename(columns={"BestVerpBezeichnung": "name"})
]).dropna().drop_duplicates().reset_index(drop=True)
df_uom = df_uom[df_uom["name"].astype(str).str.strip() != ""]
df_uom["category_id"] = "Orthopädie-Einheit"
df_uom.to_excel(output_path + "product_uom.xlsx", index=False)

#tarif procedure
df_tarif = pd.read_excel(input_path + excel_files["suppl_healthcare_tarifs"], usecols=tarif_cols)
df_group = df_tarif["Positionsnummer"].dropna().astype(str).apply(lambda x: x[:5]).drop_duplicates()
df_tarifinfo = df_tarif.drop_duplicates(subset=["key1", "key2", "key3"])

#product procedure
df_product["Bezeichnung"] = df_product["Bezeichnung"].fillna("SUPPL_ohne_Bezeichnung")
for col in ["Verpackungsbezeichnung", "BestVerpBezeichnung"]:
    df_product[col] = df_product[col].apply(
        lambda x: "Stück" if pd.isna(x) or str(x).strip() == "" else x
    )
df_product["sale_ok"] = True
df_product["purchase_ok"] = True
df_product["available_in_pos"] = True
df_product["detailed_type"] = 'product'
df_product["invoice_policy"] = 'order'
df_product = df_product.merge(
    df_child_cat[["cat_nr", "pos_categ_ids", "categ_id"]].drop_duplicates(),
    left_on=["Nr_Warengruppe"],
    right_on=["cat_nr"],
    how="left"
)
df_product["pos_categ_ids"] = df_product["categ_id"]
df_product["MWST"] = df_product["MWST"].apply(lambda x: "20% Ust" if x == 0.2 else "0% Ust O Exempt" if x == 0 else "")
df_product["Preis"] = df_product["Preis"].fillna(0) * (1 + df_product["MWST"].fillna(0))
df_product["barcode"] = df_product.apply(lambda row: row["alterEANCode"] if pd.notna(row["alterEANCode"]) else row["Best_EAN"] if pd.notna(row["Best_EAN"]) else pd.NA, axis=1)

#supplier procedure
df_supplier_info = df_product[df_product["Nr_Lieferant"] > 0][["Artikelnummer"] + supplier_price_cols].fillna("").copy()
#merge mit Artikelnummer -> defaultcode/Produkt externe ID, Nr_Lieferant -> ref/Lieferant externe ID
df_odoo_supplier = pd.read_excel(input_path + "Odoo_Supplier.xlsx").rename(columns={"id": "partner_id/id"})
df_odoo_product = pd.read_excel(input_path + "Odoo_Product.xlsx").rename(columns={"id": "product_tmpl_id/id"})
df_supplier_info = df_supplier_info.merge(
    df_odoo_supplier,
    left_on=["Nr_Lieferant"],
    right_on=["ref"],
    how="left"
)
df_supplier_info = df_supplier_info.merge(
    df_odoo_product,
    left_on=["Nr"],
    right_on=["default_code"],
    how="left"
)
df_supplier_info = df_supplier_info.drop(columns=["Artikelnummer", "Nr_Lieferant", "ref", "default_code"])
df_supplier_info = df_supplier_info.rename(columns={"Beschaffungszeit": "delay", "Bestellnummer": "product_code"})

#export preparation
df_product = df_product.drop(columns=["cat_nr", "Nr_Warengruppe", "Nr", "Positionsnummer2", "alterEANCode", "Best_EAN", "Status", "EK", "RA"] + supplier_price_cols).copy()
df_product = df_product.rename(columns=product_map)

#export product file
df_product.to_excel(output_path + 'product_template.xlsx', index=False)
df_supplier_info.to_excel(output_path + 'product_pricelist.xlsx', index=False)

