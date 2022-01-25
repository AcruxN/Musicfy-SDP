import mysql.connector


sql_db = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'musicfy2',
    database = 'musicfy_db'
)
