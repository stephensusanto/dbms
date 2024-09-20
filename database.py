#!/usr/bin/env python3
import psycopg2

#####################################################
##  Database Connection
#####################################################

'''
Connect to the database using the connection string
'''
class ConnectionDB:

    def __init__(self) :
        # name of database
        self.database_name = 'hospital_usyd'
        # name of username
        self.username = 'postgres'
        # password to connect database
        self.password = '123456'
        # host server 
        self.host = 'localhost'
        # a flag to check connect or not
        self.conn = None

    def connect_to_database(self):
        try:
            # connection to database
            self.conn = psycopg2.connect(
                database = self.database_name,
                user = self.username,
                password = self.password,
                host = self.host
            )
            # if success return True
            return self.conn
        except psycopg2.Error as error:
            # if there something wrong error
            print("psycopg2.Error : " + error.pgerror)
            return False
        
    def open_connection(self):
        # check if there is connection or not
        if self.conn == None:
            # if not this response will shown up
            print("You are already connected to the database no second connection is needed!")
        else :
            # if success to connect
            if self.connect_to_database():
                # this response will shown up
                print("You are successfully connected to the database.")
                return True
            else:
                print("Oops - something went wrong.")
        return False
    
    def close_connection(self):
        try:
            # try to close connection
            self.conn.close()
            self.conn = None
            print("Database Connection is closed.")
        except psycopg2.Error as err:
            print("psycopg2.Error: " + err.pgerror)
        except Exception as err:
            # if there is no conection this response will shown up
            print("You are not connected to the database!")


'''
Validate staff based on username and password
'''
def checkLogin(login, password):
    try:
        connect_db = ConnectionDB()
        conn = connect_db.connect_to_database()
        cursor = conn.cursor()
        cursor.callproc("login_process", [str(login), str(password)])
        records = cursor.fetchone()

        cursor.close()
    except psycopg2.Error as err:
        print(err)
    finally:
        connect_db.close_connection()
    return records


'''
List all the associated admissions records in the database by staff
'''
def findAdmissionsByAdmin(login):

    return


'''
Find a list of admissions based on the searchString provided as parameter
See assignment description for search specification
'''
def findAdmissionsByCriteria(searchString):

    return


'''
Add a new addmission 
'''
def addAdmission(type, department, patient, condition, admin):
    
    return


'''
Update an existing admission
'''
def updateAdmission(id, type, department, dischargeDate, fee, patient, condition):
    

    return
