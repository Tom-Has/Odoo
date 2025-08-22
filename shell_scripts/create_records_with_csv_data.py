import csv

filename = "filename.csv"
auto_values = []

with open(filename, 'r', encoding='utf-8') as data:
    reader = list(csv.DictReader(data))
    auto_values = [line["auto"] for line in reader]
    order_lines = env['sale.order.line'].search([
        ("x_SUPPL_Sansoft_auto", "in", auto_values)
    ])
    auto_to_order_id = {
        ol.x_SUPPL_Sansoft_auto: ol.order_id.id
        for ol in order_lines
    }
    SaleOrder = env['sale.order']
    counter = 0
    limit = 1000
    for line in reader:
        order_id = auto_to_order_id.get(line["auto"])
        if order_id:
            SaleOrder.browse(order_id).write({
                'x_SUPPL_Sansoft_Zusatztext': line["Zusatztext"]
            })
        counter += 1
        if counter > limit:
            env.cr.commit()
            print(f"{limit} Batch erledigt.")
            counter = 0
    if counter > 0:
        env.cr.commit()
        print("Vorgang abgeschlossen.")

env.cr.commit()
