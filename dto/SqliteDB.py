import sqlite3
from logging_module import Logger
from parameters import Parameters

class DBManipulator:
    def __init__(self,dbpath:str):
        self.con=sqlite3.connect(dbpath)

    def execute(self,sql:str)->sqlite3.Cursor:
        cur =self.con.cursor()
        if not sql.endswith(";"):
            sql+=";"
        return cur.execute(sql)

    def commit(self):
        self.con.commit()

    def execute_and_commit(self,sql:str):
        self.execute(sql)
        self.commit()

    def createNew(self):
        tablelist=self.execute("select * from sqlite_master where type = 'table';").fetchall()
        checkValid=True
        for i in ["nameTable","metadataTable","downloadTable","subscriptionTable","categoryMap","UserData"]:
            checkValid = checkValid and (i in tablelist)
        if not checkValid:
            Logger().error("DB is not valid, compatibly working...")
        

    def get_cursor(self,type=None,adaptor=None,type_name="",converter=None)->sqlite3.Cursor:
        if type!=None:
            sqlite3.register_adapter(type,adaptor)
            sqlite3.register_converter(type_name,converter)
        return self.con.cursor()

    def close(self):
        self.con.close()

    def __del__(self):
        self.con.close()