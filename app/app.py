# filepath: app/app.py
import pymysql
pymysql.install_as_MySQLdb()

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@db/students'
db = SQLAlchemy(app)

class Student(db.Model):
    studentID = db.Column(db.String(80), primary_key=True)
    studentName = db.Column(db.String(120), nullable=False)
    course = db.Column(db.String(80), nullable=False)
    presentDate = db.Column(db.String(80), nullable=False)

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Welcome to the Student API"}), 200

@app.route('/student', methods=['POST'])
def create_student():
    data = request.get_json()
    existing_student = Student.query.get(data['studentID'])
    if (existing_student):
        return jsonify({'message': 'student already exists'}), 409
        
    new_student = Student(
        studentID=data['studentID'],
        studentName=data['studentName'],
        course=data['course'],
        presentDate=data['presentDate']
    )
    
    db.session.add(new_student)
    db.session.commit()
    return jsonify({'message': 'student created successfully'}), 201

@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)