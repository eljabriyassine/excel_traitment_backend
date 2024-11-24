import os
from flask import Flask, request, send_file, jsonify
import pandas as pd
import xlsxwriter
from io import BytesIO
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/process_excel", methods=["POST"])
def read_and_return():
    # Load the Excel file
	file_path = "./data.xlsx"  # Replace with your file path
	df = pd.read_excel(file_path)

	# Strip whitespace from column names
	df.columns = df.columns.str.strip()

	# Convert the 'MNT IMP' column to integers
	df['MNT IMP'] = df['MNT IMP'].apply(lambda x: int(x))

	# Remove duplicates based only on the 'TEL CLIENT' column
	df = df.drop_duplicates(subset=['TEL CLIENT'])

	# Modify 'TEL CLIENT' column
	df['TEL CLIENT'] = df['TEL CLIENT'].astype(str).apply(lambda x: '0' + x[3:])


	output = BytesIO()
	with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
		df.to_excel(writer, index=False, sheet_name="Sheet1")

	output.seek(0)  

	# Return the file for download
	return send_file(
		output,
		mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
		download_name="returned_data.xlsx",  # Set the download filename
		as_attachment=True,
	)






if __name__ == '__main__':
    app.run(debug=True)
