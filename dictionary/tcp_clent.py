import os
from socket import *
import sys
import time
HOST = '0.0.0.0'
PORT = 8000
ADDR = (HOST,PORT)
import getpass
#创建网络连接
def do_regist(cmd,s):
    while True:
        username = input("用户名：")
        password = getpass.getpass()
        password1 = getpass.getpass("Again:")
        if (' ' in username) or (' ' in password):
            print("用户名和密码不许有空格")
            continue
        elif password != password1:
            print('输入密码不一致')
            continue
        data = "R" + " " + username + " " + password
        s.send(data.encode('gb18030'))
        data = s.recv(1024).decode('gb18030')
        if data == 'OK':
            return 0
        elif data == 'EXISTS':
            return 1


def do_query(s,username):
    while True:
        word = input("请输入查询单词：")
        if word == '##':
            break
        word = "Q" + " " + word + " " + username
        s.send(word.encode('gb18030'))
        data = s.recv(1024).decode('gb18030')
        print(data)
        if data == "OK":
            word = s.recv(2048).decode('gb18030')
            time.sleep(0.1)
            interpret = s.recv(2048).decode('gb18030')
            print('单词：%s'%word)
            print('解释：%s' % interpret)
        else:
            print('没有查到该单词')
            return

def do_hist(s,username):
    data = "H" + " " + username
    s.send(data.encode('gb18030'))
    data = s.recv(1024).decode('gb18030')
    if data == "OK":
        while True:
            his = s.recv(2048).decode('gb18030')
            if his == '##':
                break
            print(his)
    else:
        print('没有历史记录')



def do_login(s):
    username = input("用户名：")
    password = input("密码：")
    data = "L" + " " + username + " " + password
    s.send(data.encode('gb18030'))
    info = s.recv(1024).decode('gb18030')
    if info == "OK":
        while True:
            print('''
            ============欢迎登陆===========
            ---1.查询  2.历史记录   3.退出--
            =============================
            ''')
            try:
                cmd = int(input("请输入选择："))
            except Exception:
                print("输入正确指令")
            if cmd not in [1,2,3]:
                sys.stdin.flush()
            elif cmd == 1:
                do_query(s,username)
            elif cmd == 2:
                do_hist(s,username)
            elif cmd == 3:
                return
    else:
        print("登陆失败")
        return 1



def do_exe():
    pass


def main():
    if len(sys.argv) < 3:
        print("argv is error")
        return
    s = socket()
    try:
        s.connect(ADDR)
    except Exception as e:
        print(e)
        return

    while True:
        print('''
        ===============Welcome============
            --1.注册   2.登陆   3.退出---
        ==================================
        ''')
        try:
            cmd = int(input("请输入选项>>>"))
        except Exception as e:
            print("命令错误")
            continue
        if cmd == 1:
            cmd = '注册'
            data = do_regist(cmd,s)
            if data == 0:
                print('注册成功')
            elif data == 1:
                print('用户存在')
            else:
                print('注册失败')
        elif cmd == 2:
            cmd = '登陆'
            data = do_login(s)
            if data == 1:
                print("登陆失败")
        elif cmd == 3:
            s.send('E'.encode('gb18030'))
            sys.exit()
        else:
            print("你的输入有误！！")
            sys.stdin.flush()
            continue

if __name__ == "__main__":
    main()