import os
import json
from flask import Flask, request, send_file, jsonify
import pandas as pd
import xlsxwriter
from io import BytesIO
from flask_cors import CORS
from helper import process_phone_data,convert_to_integer_column
from datetime import datetime

from db_config import db, ExcelFile  
import zipfile



app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123@localhost/gomobile'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the app
db.init_app(app)



#endoipoit say Hello 
@app.route("/", methods=["GET"])
def hello():
	return "Hello, World! :)"

@app.route("/process_excel", methods=["POST"])
def read_and_return():
	# Load the Excel file
	input_file = request.files['file']
	selected_options_str = request.form.get("selectedOptions")
	
	selected_options = json.loads(selected_options_str)


	
	#check if no file uploaded 
	if not input_file:
		return jsonify({"error": "No file uploaded"}), 400

	file_extension = input_file.filename.split('.')[-1].lower() 

	 #check if the file is an excel file
	if file_extension == 'csv':
		df = pd.read_csv(input_file)
	elif file_extension == 'xlsx':
		df = pd.read_excel(input_file, engine='openpyxl')
	elif file_extension == 'xls':
		df = pd.read_excel(input_file, engine='xlrd')
	else:
		return jsonify({"error": f"Unsupported file format: {file_extension}"}), 400
	
	#check if the file is empty
	if df.empty:
		return jsonify({"error": "File is empty"}), 400

	size = df.shape[0]
	#check if the file has empty header
	# Check if any column header is empty or contains 'Unnamed'
	headers = df.columns.tolist()
	for header in headers:
		
		if len(header.strip()) == 0 or 'unnamed' in header.lower():
			 # Save the file to the database
			excel_file = ExcelFile(
				file_name=input_file.filename,
				size=size,
				raison="Empty header found in the file"
			)
			db.session.add(excel_file)
			db.session.commit()
			#return with the index of column of invalid data
			
			# return jsonify({"error": "Empty header found in the file"}), 400


	invalid_data = pd.DataFrame()

	for key, value in selected_options.items():
		#check if the value is equal the telephone
		if value == 'telephone':
			df, invalid_data = process_phone_data(df,invalid_data,key,drop_duplicates=True)
		elif value == 'montant':
			df,invalid_data = convert_to_integer_column(df,invalid_data,key)    
	
	
 
	valid_output_file = BytesIO()
	with pd.ExcelWriter(valid_output_file, engine="xlsxwriter") as writer:
		df.to_excel(writer, index=False, sheet_name="Valid data")

	valid_output_file.seek(0)  

	# Save the invalid data to a separate sheet
	invalid_data_output_file = BytesIO()
	with pd.ExcelWriter(invalid_data_output_file, engine="xlsxwriter") as writer:
		invalid_data.to_excel(writer, index=False, sheet_name="Invalid Data")
		
	invalid_data_output_file.seek(0)


	 # Save the file to the database
	excel_file = ExcelFile(
		file_name=input_file.filename,
		size=size,
		name_valid_data=f'valid_{input_file.filename}',
		name_invalid_data=f'invalid_{input_file.filename}',
	)
	db.session.add(excel_file)
	db.session.commit()

	#check	if the file is saved in the database
	if not excel_file.id:
		return jsonify({"error": "Failed to save file to database"}), 500

	new_id = excel_file.id



	os.makedirs(f'./uploads/{new_id}')

	input_file.save(f'./uploads/{new_id}/{input_file.filename}')

	valid_output_file_path = f'./uploads/{new_id}/valid_{input_file.filename}'
	with open(valid_output_file_path, 'wb') as f:
		f.write(valid_output_file.read()) 

	invalid_data_output_file_path = f'./uploads/{new_id}/invalid_{input_file.filename}'
	with open(invalid_data_output_file_path, 'wb') as f:
		f.write(invalid_data_output_file.read())
	
	

	return jsonify({"message": "File processed successfully"})


@app.route("/get_all_file_excel" , methods=["GET"])
def return_all_file():
	#return all file from the database describe reverse
	data = request.args
	file_name = data.get('file_name')
	print(file_name)
	if file_name:
		excel_files = ExcelFile.query.filter(ExcelFile.file_name.like(f'%{file_name}%')).all()
	else:
		excel_files = ExcelFile.query.order_by(ExcelFile.id.desc()).limit(20).all()
	print(len(excel_files))
	if len(excel_files) == 0:
		return jsonify({"message": "No file found"}), 404

	files = []
	for file in excel_files:
		files.append({
			"id": file.id,
			"file_name": file.file_name,
			"size": file.size,
			"name_valid_data": file.name_valid_data,
			"name_invalid_data": file.name_invalid_data,
			"uploaded_at": file.uploaded_at,
			"raison": file.raison
		})
	return jsonify(files)

@app.route("/get_file_by_file_name", methods=["GET"])
def get_file_by_file_name():
	data = request.args
	file_name = data.get('file_name')

	if not file_name:
		return jsonify({"error": "No file name provided"}), 400

	excel_file = ExcelFile.query.filter_by(file_name=file_name).all()
	if not excel_file:
		return jsonify({"error": "File not found"}), 404

	return jsonify({
		"id": excel_file.id,
		"file_name": excel_file.file_name,
		"size": excel_file.size,
		"name_valid_data": excel_file.name_valid_data,
		"name_invalid_data": excel_file.name_invalid_data,
		"uploaded_at": excel_file.uploaded_at,
		"raison": excel_file.raison
	})

#get file by id 
@app.route("/download_file", methods=["GET"])
def get_file():

    data = request.args  
    file_id = data.get('id')
    file_type = data.get('type')

    if not file_id:
        return jsonify({"error": "No file ID provided"}), 400
    if not file_type:
        return jsonify({"error": "No file type provided"}), 400

    # Retrieve the data from the database based on the id
    excel_file = ExcelFile.query.filter_by(id=file_id).first()
    if not excel_file:
        return jsonify({"error": "File not found"}), 404

    # Construct the file path
    file_path = f'./uploads/{file_id}/{file_type}_{excel_file.file_name}'
    
    # Validate and ensure file exists
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found on the server"}), 404

    try:
        return send_file(
            file_path,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            download_name=excel_file.file_name,
            as_attachment=True
        )
    except Exception as e:
        return jsonify({"error": f"Failed to send file: {str(e)}"}), 500

if __name__ == '__main__':
	app.run(debug=True)
