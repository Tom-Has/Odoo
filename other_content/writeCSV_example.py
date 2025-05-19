file_path = f"claims.csv"
f = open(file_path, "x")
f.write("ID,Partner_ID\n")

for claim in claims:
    f.write(str(claim.id) + "," + str(claim.partner_id.id) + "\n")

f.close()