import psycopg2
import psycopg2.extras
from psycopg2._psycopg import connection, cursor

from configs import DB_CONNECTION
from core.models import DBModel

email_u = ''
name_u = ''
family_u = ''
id_u=''
isLogin = False


class DBManager:
    HOST = DB_CONNECTION["HOST"]
    USER = DB_CONNECTION["USER"]
    PORT = DB_CONNECTION["PORT"]
    PASSWORD = DB_CONNECTION["PASSWORD"]

    def __init__(self, database, user=USER, host=HOST, port=PORT, password=PASSWORD) -> None:
        self.database = database
        self.user = user
        self.host = host
        self.port = port
        self.password = password

        self.conn: connection = \
            psycopg2.connect(dbname=self.database, user=self.user, host=self.host, port=self.port, password=password)

    def __del__(self):
        self.conn.close()  # Close the connection on delete

    def __get_cursor(self) -> cursor:
        # Changing the fetch output from Tuple to Dict utilizing RealDictCursor cursor factory
        return self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    def create(self, User):
        conn = ''
        try:
            conn = psycopg2.connect(database="postgres", user="postgres", password="123456", host="localhost",
                                    port="5432")
        except:
            print("I am unable to connect to the database")

        cur = conn.cursor()
        try:
            cur.execute("select exists(select * from information_schema.tables where table_name=%s)", ('userstable',))
            if bool(cur.fetchone()[0]):
                cur.execute(
                    "INSERT INTO userstable (id,name,family,phone,emailAddress,password,user_role)VALUES(default,  %s, %s, %s, %s, %s, %s)",
                    (User.name, User.family, User.phone, User.emailAddress, User.password, User.user_role))
            else:
                cur = conn.cursor()
                try:
                    cur.execute(
                        "CREATE TABLE userTable (id serial PRIMARY KEY, name VARCHAR(255), family VARCHAR(255),phone VARCHAR(255),emailAddress VARCHAR(255),password VARCHAR(255),user_role VARCHAR(255));")
                    cur.execute(
                        "INSERT INTO userstable (id,name,family,phone,emailAddress,password,user_role)VALUES(default,  %s, %s, %s, %s, %s, %s)",
                        (User.name, User.family, User.phone, User.emailAddress, User.password, User.user_role))

                except:
                    print("I can't create user database!")

                conn.commit()  # <--- makes sure the change is shown in the database
                conn.close()
                cur.close()

        except Exception as e:
            print(e)

        conn.commit()
        conn.close()
        cur.close()

    def read(self, model_class: type, pk) -> DBModel:  # get
        """
            returns an instance of the Model with inserted values
        """

    def update(self, model_instance: DBModel) -> None:
        """
            update instance in db table by get all model_instance attrs
        """

    def delete(self, model_instance: DBModel) -> None:
        """
            delete instance method
        """

    def read_file(self):
        conn = ''
        try:
            conn = self.conn
        except:
            print("I am unable to connect to the database")

        cur = conn.cursor()
        try:

            postgreSQL_select_Query = "select * from fileTable"

            cur.execute(postgreSQL_select_Query)
            print("Selecting rows from user table using cursor.fetchall")
            mobile_records = cur.fetchall()

            print("Print each row and it's columns values")
            for row in mobile_records:
                print("Id = ", row[0], )
                print("name = ", row[1])
                print("directory  = ", row[2])
                print("dateCreate  = ", row[3])
                print("dateLastChange  = ", row[4])
                print("seller_id  = ", row[5])
        except:
            print("we dont have file yet")

        conn.commit()  # <--- makes sure the change is shown in the database
        conn.close()
        cur.close()

    def login_user(self, email, password):
        conn = ''
        try:
            conn = self.conn
        except:
            print("I am unable to connect to the database")
        try:

            cur = conn.cursor()
            sql_select_query = """select * from userstable where emailAddress = %s and password=%s"""

            cur.execute(sql_select_query, (email, password))
            record = cur.fetchone()
            print(record[4], record[5])

            global id_u
            global name_u
            global family_u
            global email_u
            global isLogin
            id_u = record[0]
            name_u = record[1]
            family_u = record[1]
            email_u = record[4]
            isLogin = True
            conn.commit()
            # conn.close()
            cur.close()
            return record[4], record[5]

        except:
            print("I am unable to find this user")

    def add_comment(self, file_name, description):

        conn = ''
        try:
            conn = self.conn
        except:
            print("I am unable to connect to the database")

        cur = conn.cursor()
        try:
            cur.execute("select exists(select * from information_schema.tables where table_name=%s)",
                        ('comment',))
            if bool(cur.fetchone()[0]):
                if isLogin:

                    cur.execute(
                        "INSERT INTO comment (id,description,fileName,username,userfamily,useremail)VALUES(default, %s, %s, %s, %s, %s)",
                        (file_name, description, name_u, family_u, email_u))
                else:
                    try:
                        name, family, email = input('enter name,family,email seprate with coma').split(',')
                        cur.execute(
                            "INSERT INTO comment (id,description,fileName,username,userfamily,useremail)VALUES(default, %s, %s, %s, %s, %s)",
                            (file_name, description, name, family, email))
                    except Exception as e:
                        print(e)


            else:

                cur.execute(
                    "CREATE TABLE comment(id serial PRIMARY KEY, description VARCHAR(255), fileName VARCHAR(255),username VARCHAR(255),userfamily VARCHAR(255),useremail VARCHAR(255));")
                if isLogin:
                    cur.execute(
                        "INSERT INTO comment (id,description,fileName,username,userfamily,useremail)VALUES(default,  %s, %s, %s, %s, %s)",
                        (file_name, description, name_u, family_u, email_u))
                else:
                    try:
                        name, family, email = input('enter name,family,email seprate with coma').split(',')
                        cur.execute(
                            "INSERT INTO comment (id,description,fileName,username,userfamily,useremail)VALUES(default, %s, %s, %s, %s, %s)",
                            (file_name, description, name, family, email))
                    except Exception as e:
                        print(e)

        except:
            print("I can't drop our file database!")

        conn.commit()  # <--- makes sure the change is shown in the database
        # conn.close()
        cur.close()

    def add_file(self, filename, file_path, create, change):
        conn = ''
        try:
            conn = self.conn
        except:
            print("I am unable to connect to the database")

        cur = conn.cursor()
        try:
            cur.execute("select exists(select * from information_schema.tables where table_name=%s)",
                        ('filetable',))
            if bool(cur.fetchone()[0]):
                cur.execute(
                    "INSERT INTO fileTable (id,name,directory,dateCreate,dateLastChange,seller_id,alias_name,buyer_id)VALUES(default,  %s, %s, %s, %s, %s, %s, %s)",
                    (filename, file_path, create, change, id_u, filename + 'alias',0))
            else:
                cur.execute(
                    "CREATE TABLE fileTable (id serial PRIMARY KEY, name VARCHAR(255), directory VARCHAR(255),dateCreate VARCHAR(255),dateLastChange VARCHAR(255),seller_id VARCHAR(255),alias_name VARCHAR(255),buyer_id VARCHAR(100));")

                cur.execute(
                    "INSERT INTO fileTable (id,name,directory,dateCreate,dateLastChange,seller_id,alias_name,buyer_id)VALUES(default,  %s, %s, %s, %s, %s, %s, %s)",
                    (filename, file_path, create, change, id_u, filename + 'alias',0))

        except:
            print("I can't drop our file database!")

        conn.commit()  # <--- makes sure the change is shown in the database
        # conn.close()
        cur.close()

    def buy_file(self, fileName):
        try:
            connection = self.conn

            cursor = connection.cursor()

            print("Table After updating record ")
            sql_select_query = """select * from userstable where emailAddress = %s"""
            cursor.execute(sql_select_query, (email_u,))
            record = cursor.fetchone()
            print(record[0], record[6])

            print("Table After updating record ")
            sql_select_query = """select * from filetable where name = %s"""
            cursor.execute(sql_select_query, (fileName,))
            recordFile = cursor.fetchone()
            print(recordFile)

            # Update single record now
            sql_update_query = """Update filetable set buyer_id = %s where id = %s"""
            cursor.execute(sql_update_query, (record[0], recordFile[0]))
            connection.commit()
            count = cursor.rowcount
            print(count, "Record Updated successfully ")



        except (Exception, psycopg2.Error) as error:
            print("Error in update operation", error)

        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")
    @staticmethod
    def check_is_login():
        if isLogin:
            return True
        else:
            return False