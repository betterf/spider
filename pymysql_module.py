import pymysql
#connect(数据库地址，用户名，密码，数据库名)
#连接mysql服务器
db=pymysql.connect("localhost",'root','',"zhilian")
#创建游标对象
cursor=db.cursor()
#执行sql语句
# sql="insert into user(id,name) values(3,'zhangsan1')"
sql="delete from user"
cursor.execute(sql)
#提交
db.commit()
#得到返回的结果
# print(cursor.fetchone())
# print(cursor.fetchall())
#查看影响的条数 rowcount
print(cursor.rowcount)
#关闭数据库
db.close()