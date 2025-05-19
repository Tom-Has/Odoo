import os
import gzip

search_string_list = []
log_dir = os.path.join(os.getcwd(), "logs")

for file in os.listdir(log_dir):
    filename = os.fsdecode(file)
    full_path = os.path.join(log_dir, filename)
    
    # Zähler pro Datei initialisieren
    counter_list = [0] * len(search_string_list)
    
    # Dateiinhalt lesen (gzip oder normal)
    open_func = gzip.open if filename.endswith(".gz") else open
    
    with open_func(full_path, 'rt') as log:
        for line in log:
            for i, search_string in enumerate(search_string_list):
                if search_string in line:
                    counter_list[i] += 1
    
    # Ausgabe, wenn es Treffer gab
    for i, counter in enumerate(counter_list):
        if counter > 0:
            print(f"{filename} has {counter} occurrences of '{search_string_list[i]}'.")


"""
Mögliche SuchbegriffeN.
'action_archive'
'deleted ir.model.data records with IDs:'
...
"""
