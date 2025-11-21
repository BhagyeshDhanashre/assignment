import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="DATABASE_NAME",
        user="USER_NAME",
        password=YOUR_PASSWORD,
        host="localhost",
        port="5432"
    )
