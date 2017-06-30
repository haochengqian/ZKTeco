import win32com.client,ctypes,datetime,sys,pika
import json,multiprocessing,os,pickle,logging
import smtplib,time

class Device:
    def FetchAll(self): #implement
        return
    def AddInfo(self):
        return
    def DoorStatue(self):
        return
    def OpenRecord(self):
        return
    def AddIP(self):
        return
    def SetOpenTime(self):
        return
    def DeleteUser(self):
        return
    def SetUserTime(self):
        return 

    def DealWithJson(self,body):
        info_deel = json.loads(body)
        if info_deel["key"] == 'fetchall': #fetch all information
            return self.FetchAll(info_deel)
        elif info_deel["key"] == 'addinfo': #add one piece information
            return self.AddInfo(info_deel)
        elif info_deel["key"] == 'doorstatue': #query door statue
            return self.DoorStatue(info_deel)
        elif info_deel["key"] == 'openrecord': #add open door time index
            return self.OpenRecord(info_deel)
        elif info_deel["key"] == 'addip': #add an ip of door
            return self.AddIP(info_deel)
        elif info_deel["key"] == 'setopentime':
            return self.SetOpenTime(info_deel) #call back function
        elif info_deel["key"] == 'deleteuser':
            return self.DeleteUser(info_deel)
        elif info_deel["key"] == 'setusertime':
            return self.SetUserTime(info_deel)

    def MQ(self,id,brand):
        username = 'haochengqian'
        pwd = 'haochengqian'
        user_pwd = pika.PlainCredentials(username,pwd)
        conn = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1',5672))
        chan = conn.channel()
        if brand == 'zk':
            chan.queue_declare(queue= brand + str(id))
            def callback(ch,method,properties,body):
                self.DealWithJson(body)
            chan.basic_consume(callback,queue = brand+str(id),no_ack=True)
        elif brand == 'MainProcess':
            chan.queue_declare(queue="MainProcess")
            def callback(ch,method,properties,body):
                self.DealWithJson(body)
            chan.basic_consume(callback,queue="MainProcess",no_ack=True)
        logging.warning("waiting for msg .")
        chan.start_consuming()

    def WriteLogInit(self,No,brand):
        logging.basicConfig(level = logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename= brand + 'Device' + str(No) + '.log',
                filemode='w')
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)
