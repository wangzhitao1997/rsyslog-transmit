#!/usr/bin/python
# _*_ coding:utf-8 _*_
import os
import sys
import pyinotify
from pyinotify import WatchManager,Notifier,ProcessEvent,EventsCodes
import hashlib
import json
import jsonlogger
from Queue import Queue
from threading import Thread
import multiprocessing
from logclean import logclean
pos=0
#conffile ='loghash.conf'

def mymd5(line):
    try:
        m2=hashlib.md5()
        m2.update(line)
        return m2.hexdigest()
    except Exception,e:
        print str(e)
        return ''

confpath="/opt/RsyslogTransmit-client/rsyslog-transmit.conf/loginotify.conf/"

def printlog(path):
#global pos
    try:
        pos=0
        newhash=''
        fd=open(path)
        fd.seek(0,os.SEEK_SET)
        line = fd.readline()
        newhash=mymd5(line)
        
        filename=os.path.split(path)
        #conffile=filename[1]+'-file.conf'
        conffile=os.path.join(confpath,filename[1]+'-file.conf')
        print (conffile)
        if os.path.exists(conffile) == False:
            fr = open(conffile,'w')
            fr.write(json.dumps({"path":path,"pos":pos,"myhash":"0","flag":"True"}))
            fr.close()

        fr=open(conffile)
        data=json.loads(fr.read())
        fr.close()

        myhash =data['myhash']
        print(newhash)
        if newhash == myhash:
            pos = data['pos']
        else:
            pass
        print pos
        if pos != 0:
            fd.seek(pos,0)
            fd.readline()
        while True:
            line = fd.readline()
            if line.strip():
                if data['flag'] == 'True':
                    pass
                else:
                    s =line.strip()
                    jsonlogger.jsonlogger(s,path)
                pos=pos+len(line)
            else:
                break
        fd.close()
        logclean()

        fr = open(conffile,'w')
        fr.write(json.dumps({"path":path,"pos":pos,"myhash":newhash,"flag":"False"}))
        fr.close()

    except Exception,e:
        print str(e)

    


class MyEventHandler(ProcessEvent):
    def __init__(self,path):
        self.path = path
    def process_IN_MODIFY(self,event):
        try:
            printlog(self.path)
        except Exception,e:
            print str(e)

    def process_IN_MOVE_SELF(self,event):
        global notifier
        try:
            notifier.stop()
        except Exception,e:
            print str(e)
notifier = None

class Controller():
    def __init__(self,path):
        self.path = path
    def run(self):
        while True:
            if os.path.isfile(self.path):
                printlog(self.path)
                pc = MyEventHandler(self.path)
                wm = WatchManager()
                print('notifire'+self.path)
                wm.add_watch(self.path,pyinotify.ALL_EVENTS,rec = True)
                notifier = Notifier(wm,pc)
                try:
                    notifier.loop()
                except Exception,e:
                    print str(e)
            else:
                time.sleep(60)


def main(path):
    monitor = Controller(path)
    monitor.run()


def logmonitorThread():
    loglist=["/var/log/secure","/var/log/audit/audit.log"]
    #loglist=["/var/log/secure"]
    pool = multiprocessing.Pool(processes=2) #
    for monitorlog in loglist:
        #monitor=Controller(log)
        #worker =Thread(target=test,args=(monitorlog))
        #worker.setDaemon(True)
        #worker.start()
        pool.apply_async(main, (monitorlog, ))
    pool.close()
    pool.join()

    


if __name__ == '__main__':
    logmonitorThread()
