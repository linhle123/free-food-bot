# import os
# import urlparse
# import psycopg2

# urlparse.uses_netloc.append("postgres")
# url = urlparse.urlparse(os.environ["DATABASE_URL"])
# conn = psycopg2.connect(
#     database=url.path[1:],
#     user=url.username,
#     password=url.password,
#     host=url.hostname,
#     port=url.port
# )
# cur = conn.cursor()
# print('PostgreSQL database version:')
# cur.execute('SELECT version()')


import psycopg2
import sys
 
 
con = None
 
try:
    con = psycopg2.connect("host='localhost' dbname='testdb' user='pythonspot' password='password'")   
    cur = con.cursor()
    cur.execute("CREATE TABLE Products(Id INTEGER PRIMARY KEY, Name VARCHAR(20), Price INT)")
    cur.execute("INSERT INTO Products VALUES(1,'Milk',5)")
    cur.execute("INSERT INTO Products VALUES(2,'Sugar',7)")
    cur.execute("INSERT INTO Products VALUES(3,'Coffee',3)")
    cur.execute("INSERT INTO Products VALUES(4,'Bread',5)")
    cur.execute("INSERT INTO Products VALUES(5,'Oranges',3)")
    con.commit()
except psycopg2.DatabaseError, e:
    if con:
        con.rollback()
 
    print 'Error %s' % e    
    sys.exit(1)
 
finally:   
    if con:
        con.close()