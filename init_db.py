import sqlite3
from werkzeug.security import generate_password_hash,check_password_hash
import secrets


# 生成随机密码
password_length = 16
pwd = secrets.token_urlsafe(password_length)

# 读取初始化 SQL 脚本文件
sqlScript = ""
with open('init_db.sql', 'r',encoding="utf-8") as sqlFile:
    sqlScript = sqlFile.read()

# 连接数据库并执行初始化 SQL
conn = sqlite3.connect('db/pkd.sqlite3')
cursor = conn.cursor()
cursor.executescript(sqlScript)
cursor.execute(f'''INSERT INTO users (id, username, password) VALUES (1, 'admin', '{generate_password_hash(pwd)}');''')
conn.commit()
conn.close()

print("init db done.")
print("admin account:","admin")
print("password:",pwd)

