import pymysql

user='root'
password='TGSPOIDEr#1234'
host='localhost'
port=3306
db='project_tracker'

try:
    conn = pymysql.connect(host=host, user=user, password=password, port=port)
    cur = conn.cursor()
    cur.execute(f"CREATE DATABASE IF NOT EXISTS `{db}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    conn.commit()
    cur.close()
    conn.close()
    print('Database ensured')
except Exception as e:
    print('ERROR', e)
