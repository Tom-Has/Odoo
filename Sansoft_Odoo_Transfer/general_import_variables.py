#packages
import pandas as pd
import re
import os
import pycountry as pc
import requests as req
import base64
import mimetypes

#mapping preparation
excel_files = {
    'res_partner': 'ADRESSEN.xlsx',
    #'claims': 'ADRESSEN_ANSPRUECHE.xlsx',
    #'res_titles': 'ANREDE.xlsx',
    'product_templates': 'ARTIKEL.xlsx',
    'suppl_healthcare_tarifs': 'ARTIKEL_TARIF.xlsx',
    #'res_employees': 'BETREUER.xlsx',
    'res_partner_category': 'BRANCHEN.xlsx',
    'ir_documents': 'DOKUMENTE.xlsx',
    'ir_documents_use': 'DOKUMENTE_USE.xlsx',
    #'sales_sales_groups': 'FILIALEN.xlsx',
    'product_parent_cat': 'GESCHAEFTSBEREICH.xlsx',
    'product_sub_cat': 'WARENGRUPPE.xlsx',
    'res_partner_prescriber': 'KK_ARZT.xlsx',
    'suppl_healthcare_prescriptions': 'KK_VO.xlsx',
    'res_partner_insurer': 'KRANKENKASSEN.xlsx',
    'res_partner_patient_doctor': 'KUNDEN_ARZT.xlsx',
    'res_partner_phone': 'TELEFONNUMMERN.xlsx'
}

#path name preparation
input_path = "C:\\Users\ThomasHabenschuss\Documents\Datenimports\Schaper\Datenbank20250303\\"
output_path = input_path + "import_prep\\"
if not os.path.exists(output_path):
    os.makedirs(path)

#export size
chunk_size = 20000
