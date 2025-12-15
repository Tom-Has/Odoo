"""
code to migrate pdf files from a predecessor system to Odoo via XMLRPC API
based on Odoo major version 17 
"""

import os
import base64
import ast
import xmlrpc.client
from collections import namedtuple

# define relevant file and directory paths
root_path = 'path/to/startingpoint'
folder_subset_file = 'path/to/folderlist/folderfilename.txt'    # must contain folder names as type string

# provide credentials for XMPRPC API connection
user_uid = 2    # admin user or adapt to user for which password or API key is available
user_name = 'admin' # admin user or adapt to specific user
user_auth = password or api_key

# provide connection specifications
url = 'https://url.to.db'
db = 'db_name'

# establish connection to database
try:
    common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
    common.authenticate(db, user_name, user_auth, {})
except Exception as e:
    print(f'Error during establishing connection to {db}: {e}')

# get paremeter for record processing
try:
    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
except Exception as e:
    print(f'Error during obtaining object processing parameter of {db}: {e}')

# provide a list of folders when only a subset of pdf files needs to be migrated
if os.path.isfile(folder_subset_file):
    with open(folder_subset_file, 'r') as f:
        folder_subset_list = ast.literal_eval(f.read())
else:
    folder_subset_list = []

# prepare error handling
ErrorRecord = namedtuple('ErrorRecord', ['filename', 'reason'])
error_list = []

# iterate through root directory and create attachment records via API call
for dirpath, dirnames, filenames in os.walk(root_path):
    for filename in [f for f in filenames if f.lower().endswith('.pdf')]:
        parent_folder = os.path.basename(dirpath)
        if (len(folder_subset_list) == 0 or parent_folder in folder_subset_list):
            try:
                with open(os.path.join(dirpath, filename), 'rb') as pdf_file:
                    base64_content = base64.b64encode(pdf_file.read()).decode('utf-8')
            except Exception as e:
                print(f'Error while encoding {filename}: {e}')
                error_list.append(ErrorRecord(filename, 'error#encoding'))
                continue
            if base64_content:
                try:
                    id = models.execute_kw(db, user_uid, user_auth, 'ir.attachment', 'create', [{
                        'name': filename,
                        'datas': base64_content,
                        'key': parent_folder,
                        'res_model': res_model_string or '',
                        'res_id': res_id or 0,
                        'mimetype': 'application/pdf',
                        'type': 'binary'
                    }])
                except Exception as e:
                    print(f'Error while encoding {filename}: {e}')
                    error_list.append(ErrorRecord(filename, 'error#apiconnect'))
                    continue
            else:
                print(f'{filename} seems to be empty.')
                error_list.append(ErrorRecord(filename, 'error#emptyfile'))
                continue
        else:
            print(f'{filename} seems to be empty.')
            error_list.append(ErrorRecord(filename, 'skipped#notspecified'))
            continue
