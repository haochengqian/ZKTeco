import zk
import win32com.client,ctypes,datetime,sys,pika
import json,multiprocessing,os,pickle,logging
import smtplib,time

class Process_Controller:
    process = []
    def __init__(self):
        self.idnum = 0
        self.pickle_file_position = 'ipstore.pkl'
        self.OpenProcess()

    def LoadFile(self):
        self.pickle_file = open(self.pickle_file_position,'r')
    
    def WritePickle(self,ip,port,id,position,brand):
        self.pickle_file = open(self.pickle_file_position,'w')
        obj = {"ip":ip,"port":port,"id":id,"position":position,"brand":brand}
        pickle.dump(obj,self.pickle_file)

    def CreateProcess(self,ip,port,n,brand):
        if brand == 'zk':
            selfdevice = zk.zk(ip,port,n,brand)
        else:
            return
            
    def OpenProcess(self):
        self.WriteLogInit()
        self.WritePickle('10.0.1.136',4370,1,'hsdjklsfsdf','zk')
        self.processCount = 0
        self.pickle_file = open(self.pickle_file_position,'r')
        while 1:
            try:
                dic_ip_port_id_info_brand = pickle.load(self.pickle_file)
            except EOFError:
                break
            ip = dic_ip_port_id_info_brand["ip"]
            port = dic_ip_port_id_info_brand["port"]
            id = dic_ip_port_id_info_brand["id"]
            position = dic_ip_port_id_info_brand["position"]
            brand = dic_ip_port_id_info_brand["brand"]
            self.process.insert(self.processCount,multiprocessing.Process(target = self.CreateProcess,args = (ip,port,id,brand,)) )
            self.process[self.processCount].start()
            logging.warning("process.id " + str(self.process[self.processCount].pid))
            logging.warning("process.name " + str(self.process[self.processCount].pid))
            logging.warning("process.is_alive " + str(self.process[self.processCount].is_alive()))
            self.process[self.processCount].join()
            self.processCount = self.processCount + 1

    def WriteLogInit(self):
        logging.basicConfig(level = logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename= 'manager.log',
                filemode='w')
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)


