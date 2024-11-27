import pandas as pd
import re
from helper import process_phone_data,convert_to_integer


# Example usage
input_file = './compagne.xlsx'
# input_file2 = './teste.csv'

# Process the file

df=pd.read_excel(input_file)
cleaned_df = process_phone_data(df,'Tél_Client',drop_duplicates=True)
cleaned_df = convert_to_integer(df,'Nbre_IMP')
cleaned_df = convert_to_integer(df,'Mnt Imp')


# print(cleaned_df.head(10))

#save the cleaned data to a new excel file
cleaned_df.to_excel('hello.xlsx', index=False)

# print(df.head())
# print(cleaned_df2)


