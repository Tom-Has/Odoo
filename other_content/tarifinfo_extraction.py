#import packages
import pandas as pd
import os
import re
#import pathlib

#get spreadsheet files in target folder
source_path = "path/to/Tarifinfo_2025"
#file_list = list(pathlib.Path(source_path).glob('*.xlsx'))
file_list = [i for i in os.listdir(source_path) if re.search(r"\.xlsx$", i, re.IGNORECASE)]

#iterate through DF collection to extract tariff information
for file in file_list:
    complete_file = pd.ExcelFile(file)
    for sheet in complete_file.sheet_names:
        df = adjust_header(pd.read_excel(complete_file, sheet_name=sheet))
        

#eliminate irrelevant "header" rows and replace unnamed columns with tariff columns
def adjust_header(df):
    indices_to_drop = []
    pattern = 'pos\.?-?|lfd?\.?-?'  #needs rework potentially
    if sum(df.columns.str.contains(pattern, regex=True, case=False) == 0):
        for index, row in df.iterrows():
            if sum(row.str.contains(pattern, regex=True, case=False) >= 1):
                df = df.rename(columns=dict(zip(df.columns.tolist(), row.to_list())))
                indices_to_drop.append(index)
                break
            else:
                indices_to_drop.append(index)
        df = df.drop(indices_to_drop)
    return df

