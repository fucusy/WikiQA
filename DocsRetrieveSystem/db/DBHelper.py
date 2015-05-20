#!encoding=utf8
__author__ = 'user'

import MySQLdb

from DocsRetrieveSystem.config.config import DB
from DocsRetrieveSystem.helper.helper import Singleton
from DocsRetrieveSystem import helper


doc_table = "wiki_doc"
term_doc_table = "wiki_term_doc"

docs_count_cache_id = "docs_count"
docs_average_len_cache_id = "docs_average_len"


class DBHelper:
    __metaclass__ = Singleton
    db_config = DB
    connection = ''
    cursor = ''
    charset = 'utf8'
    def __init__(self):
        self.connection = MySQLdb.connect(self.db_config.host, self.db_config.username, self.db_config.password, self.db_config.database, charset = self.charset)
        self.cursor = self.connection.cursor()

    def get_scalar(self,sql):
        result = self.run_sql(sql)
        if result is not None and len(result) > 0 and len(result[0]) > 0:
            return result[0][0]

        return None

    def run_sql_with_var(self, sql, var_tuple):

        result = None
        try:
            self.cursor.execute(sql,var_tuple)
            self.connection.commit()
            result = self.cursor.fetchall()

        except:
            print "fail to run sql: %s"%sql
            print "with tuple"
            for i in var_tuple:
                print i
            print self.connection.error()
            self.connection.rollback()
        return result
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

    def insert_record_with_var(self,sql,var_tuple):

        self.run_sql_with_var(sql,var_tuple)

        return self.cursor.lastrowid

    def insert_record(self,sql):
        self.run_sql(sql)
        return self.cursor.lastrowid

class doc_term:
    table_name = "wiki_doc_term"

    db = DBHelper()

    doc_id = ""
    term_id = ""
    count = ""


    def get_doc_term_list_by_term_id(self,term_id):
        doc_term_list = []
        sql = "select `doc_id`, `count` from %s where `term_id` = %d "%(self.table_name, term_id)
        result = self.db.run_sql(sql)
        for r in result:
            t = doc_term()
            t.term_id = term_id
            t.doc_id = r[0]
            t.count = r[1]
            doc_term_list.append(t)
        return doc_term_list


    def insert_record(self,term_id,doc_id,count):
        """
        :param term_id:
        :param doc_id:
        :param count:
        :return: True if insert success else False
        """
        t = term()
        d = doc()
        result = False
        if t.check_term_exist_by_term_id(term_id) and d.check_term_exist_by_id(doc_id) and count > 0:
            sql = "insert into %s (`term_id`,`doc_id`,`count`) VALUES (%d,%d,%d)"%(self.table_name,term_id,doc_id,count)

            self.db.run_sql(sql)


            result = True

        return result

class doc:
    table_name = "wiki_doc"

    doc_id = ""
    doc_len = ""
    doc_path = ""

    db = DBHelper()

    def ini_by_id(self,id):

        is_init = False

        self.doc_id = id
        if self.check_term_exist_by_id(id):

            sql = "select `doc_len`, `doc_path`  from  %s  where `doc_id`  = %d"%(self.table_name, id)
            result = self.db.run_sql(sql)
            if len(result) > 0:
                self.doc_len = int(result[0][0])
                self.doc_path = result[0][1]
                is_init = True
        return is_init

    @staticmethod
    def check_term_exist_by_id(id):
        """

        :param term_id:
        :return: True if term_id exists else False
        """
        criteria = "doc_id = %d"%id
        d = doc()
        return d.get_doc_id_by_criteria(criteria) > 0

    def get_doc_id_by_criteria(self, criteria):
        """
        :param criteria:
        :return: if none exists return 0
        """
        sql = "select doc_id from %s where %s  limit 1"%(self.table_name, criteria)
        d = DBHelper()
        result = d.run_sql(sql)
        if len(result) > 0:
            return result[0][0]
        else:
            return 0

