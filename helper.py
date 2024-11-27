import pandas as pd
import re


def process_phone_data(df,name_col,drop_duplicates=False):
    
    
    # Remove duplicates based on the name_col column
    if drop_duplicates:
        df = df.drop_duplicates(subset=[name_col])
    
    # # Function to clean phone numbers
    def clean_phone_number(phone):
        # Use regex to remove spaces, dashes, or other non-digit characters
        cleaned = re.sub(r"[^\d+]", "", phone)
        return cleaned
    
    # Apply cleaning to name_col column
    df.loc[:, name_col] = df[name_col].astype(str).apply(clean_phone_number)
    
    
    # Add '0' to numbers with length 9
    df.loc[:, name_col] = df[name_col].apply(lambda x: '0' + x if len(x) == 9 else x)
    
    # Replace numbers starting with +212 or 00212 with 0
    df.loc[:, name_col]  = df[name_col].apply(lambda x: '0' + x[4:] if x.startswith('+212') else x)
    df.loc[:, name_col]  = df[name_col].apply(lambda x: '0' + x[3:] if x.startswith('212') else x)
    df.loc[:, name_col]  = df[name_col].apply(lambda x: '0' + x[5:] if x.startswith('00212') else x)
    
    # Remove rows where the length of name_col is not 10
    df = df.loc[
        (df[name_col].str.startswith(('05', '06', '07', '08')))
    ]
    #Remove rows where the length of name_col is not 10
    df = df.loc[
        (df[name_col].str.len() == 10)
    ]

    # print(df.head(10))
    
    return df


def convert_to_integer_column(series):
    return series.apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)