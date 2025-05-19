#create social security number from prefix and date of birth
def build_sv_nr(row):
    try:
        if row["Branchenkennzeichen"] not in ("Patient", "Zustelladresse"):
            return None

        val = row.get("SozVersNr", "")
        if isinstance(val, float) and val.is_integer():
            val = int(val)
        val_str = str(val).strip()
        if val_str.isdigit() and len(val_str) in (3, 4):
            soz = val_str.zfill(4)
        else:
            soz = ""

        geb = pd.to_datetime(row.get("GebDatum", ""), errors="coerce")
        
        svnr2 = str(row.get("SVNr2", "")).strip()

        if len(soz) != 4 or pd.isnull(geb):
            if re.fullmatch(r"\d{10}", svnr2):
                return svnr2
            return None

        result = f"{soz}{geb.day:02d}{geb.month:02d}{geb.year % 100:02d}"
        if re.fullmatch(r"\d{10}", result):
            return result
        return None

    except Exception as e:
        # bad_rows.append((row["Nr"], str(e)))
        return None

#consolidate various country shortcodes
def unify_country_code(code):
    code = str(code).strip().upper()
    if code == "A":
        return "AT"
    elif code == "D":
        return "DE"
    elif code == "C":
        return "CH"
    else:
        country = pc.countries.get(alpha_2=code)
        if not country:
            country = pc.countries.get(alpha_3=code)
        return country.alpha_2 if country else ""

#remove obviously nonsensical vat ID numbers
def validate_and_clean_uid(row):
    original_uid = str(row.get("UID", "")).strip()
    cleaned_uid = re.sub(r"[^A-Z0-9]", "", original_uid.upper())

    if not re.fullmatch(r"^[A-Z]{2}[A-Z0-9]{6,12}$", cleaned_uid):
        return ""

    if re.search(r"(\d)\1{5}", cleaned_uid):
        return ""

    return cleaned_uid

#create company name from components
def generate_company_name(row):
    if not row.get("is_company", False):
        return ""

    parts_raw = [
        str(row.get("Anrede", "")).strip(),
        str(row.get("Name2", "")).strip(),
        str(row.get("Name", "")).strip(),
    ]

    parts_clean = [p for p in parts_raw if p]
    amp_parts = [p for p in parts_clean if p.startswith("&")]
    normal_parts = [p for p in parts_clean if not p.startswith("&")]
    combined = normal_parts + amp_parts
    name = " ".join(combined).strip()

    if not name:
        return "SUPPL_Firma_Unbekannt"

    return name
