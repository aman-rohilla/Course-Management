from bson import ObjectId
from vars import db
from flask import jsonify
courses = db.courses

class Course():

  def __init__(self, name, teacher_id, teacher) -> None:
    self._id      = None
    self.name     = name
    self.teacher_id  = teacher_id
    self.teacher  = teacher
    self.students = []

  def publish(self):
    course = courses.find_one({'name': self.name})
    if(course):
      return f'{self.name} is already published'

    course = courses.insert_one({'name': self.name, 'teacher': self.teacher, 'teacher_id': self.teacher_id, 'students': []})
    self._id = str(course.inserted_id)
    return True

  def update(self, name):
    self.name = name
    courses.update_one({'_id': ObjectId(self._id)}, {'$set': {'name': self.name}})

  def delete(self):
    courses.delete_one({'_id': ObjectId(self._id)})

  @classmethod
  def find(cls, data):
    course = courses.find_one(data, {'students':0})
    if(course):
      course_obj = cls(name=course['name'], teacher_id=course['teacher_id'], teacher = course['teacher'])
      course_obj._id = str(course['_id'])
      return course_obj

  def enroll(self, student):
    courses.update_one({'_id': ObjectId(self._id)}, {'$push': {'students': {'student_id': student['_id'], 'student_name': student['name']}}})

  def unenroll(self, student):
    courses.update_one({'_id': ObjectId(self._id)}, {'$pull': {'students': {'student_id': student['_id']}}})


  def __str__(self) -> str:
    return str({
      '_id': self._id,
      'name': self.name,
      'teacher': self.teacher
    })
