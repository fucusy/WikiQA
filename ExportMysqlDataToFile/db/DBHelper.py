__author__ = 'user'

import MySQLdb

from config import DB
from helper.helper import Singleton

class DBHelper:
    db_config = DB
    connection = ''
    cursor = ''
    charset = 'utf8'
    __metaclass__ = Singleton
    def __init__(self):
        self.connection = MySQLdb.connect(self.db_config.host, self.db_config.username, self.db_config.password, self.db_config.database, charset = self.charset)
        self.cursor = self.connection.cursor()

    def run_sql(self, sql):
        result = None
        try:
            self.cursor.execute(sql)
            self.connection.commit()
            result = self.cursor.fetchall()
        except:
            print "fail to run sql: %s"%sql
            print self.connection.error()
            self.connection.rollback()
        return result
