#!/usr/bin/env python
# _*_ coding:utf-8 _*_ 
import json
from threading import Thread
#import requests
from socket import *
from time import ctime
import os
import ast
from setting import serversettings
##记录日志的路径
recordpath=serversettings().recordpath
HOST = serversettings().host
PORT = serversettings().port

BUFSIZ = 2048
ADDR = (HOST,PORT)

tcpSerSock = socket(AF_INET,SOCK_STREAM)
tcpSerSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(serversettings().maxnum)  ##最大的连接数

def recordlog(dictdata,addr):
    logpath=dictdata['logpath']
    log=dictdata['log']
    if os.path.exists(recordpath+addr[0]) == False:
        os.mkdir(recordpath+addr[0])
    filename=recordpath+addr[0]+'/'+logpath.replace('/','-')
    print (filename)
    with open(filename,'a+')as f:
        f.write(json.dumps(log,indent=2,ensure_ascii=True))
        
def tcplink(sock,addr):
    print (addr)
    print(addr[0])
    while True:
        data = tcpCliSock.recv(BUFSIZ)
        print (data)
        print(type(data))
        if not data:
            break
        dictdata=json.loads(data)
        print (dictdata['logpath'])
        print (dictdata['log'])
        #print (dictdata)
        recordlog(dictdata,addr)
        if not data:
            break
    tcpCliSock.close()

while True:
    print('waiting for connection...')
    tcpCliSock,addr = tcpSerSock.accept()
    print('...connected from:',addr)
    t=Thread(target=tcplink,args=(tcpCliSock,addr))
    t.start()

tcpSerSock.close()

    
    
    
