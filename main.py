import http
import pdb
from typing import Tuple, Dict, Union, List

from flask import Flask, request

from Classes.data_defination import Customer
from db.db import DBOp, DbConnection
from utilities import token_required, create_emp_obj

app = Flask(__name__)

conn = DbConnection().conn
db_op = DBOp()
db_op.init_db(conn)


@app.post('/customer')
@token_required
def add_customer() -> tuple[dict, int]:
    """
    Adds a customer to the database
    Automatically creates a country if not available
    :return:
    """
    payload = request.get_json()
    emp = create_emp_obj(payload)
    emp.dept_id = int(db_op.get_department_id(conn, emp.department))
    emp.country_id = int(db_op.get_country_id(conn, emp.country))
    sql = '''
            INSERT INTO customer(id,name,phone,email,Dept_id,Country_id) VALUES ('%s','%s',%d,'%s',%d,%d) RETURNING id
          ''' % (emp.ID, emp.name, emp.phone, emp.email, emp.dept_id, emp.country_id)
    resp = db_op.execute_with_get(conn, sql)
    return {"message": f"Customer added with ID {resp[0]}"},http.HTTPStatus.OK



@app.get("/customer/")
@token_required
def get_all_customer() -> tuple[any, int]:
    """
    Gets all the customers
    :return:
    """
    emp_list = db_op.get_customer_from_db(conn,all=True)
    return emp_list,http.HTTPStatus.OK


@app.get("/customer/<id>")
@token_required
def get_customer(id: str) -> tuple[dict, int]:
    """
    Gets a customer detail by id
    :param id:
    :return:
    """
    emp = db_op.get_customer_from_db(conn, id)
    if not emp:
        return {"message": f"Not a valid id {id}"}, http.HTTPStatus.NOT_FOUND
    return emp.to_json(),http.HTTPStatus.OK


@app.delete("/customer/<id>")
@token_required
def delete_customer(id: str) -> tuple[dict,int]:
    """
    Deletes a customer
    :param id:
    :return:
    """
    sql = '''
        DELETE FROM customer
        where id='%s' RETURNING id ;
    ''' % id
    print(sql)
    resp = db_op.execute_with_get(conn, sql)
    if not resp:
        return {"message": f"Cannot delete {id}"} , http.HTTPStatus.NOT_FOUND

    return {"message": f"deleted {id}"},http.HTTPStatus.OK


@app.post("/customer/<id>")
@token_required
def update_customer(id: str) -> tuple[dict, int]:
    """
    Updates a customer
    :param id:
    :return:
    """
    payload = request.get_json()
    existing_details = db_op.get_customer_from_db(conn, id)
    if not existing_details:
        return {"message": f"Not a valid id {id}"}, http.HTTPStatus.NOT_FOUND
    if "department" in payload:
        d_id = db_op.get_department_id(conn, payload["department"])
        existing_details.dept_id = d_id
    elif "country" in payload:
        c_id = db_op.get_country_id(conn, payload["country"])
        existing_details.country_id = c_id
    for k, v in payload.items():
        setattr(existing_details, k, v)

    sql = '''
        UPDATE customer 
        set name='%s', email='%s', phone=%d, dept_id=%d, country_id=%d
        WHERE id='%s' RETURNING id
    ''' % (existing_details.name, existing_details.email, existing_details.phone, existing_details.dept_id,
           existing_details.country_id, id)
    print(sql)
    resp = db_op.execute_with_get(conn, sql)
    return {"message": f"updated {id}"},http.HTTPStatus.OK


app.run(debug=True, host='127.0.0.1', port=8080,use_reloader=False)
