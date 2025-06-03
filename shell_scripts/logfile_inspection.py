import os
import gzip

search_string_list = [
    'Ignored mail from "Sales AT | neoom" <sales.at@neoom.com> to er@wirsindsolarunger.odoo.com',
    'Routing mail from "Sales AT | neoom" <sales.at@neoom.com> to er@wirsindsolarunger.odoo.com'
]
log_dir = os.path.join(os.getcwd(), "logs")

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
    except:
        print(f"\n{filename} is not of type .gz or text file.")
        continue


"""
Mögliche SuchbegriffeN.
'action_archive'
'deleted ir.model.data records with IDs:'
'Ignored mail from "Sales AT | neoom" <sales.at@neoom.com>'
'Ignored mail from "Sales AT | neoom" <sales.at@neoom.com> to er@wirsindsolarunger.odoo.com,"er@wirsindsolarunger.odoo.com" <er@wirsindsolarunger.odoo.com>'
'Routing mail from "Sales AT | neoom" <sales.at@neoom.com> to er@wirsindsolarunger.odoo.com,"er@wirsindsolarunger.odoo.com" <er@wirsindsolarunger.odoo.com>'
...
"""
