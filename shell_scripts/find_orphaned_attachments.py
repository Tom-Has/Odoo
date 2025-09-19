import os
import psycopg2

# DB connection
# conn = psycopg2.connect("dbname=mydb user=odoo password=*** host=localhost")
conn = psycopg2.connect("dbname=mydb")  # user odoo is logged in directly in odoo.sh shell 
cur = conn.cursor()

# fetch referenced files
cur.execute("SELECT store_fname FROM ir_attachment WHERE store_fname IS NOT NULL;")
db_files = set(row[0] for row in cur.fetchall())

# fetch all files in filestore
filestore_path = "/data/filestore/mydb" # odoo.sh standard path to filestore
fs_files = set()
for root, _, files in os.walk(filestore_path):
    for f in files:
        rel_path = os.path.relpath(os.path.join(root, f), filestore_path)
        fs_files.add(rel_path)

# determine orphaned files (in filestore but not in DB)
orphans = fs_files - db_files

# display exemplary or all orphaned files
max_display = 10
print(f"found orphaned files: {len(orphans)}")
for o in list(orphans)[:max_display]:  # show only first max_display
    print(o)
