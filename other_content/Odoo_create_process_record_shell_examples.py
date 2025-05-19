#create a record
uom = env['uom.uom']
for ele in oum_list:
    uom.create({'category_id': 1, 'name': ele['name'], 'uom_type': 'bigger', 'factor': 1/ele['zahl']})

#update calculations in a record
for order in orders:
    for line in lines:
        line._compute_amount()


