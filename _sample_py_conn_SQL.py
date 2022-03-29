import mysql.connector

def db_connection():

    db = mysql.connector.connect(
        host = "localhost",
        user = "Username",
        passwd = "Your Pass",
        database = "Your Database"
    )
    mycursor = db.cursor()
    return db, mycursor

db, mycursor = db_connection()

audioQuery = mycursor.execute("select * from audio_tbl")
myresult = mycursor.fetchall()

for x in myresult:
  print(x)
