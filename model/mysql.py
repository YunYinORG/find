#!/usr/bin/env python
#coding=utf-8
import settings
import MySQLdb
import MySQLdb.cursors
class mysql:
    def __init__(self):
        host = DB_HOST
        port = DB_PORT
        user = DB_USER
        pwd = DB_PWD
        db = DB_NAME
        self.conn = MySQLdb.connect(host, port, user, pwd, db, cursorclass = MySQLdb.cursors.DictCursor)
        self.cursor = self.conn.cursor()

    def fetchAll(self, sql,data=[]):
        result = None
        if self.cursor.execute(sql,data):
            result = self.cursor.fetchall()
        return result

    def fetchOne(self, sql,data=[]):
        result = None
        if self.cursor.execute(sql,data):
            result = self.cursor.fetchone()
        return result

    def getList(self,tableName,colums,condition,orders='',limits=''):
        sql = "SELECT "+colums+" FROM " + tableName + " WHERE 1=1"
        if  type(condition) == dict:
            for i in condition.keys():
                sql = sql + " AND "+i+"=?"
        else:
            sql = sql + condition
        if orders !='':
            sql = sql+' order by '+orders
        if limits != '':
            sql = sql+' limit '+limits
        return self.fetchAll(sql,condition.values())

    def getOne(self,tableName,colums,condition,orders='',limits=''):
        sql = "SELECT "+colums+" FROM " + tableName + " WHERE 1=1"
        if  type(condition) == dict:
            for i in condition.keys():
                sql = sql + " AND "+i+"=?"
        else:
            sql = sql + condition
        if orders !='':
            sql = sql+' order by '+orders
        if limits != '':
            sql = sql+' limit '+limits
        return self.fetchOne(sql,condition.values())

    def insert(self, tableName, data):
        sql = "INSERT INTO " + tableName + "("

        sql = sql + ','.join(data.keys())
        sql = sql + ") VALUES('"
        sql = sql + "','".join(data.values())
        sql = sql + "')"
        status = self.cursor.execute(sql)
        self.conn.commit()
        return status

    def delete(self, tableName, condition):
        sql = "DELETE FROM " + tableName + " WHERE 1=1"
        if  type(condition) == dict:
            for i in condition.keys():
                sql = sql + " AND "+i+"=?"
        else:
            sql = sql + condition
        status = self.cursor.execute(sql, condition.values())
        self.conn.commit()
        return status

    def update(self, tableName, data,condition):
        sql = "UPDATE " + tableName + " SET "
        if  type(data) == dict:
            for i in data.keys():
                sql = sql + " AND "+i+"=?"
        else:
            sql = sql + data
        sql = sql + " WHERE 1=1 "
        if  type(condition) == dict:
            for i in condition.keys():
                sql = sql + " AND "+i+"=?"
        else:
            sql = sql + condition
        status = self.cursor.execute(sql, data.values()+condition.values())
        self.conn.commit()
        return status

    def execute(self,sql):
        status = self.cursor.execute(sql)
        self.conn.commit()
        return status