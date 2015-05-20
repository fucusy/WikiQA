__author__ = 'user'

import xmldict
import os
import random
from QuestionAnalysis.config.main import Location
import operator

def parse_xml(file_path):
    f = open(file_path,"r")
    result = xmldict.xml_to_dict(f.read())
    f.close()
    return result['QuestionSet']['question']

def dic_to_xml(dic):
    return xmldict.dict_to_xml(dic)


def save_to_file(data, file_name = "", replace=False):
    if file_name == "":
        file_name = random.random()

    count = 1
    old_file_name = file_name

    file_location = "%s/data/%s"%(Location.module_path, file_name)

    if not replace:
        while os.path.isfile(file_location):
            print file_name + "already exist "
            file_name = old_file_name + str(count)
            count += 1
            print "change filename to %s"%file_name
            file_location = "%s/data/%s"%(Location.module_path, file_name)
    else:
        if os.path.isfile(file_location):
            print "%s file already exist, now it will be over writed"



    with open(file_location, "w") as f:
        f.write(data)


def temp_count_type():
    type_count = {}

    count_sum = 0

    with open(Location.module_path+"/data/question_type_data.txt","r") as f:
        for line in f:
            count_sum += 1
            split =  line.split()
            if not type_count.has_key(split[0]):
                type_count[split[0]] = 1
            else:
                type_count[split[0]] += 1

    sort_type_count = sorted(type_count.items(), key=operator.itemgetter(1),reverse=True )

    for i in sort_type_count:
        percent = i[1]*1.0 / count_sum
        print "%s count :%d, percent %.5s"%(i[0], i[1], percent )

def temp_xml_to_text():
    d = parse_xml(Location.module_path+"/data/question_type_data.xml")
    q_to_t = {}
    for i in d:
        if i["t"].__class__.__name__ == "str":
            if not q_to_t.has_key(i["q"]):
                q_to_t[i["q"]] = i["t"]
    sort_q_to_t = sorted(q_to_t.items(), key = operator.itemgetter(1))
    s = ""
    for i in sort_q_to_t:
        s += i[1] + "\t" + i[0] + "\n"

    save_to_file(s,"question_type_data.txt")

if __name__ == '__main__':
    q_to_t = {}
    with open(Location.module_path+"/data/question_type_data.txt2","r") as f:
        for line in f:
            split = line.split()
            q_to_t[split[1]] = split[0]
    sort_q_to_t = sorted(q_to_t.items(), key = operator.itemgetter(1))
    s = ""
    for i in sort_q_to_t:
        s += i[1] + "\t" + i[0] + "\n"

    save_to_file(s,"question_type_data.txt")