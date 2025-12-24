"""
code to migrate pdf files from a predecessor system to Odoo via XMLRPC API
based on Odoo major version 17
note that this API will be phased out with major version 20
"""

"""
import statements and variables section
"""

# import relevant packages
import os
import base64
import pandas as pd
import mimetypes
import xmlrpc.client
from collections import namedtuple

# root directory for files, path to specification file and paths to other potentially relevant files
root_path = 'path/to/startingpoint'
spec_file_path = 'path/to/filespecs.csv|xlsx'

# specification colums
file_path_col = 'file_path_col'
key_col = 'key_col'
model_col = 'model_col'
doc_id = 'id'

# filter string for reducing dataframe
filter_string = f'{file_path_col}.notnull() and {model_col}  not in [] and ...'

# establish res.model map or default value and key parameters
res_model_default = 'suppl.healthcare.supply.order'
res_model_search = 'model.to.be.investigated.for.key'
res_model_map = {
    'VO': 'suppl.healthcare.prescription',
    'RE': 'res.partner',
}
key_field = 'x_Sansoft_auto'

# provide credentials for XMPRPC API connection
user_name = 'my_user' # admin user or adapt to specific user
password = ''    # user real password (OR preferentially)
api_key = 'my_api_key'    # use real API key
user_auth = api_key or password

# provide connection specifications
url = 'https://url.to.my_db'
db = 'my_db'

"""
procedural logic section
"""

# ensure relevant mimetypes
mimetypes.add_type('text/csv', '.csv')
mimetypes.add_type('application/excel', '.xls')
mimetypes.add_type('application/excel', '.xlsx')
mimetypes.add_type('application/opendocument', '.ods')

# ensure existence of root directory
if not os.path.exists(root_path)):
    exit("A directory for attachment files must be provided!")
root_directory = pathlib.Path(root_path)

# ensure existence and correct type of specification file
spec_file_mimetype = mimetypes.guess_type(spec_file_path)[0]
if not (spec_file_mimetype in ['application/excel', 'text/csv', 'application/json'] and os.path.isfile(spec_file_path)):
    exit("A file containing paths to attachment files must be provided and be of type Excel, csv or json!")

# read and filter specification file
if spec_file_mimetype == 'text/csv':
    df_file_specs = pd.read_csv(spec_file_path)
elif spec_file_mimetype == 'application/excel':
    df_file_specs = pd.read_excel(spec_file_path)
elif spec_file_mimetype == 'application/json':
    df_file_specs = pd.read_json(spec_file_path)
else:
    exit("Unknown error while reading specification file!")
df_file_specs_filtered = df_file_specs.query(filter_string)

# establish connection to database
try:
    common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
    user_uid = common.authenticate(db, user_name, user_auth, {})
except Exception as e:
    exit(f'Error during establishing connection to database: {e}')

# get paremeter for record processing
try:
    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
except Exception as e:
    exit(f'Error during obtaining object processing parameter of database: {e}')

# prepare error handling
ErrorRecord = namedtuple('ErrorRecord', ['filename', 'reason'])
error_list = []

# iterate through file dataframe and create attachment records via API call
for index, rows in df_file_specs_filtered.iterrows():
    filename = row[file_path_col].split('/')[-1].strip()
    mimetype, _ = mimetypes.guess_type(filename)
    
    try:
        with open(os.path.join(root_path, row[file_path_col]), 'rb') as file:
            base64_content = base64.b64encode(file.read()).decode('utf-8')
    except Exception as e:
        print(f'Error while encoding {filename}: {e}')
        error_list.append(ErrorRecord(filename, 'error#encoding'))
        continue
    
    if base64_content:
        res_model_string = res_model_map.get(row[model_col], res_model_default)
        res_id = env[res_model_search].search([(key_field, '=', row[key_col])], limit=1).id
        try:
            id = models.execute_kw(db, user_uid, user_auth, 'ir.attachment', 'create', [{
                'name': filename,
                'datas': base64_content,
                'key': row[doc_id] or '',
                'res_model': res_model_string,
                'res_id': res_id or 0,
                'mimetype': mimetype or 'application/octet-stream',
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
