#!/usr/bin/python


import cgitb
import sys

sys.path.insert(1, '/Users/user/PycharmProjects/WikiQA/DocsRetrieveSystem')
cgitb.enable()

from DocsRetrieveSystem.docs_process import *

print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<meta charset='UTF-8'>"
print "<title>Hello - Second CGI Program</title>"
print "</head>"
print "<body>"
print "<h2>Hello %s %s</h2>"

print search("天上人间")

print "</body>"
print "</html>"