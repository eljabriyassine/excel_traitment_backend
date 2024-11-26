import pandas as pd
import re
import os 


def process_phone_data(input_file):
    """
    Processes phone number data in a CSV file.
    
    Args:
        input_file (str): Path to the input CSV file.
        
    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """

	#determine the file extension
	# file_extension = os.path.splitext(input_file)[1]
	file_extension = os.path.splitext(input_file)[1].lower() 

	#check if the file is an excel file
	if file_extension == '.csv':
		df.read_csv(input_file)
	elif file_extension == '.xlsx':
        df = pd.read_excel(input_file, engine='openpyxl')
	elif file_extension == '.xls':
        df = pd.read_excel(input_file, engine='xlrd')

    
    # Strip whitespace from column names
    df.columns = df.columns.str.strip()
    
    # Convert the 'MNT IMP' column to integers
    df['MNT IMP'] = df['MNT IMP'].apply(lambda x: int(x))
    
    # Remove duplicates based on the 'TEL CLIENT' column
    df = df.drop_duplicates(subset=['TEL CLIENT'])
    
    # Function to clean phone numbers
    def clean_phone_number(phone):
        # Use regex to remove spaces, dashes, or other non-digit characters
        cleaned = re.sub(r"[^\d+]", "", phone)
        return cleaned
    
    # Apply cleaning to 'TEL CLIENT' column
    df['TEL CLIENT'] = df['TEL CLIENT'].astype(str).apply(clean_phone_number)
    
    # Add '0' to numbers with length 9
    df['TEL CLIENT'] = df['TEL CLIENT'].apply(lambda x: '0' + x if len(x) == 9 else x)
    
    # Replace numbers starting with +212 or 00212 with 0
    df['TEL CLIENT'] = df['TEL CLIENT'].apply(lambda x: '0' + x[4:] if x.startswith('+212') else x)
    df['TEL CLIENT'] = df['TEL CLIENT'].apply(lambda x: '0' + x[5:] if x.startswith('00212') else x)
    
    # Remove rows where the length of 'TEL CLIENT' is not 10
    df = df[df['TEL CLIENT'].str.len() == 10]
    
    
    return df
