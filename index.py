import pandas as pd
import re
from helper import process_phone_data

# Example usage
input_file = './teste.csv'
output_file = './cleaned_data.csv'

# Process the file
cleaned_df = process_phone_data(input_file)

# Display the cleaned DataFrame
print(cleaned_df)
