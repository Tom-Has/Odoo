"""
field structure in QWeb
"""

# field declaration
<field name="parent_id""/>

# field name
name="parent_id"

# name of field (overwrites String value)
string="Contact Name"

# placeholder (no default value)
placeholder="Country"

# graphic display of field values
widget="many2many_tags"

# additional options for graphic display of field values
options="{'horizontal': true}"

# record filter for one/many2many field connections
domain="[('is_company', '=', True)]"

# visibility conditions
invisible="((is_company and not parent_id) or company_name) and company_name != ''"

# read only conditions
readonly="type == 'contact' and parent_id"

# conditions for value requirement
required="type == 'contact'"

# default values for opening or creating a record
context="{'default_is_company': True, 'show_vat': True, 'default_user_id': user_id}"

"""
special
"""

# dynamic time filter
[["date_deadline", "<=", (context_today() + datetime.timedelta(weeks = 2)).strftime("%Y-%m-%d")]]
