import pandas as pd
import re


def process_phone_data(df, invalid_data, name_col, drop_duplicates=False):
    import re

    # Function to clean phone numbers
    def clean_phone_number(phone):
        # Use regex to remove spaces, dashes, or other non-digit characters
        return re.sub(r"[^\d+]", "", phone)

    # Clean the phone numbers
    df[name_col] = df[name_col].astype(str).apply(clean_phone_number)

    # Add '0' to numbers with length 9
    df[name_col] = df[name_col].apply(lambda x: '0' + x if len(x) == 9 else x)

    # Normalize numbers starting with country codes
    df[name_col] = df[name_col].apply(lambda x: '0' + x[4:] if x.startswith('+212') else x)
    df[name_col] = df[name_col].apply(lambda x: '0' + x[3:] if x.startswith('212') else x)
    df[name_col] = df[name_col].apply(lambda x: '0' + x[5:] if x.startswith('00212') else x)

    # Remove rows where the length of name_col is not 10
    invalid_length = df.loc[df[name_col].str.len() != 10].copy()  # Create a copy to avoid warnings
    invalid_length["reason"] = "phone number length"
    invalid_data = pd.concat([invalid_data, invalid_length], ignore_index=True)
    df = df.loc[df[name_col].str.len() == 10]

    # Remove rows not starting with specific prefixes
    invalid_prefix = df.loc[~df[name_col].str.startswith(('05', '06', '07', '08'))].copy()
    invalid_prefix["reason"] = "phone number prefix"
    invalid_data = pd.concat([invalid_data, invalid_prefix], ignore_index=True)
    df = df.loc[df[name_col].str.startswith(('05', '06', '07', '08'))]

    # Remove duplicates based on the name_col column
    if drop_duplicates:
        duplicates = df[df.duplicated(subset=[name_col], keep='first')].copy()
        duplicates["reason"] = "Duplicate phone number"
        invalid_data = pd.concat([invalid_data, duplicates], ignore_index=True)
        df = df.drop_duplicates(subset=[name_col], keep='first')

    return df, invalid_data



def convert_to_integer_column(df, invalid_data, key):
    # Identify rows where the value cannot be converted to a numeric type
    invalid_rows = df[df[key].apply(pd.to_numeric, errors='coerce').isna()]

    # Add a reason column to the invalid rows
    invalid_rows = invalid_rows.copy() 
    invalid_rows["reason"] = f"Invalid montant"

    # Append the invalid rows to invalid_data
    invalid_data = pd.concat([invalid_data, invalid_rows], ignore_index=True)

    # Remove invalid rows from the original dataframe
    df = df.drop(invalid_rows.index)

    # Convert valid rows to numeric
    df[key] = df[key].apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)

    return df, invalid_data