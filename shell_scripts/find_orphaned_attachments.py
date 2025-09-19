import os
import psycopg2

# DB connection
# conn = psycopg2.connect("dbname=myDB user=odoo password=*** host=localhost")
conn = psycopg2.connect("dbname=myDB")  # user odoo is logged in directly in odoo.sh shell 
cur = conn.cursor()

# fetch files referenced in DB
cur.execute("SELECT store_fname FROM ir_attachment WHERE store_fname IS NOT NULL;")
db_files = set(row[0] for row in cur.fetchall())

# fetch all files in filestore
filestore_path = "/home/odoo/data/filestore/myDB" # odoo.sh standard path to filestore
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

# calculate size of files
total_size = 0
orphan_info = []
for rel_path in orphans:
    full_path = os.path.join(filestore_path, rel_path)
    size = os.path.getsize(full_path)
    total_size += size
    orphan_info.append((rel_path, size))

# display size in MB
print(f"found orphaned files: {len(orphan_info)}")
print(f"total size of orphaned files: {total_size/(1024*1024):.2f} MB")

# display max_display files ordered by size
for path, size in sorted(orphan_info, key=lambda x: x[1], reverse=True)[:max_display]:
    print(f"{path}: {size/1024/1024:.2f} MB")

# create text file of orphaned files for subsequent deletion
with open("orphans.txt", "w") as out:
    for o in orphans:
        out.write(o + "\n")
print(f"{len(orphans)} verwaiste Dateien in orphans.txt gespeichert.")

"""
# use this snippet in the shell for deletion if necessary

# examine
wc -l orphans.txt
head orphans.txt

# delete
while read -r line; do
    rm -f "/home/odoo/data/filestore/myDB/$line"
done < orphans.txt
"""
