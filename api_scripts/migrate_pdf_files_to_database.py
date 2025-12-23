"""
code to migrate pdf files from a predecessor system to Odoo via XMLRPC API
based on Odoo major version 17
note that this API will be phased out with major version 20
"""

import os
import base64
import re
import ast
import xmlrpc.client
from collections import namedtuple

# define relevant file and directory paths
root_path = 'path/to/startingpoint'
folder_subset_file = 'path/to/folderlist/folderfilename.txt'

# define relevant mimetypes
mimetype_map = {
    'pdf': 'application/pdf',
    'jpe?g': 'image/jpeg',
    'tiff?': 'image/tiff'
}

# provide credentials for XMPRPC API connection
user_name = 'my_user' # admin user or adapt to specific user
password = 'my_password'    # user real password (OR preferentially)
api_key = 'my_api_key'    # use real API key
user_auth = password or api_key

# provide connection specifications
url = 'https://url.to.my_db'
db = 'my_db'

# establish connection to database
try:
    common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
    user_uid = common.authenticate(db, user_name, user_auth, {})
except Exception as e:
    print(f'Error during establishing connection to {db}: {e}')

# get paremeter for record processing
try:
    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
except Exception as e:
    print(f'Error during obtaining object processing parameter of {db}: {e}')

# provide a list of folders (ensure type string) when only a subset of pdf files needs to be migrated
if os.path.isfile(folder_subset_file):
    with open(folder_subset_file, 'r') as f:
        folder_subset_list = ast.literal_eval(f.read())
else:
    folder_subset_list = []
folder_subset_list = list(map(str, folder_subset_list))

# prepare error handling
ErrorRecord = namedtuple('ErrorRecord', ['filename', 'reason'])
error_list = []

# iterate through root directory and create attachment records via API call
for dirpath, dirnames, filenames in os.walk(root_path):
    for filename in filenames:
        mimetype = ''
        for key in mimetype_map.keys():
            if re.findall(key, filename.split('.')[-1]):
                mimetype = mimetype_map.get(key)
                break
        if not mimetype:
            print(f'{filename} has no specified mime type.')
            error_list.append(ErrorRecord(filename, 'skipped#nomimetype'))
            continue
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
                """
                TBD:
                logic for determining or defining res model and res id
                conditional for when to use parent folder as key and what would be the alternative
                """
                res_model_string = ''
                res_id = 0
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
            print(f'{filename} is not in list.')
            error_list.append(ErrorRecord(filename, 'skipped#notspecified'))
            continue


