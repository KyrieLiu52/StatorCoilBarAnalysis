import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)

# 连接数据库，不存在就新建
con = sqlite3.connect("demo.db")

# 创建游标
cur = con.cursor()

# 建表
# sql = "create table if not exists tb_users(user_id INTEGER PRIMARY KEY, username TEXT, password TEXT)"
# cur.execute(sql)

# 插入
# data = "1,'admin','123456'"
# cur.execute('insert into tb_users values (%s)' % data)
# con.commit()

# 查询
cur.execute("select * from tb_users where username=? and password=?", ("admin","123456"))
print(cur.fetchone() is None)

# 关闭连接
cur.close()
con.close()
