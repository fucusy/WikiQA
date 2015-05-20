#!/usr/bin/python
#!encoding=utf8



# CGI处理模块
import cgi
import sys
sys.path.insert(1, '/Users/user/PycharmProjects/WikiQA/DocsRetrieveSystem')
from DocsRetrieveSystem.docs_process import *
# 创建 FieldStorage 的实例化


#cgitb.enable()

form = cgi.FieldStorage() 

# 获取数据
first_name = form.getvalue('first_name')
last_name  = form.getvalue('last_name')

print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<meta charset='UTF-8'>"
print "<title>Hello - Second CGI Program</title>"
print "</head>"
print "<body>"
print "<h2>Hello %s %s</h2>" % (first_name, last_name)
print search("姚期智")

print "</body>"
print "</html>"