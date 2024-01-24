import mysql.connector
from dotenv import load_dotenv
from pymongo import MongoClient
import os
load_dotenv()

try:

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
        comments = mycursor.fetchall()
        if not comments:
            print("Comments Table Cleared")
        mycursor.execute(SELECTQUERY2)
        video = mycursor.fetchall()
        if not comments:
            print("video Table Cleared")
        mycursor.execute(SELECTQUERY3)
        playlist = mycursor.fetchall()
        if not comments:
            print("playlist Table Cleared")
        mycursor.execute(SELECTQUERY4)
        channel = mycursor.fetchall()
        if not comments:
            print("channel Table Cleared")
        print("----------------------------")
    clear_sqldatabase()


    def clearmongodb():
        con_string = os.getenv("connectionstring")
        client = MongoClient(con_string)
        db = client["youtube_db"]
        result = db.channel_collection.delete_many({})
        if result.acknowledged:
            print("Mongodb youtube collection Cleared")
    clearmongodb()

except Exception as e:
    print(e)

