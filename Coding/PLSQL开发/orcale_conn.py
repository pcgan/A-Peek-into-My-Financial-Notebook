#连接
import cx_Oracle
conn = cx_Oracle.connect('scott/tiger@127.0.0.1/ORCL') #("用户名 / 密码@ Oracle服务器IP / Oracle的SERVICE_NAME")
#conn = cx_Oracle.connect('scott','tiger','orcl')

#执行
cur = conn.cursor() #创建游标
sql = "select  * from emp where rownum <10 "
data = cur.execute(sql)
print(data.fetchone())
print(data.fetchall())

cur.close()
conn.close()