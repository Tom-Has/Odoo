# Duplikatgruppen SV-Nr. im Deduplizierungsmodell
id = <..>
dupe_model = env['data_merge.model'].browse(id)
dupe_groups = env['data_merge.group'].search([('model_id.id', '=', dupe_model)])
model_name = dupe_model.res_model_id.name

# Iteration ueber Duplikatgruppen:
for group in sv_dupe_groups:
    # Iteration uber Eintraege in Gruppe
    # Funktionaler Code hier
    
    for record in group:
        # Belasse den Eintrag mit Vema-Referenz, sonst mit Beginn Hauptversicherter, sonst beliebigen
        full_rec = env[model_name].browse(record.id)
