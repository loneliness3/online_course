import psycopg2

con = psycopg2.connect(
        host="localhost",
        database="online_course",
        user="loneliness",
        password="ohdude;"
)

cursor = con.cursor()

create_table = '''CREATE TABLE users (id UUID PRIMARY KEY, username VARCHAR(80), password VARCHAR(80));'''


cursor.execute(create_table)

con.close()
