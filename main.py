from flask import Flask, request

from db.db import DBOp, DbConnection
from utilities import token_required, create_emp_obj

app = Flask(__name__)

conn = DbConnection().conn
db_op = DBOp()
db_op.init_db(conn)


@app.post('/customer')
@token_required
def add_customer():
    payload = request.get_json()
    emp = create_emp_obj(payload)
    emp.dept_id = int(db_op.get_department_id(conn, emp.department))
    emp.country_id = int(db_op.get_country_id(conn, emp.country))
    sql = '''
            INSERT INTO customer(id,name,phone,email,Dept_id,Country_id) VALUES ('%s','%s',%d,'%s',%d,%d) RETURNING id
          ''' % (emp.ID, emp.name, emp.phone, emp.email, emp.dept_id, emp.country_id)
    resp = db_op.execute_with_get(conn, sql)
    return f"Customer added with ID {resp[0]}"


@app.get("/customer/all")
@token_required
def get_all_customer():
    emp_list = db_op.get_all_customers_from_db(conn)
    return emp_list


@app.get("/customer/<id>")
@token_required
def get_customer(id):
    emp = db_op.get_customer_from_db(conn, id)
    return emp.to_json()


@app.delete("/customer/<id>")
@token_required
def delete_customer(id):
    sql = '''
        DELETE FROM customer
        where id='%s' RETURNING id ;
    ''' % id
    print(sql)
    resp = db_op.execute_with_get(conn, sql)
    return "Success"


@app.post("/customer/<id>")
@token_required
def update_customer(id):
    payload = request.get_json()
    existing_details = db_op.get_customer_from_db(conn, id)
    if not existing_details:
        return f"Not a valid id {id}"
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
    return "Success"


app.run(debug=True, host='127.0.0.1', port=8080)