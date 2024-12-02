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
    


    invalid_data = pd.DataFrame()

    for key, value in selected_options.items():
        #check if the value is equal the telephone
        if value == 'telephone':
            print("process phone data" + key + " " + value)
            df, invalid_data = process_phone_data(df,invalid_data,key,drop_duplicates=True)
        elif value == 'montant':
            print("convert to integer" + key + " " + value)
            df[key] = convert_to_integer_column(df[key])    
    
    

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
        name_valid_data=f'valid_{input_file.filename}',
        name_invalid_data=f'invalid_{input_file.filename}',
    )
    db.session.add(excel_file)
    db.session.commit()




    input_file.save(f'./uploads/{input_file.filename}')

    valid_output_file_path = f'./uploads/valid_{input_file.filename}'
    with open(valid_output_file_path, 'wb') as f:
        f.write(valid_output_file.read()) 

    invalid_data_output_file_path = f'./uploads/invalid_{input_file.filename}'
    with open(invalid_data_output_file_path, 'wb') as f:
        f.write(invalid_data_output_file.read())
    
    
 
    valid_output_file.seek(0)
    invalid_data_output_file.seek(0)

    
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        # Add the valid output file to the ZIP
        valid_output_file.seek(0)
        zip_file.writestr(f'valid_{input_file.filename}', valid_output_file.read())
        
        # Add the invalid output file to the ZIP
        invalid_data_output_file.seek(0)
        zip_file.writestr(f'invalid_{input_file.filename}', invalid_data_output_file.read())

    
    
    zip_buffer.seek(0)
    return send_file(
        zip_buffer,
        mimetype="application/zip",
        download_name="data_files.zip",
        as_attachment=True,
    )


@app.route("/get_all_file_excel" , methods=["GET"])
def return_all_file():
    #return all file from the database
    excel_files = ExcelFile.query.all()
    files = []
    print(excel_files)
    for file in excel_files:
        files.append({
            "id": file.id,
            "file_name": file.file_name,
            "name_valid_data": file.name_valid_data,
            "name_invalid_data": file.name_invalid_data,
            "uploaded_at": file.uploaded_at
        })
    return jsonify(files)

#get file by id 
@app.route("/get_file", methods=["GET"])
def get_file():
    id = request.args.get('id')
	return f"Received ID via GET query: {id}"

if __name__ == '__main__':
    app.run(debug=True)
