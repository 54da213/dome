# -*- coding: utf-8 -*-
import abc

import MySQLdb


class Database(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self,host="",port=3306,user=None,pwd=None,db_name=None,charset="utf8"):
        self.host=host
        self.port=port
        self.user=user
        self.pwd=pwd
        self.db_name=db_name
        self.charset=charset
        self.db=None
        self.cursor=None


    @abc.abstractmethod
    def connect(self):
        pass

    @abc.abstractmethod
    def execute(self,query, args=None):
        pass

    @abc.abstractmethod
    def close(self):
        pass

class Mysql(Database):
    def __init__(self,host="",port=3306,user=None,pwd=None,db_name=None,charset="utf8"):
        super(Mysql,self).__init__(host,port,user,pwd,db_name,charset)

    def connect(self):
        self.db=MySQLdb.Connect(self.host,self.user,self.pwd,self.db_name,self.charset)
        self.cursor = self.db.cursor()

    def execute(self,query, args=None):
        self.cursor.execute(query,args)

    def commit(self):
        self.db.commit()
    def close(self):
        self.db.close()