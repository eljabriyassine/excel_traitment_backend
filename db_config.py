from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create SQLAlchemy instance
db = SQLAlchemy()

class ExcelFile(db.Model):
    __tablename__ = 'excel_files'  # Optional: specify table name
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    file_name = db.Column(db.String(255), nullable=False)
    name_valid_data = db.Column(db.String(255))
    name_invalid_data = db.Column(db.String(255))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
