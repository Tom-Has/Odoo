"""
This snippet might be useful for custom modules where no view and/or export procedure is defined and an occasional list of given records is needed.
"""

# adapt name as needed
filename = 'export.csv'

# adapt to custom model as needed
model = env['res.partner']

# adapt exportable fields as needed
model_fields = ['id', 'name']

# adapt search filter as needed
domain_filter = []

# get records and write field values to file
with open(filename, "w") as csv_file:
    csv_file.write(model_fields.join(',') + '\n')
    for rec in model.search(domain_filter):
        """
        this part needs to be updated to functioning logic
        """
        csv_file.write(f"" + "\n")
