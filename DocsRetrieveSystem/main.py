#!encoding=utf8
__author__ = 'user'

from docs_process import *
import config

# def xml_to_txt_question_answer():
#     txt = ""
#     for i in file.parse_xml(Location.question_answer_sample_file):
#         txt += "%s:%s\n"%(i["q"].encode("utf8"),i["a"].encode("utf8"))
#     save_to_file(txt, "question_answer_sample.txt", replace=True)


if __name__ == '__main__':
    scan_files(config.fragment_file_dir)





