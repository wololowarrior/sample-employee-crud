import urllib.parse as up

import psycopg2
import psycopg2.errors

from Classes.data_defination import Departments, Employee


class DbConnection:
    def __init__(self):
        self.conn = self.__create_conn()

    def __create_conn(self):
        up.uses_netloc.append("postgres")
        url = up.urlparse("postgres://mkqjnaan:6M0CBjG25dwLk3UtwvNikjKTMRU4qCz1@floppy.db.elephantsql.com/mkqjnaan")
        conn = psycopg2.connect(database=url.path[1:],
                                user=url.username,
                                password=url.password,
                                host=url.hostname,
                                port=url.port
                                )
        return conn


class DBOp:
    def init_db(self, conn):
        sql_list = []

        sql = '''
                DROP TABLE IF EXISTS Departments CASCADE
              '''

        sql_list.append(sql)
        # sql = '''
        #         DROP TABLE IF EXISTS country CASCADE
        #       '''
        #
        # sql_list.append(sql)
        # sql = '''
        #         DROP TABLE IF EXISTS Customer CASCADE
        #       '''
        #
        # sql_list.append(sql)
        sql = '''
                CREATE TABLE IF NOT EXISTS Departments 
                (id serial PRIMARY KEY,
                name varchar(10) NOT NULL)
              '''
        sql_list.append(sql)
        self.execute(conn, sql)
        for dept in Departments:
            sql = '''
                    INSERT INTO Departments(name) values ('%s');
                  ''' % (dept.name)
            sql_list.append(sql)

        sql = '''
                CREATE TABLE IF NOT EXISTS country 
                (id serial PRIMARY KEY, 
                name varchar(20) NOT NULL)
              '''
        sql_list.append(sql)

        sql = '''
                CREATE TABLE IF NOT EXISTS Customer
                 (id varchar(50) PRIMARY KEY, 
                 name varchar (30) NOT NULL, 
                 email varchar (30), phone BIGINT NOT NULL,
                 Dept_id INT references Departments(id),
                 Country_id INT references country(id))
              '''
        sql_list.append(sql)
        for sql in sql_list:
            self.execute(conn, sql)

    def get_country_id(self, conn, country_name):
        sql = '''
        SELECT id FROM country where name='%s' 
        ''' % (country_name)
        resp = self.execute_with_get(conn, sql)
        if resp:
            # for row in resp:
            print(f"country {country_name} has id {resp[0]}")
            return resp[0]
        else:
            print(f"country {country_name} has no entry, Creating..")
            country_id = self.create_country(conn, country_name)
            print(f"country {country_name} has id {country_id}")
            return country_id

    def get_department_id(self, conn, dept_name):
        sql = '''
                SELECT id FROM Departments where name='%s' 
                ''' % (dept_name)
        resp = self.execute_with_get(conn, sql)
        if len(resp):
            # for row in resp:
            print(f"Department {dept_name} has id {resp[0]}")
            return resp[0]
        else:
            raise ValueError(f"Department {dept_name}  doesnt exist")

    def create_country(self, conn, country_name):
        sql = '''
        INSERT into country(name) values ('%s') RETURNING id
        ''' % (country_name)
        data = self.execute_with_get(conn, sql)
        return data[0]

    def execute_with_get(self, conn, sql):
        cur = conn.cursor()
        try:
            # print(sql)
            cur.execute(sql)

            data = cur.fetchone()
            self.commit(conn)
        except Exception as e:
            print(e)
            raise
        finally:
            cur.close()
        return data

    def execute_with_get_all(self, conn, sql):
        cur = conn.cursor()
        try:
            cur.execute(sql)
            data = cur.fetchall()
        except Exception as e:
            print(e)
            raise
        finally:
            cur.close()
        return data

    def execute(self, conn, sql):
        cur = conn.cursor()
        try:
            cur.execute(sql)
        except Exception as e:
            print(e)
            raise
        finally:
            cur.close()
        self.commit(conn)
        cur.close()

    def commit(self, conn):
        conn.commit()

    # DBOp().init_db(DbConnection().conn)
    # print(DBOp().get_country_id(DbConnection().conn,'INDIA'))
    def get_customer_from_db(self, conn, id):
        sql = '''
                SELECT customer.id,customer.name as c_name,
                customer.phone,customer.email,
                Departments.name as d_name,
                country.name as country_name,
                customer.dept_id,
                customer.country_id
                FROM customer
                INNER JOIN Departments
                        ON Departments.id = customer.dept_id
                        INNER JOIN country on country.id = customer.country_id 
                        where customer.id='%s';
            ''' % id
        resp = self.execute_with_get(conn, sql)
        if resp:
            emp = Employee(ID=resp[0], name=resp[1], phone=resp[2], email=resp[3], department=resp[4], country=resp[5],
                           dept_id=resp[6], country_id=resp[7])
            return emp
        else:
            return None

    def get_all_customers_from_db(self, conn):
        c_list = []
        sql = '''
                        SELECT customer.id,customer.name as c_name,
                        customer.phone,customer.email,
                        Departments.name as d_name,
                        country.name as country_name,
                        customer.dept_id,
                        customer.country_id
                        FROM customer
                        INNER JOIN Departments
                                ON Departments.id = customer.dept_id
                                INNER JOIN country on country.id = customer.country_id 
                    '''
        resp_list = self.execute_with_get_all(conn, sql)
        if resp_list:
            for resp in resp_list:
                emp = Employee(ID=resp[0], name=resp[1], phone=resp[2], email=resp[3], department=resp[4],
                               country=resp[5],
                               dept_id=resp[6], country_id=resp[7])
                c_list.append(emp.to_json())
            return c_list
        else:
            return None
