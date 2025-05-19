"""
Anmerkungen zum Import von historischen Aufträgen:
Import via Modell sale_order als normaler Verkaufsauftrag
Verordnungen und Ansprüche werden nicht zu Kunden importiert, demnach hier keine Felder, demnach alle lines auf privat gestellt
"""

#import supply order files to DataFrames
df_so = pd.read_excel(input_path + excel_files["suppl_healthcare_prescriptions"], usecols=sale_order_cols).query("Nr_Adresse > 0")
df_documents = pd.read_excel(input_path + excel_files["ir_documents"], usecols=document_cols).dropna(subset=['Dateiname'])
df_link = pd.read_excel(input_path + excel_files["ir_documents_use"]).query("Art == 'VO'").dropna(subset=['Nr_Dokument'])
df_patients = pd.read_excel(input_path + "Odoo_Patient.xlsx").rename(columns={"id": "partner_id/id", "ref": "ref_patient"})
#df_doctors = pd.read_excel(input_path + "Odoo_Doctor.xlsx").rename(columns={"id": "healthcare_prescriber_id/id", "ref": "ref_doctor"})
#df_doctors["ref_doctor"] = df_doctors["ref_doctor"].apply(lambda x: float(x))
#df_products = pd.read_excel(input_path + "Odoo_Product.xlsx").rename(columns={"id": "product_id/id", "ref": "ref_doctor"})
#df_products["default_code"] = df_products["default_code"].apply(lambda x: float(x))

#prepare merge patient and removal of excess entries
df_patients["ref_patient"] = pd.to_numeric(df_patients["ref_patient"], errors="coerce")
df_so = df_so.merge(
    df_patients,
    left_on=["Nr_Adresse"],
    right_on=["ref_patient"],
    how="inner"
)

#prepare dates
df_so["Datum"] = pd.to_datetime(df_so["Datum"], errors="coerce").fillna(pd.Timestamp("2025-01-01 00:00:00.999999"))
df_so["date_order"] = df_so["Datum"].dt.normalize()

#prepare order line info
df_so["order_line/product_id"] = "SUPPL_default_product"
df_so["order_line/name"] = df_so["auto"]
df_so = df_so.rename(columns={"Preis": "order_line/price_unit", "Anz": "order_line/product_uom_qty", "auto": "order_line/x_SUPPL_Sansoft_auto"})

#prepare sale order info
df_so = df_so.sort_values(["partner_id/id", "date_order"])
mask = df_so.duplicated(subset=["partner_id/id", "date_order"])
df_so.loc[mask, ["partner_id/id"]] = pd.NA
df_so.loc[mask, "date_order"] = pd.NaT
df_so.loc[~mask, "client_order_ref"] = df_so.loc[~mask, "Nr_Adresse"].astype(str) + "_" + df_so.loc[~mask, "Nr_Arzt"].astype(str) + "_" + df_so.loc[~mask, "Nr_Betreuer"].astype(str)

#drop excess columns
df_so = df_so.drop(columns=["Nr_Adresse", "Nr_Arzt", "Nr_Betreuer", "Datum", "ref_patient"])

#export sale oders
df_so.to_csv(output_path + "sale_order_historic_full.csv", index=False)
df_so.to_excel(output_path + "sale_order_historic_full.xlsx", index=False)

"""
#client_order_ref for all order lines
df_so["client_order_ref"] = (
    df_so["Nr_Adresse"].astype(str) + 
    df_so["Datum"].dt.strftime("%Y%m%d%H%M%S%f")
)
df_so["client_order_ref"] = df_so.groupby(["Nr_Adresse", "date_order"])["client_order_ref"].transform("first")
"""


"""
sale_orders = df_so.groupby(sale_order_group_key).agg({"Preis": "sum", "Nr_Arzt": "max", "Datum": "last", "auto": "first"}).reset_index()

sale_order_import = df_link[["Nr_fremd", "Art"]].merge(
    sale_orders,
    left_on=["Nr_fremd"],
    right_on=["auto"],
    how="inner"
)
#sale_order_import = sale_order_import.drop_duplicates("auto", keep="last")

sale_order_import = sale_order_import.merge(df_patients, how='left', left_on="Nr_Adresse", right_on="ref_patient")
sale_order_import = sale_order_import.dropna(subset=['partner_id/id'])
sale_order_import = sale_order_import.merge(df_doctors, how='left', left_on="Nr_Arzt", right_on="ref_doctor")

#sale_order_import["client_order_ref"] = sale_order_import["Nr_Adresse"].astype(str) + sale_order_import["Datum"].dt.strftime("%Y%m%d%H%M%S%f")
#Überprüfung auf versehentliche Duplikate nicht vergessen!!!

sale_order_import = sale_order_import.rename(columns={"Preis": "order_line/price", "auto": "client_order_ref"})
sale_order_import = sale_order_import.drop(columns=["Nr_fremd", "Art", "Nr_Adresse", "Nr_Arzt", "ref_patient", "ref_doctor", "Datum"])

#sale_order_import["force_invoiced"] = True
#sale_order_import["state"] = "sale"

sale_order_import.to_excel(output_path + "sale_order_historic_prescript_only.xlsx", index=False)

#sale_order_import["healthcare_force_invoiced"] = True
"""

#prepare document links
df_documents_filtered = df_link.merge(
    df_documents,
    left_on=["Nr_Dokument"],
    right_on=["Nr"],
    how="inner"
)

"""
#url for obtaining attachment documents
base_url = ""
document_path = "C:\\Users\ThomasHabenschuss\Documents\Datenimports\Schaper\Dokumente\\"
"""

#prepare files as base64 strings
df_documents_filtered["datas"] = df_documents_filtered["Dateiname"].apply(file_to_base64)
df_documents_filtered = df_documents_filtered.dropna(subset="datas")

#prepare import properties
df_documents_filtered["name"] = df_documents_filtered["Dateiname"].apply(lambda x: x.split("\\")[-1])
df_documents_filtered["mimetype"] = df_documents_filtered["name"].apply(lambda x: mimetypes.types_map["." + x.split(".")[-1]])
df_documents_filtered["type"] = "binary"
df_documents_filtered["res_model"] = "sale.order"
df_documents_filtered = df_documents_filtered.fillna(value={"Text": "", "Bemerkung": ""})
df_documents_filtered["Datum"] = pd.to_datetime(df_documents_filtered["Datum"], errors="coerce").fillna(pd.Timestamp("2025-01-01 00:00:00.999999"))
df_documents_filtered["description"] = "Datum original: " + df_documents_filtered["Datum"].dt.strftime("%Y-%m-%d") + "<br>Text original: " + df_documents_filtered["Text"] + "<br>Bemerkung original: " + df_documents_filtered["Bemerkung"]

#rename and drop excess columns
df_documents_filtered = df_documents_filtered.rename(columns={"Nr_fremd": "key"})
df_documents_filtered = df_documents_filtered.drop(columns=["Nr_x", "Nr_y", "Art", "Dateiname", "Datum", "Text", "Bemerkung", "Nr_Dokument"])

"""
df_orders = pd.read_excel(input_path + "Odoo_Saleorder.xlsx").rename(columns={"ID": "res_id", "Kundenreferenz": "auto"})
df_documents_filtered_odoo_id = df_documents_filtered.merge(
    df_orders,
    how="left",
    left_on="Nr_so_auto",
    right_on="auto"
)
"""

#export to csv due to Excel base64 length restrictions
df_documents_filtered.to_csv(output_path + "file_import.csv", index=False)

