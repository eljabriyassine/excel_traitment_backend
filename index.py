import pandas as pd
import re
from helper import process_phone_data,convert_to_integer_column


# Example usage
input_file = './compagne.xlsx'

# Process the file

	
df=pd.read_excel(input_file)
df = process_phone_data(df,'Tél_Client',drop_duplicates=True)
df = process_phone_data(df,'Tél_ Gestionnaire',drop_duplicates=False)
df['Nbre_IMP'] = convert_to_integer_column(df['Nbre_IMP'])
df['Mnt Imp'] = convert_to_integer_column(df['Mnt Imp'])


print(df.head(10))

#save the cleaned data to a new excel file
df.to_excel('cleaned_data.xlsx', index=False)

# print(df.head())
# print(cleaned_df2)


