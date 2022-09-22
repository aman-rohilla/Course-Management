from enum import Enum
from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

class Role(Enum):
  ADMIN = 'admin'
  STUDENT = 'student'
  TEACHER = 'teacher'

def decode_role(role):
  roles = {
    'admin': Role.ADMIN,
    'student': Role.STUDENT,
    'teacher': Role.TEACHER
  }
  return roles[role]

MONGODB_CONNECTION_STRING = os.environ.get('MONGODB_CONNECTION_STRING')
client = MongoClient(MONGODB_CONNECTION_STRING)
db = client.course_mangement # database
