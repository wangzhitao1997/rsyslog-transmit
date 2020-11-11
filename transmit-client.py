#!/usr/bin/env python
# _*_ encoding:utf-8 _*_
import json
#import ijson
from threading import Thread,Lock
import subprocess
from Queue import Queue
from setting import clientsettings
from diskwalk import diskwalk
import os 
from socket import *
import time


dictdata={'logpath':' ','log':' '}

HOST = clientsettings().host
PORT = clientsettings().port
BUFSIZ = 2048
ADDR  = (HOST,PORT)

tcpCliSock = socket(AF_INET,SOCK_STREAM)
tcpCliSock.connect(ADDR)
lock=Lock()

def readmessage(i,q):
    lock.acquire()
    path=q.get()
    print("Thread %s"%(i)+path)
    with open(path,'r+')as f:
        objects = json.load(f)
        if not objects:
            lock.release()
            q.task_done()
        dictdata['logpath']=path
        dictdata['log']=objects
        newdata=json.dumps(dictdata)
        print (newdata)
        tcpCliSock.sendall(newdata)
        print("read message completely")
        f.seek(0)
        f.truncate() #清空文件
        lock.release()
    q.task_done()

###创建线程
def clientthread():
    queue=Queue()
    path = clientsettings().path
    Listpaths=diskwalk(path).enumeratepaths()
    print(Listpaths)
    ###日志为空
    for paths in Listpaths[::-1]:
        if os.path.getsize(paths)<2:
            Listpaths.remove(paths)
    Numpaths=len(Listpaths)

    for path in Listpaths:
        queue.put(path)

    for i in range(Numpaths):
        worker =Thread(target=readmessage,args=(i,queue))
        worker.setDaemon(True)
        worker.start()
    print("Main Thread Waiting")
    queue.join()
    print("Done")

while True:
    clientthread()
    time.sleep(clientsettings().frequency)


tcpCliSock.close()
