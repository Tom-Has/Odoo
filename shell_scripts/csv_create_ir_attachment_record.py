"""
Run this snippet via shell to create attachtments from base64 strings
"""

# files or paths to files
paths = ["encoded_pdfs.csv"]  # add or adpapt paths as needed

# constants
att_model = env['ir.attachment']
res_model_string = 'res.model'    # change name as needed
counter = 0
limit = 1000

# writing iteration
for path in paths:
    with open(path, 'r') as file:
        for index, line in enumerate(file):
            if index == 0:
                continue
            parts = line.strip().split(",")
            name = "prefix-" + parts[0]    # adapt name as needed
            filename = name + ".pdf"    # construct file name as needed
            id = env[res_model_string].search([('name', '=', name)]).id # adapt filter as needed
            att_model.create({
                "key": parts[0],
                "datas": parts[1],
                "name": name,
                "res_name": filename,
                "res_model": res_model_string,
                "res_id": id,
                "mimetype": "application/pdf",
                "type": "binary"
            })
            counter += 1
            if counter % limit == 0:
                env.cr.commit()
                print(f"Bisher {counter} Dateien angelegt.")
        env.cr.commit()
        print(f"Fertig! {counter} Dateien angelegt.")
