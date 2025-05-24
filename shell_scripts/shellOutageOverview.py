import datetime

# start_date of RKSV outages to clear in Finanzonline
start_date = datetime.datetime(2024, 9, 1)

# path to save the csv result file
file_path = f"RKSV_outage_data_{start_date}.csv"
f = open(file_path, "x")

# load RKSV outage records
recent_outages = env['pos.rksv.signature.outage'].search([('outage_start', '>=', start_date)])

# csv header
f.write("Outage-ID,RKSV-Belegnr.,Odoo-Belegnr.,Belegdatum,Belegsumme,Start Ausfall,Ende Ausfall,Kasse\n")

# data according to header
for outage in recent_outages:
    if outage.outage_end and outage.outage_start:
        hours = (outage.outage_end - outage.outage_start).total_seconds() / 3600
        if hours >= 48:
            if outage.pos_config_id and outage.affected_receipt_ids:
                for rec in outage.affected_receipt_ids:
                    f.write(
                    str(outage.id) + "," +
                    rec.rksv_receipt_number + "," + 
                    rec.pos_reference + "," + 
                    rec.date_order_local + "," +
                    str(round(rec.amount_total, 2)) + "," +
                    outage.outage_start_local + "," +
                    outage.outage_end_local + "," +
                    outage.pos_config_id.name + "\n"
                    )
                    
# close file
f.close()

# to read and/or download result csv click 'EDITOR' tab and navigate to the directory path given at the beginning of the script
# if only a file name is given, the result csv is found on the level at which the terminal running the script was called


