import os
import json
from flask import Flask, request, send_file, jsonify
import pandas as pd
from flask_sqlalchemy import SQLAlchemy

import xlsxwriter
from io import BytesIO
from flask_cors import CORS
from helper import process_phone_data,convert_to_integer_column

app = Flask(__name__)
CORS(app)


# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123'
app.config['MYSQL_DB'] = 'my_database'


@app.route("/process_excel", methods=["POST"])
def read_and_return():
    # Load the Excel file
    input_file = request.files['file']
    selected_options_str = request.form.get("selectedOptions")
    
    selected_options = json.loads(selected_options_str)


    print(selected_options)

   
    
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
        raise ValueError(f"Unsupported file format: {file_extension}")

    # Convert the 'MNT IMP' column to integers


    for key, value in selected_options.items():
        #check if the value is equal the telephone
        if value == 'telephone':
            print("process phone data" + key + " " + value)
            df = process_phone_data(df,key,drop_duplicates=True)
        elif value == 'montant':
            print("convert to integer" + key + " " + value)
            df[key] = convert_to_integer_column(df[key])
    
    

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
