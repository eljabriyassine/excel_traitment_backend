import pandas as pd

# Load the Excel file
df = pd.read_excel('./data.xlsx')

# Strip whitespace from column names
df.columns = df.columns.str.strip()

# Remove duplicates based only on the 'TEL CLIENT' column
df = df.drop_duplicates(subset=['TEL CLIENT'])

# Function to transform numbers in the first column
def transform_number(num):
    num_str = str(num)  # Convert the number to a string
    if len(num_str) == 9:  # If the number has exactly 9 digits
	print(num_str)
        return '123' + num_str  # Add prefix or a specific number (e.g., '123')
    elif num_str.startswith('+212'):  # If the number starts with '+212'
        return '0' + num_str[4:]  # Replace '+212' with '0'
    else:
        return num_str  # Return unchanged for all other cases

# Apply the transformation to the first column
df['TEL CLIENT'] = df['TEL CLIENT'].apply(transform_number)

# Display the transformed data

# Save the modified DataFrame to a new Excel file
output_file = './transformed_data.xlsx'
df.to_excel(output_file, index=False)

print(f"File saved successfully as {output_file}")
