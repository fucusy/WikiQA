__author__ = 'user'

from db.DBHelper import *

class Text:
    db =  DBHelper()

    def get_content_by_text_id(self, text_id = 1):
        sql = "SELECT old_text FROM text WHERE old_id = %d"%text_id
        result = self.db.run_sql(sql)
        return result[0][0]

t = Text()
t.get_content_by_text_id(1363831)