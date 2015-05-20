#!encoding=utf8
__author__ = 'user'

from DocsRetrieveSystem.docs_process import *
from QuestionAnalysis.config.main import Location
from QuestionAnalysis.process.file import save_to_file
import QuestionAnalysis.process.file  as file

def xml_to_txt_question_answer():
    txt = ""
    for i in file.parse_xml(Location.question_answer_sample_file):
        txt += "%s:%s\n"%(i["q"].encode("utf8"),i["a"].encode("utf8"))
    save_to_file(txt,"question_answer_sample.txt",replace=True)


if __name__ == '__main__':
    xml_to_txt_question_answer()





