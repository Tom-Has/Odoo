"""
batch creation of files and associated ir.attachtment records from external pdf files
"""

"""
local or external procedure
"""

import os
import base64
import csv
import ast

# helper function for converting pdf content to Base64
def encode_file_to_base64(file_path):
    try:
        with open(file_path, "rb") as file:
            return base64.b64encode(file.read()).decode('utf-8')
    except Exception as e:
        print(f"Fehler beim Kodieren der Datei {file_path}: {e}")
        return None


# define relevant directories
root_path = 'path/to/startingpoint'
folder_subset_file = 'path/to/folderlist'
csv_file = 'path/to/result'

# provide a list of folders when a subset of content needs to be converted
with open(folder_subset_file, 'r') as f:
    folder_subset_list = ast.literal_eval(f.read())

# list to store conversion results
data = []

# Durch das Verzeichnis iterieren
for dirpath, dirnames, filenames in os.walk(root_path):
    for filename in filenames:
        try:
            parent_folder = os.path.basename(dirpath)
            if filename.lower().endswith('.pdf') and (int(parent_folder) in folder_subset_list or len(folder_subset_list) :

        except Exception as e:
            print(f"Fehler beim Durchsuchen des Ordners: {e}")
    try:
        if os.path.isdir(folder_path) and int(folder) in folder_list:
            for file in os.listdir(folder_path):
                if file.lower().endswith(".pdf"):
                    file_path = os.path.join(folder_path, file)
                    base64_content = encode_file_to_base64(file_path)
                    if base64_content:
                        data.append([folder, base64_content])
                    break


# CSV-Datei schreiben
try:
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Ordnername", "Base64 Inhalt"])
        writer.writerows(data)
    print(f"CSV-Datei '{csv_file}' wurde erfolgreich erstellt.")
except Exception as e:
    print(f"Fehler beim Schreiben der CSV-Datei: {e}")


"""
odoo shell procedure
"""

# files or paths to files
paths = ["encoded_pdfs.csv"]  # add or adpapt paths as needed

# constants
att_model = env['ir.attachment']
res_model_string = 'res.model'    # change name as needed
counter = 0
limit = 1000

# writing iteration
for path in paths:
    with open(path, 'r') as file:
        for index, line in enumerate(file):
            if index == 0:
                continue
            parts = line.strip().split(",")
            name = "prefix-" + parts[0]    # adapt name as needed
            filename = name + ".pdf"    # construct file name as needed
            id = env[res_model_string].search([('name', '=', name)]).id # adapt filter as needed
            att_model.create({
                "key": parts[0],
                "datas": parts[1],
                "name": name,
                "res_name": filename,
                "res_model": res_model_string,
                "res_id": id,
                "mimetype": "application/pdf",
                "type": "binary"
            })
            counter += 1
            if counter % limit == 0:
                env.cr.commit()
                print(f"Bisher {counter} Dateien angelegt.")
        env.cr.commit()
        print(f"Fertig! {counter} Dateien angelegt.")
