import os
import gzip

def inspect_log_files(search_string_list):
    log_dir = '/home/odoo/logs'
    for file in os.listdir(log_dir):
        filename = os.fsdecode(file)
        full_path = os.path.join(log_dir, filename)
        counter_list = [0] * len(search_string_list)
        try:
            open_func = gzip.open if filename.endswith(".gz") else open
            with open_func(full_path, 'rt', errors='ignore') as log:
                for line in log:
                    for i, search_string in enumerate(search_string_list):
                        if search_string in line:
                            counter_list[i] += 1
            if any(counter_list):
                print(f"\n{filename} has:")
                for i, counter in enumerate(counter_list):
                    if counter > 0:
                        print(f"{counter} occurrences of '{search_string_list[i]}'.")
        except (OSError, gzip.BadGzipFile, UnicodeDecodeError) as e:
            print(f"\n{filename} konnte nicht gelesen werden ({type(e).__name__}).")
        except Exception as e:
            print(f"\nUnbekannter Fehler bei {filename}: {e}")
            continue

search_string_list = ['string1', 'string2', '...']
inspect_log_files(search_string_list)

"""
# Output exemplary:

odoo.log.2025-08-26.gz has:
48025 occurrences of 'string1'.

odoo.log.2025-08-30.gz has:
393 occurrences of 'string1'.

.ipynb_checkpoints konnte nicht gelesen werden (IsADirectoryError).
"""
