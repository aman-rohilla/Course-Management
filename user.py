from bson import ObjectId
from vars import Role, db
from flask_jwt_extended import create_access_token, create_refresh_token
users = db.users

class User():

  @staticmethod
  def parse_user(data):
    user = {}

    try:
      user['_id']      = data.get('_id', None)
      user['name']     = data['name'].strip()
      user['email']    = data['email'].strip()
      user['password'] = data['password'].strip()
      user['role']     = data['role'].strip()
    except:
      return 'JSON data was expected in request body'

    result = User.validate(user)
    if result != True:
      return result

    return User(user)

  def __init__(self, user) -> None:
    self._id      = user['_id']
    self.name     = user['name']
    self.email    = user['email']
    self.password = user['password']
    self.role     = user['role']


  def create(self):
    user = users.find_one({'email': self.email})
    if(user):
      return f'{self.email} is already registered'

    user = users.insert_one({
      'name': self.name,
      'email': self.email,
      'password': self.password,
      'role': self.role,
    })
    self._id = str(user.inserted_id)
    return True

  def update(self, user):
    # self._id = user.get('_id', self._id)
    self.name = user.get('name', self.name)
    # self.email = user.get('email', self.email)
    # self.password = user.get('password', self.password)
    # self.role = user.get('role', self.role)

    users.update_one({'_id': ObjectId(self._id)}, {'name': self.name})

  def delete(self):
    users.delete_one({'_id': ObjectId(self._id)})

  @classmethod
  def find(cls, data):
    user = users.find_one(data)
    if(user):
      user['_id'] = str(user['_id'])
      return cls(user)


  @staticmethod
  def validate(user):

    name = user.get('name', None)
    email = user.get('email', None)
    password = user.get('password', None)
    role = user.get('role', None)

    if not name or not email or not password or not role :
      return 'Some fields are empty'

    if role != Role.STUDENT.value and role != Role.TEACHER.value:
      return 'Role must be student or teacher'

    return True

  def gen_access_token(self):
    token = create_access_token(identity={'_id': self._id, "email": self.email, 'name': self.name, 'role': self.role})
    return f'Bearer {token}'

  def gen_refresh_token(self):
    token = create_refresh_token(identity={'_id': self._id, "email": self.email, 'name': self.name, 'role': self.role})
    return f'Bearer {token}'
