__author__ = 'user'

class DB:
    host = "127.0.0.1"
    username = "root"
    password = ""
    database = "zhwiki20141009"


project_base_path = "/Users/user/PycharmProjects/ExportMysqlDataToFile"

data_base_path = "/Volumes/Apple HD/Documents/scu.computer.scienct.2015.graduate.project/data"

document_file_path = data_base_path+"/temp"
document_file_path_1 = data_base_path+"/temp1"
fragment_file_path = data_base_path+"/fragment"
fragment_file_path_1 = data_base_path+"/fragment1"
log_file = project_base_path+"/log.txt"










last_split_process_id = 0
try:
    f = open(log_file)
    line = f.read()
    f.close()
    last_split_process_id = int(line.split(" ")[0])
except:
    pass



print last_split_process_id