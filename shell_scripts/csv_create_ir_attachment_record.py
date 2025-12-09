"""
Run this script via shell to create attachtments from base64 strings
"""

#variable arguments
paths = ["encoded_pdfs_1.csv", "encoded_pdfs_2.csv", "encoded_pdfs_3.csv"]  # add paths as needed

#constants
att_model = env['ir.attachment']
res_model_string = 'res.model'    # change name as needed
start = 0
limit = 1000

for path in paths:
    with open(path, 'r') as file:
        for index, line in enumerate(file):
            if index == 0:
                continue
            parts = line.strip().split(",")
            name = "prefix-" + parts[0]    # adapt name as needed
            filename = name + ".pdf"    # construct file name as needed
            id = env[res_model_string].search([('name', '=', name)]).id # adapt filter as needed
            att_model.create({"key": parts[0], "datas": parts[1], "name": name, "res_name": filename, "mimetype": "application/pdf", "type": "binary", "res_model": res_model_string, "res_id": id})
            start += 1
            if start % limit == 0:
                env.cr.commit()
                print(f"Bisher {start} Dateien angelegt.")
        env.cr.commit()
        print(f"Fertig! {start} Dateien angelegt.")
