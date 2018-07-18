import utils
from utils import *

conf = utils.get_config()

ERROR = "\n ERROR!"
DBHOST = conf["MySQL"]["server"] 
DBUSER = conf["MySQL"]["dbuser"]
DBNAME = conf["MySQL"]["dbname"]
DBCHARSET = conf["MySQL"]["dbcharset"]

def drop_db(conn,table):
    SQL = "DROP TABLE IF EXISTS " + table
   # db = db_connection(DBHOST,DBUSER,DBNAME,DBCHARSET)
    conn.execute(SQL)
   # conn = db.cursor()
    #conn.execute('CREATE database IF NOT EXISTS slbbot')


response = query_yes_no("Are you ready get started?")

if response:
    
    db = db_connection(DBHOST,DBUSER,DBNAME,DBCHARSET)
    
    conn = db.cursor()
    try:
        drop_db(conn,"sentence")
        conn.execute("CREATE TABLE IF NOT EXISTS sentence(hashID varchar(16) not null PRIMARY KEY, questions varchar(400));")
        conn.execute("CREATE TABLE IF NOT EXISTS answers(ansID varchar(16) not null PRIMARY KEY, statement varchar(400));")
        conn.execute("CREATE TABLE IF NOT EXISTS admin_user(userID int(16) not null AUTO_INCREMENT PRIMARY KEY, username varchar(50), password varchar(10));")
        db.commit()
        print("Database Table Created")
      # db.close()
    except Exception as e:
        print(ERROR,e)
       

else:
    exit(0)
