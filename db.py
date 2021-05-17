import os
import pymysql
from flask import jsonify

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')


def open_connection():
    unix_socket = '/cloudsql/{}'.format(db_connection_name)
    try:
        if os.environ.get('GAE_ENV') == 'standard':
            conn = pymysql.connect(user=db_user, password=db_password,
                                unix_socket=unix_socket, db=db_name,
                                cursorclass=pymysql.cursors.DictCursor
                                )
    except pymysql.MySQLError as e:
        print(e)

    return conn

# Read all projects in DB front-end index it
def get_projects():
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT * FROM PROJECTS;')
        projects = cursor.fetchall()
        if result > 0:
            got_projects = jsonify(projects)
        else:
            got_projects = 'No projects found in Database'
    conn.close()
    return got_projects


# Create Survey Project
def add_projects(project):
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO PROJECTS (name, description, formData) VALUES(%s, %s, %s)', (project["name"], project["description"], project["formData"]))
    conn.commit()
    conn.close()
    
 # Get User response by Selected ProjectID   
def get_responses():
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT * FROM USER_RESPONSES;')
        responses = cursor.fetchall()
        if result > 0:
            got_responses = jsonify(responses)
        else:
            got_responses = 'No user responses on database'
    conn.close()
    return got_responses


# def get_responsesByProjectID():
#     conn = open_connection()
#     with conn.cursor() as cursor:
#         result = cursor.execute('SELECT USER_RESPONSES.responseData, USER_RESPONSES.ProjectID, PROJECTS.projectID FROM USER_RESPONSES INNER JOIN PROJECTS ON USER_RESPONSES.ProjectID=PROJECTS.projectID;')
#         responsesByID = cursor.fetchall()
#         if result > 0:
#             got_responses = jsonify(responsesByID)
#         else:
#             got_responses = 'No projects found in Database'
#     conn.close()
#     return got_responses


# Submit response
def submit_response(response):
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO USER_RESPONSES (responseID, responseData, projectID) VALUES(%s, %s, %s)', (response["responseID"],response["responseData"], response["projectID"]))
    conn.commit()
    conn.close()
    