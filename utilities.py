import http
from functools import wraps

from flask import request, jsonify

from Classes.data_defination import Customer


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        if 'x-api-key' in request.headers:
            token = request.headers['x-api-key']

        if not token:
            return jsonify({'message': 'a valid token is missing'}), http.HTTPStatus.UNAUTHORIZED

        try:
            if token == 'FMfcgzGrbHsKxblngBMPGtCpQvzfkvSJ':
                resp,status_code = f(*args, **kwargs)
                return resp,status_code
            else:
                return jsonify({'message': 'token is invalid'}), http.HTTPStatus.UNAUTHORIZED

        except Exception as e:
            return jsonify({"message": 'some error occured', 'stackTrace': (str(e))}) , http.HTTPStatus.INTERNAL_SERVER_ERROR

    return decorator


def create_emp_obj(payload):
    name = payload["name"]
    email = payload["email"]
    phone = int(payload["phone"])
    department = payload["department"]
    country = payload["country"]
    emp = Customer(name=name, email=email, phone=phone, department=department, country=country)
    return emp
