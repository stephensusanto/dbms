#!/usr/bin/env python3
import psycopg2

#####################################################
##  Database Connection
#####################################################

'''
Connect to the database using the connection string
'''
def openConnection():
    # connection parameters - ENTER YOUR LOGIN AND PASSWORD HERE
    userid = "postgres"
    passwd = "123456"
    myHost = "localhost"
    database = "hospital_usyd"


    # Create a connection to the database
    conn = None
    try:
        # Parses the config file and connects using the connect string
        conn = psycopg2.connect(database=database,
                                    user=userid,
                                    password=passwd,
                                    host=myHost)

    except psycopg2.Error as sqle:
        print("psycopg2.Error : " + sqle.pgerror)
    
    # return the connection to use
    return conn


'''
Validate staff based on username and password
'''
def checkLogin(login, password):
    try:
        conn = openConnection()
        cursor = conn.cursor()
        cursor.callproc("login_process", [str(login), str(password)])
        records = cursor.fetchone()
    
        cursor.close()
    except psycopg2.Error as err:
        print(err)
    return records


'''
List all the associated admissions records in the database by staff
'''
def findAdmissionsByAdmin(login):
    try:
        conn = openConnection()
        cursor = conn.cursor()
        # TODO: CHECK QUERY AGAIN THERE IS STILL HAVE ANOMALY DATA IN FEE
        cursor.callproc("admission_data_based_on_login", [str(login)])
        records = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        admission_list = [dict(zip(columns, row)) for row in records]
        cursor.close()
    except psycopg2.Error as err:
        print(err)
    
    return admission_list
    


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
    try:
        conn = openConnection()
        cursor = conn.cursor()
        cursor.execute("SELECT add_admission (%s, %s, %s, %s, %s)", (str(type), str(department), str(patient), str(admin), str(condition)))
        conn.commit()
        cursor.close()
        return True
    except psycopg2.Error as err:
        print(err)
        return False
    
    return admission_list


'''
Update an existing admission
'''
def updateAdmission(id, type, department, dischargeDate, fee, patient, condition):
    

    return
