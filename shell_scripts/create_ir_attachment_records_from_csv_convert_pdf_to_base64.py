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
import paramiko
from scp import SCPClient

# helper function for converting pdf content to Base64
def encode_file_to_base64(file_path):
    try:
        with open(file_path, 'rb') as file:
            return base64.b64encode(file.read()).decode('utf-8')
    except Exception as e:
        print(f'Error while encoding {file_path}: {e}')
        return None


# define relevant file paths, directories and IP-addresses
root_path = 'path/to/startingpoint'
folder_subset_file = 'path/to/folderlist/folderfilename.txt'
result_name = 'encoded_pdfs.csv'
result_path = os.path.join('path/to/result', result_name)
server_ip = '127.0.0.1'
result_path_server = '/path/to/odoo_bin'

# provide credentials for ssh connection
user_name = 'root'
user_pw = 'root_pw'

# provide a list of folders when a subset of content needs to be converted
if os.path.isfile(folder_subset_file):
    with open(folder_subset_file, 'r') as f:
        folder_subset_list = ast.literal_eval(f.read())
else:
    folder_subset_list = []

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
                print(f'Directory {parent_folder} skipped because of conversion error: {e}')
                continue
            if filename.lower().endswith('.pdf') and (len(folder_subset_list) == 0 or parent_folder_int in folder_subset_list):
                base64_content = encode_file_to_base64(os.path.join(dirpath, filename))
                if base64_content:
                    data.append([parent_folder, filename, base64_content])
        except Exception as e:
            print(f'Error during directory iteration: {e}')

# write data to csv file
try:
    with open(result_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['foldername', 'filnemame', 'base64_datas_content'])
        writer.writerows(data)
    print(f'{result_name} was created.')
except Exception as e:
    print(f'Error while creating {result_name}: {e}')

# upload csv file to server
try:
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.connect(server_ip, username=user_name, password=user_pw)
    with SCPClient(ssh.get_transport()) as scp:
        scp.put(result_path, result_path_server)
except Exception as e:
    print(f'Error while uploading {result_name}: {e}')


"""
SERVER - Odoo shell procedure
"""

# constants
att_model = env['ir.attachment']
res_model_string = 'res.model'    # change name as needed
counter = 0
limit = 1000
result_name = 'encoded_pdfs.csv'

# writing iteration (beware path to file when file is not in odoo-bin directory)
with open(result_name, 'r') as file:
    for index, line in enumerate(file):
        if index == 0:
            continue
        parts = line.strip().split(',')
        res_key = parts[0]
        filename = parts[1]
        res_id = env[res_model_string].search([('name', '=', res_key)]).id # adapt filter as needed
        att_model.create({
            'key': res_key,
            'datas': parts[2],
            'name': filename,
            'res_name': filename,
            'res_model': res_model_string,
            'res_id': res_id,
            'mimetype': 'application/pdf',
            'type': 'binary'
        })
        counter += 1
        if counter % limit == 0:
            env.cr.commit()
            print(f'{counter} files and associated records created so far.')
    env.cr.commit()
    print(f'Finished! {counter} total files and associated records created.')
