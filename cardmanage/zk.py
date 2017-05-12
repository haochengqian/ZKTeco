import DeviceManager
import win32com.client,ctypes,datetime,sys,pika
import json,multiprocessing,os,pickle,logging
import smtplib,time

class zk(DeviceManager.Device):
    def __init__(self,ip,port,n,brand):
            self.WriteLogInit(n,brand)
            self.zk = win32com.client.Dispatch('zkemkeeper.ZKEM.1')
            self.OpenService(self.zk,ip,port)
            self.MQ(n,brand)
            self.zk.Disconnect()

    def OpenService(self,zk,ip,port):
           while 1:
                logging.warning(ip + ':' + str(port))
                statue = zk.Connect_Net(ip,port)
                if not statue:
                    print "Connect Error"
                    time.sleep(1)
                else:
                    break
            
    def fetchall(self,info_deel):#fetch all information not shutdown key : fetchall (ckecked)
        uid = {}
        self.zk.ReadAllUserID(1)
        while 1:
            exists,idNum,username,other,privilege,enable = self.zk.GetAllUserInfo(1)
            if not exists:
                break
            else:
                if enable:
                    uid[idNum] = username.split(u'\x00')[0].encode('gbk')
        logging.warning(uid)
        return
    def addinfo(self,info_deel):
        idconnect = 1
#        rev,temp1,temp2,temp3,temp4 = self.zk.GetUserInfo(idconnect,1)
        idwUser = info_deel["userid"]
        sName = info_deel["username"]
        sPassword = info_deel["userpwd"]
        iPrivilege = info_deel["privilege"]
        cCardnumber = info_deel["cardnumber"]
        enable = info_deel["enable"]
        sUserGroup = info_deel["usergroup"]
        iPrivilege = long(iPrivilege)
        if enable == '1':
            enable = True
        else :
            enbale = False
        if sPassword == 'NONE':
            sPassword = None
        rev2 = self.zk.SetStrCardNumber(cCardnumber)  
        rev1 = self.zk.SSR_SetUserInfo(idconnect,idwUser,sName,sPassword,iPrivilege,enable)
        rev3 = self.zk.SetUserGroup(idconnect,idwUser,sUserGroup)
        if rev1 == 1 and rev2 == 1 and rev3 == 1:
            logging.warning("setuserinfo " + str(idwUser) + " ok!")
        else :
            logging.warning("setuserinfo " + str(idwUser) + " fall!" + str(rev3))
        return #add user information  key: addinfo,userid:,username:,userpwd:,privilege:,cardnumber:,enable:,usergroup:

    def doorstatue(self,info_deel):
        idconnect = 1
        exsit,state = self.zk.GetDoorState(idconnect)
        if exsit == 1:
            logging.warning("check door statue successful")
            logging.warning("door is " + str(state))
        else :
            logging.warning("cant connect door")
        return #check doorstatue (checked)

    def openrecord(self,info_deel):
        #logging.warning(str(info_deel))
        idconnect = 1
        tzIndex = info_deel["tzIndex"]
        TZ = info_deel["tz"]
        rev = self.zk.SetTZInfo(idconnect,tzIndex,TZ)
        if rev == 1:
            logging.warning("set time range successful")
        else:
            logging.warning("set time range fail")
        return #set open door time range

    def setopentime(self,info_deel):
        idconnect = 1
        groupIndex = info_deel["usergroup"]
        groupTZs = info_deel["grouptzs"]
        rev = self.zk.SetGroupTZStr(idconnect,groupIndex,groupTZs)
        return #set usergroup time range number

    def deleteuser(self,info_deel):
        idconnect = 1
        userNumber = info_deel["usernumber"]
        recv = self.zk.SSR_DeleteEnrollData(idconnect,userNumber,12)
       
        if recv == 1:
            logging.warning("delete " + str(userNumber) + " successful!")
        else :
            recv2 = self.zk.GetLastError()
            logging.warning("delete " + str(userNumber) + " fail! " + str(recv2))
        return #delete user info

    def setusertime(self,info_deel):
        idconnect = 1
        usernumber = long(info_deel["usernumber"])
        tzs = info_deel["tzs0"]+":"+info_deel["tzs1"]+":"+info_deel["tzs2"]+":"+info_deel["tzs3"]
        rev = self.zk.SetUserTZStr(idconnect,usernumber,tzs)
        if rev == 1:
             logging.warning("set " + str(usernumber) + " successful!")
        else:
             recv2 = self.zk.GetLastError()
             logging.warning("set " + str(usernumber) + tzs + " fail! " + str(recv2))