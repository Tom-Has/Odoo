import os
import gzip

def inspect_log_files(search_string_list):
    log_dir = '/home/odoo/logs'
    for file in os.listdir(log_dir):
        try:
            filename = os.fsdecode(file)
            full_path = os.path.join(log_dir, filename)       
            counter_list = [0] * len(search_string_list)
            open_func = gzip.open if filename.endswith(".gz") else open
            with open_func(full_path, 'rt') as log:
                for line in log:
                    for i, search_string in enumerate(search_string_list):
                        if search_string in line:
                            counter_list[i] += 1
            if not all(item == 0 for item in counter_list):
                print(f"\n{filename} has:")
                for i, counter in enumerate(counter_list):
                    if counter > 0:
                        print(f"{counter} occurrences of '{search_string_list[i]}'.")
              # bekannte Fehlerarten gezielt abfangen
        except (OSError, gzip.BadGzipFile, UnicodeDecodeError) as e:
            print(f"\n{filename} konnte nicht gelesen werden ({type(e).__name__}).")
        except Exception as e:
            print(f"\nUnbekannter Fehler bei {filename}: {e}")
            continue

