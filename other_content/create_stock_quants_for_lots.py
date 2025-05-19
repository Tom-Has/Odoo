lots = env['stock.lot'].search([('product_qty', '=', 0), ('product_id.detailed_type', '=', 'product')])
quants = env['stock.quant']

for lot in lots:
    prod = lot.product_id.id
    quants.create([{'product_id': prod, 'location_id': 20, 'lot_id': lot.id, 'quantity': 1}])