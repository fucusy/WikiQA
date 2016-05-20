__author__ = 'user'
import os


module_path = "/Users/fucus/PycharmProjects/WikiQA/DocsRetrieveSystem"
log_file = module_path+"/log.txt"

class DB:
    host = "127.0.0.1"
    username = "root"
    password = ""
    database = "wiki_search"


class BM25:
    TF_Transformation_k = 3
    Length_Normalization_b = 0.5

fragment_file_dir = "/Volumes/Passport/WikiQA_DATA/data/fragment/"

wiki_entity_list_file_path = module_path+"/wiki_entity_list.txt"

stop_word_file_path = module_path + "/stopword.txt"

stop_word = set()
if os.path.exists(stop_word_file_path):
    stop_word_file = open(stop_word_file_path, "r")
    for line in stop_word_file:
        line = line.strip()
        stop_word.add(line.decode('utf8'))