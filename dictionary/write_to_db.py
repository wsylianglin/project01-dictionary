import pymysql

def connection_mysql():
    """连接数据库"""
    try:
        db = pymysql.connect(host="localhost",
                             user="root",
                             password="lianglin0405",
                            db="dictionary",port=3306,
                             chartset="utf-8")
        return db
    except Exception as e:
        print(e)
        return e


def write_to_mysql(filename):
    """文件写入到数据库"""
    db = connection_mysql()
    cur = db.cursor()
    with open(filename,'rb') as f:
        while True:
            if not data:
                break
            data = f.readline().rstrip("\n")
            sql = "insert into words() values (%s,%s)%()"