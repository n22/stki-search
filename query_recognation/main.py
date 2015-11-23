__author__ = 'hamdiahmadi'

import MySQLdb

class restrict():
    def __init__(self):
        pass

    def getListTabelNCol(self):
        
        return

class db(restrict):

    def __init__(self):
        pass

    def openConnection(self,addrs,users,passwords,dbNames):
        return MySQLdb.connect(passwd=passwords,db=dbNames,host=addrs,user=users)

    def execute(self,cursor,command):
        return cursor.execute(command)

    def closeConnection(self,cursor):
        return cursor.close()

    def fetchAll(self,cursor):
        return cursor.fetchall()

    def getDataBase(self,port,user,password,dbName):
        db = self.openConnection(addr,user,password,dbName)
        listTabelNCol = restrict.getListTabelNCol(self)
        cursor = db.cursor()
        return


if __name__ == '__main__':
    database = db()
    addr = "128.199.181.164"
    user = "stki"
    password = "stki2015"
    dbName = "stki"
    database.getDataBase(addr,user,password,dbName)