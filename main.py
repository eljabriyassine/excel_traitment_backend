import os
from flask import Flask, request, send_file, jsonify
import pandas as pd
import xlsxwriter
from io import BytesIO
from flask_cors import CORS
from helper import process_phone_data

app = Flask(__name__)
CORS(app)


@app.route("/process_excel", methods=["POST"])
def read_and_return():
    # Load the Excel file
	file = request.files['file']
	
	#check if no file uploaded 
	if not file:
		return jsonify({"error": "No file uploaded"}), 400

	df = pd.read_excel(file)


	#sleep from 3 seconds
	import time
	time.sleep(3)


	# Strip whitespace from column names
	df.columns = df.columns.str.strip()

	# Convert the 'MNT IMP' column to integers
	df['MNT IMP'] = df['MNT IMP'].apply(lambda x: int(x))

	cleaned_df = process_phone_data(file)



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
