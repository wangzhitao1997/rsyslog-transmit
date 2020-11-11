#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import json
import time 
import re
#s='''type=SERVICE_STOP msg=audit(1604628743.200:665): pid=1 uid=0 auid=4294967295 ses=4294967295 msg='unit=NetworkManager-dispatcher comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success UID="root" AUID="unset" '''

def jsonlogger(s,path):
    print s,path
    localtime=time.strftime("%Y-%m-%d",time.localtime())
    if path == "/var/log/audit/audit.log" and s != '': 
        if s.find("SERVICE_STOP") != -1 or s.find("SERVICE_START") != -1:
            print "yes"
            list=s.replace('"','').split(' ')
            sertype=list[0].split('=')[1]
            pid=list[2].split('=')[1]
            uid=list[3].split('=')[1]
            auid=list[4].split('=')[1]
            subj=list[6].split('=')[1]
            unit=list[7].split('=')[2]
            comm=list[8].split('=')[1]
            exe=list[9].split('=')[1]
            res=list[13].split('=')[1]
            auditid=list[15].split('=')[1]
            nowtime=time.strftime("%H:%M:%S",time.localtime())
    
            auditpath="/var/log/SecAudit/AKOS/"+"audit-"+localtime+".json"
            print auditpath
            fp=open(auditpath,'w')
            data={"type":sertype, 'pid':pid,"uid":uid,"auid":auid,"subj":subj,"unit":unit,"comm":comm,"exe":exe,"res":res,"auditid":auditid,"time":nowtime}
            fp.write(json.dumps(data, indent=2,ensure_ascii=True)) #缩进两个字符输出
            fp.close
        else:
            pass
    elif path=="/var/log/secure":
        if s.find("pam_unix") != -1:
            oldlist=s.split(': ')
            string=oldlist[0]
            newlist=re.split(r"[ ]+",string)
            logintime=newlist[2]
            logintype=newlist[4]
            pam_module=oldlist[1]
            action=oldlist[2]

            loginpath="/var/log/SecAudit/AKOS/"+"login-"+localtime+".json"
            fp=open(loginpath,'w')
            data={'time':logintime,'logintype':logintype,'pam_module':pam_module,'action':action}
            fp.write(json.dumps(data,indent=2,ensure_ascii=True))
            fp.close

#jsonlogger(s)
