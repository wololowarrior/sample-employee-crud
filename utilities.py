from functools import wraps

from flask import request, jsonify

from Classes.data_defination import Employee


def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):

      token = None

      if 'x-api-key' in request.headers:
         token = request.headers['x-api-key']

      if not token:
         return jsonify({'message': 'a valid token is missing'})

      try:
         if token == 'FMfcgzGrbHsKxblngBMPGtCpQvzfkvSJ':
            return f(*args, **kwargs)
         else:
            return jsonify({'message': 'token is invalid'})

      except Exception as e:
         return jsonify({"message":'some error occured','stackTrace':e})

   return decorator


def create_emp_obj(payload):
    name = payload["name"]
    email = payload["email"]
    phone = int(payload["phone"])
    department = payload["department"]
    country = payload["country"]
    emp = Employee(name=name, email=email, phone=phone, department=department, country=country)
    return emp
