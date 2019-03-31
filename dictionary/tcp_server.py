from socket import *
import time
import os
import signal
import pymysql
import sys

#定义需要的全局变量
DICT_TEXT = './dict.txt'
HOST = '0.0.0.0'
PORT = 8000
ADDR = (HOST,PORT)

#流程控制
def regist(data,db,c):
    username = data[1]
    password = data[2]
    cur = db.cursor()
    sql = "select * from user where u_name = '%s'" % username
    cur.execute(sql)
    db.commit()
    rel = cur.fetchone()
    if rel != None:
        c.send('EXISTS'.encode('gb18030'))
        return
    #用户不存在的情况下插入用户
    else:
        sql = "insert into user(u_name,u_password)values ('%s','%s')"%(username,password)
        try:
            cur.execute(sql)
            db.commit()
            c.send('OK'.encode('gb18030'))
        except:
            db.rollback()
            c.send('FILE'.encode('gb18030'))
        else:
            print('%s注册成功'%username)
        #cur.close()
        #db.close()

def login(data,db,c):
    print("登陆操作")
    username = data[1]
    password = data[2]
    cur = db.cursor()
    sql = "select u_name from user where u_name = '%s' and u_password = '%s'"%(username,password)
    cur.execute(sql)
    db.commit()
    data = cur.fetchall()
    if data:
        c.send("OK".encode('gb18030'))
    else:
        c.send("FILE".encode('gb18030'))
    cur.close()
    #db.close()


def query(data,db,c):
    print("查询操作")
    word = data[1]
    name = data[2]
    print(word,name)
    cur = db.cursor()

    def insert_history(name,word):
        tm = time.ctime()
        name = name
        word = word

        sql = "insert into hist (u_name,w_name,w_time) \
        values('%s','%s','%s')" % (name, word, tm)
        try:
            cur.execute(sql)
            db.commit()
        except:
            db.rollback()

    sql = "select * from words where w_name = '%s'"%word
    try:
        cur.execute(sql)
        rel = cur.fetchone()
        print(rel)
        if rel:
            c.send("OK".encode('gb18030'))
            time.sleep(0.1)
            c.send(rel[1].encode('gb18030'))
            c.send(rel[2].encode('gb18030'))
            print("插入历史记录")
            insert_history(name,word)
            print("插入成功！")
        else:
            c.send("FALL".encode('gb18030'))
    except:
        db.rollback()


def hist(data,db,c):
    print("查询历史记录")
    name = data[1]
    cur = db.cursor()
    sql = "select * from hist where u_name='%s'"%name
    try:
        cur.execute(sql)
        rel = cur.fetchall()
        if not rel:
            c.send("FALL".encode('gb18030'))
            return
        else:
            c.send("OK".encode('gb18030'))
            for i in rel:
                msg = "%s  %s  %s"%(i[1],i[2],i[3])
                c.send(msg.encode('gb18030'))
                time.sleep(0.5)
            c.send("##".encode('gb18030'))
            print("历史记录查询完成")
    except:
        db.rollback()


def do_child(c,db):
    while True:
        data = c.recv(1024).decode('gb18030').split(' ')
        cmd = data[0]
        if cmd == 'R':
            regist(data,db,c)
        elif cmd == 'L':
            login(data,db,c)
        elif cmd == 'Q':
            query(data,db,c)
        elif cmd == 'H':
            hist(data,db,c)
        elif cmd == 'E' or not data:
            c.close()
            sys.exit(0)


def main():
    #创建数据库连接
    db = pymysql.connect('localhost','root','lianglin0405','dictionary')

    #创建套接字
    s = socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)
    s.listen(5)

    #使用忽略子进程信号
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)
    while True:
        try:
            c, addr = s.accept()
            print('connect to',addr)
        except KeyboardInterrupt:
            s.close()
            sys.exit("服务器退出")
        except Exception as e:
            print(e)
            continue

        #创建子进程
        pid = os.fork()
        if pid < 0:
            print("创建子进程失败")

        #循环接受客户端请求
        elif pid == 0:
            s.close()
            do_child(c,db)
        else:
            c.close()
            continue

if __name__ == "__main__":
    main()