class term:

    table_name = "wiki_term"

    db = DBHelper()

    doc_frequency = ""
    term = ""
    term_id = ""

    def ini_by_term_id(self,term_id):

        is_init = False

        self.term_id = term_id
        if self.check_term_exist_by_term_id(term_id):

            sql = "select doc_frequency, term from wiki_term where term_id  = %d"%term_id

            result = self.db.run_sql(sql)
            if len(result) > 0:
                self.doc_frequency = result[0][0]
                self.term = result[0][1]
                is_init = True
        return is_init



    def add_term_frequency(self,term,add=1):
        """
        :param term:
        :param add:
        :return: True if success else False
        """
        result = False

        if self.check_term_exist(term):
            sql = "update %s set `doc_frequency` = `doc_frequency` + %d where term = '%s' "%(self.table_name,add, term)
            self.db.run_sql(sql)
            result = True
        return result

    def insert_term(self,term,doc_frequency = 1):
        """

        :param term:
        :param doc_frequency:
        :return: if insert success return term_id, else return 0
        """
        term_id = 0
        if not self.check_term_exist(term):
            sql = "insert into %s(`term`,`doc_frequency`) VALUES ('%s', %s)"
            term_id = self.db.insert_record(sql%(self.table_name, term, doc_frequency))
        return term_id


    def get_term_id_by_criteria(self, criteria):
        """
        :param criteria:
        :return: if none exists return 0
        """
        sql = "select term_id from %s where %s  limit 1"%(self.table_name, criteria)
        d = DBHelper()
        result = d.run_sql(sql)

        if result is not None and len(result) > 0:
            return result[0][0]
        else:
            return 0

    def check_term_exist(self,term):
        """
        :param term:
        :return: True or False
        """
        return self.get_term_id(term) != 0

    def check_term_exist_by_term_id(self,term_id):
        """

        :param term_id:
        :return: True if term_id exists else False
        """
        criteria = "term_id = %d"%term_id
        return self.get_term_id_by_criteria(criteria) > 0

    def get_term_id(self,term):
        """
        :param term:
        :return: if term no exist it will return 0
        """

        criteria = """term = "%s" """%term
        return self.get_term_id_by_criteria(criteria)

    @staticmethod
    def get_doc_frequency_by_term(s):
        t = term()
        term_id = t.get_term_id(s)
        t.ini_by_term_id(term_id)
        return t.doc_frequency

class entity():
    table_name = "wiki_entity"
    db = DBHelper()

    entity_name = ""
    term_id = None

    def find(self,wiki_name):
        sql = """select entity_id, entity_name, term_id from %s where `entity_name` = "%s" """%(self.table_name,wiki_name)
        result = self.db.run_sql(sql)

        if result is not None and len(result) >= 1 and len(result[0]) >= 3:
            self.entity_id = result[0][0]
            self.entity_name = result[0][1]
            self.term_id = result[0][2]
            return self
        return None

    def insert(self, entity_name):
        """
        :param term:
        :param doc_frequency:
        :return: if insert success return term_id, else return 0
        """
        entity_id = 0
        if self.find(entity_name) is  None:
            sql = """insert into %s(`entity_name`,`term_id`) VALUES ("%s", "%s")"""
            t = term()
            term_id =  t.get_term_id(entity_name)
            if term_id == 0:
                term_id = ''
            entity_id = self.db.insert_record(sql%(self.table_name, entity_name, term_id))
        return entity_id

def get_docs_count():
    db = DBHelper()

    cache_value = db.get_scalar("select `value` from wiki_data where `data_name` = '%s' "%docs_count_cache_id)
    if cache_value is None:
        docs_count = db.get_scalar("select count(*) from wiki_doc")
        db.insert_record("insert into wiki_data(`data_name`,`value`,`last_update`) VALUES ('%s','%s','%s')"%( docs_count_cache_id, docs_count, helper.get_datetime()))
    else:
        docs_count = cache_value
    return float(docs_count)

def get_docs_average_len():
    db = DBHelper()

    cache_value = db.get_scalar("select `value` from wiki_data where `data_name` = '%s' "%docs_average_len_cache_id)
    if cache_value is None:
        average_len = db.get_scalar("select AVG(`doc_len`) from wiki_doc")
        db.insert_record("insert into wiki_data(`data_name`,`value`,`last_update`) VALUES ('%s','%s','%s')"%( docs_average_len_cache_id, average_len, helper.get_datetime()))
    else:
        average_len = cache_value
    return float(average_len)





def update_cache():

    db = DBHelper()
    docs_count = db.get_scalar("select count(*) from wiki_doc")
    update_cache_data(docs_count_cache_id, docs_count)

    ave_len = db.get_scalar("select AVG(`doc_len`) from wiki_doc")
    update_cache_data(docs_average_len_cache_id, ave_len)

def update_cache_data(key, value):
    db = DBHelper()
    db.run_sql("update wiki_data set `value` = '%s' , `last_update` = '%s' where `data_name` = '%s'"%( value, helper.get_datetime(),key))

