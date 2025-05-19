#obtain prescription files via directory and convert them to Base64 format
def file_to_base64(row_path):
    path = "C:\\Users\ThomasHabenschuss\Documents\Datenimports\Schaper\Dokumente\\" + row_path
    try:
        with open(path, "rb") as file:
            return base64.b64encode(file.read()).decode('utf-8')
    except Exception as e:
        print(f"Fehler beim Kodieren der Datei {path}: {e}")
        return None
