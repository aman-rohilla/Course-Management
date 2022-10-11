from flask import Flask, request, jsonify
# import bcrypt as bcrypt_lib
from werkzeug.security import generate_password_hash, check_password_hash

from flask_jwt_extended import (
  JWTManager, jwt_required, 
  create_access_token, get_jwt_identity
)

from datetime import timedelta
from course import Course

from vars import Role
from user import User, users
from role_validator import role_required
from bson import ObjectId
from flask_cors import CORS

app = Flask(__name__)
CORS(app)



app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=7)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=14)
app.config['JWT_SECRET_KEY'] = 'jvdhgshemcuihchetriugrhohrdiftguieludrnygkty'


jwt = JWTManager(app)

@app.route('/register', methods=['POST'])
def register():
  result = User.parse_user(request.json)
  if(type(result) != User):
    return {'success': False, 'msg': result}

  user = result
  # user.password = bcrypt_lib.hashpw(user.password.encode('utf-8'), bcrypt_lib.gensalt()).decode('utf-8')
  user.password = generate_password_hash(user.password, 'sha256')
  result = user.create()
  if result != True: 
    return {'success': False, 'msg': result}

  return {'success': True, "access_token": user.gen_access_token(), 'refresh_token': user.gen_refresh_token()}


@app.route('/login', methods=['POST'])
def login():
  email = None
  password = None
  try:
    email = request.json.get('email', None)
    password = request.json.get('password', None)
  except Exception:
    return {'success': False, 'msg': 'JSON data was expected in request body'}

  email = email.strip()
  password = password.strip()

  if not email or not password:
    return {'success': False, 'msg': 'Email and/or password was not provided'}
  
  user = User.find({'email': email})
  if not user:
    return {'success': False, 'msg': f'{email} is not registered'}, 404

  
  # if bcrypt_lib.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
  if check_password_hash(user.password, password):
    return {'success': True, "access_token": user.gen_access_token(), 'refresh_token': user.gen_refresh_token()}
  else:
    return {'success': False, 'msg': 'Password incorrect'}


@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
  current_user = get_jwt_identity()
  return current_user


@app.route("/admin", methods=["GET"])
@role_required({Role.ADMIN})
def admin():
  # current_user = get_jwt_identity()
  return jsonify(msg='Hello Admin', success=True)

@app.route("/users", methods=["GET"])
@role_required({Role.ADMIN})
def get_all_users():
  user_list = list(users.find({}, {'password': 0}))
  for i in range(len(user_list)):
    user_list[i]['_id'] = str(user_list[i]['_id'])

  return {'success': True, 'users': user_list}



@app.route("/refresh", methods=["GET"])
@jwt_required(refresh=True)
def refresh():
  identity = get_jwt_identity()
  access_token = create_access_token(identity=identity)
  return jsonify(success=True, access_token=f'Bearer {access_token}')


@app.route("/course", methods=['POST'])
@role_required({Role.TEACHER})
def publish_course():
  name = None
  try:
    name = request.json['name'].strip()
  except Exception:
    return {'success': False, 'msg': 'JSON data was expected in request body'}

  teacher = get_jwt_identity()
  course = Course(name=name, teacher=teacher['name'], teacher_id=teacher['_id'])

  result = course.publish()
  if result != True: 
    return {'success': False, 'msg': result}

  return {'success': True, 'msg': 'Course Published'}

@app.route("/course/<id>", methods=['PUT'])
@role_required({Role.TEACHER})
def update_course(id):
  name = None
  try:
    name = request.json['name'].strip()
  except Exception:
    return {'success': False, 'msg': 'JSON data was expected in request body'}

  course = Course.find({'_id': ObjectId(id)})
  if not course: 
    return {'success': False, 'msg': f'No course found with name as {name}'}

  course.update(name)
  return {'success': True, 'msg': 'Course Updated'}

@app.route("/course", methods=['DELETE'])
@role_required({Role.TEACHER})
def delete_course():
  name = None
  try:
    name = request.json['name'].strip()
  except Exception:
    return {'success': False, 'msg': 'JSON data was expected in request body'}

  course = Course.find({'name': name})
  if not course: 
    return {'success': False, 'msg': f'No course found with name as {name}'}


  course.delete()
  return {'success': True, 'msg': 'Course Deleted'}


@app.route("/enroll", methods=['POST'])
@role_required({Role.STUDENT})
def enroll_in_course():
  name = None
  try:
    name = request.json['name'].strip()
  except Exception:
    return {'success': False, 'msg': 'JSON data was expected in request body'}

  course = Course.find({'name': name})
  if not course: 
    return {'success': False, 'msg': f'No course found with name as {name}'}

  student = get_jwt_identity()

  if len(list(courses.find({'name':name, 'students.student_id': student['_id']}))):
    return {'success': False, 'msg': f'You have already registered in {name}'}

  course.enroll(student)
  return {'success': True, 'msg': 'Enrollment Successful!'}

@app.route("/unenroll", methods=['POST'])
@role_required({Role.STUDENT})
def unenroll_in_course():
  name = None
  try:
    name = request.json['name'].strip()
  except Exception:
    return {'success': False, 'msg': 'JSON data was expected in request body'}

  course = Course.find({'name': name})
  if not course: 
    return {'success': False, 'msg': f'No course found with name as {name}'}

  student = get_jwt_identity()


  if not len(list(courses.find({'name':name, 'students.student_id': student['_id']}))):
    return {'success': False, 'msg': f'You are not registered in {name}'}
  course.unenroll(student)
  return {'success': True, 'msg': 'Unenrollment Successful!'}



from course import courses

@app.route("/course", methods=['GET'])
@jwt_required()
def get_all_courses():

  user = get_jwt_identity()

  if user['role'] == Role.TEACHER.value:
    course_list = courses.find({'teacher_id': user['_id']}, {'teacher':0, 'teacher_id': 0})
  elif user['role'] == Role.STUDENT.value:
    course_list = courses.find({'students.student_id': user['_id']}, {'name':1, 'teacher': 1})
  else:
    course_list = courses.find({})

  course_list = list(course_list)
  if len(course_list) and course_list[0].get('_id', None):
    for i in range(len(course_list)):
      course_list[i]['_id'] = str(course_list[i]['_id'])

  return {'success': True, 'msg': 'None', 'courses': course_list}

@app.route("/available-courses", methods=['GET'])
@role_required([Role.STUDENT])
def get_available_courses():

  user = get_jwt_identity()
  course_list = list(courses.find({'students.student_id': {'$ne': user['_id']}}, {'students': 0, 'teacher_id': 0}))

  for i in range(len(course_list)):
    course_list[i]['_id'] = str(course_list[i]['_id'])

  return {'success': True, 'msg': 'None', 'available_courses': course_list}





import json
@app.after_request
def set_success_false(res):
  try:
    if res.json.get('success', None) == None:
      data = res.get_json()
      data['success'] = False
      res.data = json.dumps(data)
  except:
    pass

  return res

import os

if __name__ == '__main__':
  DEBUG  = os.environ.get('DEBUG')
  RELOAD = os.environ.get('RELOAD')
  
  if DEBUG == None: DEBUG = True
  if RELOAD == None: RELOAD = True

  app.run(host='0.0.0.0', port=8000, threaded=True, debug=DEBUG, use_reloader=RELOAD)