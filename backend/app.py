# Author: Huveyscan Kamar

# set FLASK_APP=app.py
# flask run

from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector
import json

app = Flask(__name__)
CORS(app)

def connect_to_db():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="themoviedb"
    )
    return mydb

def return_every_person_from_db(mydb):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM PERSON")
    myresult = mycursor.fetchall()
    return myresult


@app.route('/',methods = ['GET'])
def get_articles():
    variableName = "Movies"
    value = "Hebele"
    mydb = connect_to_db()
    results = return_every_person_from_db(mydb)
    list = []
    for i in range (len(results)):
        list.append(results[i])
    return json.dumps(list)

# Author: Huveyscan Kamar