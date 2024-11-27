import pandas as pd
import re


def process_phone_data(df,name_col,drop_duplicates=False):
    
    # Convert the 'MNT IMP' column to integers
    # df['MNT IMP'] = df['MNT IMP'].apply(lambda x: int(x))
    
    # Remove duplicates based on the name_col column
    if drop_duplicates:
        df = df.drop_duplicates(subset=[name_col])

	
    
    # Function to clean phone numbers
    def clean_phone_number(phone):
        # Use regex to remove spaces, dashes, or other non-digit characters
        cleaned = re.sub(r"[^\d+]", "", phone)
        return cleaned
    
    # Apply cleaning to name_col column
    df[name_col] = df[name_col].astype(str).apply(clean_phone_number)
    
    
    # Add '0' to numbers with length 9
    df[name_col] = df[name_col].apply(lambda x: '0' + x if len(x) == 9 else x)
    
    # Replace numbers starting with +212 or 00212 with 0
    df[name_col] = df[name_col].apply(lambda x: '0' + x[4:] if x.startswith('+212') else x)
    df[name_col] = df[name_col].apply(lambda x: '0' + x[5:] if x.startswith('00212') else x)
    
    # Remove rows where the length of name_col is not 10
    df = df[df[name_col].str.len() == 10]
    
    return df


def convert_to_integer(df,col):
    df[col] = df[col].apply(lambda x: int(x))
    return df