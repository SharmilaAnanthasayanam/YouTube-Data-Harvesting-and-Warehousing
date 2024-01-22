import mysql.connector
from dotenv import load_dotenv
import os
load_dotenv()

password= os.getenv("password")
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password = password,
    database="youtube"
)

mycursor = mydb.cursor(buffered=True)

def clear_sqldatabase():
    CLEARQUERY1= """DELETE FROM Comments;"""
    CLEARQUERY2 = "DELETE FROM video;"
    CLEARQUERY3 = "DELETE FROM playlist;"
    CLEARQUERY4 = "DELETE FROM channel;"
    mycursor.execute(CLEARQUERY1)
    mycursor.execute(CLEARQUERY2)
    mycursor.execute(CLEARQUERY3)
    mycursor.execute(CLEARQUERY4)
    mydb.commit()

    SELECTQUERY1= """SELECT * FROM Comments;"""
    SELECTQUERY2 = "SELECT * FROM video;"
    SELECTQUERY3 = "SELECT * FROM playlist;"
    SELECTQUERY4 = "SELECT * FROM channel;"
    mycursor.execute(SELECTQUERY1)
    print("comments: ",mycursor.fetchall())
    mycursor.execute(SELECTQUERY2)
    print("video: ",mycursor.fetchall())
    mycursor.execute(SELECTQUERY3)
    print("playlist: ",mycursor.fetchall())
    mycursor.execute(SELECTQUERY4)
    print("channel: ",mycursor.fetchall())

clear_sqldatabase()