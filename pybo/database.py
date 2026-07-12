import pymysql

conn = pymysql.connect(
    host="mysql",
    user="root",
    password="1234",
    database="pybo",
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor
)