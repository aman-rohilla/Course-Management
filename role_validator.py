from flask_jwt_extended import get_jwt, verify_jwt_in_request, get_jwt_identity
from functools import wraps
from vars import decode_role

def role_required(roles):
  def wrapper(fn):
    @wraps(fn)
    def decorator(*args, **kwargs):
      verify_jwt_in_request()
      current_user = get_jwt_identity()

      if decode_role(current_user['role']) in roles:
        return fn(*args, **kwargs)
      else:
        roles_map = map(lambda role: role.value, roles)
        return {'msg': f'{", ".join(roles_map)} only route!'}, 403

    return decorator

  return wrapper
