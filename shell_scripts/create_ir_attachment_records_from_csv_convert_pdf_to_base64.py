"""
batch creation of files and associated ir.attachtment records from external pdf files
"""

"""
LOCAL - local or external procedure
"""

import os
import base64
import csv
import ast
import requests

# helper function for converting pdf content to Base64
def encode_file_to_base64(file_path):
    try:
        with open(file_path, "rb") as file:
            return base64.b64encode(file.read()).decode('utf-8')
    except Exception as e:
        print(f"Error while encoding {file_path}: {e}")
        return None


# define relevant directories
root_path = 'path/to/startingpoint'
folder_subset_file = 'path/to/folderlist'
csv_file = 'path/to/result'
server = 'IP-adress/path'
server_path = 'path/to/csv_file'

# provide a list of folders when a subset of content needs to be converted
with open(folder_subset_file, 'r') as f:
    folder_subset_list = ast.literal_eval(f.read())

# list to store conversion results
data = []

# iterate through directory
for dirpath, dirnames, filenames in os.walk(root_path):
    for filename in filenames:
        try:
            parent_folder = os.path.basename(dirpath)
            try:
                parent_folder_int = int(parent_folder)
            except Exception as e:
                print(f"Directory {parent_folder} skipped because of conversion error: {e}")
                continue
            if filename.lower().endswith('.pdf') and (len(folder_subset_list) == 0 or parent_folder_int in folder_subset_list):
                base64_content = encode_file_to_base64(os.path.join(dirpath, filename))
                    if base64_content:
                        data.append([parent_folder, base64_content])
        except Exception as e:
            print(f"Error during directory iteration: {e}")


# write data to csv
try:
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["foldername", "base64_datas_content"])
        writer.writerows(data)
    print(f"CSV file '{csv_file}' was created.")
except Exception as e:
    print(f"Error while writing csv file: {e}")

# upload csv file to server
try:
    with open(csv_file, 'rb') as f:
        response = requests.post(server, files={'file': f})
     print(f"CSV file '{csv_file}' was uploaded to {server} with response {response.status_code}.")
except Exception as e:
    print(f"Error while uploading csv file: {e}")


"""
SERVER - Odoo shell procedure
"""

# constants
att_model = env['ir.attachment']
res_model_string = 'res.model'    # change name as needed
counter = 0
limit = 1000

# writing iteration
with open(server_path, 'r') as file:
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
            print(f"{counter} files and associated records created so far.")
    env.cr.commit()
    print(f"Finished! {counter} total files and associated records created.")
