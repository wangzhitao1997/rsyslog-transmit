#!/usr/bin/env python 
# _*_ coding:utf-8 _*_
from  multiprocessing import Process
from setting import clientsettings
from diskwalk import diskwalk
import os

def logclean():
    try:
        process = os.popen("df -lh |grep /var/log  |awk '{print $5}'")
        newstr=process.read()
        process.close()
        num = int(newstr.split('%')[0])
        path = clientsettings().path
        print num,path
        while num > 85:
        ##清理空间
            Listpaths=diskwalk(path).enumeratepaths()
        ###按修改时间进行排序
            dir_list = sorted(Listpaths,key=lambda x:os.path.getmtime(x))
        ###删除最旧的日志
            os.remove(dir_list[0])
    except Exception,e:
        print str(e)

