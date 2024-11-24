import pandas as pd

# Load the Excel file
df = pd.read_excel('./data.xlsx')

# Strip whitespace from column names
df.columns = df.columns.str.strip()

# Display the column names
print(df.columns)



# Convert the 'MNT IMP' column to integers
df['MNT IMP'] = df['MNT IMP'].apply(lambda x: int(x))

# Remove duplicates based only on the 'TEL CLIENT' column
df = df.drop_duplicates(subset=['TEL CLIENT'])




df['TEL CLIENT'] = df['TEL CLIENT'].astype(str).apply(lambda x: '0' + x[3:])

print(df.head())



# Save the modified DataFrame to a new Excel file
output_file = './transformed_data.xlsx'
df.to_excel(output_file, index=False)



print(f"File saved successfully as {output_file}")