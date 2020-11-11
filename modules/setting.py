#!/usr/bin/python 
import ConfigParser
import sys,os,string

class clientsettings:
    def __init__(self):
        cf=ConfigParser.ConfigParser()
        cf.read('/opt/RsyslogTransmit-client/rsyslog-transmit.conf/client-setting.d/default-client.conf')
        self.host=cf.get('settings','receivedserver')
        self.port=cf.getint('settings','receivedport')
        self.path=cf.get('settings','inputfilename')
        self.frequency=cf.getfloat('settings','PollingInterval')


class serversettings:
    def __init__(self):
        cf=ConfigParser.ConfigParser()
        cf.read('/opt/RsyslogTransmit-server/rsyslog-transmit.conf/server-setting.d/default-server.conf')
        self.host=cf.get('settings','ReceivedServer')
        self.port=cf.getint('settings','Receivedport')
        self.recordpath=cf.get('settings','templateRemote')
        self.maxnum=cf.getint('settings','MaxClientnum')

