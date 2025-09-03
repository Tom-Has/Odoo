# search() to obtain record set (Boolean evaluation)
record_set = env['res.partner'].search([('field', 'in', value_list)])

# mapped() to obtain list of values from record set
values_list = record_set.mapped('id')
values_list = record_set.mapped(lambda r: r.field1 + r.field2)

# filtered() to obtain record set more specifically ((Boolean evaluation)
filtered_set = record_set.filtered('partner_id.is_company')
filtered_set = record_set.filtered(lambda r: r.company_id == user.company_id)

# https://www.odoo.com/documentation/18.0/developer/reference/backend/orm.html
