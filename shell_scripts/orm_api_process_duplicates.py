# group
duplicates = env['<model_name>'].read_group(
    domain=[],
    fields=['<field_name1>', '<field_name2>', '<field_name3>:<aggregate_func>'],
    groupby=['<field_name1>', '<field_name2>']
)

# process group
for entry in duplicates:
    if entry['field_name1'] > 1:
        print(f"{entry['field_name1']}: corresponds to {entry['field_name3_count']}.")

"""
Important:
Each field <field_nameX> in groupby must exist in fields.
The fields-parameter can contain more fields, e. g. for counts, sums, etc.
The aggregate functions <aggregate_func> are named count, sum, avg, min, max.
The result is always a list of dictionaries, the keys being named <field_nameX>, <field_nameX>_count, <field_nameX>_sum, etc.
"""

"""
include the following statements at the beginning when operating outside of odoo shell
from odoo import api, SUPERUSER_ID
env = api.Environment(cr, SUPERUSER_ID, {})
"""
