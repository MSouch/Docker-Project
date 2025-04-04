import pymysql
pymysql.install_as_MySQLdb()

from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@db/StudentDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
app.config['JWT_SECRET_KEY'] = 'your-secure-secret-key'  
db = SQLAlchemy(app)
jwt = JWTManager(app)

class Student(db.Model):
    __tablename__ = 'student' 
    studentID = db.Column(db.String(80), primary_key=True)
    studentName = db.Column(db.String(120), nullable=False)
    course = db.Column(db.String(80), nullable=False)
    presentDate = db.Column(db.String(80), nullable=False)

@app.route('/')
def home():
    
    # Query all students from the database
    students = Student.query.all()
    return render_template('index.html', students=students)

@app.route('/student', methods=['POST'])
def create_student():
    data = request.get_json()
    existing_student = Student.query.get(data['studentID'])
    if existing_student:
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

@app.route('/add-student', methods=['POST'])
def add_student():
    studentID = request.form['studentID']
    studentName = request.form['studentName']
    course = request.form['course']
    presentDate = request.form['presentDate']

    existing_student = Student.query.get(studentID)
    if (existing_student):
        return render_template('index.html', 
                               students=Student.query.all(), 
                               error_message='Student already exists')

    new_student = Student(
        studentID=studentID,
        studentName=studentName,
        course=course,
        presentDate=presentDate
    )

    db.session.add(new_student)
    db.session.commit()

    return render_template('index.html', 
                           students=Student.query.all(), 
                           success_message='Student created successfully!')

@app.route('/student/<string:studentID>', methods=['GET', 'PUT', 'DELETE'])
def manage_student(studentID):
    # For PUT requests
    if request.method == 'PUT':
        student = Student.query.get(studentID)
        if not student:
            return jsonify({'message': 'student not found'}), 404
        
        data = request.get_json()
        
        # Update student properties if they exist in the request
        if 'studentName' in data:
            student.studentName = data['studentName']
        if 'course' in data:
            student.course = data['course']
        if 'presentDate' in data:
            student.presentDate = data['presentDate']
        
        db.session.commit()
        return jsonify({
            'message': 'student updated successfully',
            'student': {
                'studentID': student.studentID,
                'studentName': student.studentName,
                'course': student.course,
                'presentDate': student.presentDate
            }
        }), 200
    
    # For GET requests
    if request.method == 'GET':
        student = Student.query.get(studentID)
        if not student:
            return jsonify({'message': 'student not found'}), 404
        
        return jsonify({
            'student': {
                'studentID': student.studentID,
                'studentName': student.studentName,
                'course': student.course,
                'presentDate': student.presentDate
            }
        }), 200
    
    # Handle DELETE request
    if request.method == 'DELETE':
        student = Student.query.get(studentID)
        if not student:
            return jsonify({'message': 'Student not exists'}), 404
        
        db.session.delete(student)
        db.session.commit()
        return jsonify({'message': 'Student deleted successfully'}), 200

# Login endpoint to issue tokens
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'message': 'Missing username or password'}), 400
        
    if data['username'] == 'admin' and data['password'] == 'password':
        access_token = create_access_token(identity=data['username'])
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

# Protected endpoint 
@app.route('/protected-students', methods=['GET'])
@jwt_required()
def protected_students():
    current_user = get_jwt_identity()
    students = Student.query.all()
    return jsonify(
        logged_in_as=current_user,
        students=[{
            'studentID': s.studentID,
            'studentName': s.studentName, 
            'course': s.course,
            'presentDate': s.presentDate
        } for s in students]
    ), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=8080, debug=True)