"""
Run this script via shell to create attachtments from base64 strings
"""

#variable arguments
path = "file_import.csv"

#constants
model = env['ir.attachment']
start = 0
limit = 1000

with open(path, 'r') as file:
    for index, line in enumerate(file):
        if index == 0:
            continue
        parts = line.strip().split(",")
        model.create({"key": parts[0], "datas": parts[1], "name": parts[2], "mimetype": parts[3], "type": parts[4], "res_model": parts[5], "description": parts[6]})
        start = start + 1
        if start >= limit:
            env.cr.commit()
            start = 0

env.cr.commit()