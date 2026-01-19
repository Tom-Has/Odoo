"""
find and remove invalid fields one by one
"""

spurious_cases = env['ir.property'].search([('fields_id', '=', 8526), ('company_id', '=', 1), ('res_id', '=', False)]) 
for rec in spurious_cases:
    if rec.res_id == False:
        print(f"suspicious case: #{rec.id} / {rec.name}")
        env['ir.property'].browse(rec.id).unlink()

"""
remove invalid fields when a complete list is available
"""

bad_field_ids = [8526, 8527]  # extend when new errors occur
to_delete = env['ir.property'].search([('fields_id', 'in', bad_field_ids), ('company_id', '=', 1), ('res_id', '=', False)])
to_delete.unlink()
