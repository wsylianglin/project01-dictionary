import pymysql
import re

def write_to_mysql(filename):
    """文件写入到数据库"""
    db = pymysql.connect(host="localhost",
                         user="root",
                         password="lianglin0405",
                         db="dictionary")
    cur = db.cursor()
    with open(filename,encoding='gb18030') as f:
        for line in f:
            data = re.split(r'\s+',line)
            word = data[0]
            interpres = ' '.join(data[1:])
            sql = "insert into words(w_name,interpret) values ('%s','%s')"%(word,interpres)
            try:
                cur.execute(sql)
                db.commit()
            except:
                db.rollback()
        cur.close()
        db.close()
        print('insert successful')
if __name__ == "__main__":
    write_to_mysql(filename='dict1.txt')

# import pymysql
# import re
#
# def write_to_file(filename):
#     """
#     写入文件到数据库
#     """
#     #连接数据库
#     db = pymysql.connect('localhost','root','lianglin0405','dictionary')
#     cur = db.cursor()
#     with open(filename,encoding='gb18030') as f:
#         for line in f:
#             data = re.split(r'\s+',line)
#             word = data[0]
#             interparet = ' '.join(data[1:])
#             sql = 'insert into words(w_name,interpret) values ("%s","%s")'%(word,interparet)
#             try:
#                 cur.execute(sql)
#                 db.commit()
#             except:
#                 db.rollback()
#         cur.close()
#         db.close()
#         print('插入成功')
#
# if __name__ == "__main__":
#     write_to_file(filename="dict1.txt")














