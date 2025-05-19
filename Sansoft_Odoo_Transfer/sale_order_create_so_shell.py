"""
Run this script for creating sale orders and adjusting related variables when import file(s) cause(s) timeouts because of size or limited CPU-time/request.
"""

#imports and variable arguments
import re
import csv

path = "nachtrag.csv"
default_product_id = 111048

#constants
start = 0
limit = 1000
orders = []
current_order = None
product = env["product.product"].browse(default_product_id)
uom_id = product.uom_id.id

#read sale order info
with open(path, newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    
    for index, parts in enumerate(reader, start=1):
        try:
            price_unit = float(parts[0])
            x_suppl_sansoft_auto = parts[1]
            quantity = int(float(parts[2]))
        except (ValueError, IndexError):
            print(f"⚠️  Ungültige Preis- oder Mengenangabe in Zeile {index}. Übersprungen.")
            continue
        
        partner_raw = parts[3]
        date_order = parts[4]
        client_order_ref = parts[6]
        
        if partner_raw:
            try:
                partner_id = int(re.sub(r"^__export__\.res_partner_(\d+)_.*$", r"\1", partner_raw))
            except ValueError:
                print(f"⚠️  Ungültige Partner-ID in Zeile {index}: '{partner_raw}'")
                continue
            
            current_order = {
                "partner_id": partner_id,
                "date_order": date_order,
                "client_order_ref": client_order_ref,
                "lines": []
            }
            orders.append(current_order)
        
        elif current_order is None:
            print(f"⚠️  Zeile {index} gehört zu keinem Auftrag. Übersprungen.")
            continue
        
        current_order["lines"].append({
            "product_id": product.id,
            "product_uom_qty": quantity,
            "price_unit": price_unit,
            "x_SUPPL_Sansoft_auto": x_suppl_sansoft_auto,
            "product_uom": uom_id
        })
        
        if index % 1000 == 0:
            print(f"{index} Zeilen verarbeitet...")

#create sale orders
start = 0
for order_data in orders:
    lines = [(0, 0, line) for line in order_data["lines"]]
    
    order_vals = {
        "partner_id": order_data["partner_id"],
        "date_order": order_data["date_order"],
        "order_line": lines
    }
    
    order = env["sale.order"].create(order_vals)
    order.state = "sale"
    order.force_invoiced = True
    print(f"✔️  Created SO {order.name} with {len(lines)} lines.")
    
    start += 1
    if start >= limit:
        env.cr.commit()
        start = 0

env.cr.commit()
print("✅ Import abgeschlossen.")

#force insurance reports invoiced
insurance_invoices = env['suppl.insurance.invoicing.report'].search([("res_model", "=", "sale.order.line")])
start = 0
for inv in insurance_invoices:
    inv.healthcare_force_invoiced = True
    start += 1
    if start >= 10000:
        env.cr.commit()
        start = 0
        print("10.000er Batch abgearbeitet.")

env.cr.commit()
print("✅ Historische Versicherungsabrechnungen Fakturierung erzwungen.")
