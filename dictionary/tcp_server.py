from socket import *
import datetime
import os
from multiprocessing import Process,pool

def do_child():
    pass

ADDRESS = ()
sockfd = socket(AF_INET,SOCK_STREAM)
sockfd.bind(ADDRESS)
socket.listen()
while True:
    connd, addr = socket.accept()
    if connd:
        pid = os.fork()
        if pid < 0:
            print("create pid faild....")
        elif pid == 0:
            do_child()
        else:
