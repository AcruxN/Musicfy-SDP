import mysql.connector

def db_connection():

    db = mysql.connector.connect(
        host = "localhost",
        user = "root",
        passwd = "musicfy2",
        database = "musicfy_db"
    )
    mycursor = db.cursor()
    return db, mycursor

db, mycursor = db_connection()

audioQuery = mycursor.execute("select * from audio_tbl")
myresult = mycursor.fetchall()

for x in myresult:
  print(x)
