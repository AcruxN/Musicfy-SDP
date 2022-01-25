import mysql.connector

# establishing a connection to the database
def connection():
    sql_db = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'musicfy2',
        database = 'musicfy_db'
    )

    mycursor = sql_db.cursor()
    return mycursor, sql_db