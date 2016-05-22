#!encoding=utf8
__author__ = 'user'

import config
import sys
sys.path.append("%s/../" % config.Location.module_path)

from QuestionAnalysis.process import file
from QuestionAnalysis.process import question
from DocsRetrieveSystem.docs_process import *
from AnswerExtraction.process.answer import *




def main_debug():
    count = 0
    start = False

    process_data = {'QuestionSet': {'question': []}}
    e = entity()

    count = 0
    find_answer_count = 0

    result_txt = ""

    for i in file.parse_xml(Location.question_answer_sample_file):

        result_txt += "%s:%s:" % (i["q"],i["a"])
        if question.is_q(i["q"]):
            if e.find(i["a"]) is not None:
                count += 1
                #print "%s in entity list"%i["a"]
            key_word_list = question.get_key_word_list(i["q"])
            result_txt += ",".join(key_word_list) + ":"
            #print "search by the key words list~"
            fragments_list = top_ten_docs(key_word_list)

            if len(fragments_list) == 0:
                continue

            #print "the fragment_list is:"

            f_str =  ""
            # for f in fragments_list:
            #     print f
            #     if f.find(i["a"].encode("utf8")) > -1:
            #         print "this fragment contains the answer"

            for f_i in range(len(fragments_list)):
                f_str += "%d,%s."%(f_i+1, fragments_list[f_i])

            result_txt += f_str.decode("utf8")
            result_txt += ":"

            if f_str.find(i["a"].encode("utf8")) > -1:
                result_txt += "%s:" % (u"包含",)
            else:
                result_txt += "%s:" % (u"不包含",)

            result_txt += "\n"

            top_passage = select_top_passage(i["q"], fragments_list)
            print "top passage is %s"%top_passage

            if top_passage.find(i["q"].encode("utf8")) > -1:
                print "this passage contains the answer"

            final_answer = extract_answer(i["q"], top_passage)
            print "the final answer is %s"%final_answer

            if final_answer == i["a"]:
                print "!!!!! found the answer"
                find_answer_count += 1

        else:
            print "this is not a question"
        count += 1
    save_to_file(result_txt.encode("utf8"),"document_retrieve_system.txt",replace=True)
    print "the question number:%s"%count
    print "find %s answer"%find_answer_count



def test_answer_extraction():
    count = 0
    start = False

    process_data = {'QuestionSet': {'question': []}}
    e = entity()

    count = 0
    find_answer_count = 0

    result_txt = ""

    for i in file.parse_xml(Location.question_answer_sample_file):


        if question.is_q(i["q"]):
            if e.find(i["a"]) is not None:
                count += 1
                #print "%s in entity list"%i["a"]
            key_word_list = question.get_key_word_list(i["q"])

            #print "search by the key words list~"
            fragments_list = top_ten_docs(key_word_list)

            if len(fragments_list) == 0:
                continue

            f_str = ""

            for f_i in range(len(fragments_list)):
                f_str += "%d,%s."%(f_i+1, fragments_list[f_i])

            if f_str.find(i["a"].encode("utf8")) > -1:
                result_txt += "%s:%s:" % (i["q"],i["a"])
                result_txt += ",".join(key_word_list) + ":"

                t_passage = select_top_passage(i["q"], fragments_list)
                result_txt += "%s:"%t_passage.decode("utf8")

                if t_passage.find(i["a"].encode("utf8")) > -1:
                    result_txt += "%s:" % (u"包含",)
                else:
                    result_txt += "%s:" % (u"不包含",)

                final_answer = extract_answer(i["q"], t_passage)
                result_txt += "%s:"%final_answer

                result_txt += "\n"


        else:
            print "this is not a question"
        count += 1
    save_to_file(result_txt.encode("utf8"),"answer_extraction.txt",replace=True)
    print "the question number:%s"%count
    print "find %s answer"%find_answer_count



def bool_search_debug():
    key_word_list = [u"外语片",u"华语",u"奥斯卡"]

    print "key word list :" + ",".join(key_word_list)
    print "search result :"
    fragment_list = top_ten_docs(key_word_list)
    for f in fragment_list:
        print f

if __name__ == '__main__':
    main_debug()