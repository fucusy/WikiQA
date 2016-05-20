__author__ = 'user'

class DB:
    host = "127.0.0.1"
    username = "root"
    password = ""
    database = "wikipedia"

project_base_path = "/Users/fucus/PycharmProjects/WikiQA/ExportMysqlDataToFile"

data_base_path = "/Volumes/Passport/WikiQA_DATA/data"

document_file_path = data_base_path+"/temp"
fragment_file_path = data_base_path+"/fragment"
log_file = project_base_path+"/log.txt"

last_split_process_id = 0
try:
    f = open(log_file)
    line = f.read()
    f.close()
    last_split_process_id = int(line.split(" ")[0])
except:
    pass
print "set last_split_process_id to %s" % last_split_process_id