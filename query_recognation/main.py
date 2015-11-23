__author__ = 'hamdiahmadi'

import pymysql

class db():

    def __init__(self):
        pass

    def openConnection(self,addrs,users,passwords,dbNames):
        return pymysql.connect(passwd=passwords,db=dbNames,host=addrs,user=users)

    def execute(self,cursor,command):
        return cursor.execute(command)

    def closeConnection(self,cursor):
        return cursor.close()

    def fetchAll(self,cursor):
        return cursor.fetchall()

    def getDataBase(self,port,user,password,dbName):
        self.openConnection(addr,user,password,dbName)
        return


if __name__ == '__main__':
    database = db()
    addr = "128.199.181.164"
    user = "stki"
    password = "stki2015"
    dbName = "stki"
    database.getDataBase(addr,user,password,dbName)