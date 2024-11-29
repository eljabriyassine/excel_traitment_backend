import os
import json
from flask import Flask, request, send_file, jsonify
import pandas as pd
import xlsxwriter
from io import BytesIO
from flask_cors import CORS
from helper import process_phone_data,convert_to_integer_column
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.dialects.mysql import MEDIUMBLOB



app = Flask(__name__)
CORS(app)


# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123@localhost/gomobile'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Suppress warning


# Initialize SQLAlchemy
db = SQLAlchemy(app)

class ExcelFile(db.Model):
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    file_name = db.Column(db.String(255), nullable=False)
    file_data = db.Column(MEDIUMBLOB, nullable=False) 
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)


@app.route('/upload-excel', methods=['POST'])
def upload_excel():
    # Load the Excel file
    input_file = request.files['file']
    
    if not input_file:
        return jsonify({"error": "No file uploaded"}), 400

    return jsonify({"message": f'Excel file uploaded successfully {input_file.filename}'}), 201



@app.route('/test-db-connection')
def test_db_connection():
    try:
        # Create a connection to the database using SQLAlchemy's engine
        engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        connection = engine.connect()  # Try to establish a connection
        connection.close()  # Close the connection if successful
        
        print('Database connection successful!')
        return jsonify({"message": "Database connection successful!"}), 200
    except Exception as e:
        print('Error connecting to the database:', str(e))
        return jsonify({"error": str(e)}), 500

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

    print(output)
    output.seek(0)  
    # Save the file to the database
    excel_file = ExcelFile(
        file_name="returned_data.xlsx",
        file_data=output.read()
    )

    db.session.add(excel_file)
    db.session.commit()

    output.seek(0)  

    print(output)
    print("File saved to the database!")

    # Return the file for download
    return send_file(
        output,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        download_name="returned_data.xlsx",  # Set the download filename
        as_attachment=True,
    )


if __name__ == '__main__':
    app.run(debug=True)
