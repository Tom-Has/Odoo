"""
This snippet might be useful for custom modules where no view and/or export procedure is defined and an occasional list of given records is needed.
"""

import csv

# adapt to custom model as needed
model_name = 'my.custom.model'
model = env[model_name]

# adapt exportable fields as needed
model_fields = ['id', 'partner_id/id', 'partner_id/name']

# adapt name as needed
filename = model_name + '_export.csv'

# adapt search filter as needed
domain_filter = []

# get records and write field values to file
with open(filename, "w", newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(model_fields)
    writer.writerows(model.search(domain_filter).export_data(model_fields).get('datas', []))
