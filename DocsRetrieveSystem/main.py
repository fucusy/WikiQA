#!encoding=utf8
__author__ = 'user'

from docs_process import *
import config
import sys

# def xml_to_txt_question_answer():
#     txt = ""
#     for i in file.parse_xml(Location.question_answer_sample_file):
#         txt += "%s:%s\n"%(i["q"].encode("utf8"),i["a"].encode("utf8"))
#     save_to_file(txt, "question_answer_sample.txt", replace=True)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "do_index_to_database":
        scan_files(config.fragment_file_dir)
    elif len(sys.argv) > 2 and sys.argv[1] == "search":
        related_fragments = search(sys.argv[2])
        count = 0
        for fragment in related_fragments:
            count += 1
            print("%d:%s" % (count, fragment))
    else:
        print("usage: python main.py do_index_to_database")
        print("or:python main.py search {your_query}, if your query is 天安门, you should run: python main.py search 天安门")









