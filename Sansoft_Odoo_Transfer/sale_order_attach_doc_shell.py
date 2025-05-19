"""
Run this script for connecting attachments to sale orders based on the Sansoft auto key.
"""

#data collections and constants
attachments = env['ir.attachment'].search([('key', '!=', False), ('res_id', '=', False)])
order_lines_data = env['sale.order.line'].search([('x_SUPPL_Sansoft_auto', '!=', False)]).read(['x_SUPPL_Sansoft_auto', 'order_id'])

line_lookup = {}
start = 0
limit = 10000

#create dict for connecting auto values to sale order ids
for line in order_lines_data:
    key = str(line['x_SUPPL_Sansoft_auto'])
    order_id = line['order_id']
    if isinstance(order_id, (tuple, list)) and order_id:
        line_lookup[key] = order_id[0]

#connect attachments to sale orders
for attachment in attachments:
    order_id = line_lookup.get(attachment.key)
    if order_id:
        attachment.res_id = order_id
    else:
        print(f"Anhang mit auto/key {attachment.key} nicht verknüpfbar.")
    start += 1
    if start >= limit:
        env.cr.commit()
        start = 0
        print("10.000 Batch abgearbeitet.")

env.cr.commit()
print("✅ Verknüpfung abgeschlossen.")
