__author__ = 'user'
from db.Text import *

class Page():
    page_id = ""
    page_title = ""
    page_content = ""
    text = Text()
    db =  DBHelper()

    def get_pages(self, offset=0, number=10, min_page_len=0):
        result = list()
        if number == -1:
            sql = "SELECT page_id,page_title,page_latest FROM page WHERE page_len >= %d offset %d" % (min_page_len, offset)
        else:
            sql = "SELECT page_id,page_title,page_latest FROM page WHERE page_len >= %d limit %d offset %d" % (min_page_len, number, offset)
        query_result = self.db.run_sql(sql)
        for r in query_result:
            temp_p = Page()
            temp_p.page_id = r[0]
            temp_p.page_title = r[1]
            temp_p.page_content = self.text.get_content_by_text_id(r[2])
            result.append(temp_p)
        return result