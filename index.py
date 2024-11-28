import pandas as pd

def process_phone_data(df, name_col, drop_duplicates=False):
    # Print the dataframe before removing duplicates
    print("Before dropping duplicates:")
    print(df.head())
    
    # Remove duplicates based on the name_col column
    if drop_duplicates:
        df = df.drop_duplicates(subset=[name_col])
    
    # Print the dataframe after removing duplicates
    print("After dropping duplicates:")
    print(df.head())
    
    # Convert the 'MNT IMP' column to integers (if it's a numeric column)
    if 'MNT IMP' in df.columns:
        df['MNT IMP'] = df['MNT IMP'].astype(int)
    
    return df

# Sample data
data = {
    'TEL CLIENT': ['0661250473', '0661250473', '0661772696', '0661250473'],
    'TIERS': [2802966, 3174265, 2894456, 3174224],
    'MNT IMP': [50946.65, 18924.38, 15370.78, 18414.38]
}

df = pd.DataFrame(data)

# Call the function with drop_duplicates set to True
df_cleaned = process_phone_data(df, 'TEL CLIENT', drop_duplicates=True)

# View the cleaned DataFrame
print("Cleaned data:")
print(df_cleaned)
