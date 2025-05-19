"""
documentation:
https://pandas.pydata.org/docs/index.html
"""

#import packages as needed
import pandas as pd
import math
import re

#read data from single worksheet source
df = pd.read_excel('path.xlsx', sheet_name='optional')
df_workable = pd.read_excel('path.xlsx', sheet_name='optional', usecols=col_list)
#df_prepared = df_workable[usecols=col_list['id'] >= 0]
df_prepared = pd.read_excel('path.xlsx', sheet_name='optional').loc[lambda df: df['Nr'] > 0, col_list]
df_prepared = pd.read_excel('path.xlsx', sheet_name='optional', usecols=col_list).query("Nr > 0")
df = pd.read_csv('path.csv')

#read Excel file containing multiple worksheets
multi_sheet_file = pd.ExcelFile("path.xlsx")
sheet_list = multi_sheet_file.sheet_names
df_dict = {sheet: pd.read_excel(multi_sheet_file, sheet_name=sheet) for sheet in sheet_list}
df_dict.get(sheet_list[0])["col"].head(10)  #example for accessing column
df_dict.get(sheet_list[1]).iloc[:,1].head(10)   #example for accessing column with same position but different name across ExcelFile
"""
keys_list = list(df_dict.keys())    #obtain names for small dicts
df_one = df_dict.get(keys_list[0])
for key in df_dict.keys():
    print(key)
"""

#save data
df.to_excel('output_path.xlsx', sheet_name='optional', index=False)
df.to_csv('output_path.csv', index=False)

#save data to existing file
with pd.ExcelWriter('output_path.xlsx', mode='a') as writer:  
    df.to_excel(writer, sheet_name='new_sheet')

#save data to multiple worksheets
with pd.ExcelWriter('output_path.xlsx') as writer:
    """
    df_first.to_excel(writer, sheet_name="first", index=False)
    df_second.to_excel(writer, sheet_name="second", index=False)
    """
    df_dict.get(sheet).to_excel(writer, sheet_name=sheet, index=False) for sheet in sheet_list


#read columns
cols = df.columns.tolist()
list(df)
print(*df)

#read examples
df.head()
df.tail()

#select columns
filtered_df = df.filter(items=['a', 'b', 'c'], axis=1).copy()

#rename columns
df = df.rename(columns={"A": "a", "B": "b", "C": "c"})
df = df.rename(columns=mapping_object)

#delete columns
df_dropped = df.drop(columns=["a", "b"])

#check whether columns exist
for col in ["a", "b"]:
    print(f"{col} in df:", col in df.columns)

#select rows
filtered_df = df[df['a'] > x]

#sorting
df.sort_values(by=['a', 'b'], ascending=[False, True], inplace=True)

#group/aggregate
df_grouped = df.groupby('a', 'b', 'c')
sum = df.groupby('a', 'b', 'c')['val'].sum()
custom_result = df.groupby('a', 'b', 'c')['val'].agg(custom_function)

#select values
df[df["a"].isin(['val1','val2','val3'])][["a", "b", "c"]]

#merge
df_left = df_left.merge(
    df_right[optional_col_list],
    left_on=["left_key"],
    right_on=["right_key"],
    how="left"
)

#merge connection control
merged = df_left.merge(
    df_left[optional_col_list],
    left_on=["left_key"],
    right_on=["right_key"],
    how="left",
    indicator=True
)
df_left['df_connected'] = merged['_merge'] == 'both'

#merge excess control
merged = df_left.merge(df_right, indicator=True, how="outer")
merged["_merge"].value_counts()

#add column
df['new_col'] = df['ext_col'].function(args)
df['is_company'] = df['Branche'].map(lamdba x: 'FALSE' if x not in ['Patient'] and x else 'TRUE')

#add row
df = df.append({'key1': 'val1', 'key2': 'val2'}, ignore_index=True)
df = df.append([{'key1': 'val1', 'key2': 'val2'}, {'key1': 'val3', 'key2': 'val4'}], ignore_index=True)
df_new = pd.concat(df, df_other)

#unique values
print(df['a'].unique())

#remove duplicates
df_singulars = df.drop_duplicates(subset=["key1", "key2", "key3"])

#drop NaN values according to column
df = df.dropna(subset=['a', 'b'])

#value couunts
df["a"].map(type).value_counts()
df["b"].dropna().value_counts()

#fill empty cells with default
df = df.fillna(default_value)
df["a"] = df["a"].fillna(default_value)

#iterate rows
for index, row in df.iterrows():
    print(row['a'], row['b'])

#apply function
df["col"] = df.apply(func, axis=1)
df['col'] = df['other_col'].apply(func)

#check whether plausible number of values was determined
values = df["col"].notnull().sum()

#check whether variable is a Dataframe or Series or other type
type(df).__name__ == "DataFrame"
type(df["col"]).__name__ == "Series"
type(None).__name__ == "NoneType"
type(pd.NA).__name__ == "NAType"
type(pd.NaT).__name__ == "NaTType"