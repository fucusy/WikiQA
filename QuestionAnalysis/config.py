__author__ = 'user'


class DB:
    host = "127.0.0.1"
    username = "root"
    password = ""
    database = "wiki_search"


class Location:
    module_path = "/Users/fucus/PycharmProjects/WikiQA/QuestionAnalysis"
    question_place_word_file = module_path + "/data/question.place.word.txt"
    test_set_file = "/Users/fucus/PycharmProjects/WikiQA/data/question_without_answer_100000.xml"
    question_answer_sample_file = "/Users/fucus/PycharmProjects/WikiQA/data/question_with_answer_100.xml"

    stop_word_file_path = "/Users/fucus/PycharmProjects/WikiQA/DocsRetrieveSystem/stopword.txt"

    question_type_tran_data = module_path + "/data/question_type_data.txt"
    data_path = module_path+"/data/"


class NLP:
    @staticmethod
    def get_stop_word():
        stop_word = []
        stop_word_file = open(Location.stop_word_file_path,"r")
        for line in stop_word_file:
            line = line.strip()
            line = line.decode("utf8")
            if line not in stop_word:
                stop_word.append(line)
        return stop_word

    @staticmethod
    def get_question_place_word():
        stop_word = []
        stop_word_file = open(Location.question_place_word_file,"r")
        for line in stop_word_file:
            line = line.strip()
            line = line.decode("utf8")
            if line not in stop_word:
                stop_word.append(line)
        return stop_word