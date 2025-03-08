import mysql.connector
import connect  

def db_connection():
    conn = mysql.connector.connect(
        host=connect.dbhost,
        user=connect.dbuser,
        password=connect.dbpassword,
        database=connect.dbname
    )
    return conn

