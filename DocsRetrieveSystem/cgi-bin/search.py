#!/usr/bin/python
#!encoding=utf8


# CGI处理模块
import cgi
import cgitb
import sys

sys.path.insert(1, '/Users/user/PycharmProjects/WikiQA/DocsRetrieveSystem')
from DocsRetrieveSystem.docs_process import *

# enable debug mode
cgitb.enable()

# 创建 FieldStorage 的实例化
form = cgi.FieldStorage() 

# 获取数据
q = form.getvalue('q')
q = "魔方"

print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<meta charset='UTF-8'>"
print "<title>Hello - Second CGI Program</title>"
print "</head>"
print "<body>"
print "<h2>你的问题是：%s</h2>" % q

print search(q)

print "</body>"
print "</html>"