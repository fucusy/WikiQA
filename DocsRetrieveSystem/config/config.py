__author__ = 'user'

module_path = "/Users/user/PycharmProjects/WikiQA/DocsRetrieveSystem"
log_file = module_path+"/log.txt"

class DB:
    host = "127.0.0.1"
    username = "root"
    password = ""
    database = "wiki_search"



class BM25:
    TF_Transformation_k = 3
    Length_Normalization_b = 0.5

docs_file_dir_1 = "/Volumes/Apple HD/Documents/scu.computer.scienct.2015.graduate.project/data/fragment"
docs_file_name_list_1 = "/Volumes/Apple HD/Documents/scu.computer.scienct.2015.graduate.project/data/fragment.list.txt"


docs_file_dir_2 = "/Volumes/Apple HD/Documents/scu.computer.scienct.2015.graduate.project/data/fragment1"
docs_file_name_list_2 = "/Volumes/Apple HD/Documents/scu.computer.scienct.2015.graduate.project/data/fragment1.list.txt"

wiki_entity_list_file_path = module_path+"/wiki_entity_list.txt"

test_file_path = "/Users/user/PycharmProjects/ExportMysqlDataToFile/temp/4.md"
file_folder = "temp"

stop_word_file_path = module_path + "/stopword.txt"

stop_word = []
stop_word_file = open(stop_word_file_path,"r")
for line in stop_word_file:
    line = line.strip()
    if line not in stop_word:
        stop_word.append(line)