#!encoding=utf8
__author__ = 'user'

import os
import time
import operator
from math import log

import jieba
from helper import helper
from config import stop_word
import config
from db.DBHelper import DBHelper
from db.DBHelper import term
from db.DBHelper import doc_term
from db.DBHelper import doc
from db.DBHelper import get_docs_count
from db.DBHelper import get_docs_average_len
from db.DBHelper import entity



def docs_to_vector(docs):
    """
    case insensitive

    :param docs: the docs is a fragment string
    :return: dictionary

    """
    docs = docs.lower()

    set_list = jieba.cut(docs)
    result = {}
    for term in set_list:
        if term in config.stop_word:
            continue
        if term in result.keys():
            result[term] += 1
        else:
            result[term] = 1
    return result

def get_stop_word(file_number=1000):
    file_name_list = os.listdir(config.docs_file_dir)
    f = open(config.stop_word_file_path,"wa")
    word_dict = {}

    file_counter = 0
    for file_name in file_name_list:
        file_counter += 1
        print file_counter
        if file_counter > file_number:
            break
        docs_file  = open(config.docs_file_dir + "/" + file_name,"r")
        docs_vec = docs_to_vector(docs_file.read())
        docs_file.close()
        for word in docs_vec:
            if word in word_dict.keys():
                word_dict[word] += 1
            else:
                word_dict[word] = 1
    sorted_word_dict = sorted(word_dict.items(),key=operator.itemgetter(1),reverse=True)

    counter = 0
    for (word,count) in sorted_word_dict:
        counter += 1
        if counter > 200:
            break

        if count > file_number * 0.75:
            print word + " " + str(count) + " " +  str(file_number)
        else:
            break

def scan_files(files_dir):
    """
    :param files_dir: the directory which contains fragments
            file_name_list: the filename list
    :return:
    """

    last_counter_id = 0
    try:
        f = open(config.log_file)
        line = f.read()
        f.close()
        last_counter_id = int(line.split(" ")[0])
    except:
        pass
    file_counter = 0
    for file_name in os.listdir(files_dir):
        if file_name[0] == '.':
            continue
        file_counter += 1
        if file_counter % 100 == 0:
            print "%d processed file %s" % (file_counter, file_name)
        if file_counter < last_counter_id:
            print "skip %d" % file_counter
            continue
        file_path = files_dir + "/" + file_name
        process(file_path)
        helper.log("%d processed file %s"%(file_counter, file_path))


def process(file_path):
    """
    :param file_path: the file path which is needed to process
    :return:None
    """
    try:
        doc_file = open(file_path,"r")
        docs = doc_file.read()
        doc_file.close()
    except:
        return

    doc_len = len(docs)
    d = DBHelper()

    doc_id = d.insert_record_with_var("insert into wiki_doc(`doc_len`,`doc_path`) VALUES (%s,%s)",(doc_len,file_path))
    d = docs_to_vector(docs)
    t = term()
    d_t = doc_term()
    for word in d:
        if word not in stop_word:
            term_id = 0
            if t.check_term_exist(word):
                term_id = t.get_term_id(word)
            else:
                term_id = t.insert_term(word,0)
            t.add_term_frequency(word)
            d_t.insert_record(term_id,doc_id,d[word])


def process_test():
    file_path = "/Volumes/Apple HD/Documents/scu.computer.scienct.2015.graduate.project/data/fragment/03式自動步槍-外部連結"
    try:
        doc_file = open(file_path,"r")
        docs = doc_file.read()
        doc_file.close()
    except:
        return

    doc_len = len(docs)
    d = DBHelper()
    d = docs_to_vector(docs)
    print d
def search(query):
    top_ten = top_ten_docs(query)
    count = 0
    result = "<ol>"
    for doc in top_ten:
        count += 1
        try:
            f = open(doc.doc_path)
            result += "<li>" + f.read() + "</li>\n"
            f.close()
        except:
            print "can not open %s"%doc.doc_path

    result += "</ol>"

    return result

def top_ten_docs(query):
    """
    search docs from database
    :param query the query is a list
    :return:
    """

    top_ten = []
    start = time.time()
    s_vec = {}
    for k in query:
        if s_vec.has_key(k):
            s_vec[k] += 1
        else:
            s_vec[k] = 1


    helper.log("using %ss to vector %s "%(time.time() - start, ",".join(query)))

    start = time.time()
    average_len = get_docs_average_len()
    doc_count = get_docs_count()
    helper.log("using %ss to get average length and docs count"%(time.time() - start))

    doc_rank = {}
    doc_term_count = {}
    doc_length = {}
    term_dic = {}


    start = time.time()

    doc_list_result = []
    doc_list_result_init = False
    for word in s_vec.keys():

        # for each word add {term_id}->{ "term"=> {term}, "doc_frequency"=> {doc_frequency} } into term_dic
        # get docs which contain these word
        # add doc_id -> 0 into docs_rank dictionary
        # add {doc_id}-{term_id} -> count into doc_term_count dictionary
        # if doc_id not exists in doc_length, get doc_length and save {doc_id}->{doc_length} into doc_length

        t = term()
        d_t = doc_term()
        term_id = t.get_term_id(word)
        if term_id == 0:
            continue
        t.ini_by_term_id(term_id)
        term_dic[term_id] = {"term": t.term, "doc_frequency": t.doc_frequency}

        doc_term_list = d_t.get_doc_term_list_by_term_id(term_id)

        doc_list = [d.doc_id for d in doc_term_list]
        if doc_list_result_init:
            new_doc_list_result = []
            for i in doc_list:
                if i in doc_list_result:
                    new_doc_list_result.append(i)
            doc_list_result = list(new_doc_list_result)

        else:
            doc_list_result = list(doc_list)
            doc_list_result_init = True

        for doc_term_item in doc_term_list:
            if doc_term_item.doc_id in doc_list_result and doc.check_term_exist_by_id(doc_term_item.doc_id):
                doc_term_count["%d-%d"%(doc_term_item.doc_id, doc_term_item.term_id)] = doc_term_item.count
    for i in doc_list_result:
        doc_rank[i] = 0

    for doc_item_id in doc_rank.keys():
        d = doc()
        d.ini_by_id(doc_item_id)
        doc_length[doc_item_id] = d.doc_len

    helper.log("using %s s to gather all the data"%(time.time() - start))

    #calculate the rank result

    start = time.time()
    M = doc_count
    k = config.BM25.TF_Transformation_k
    b = config.BM25.Length_Normalization_b
    average_len = int(get_docs_average_len())

    for doc_id in doc_rank.keys():
        score = 0
        for term_id in term_dic.keys():
            doc_term_id = "%d-%d"%(doc_id, term_id)
            if doc_term_id  in doc_term_count.keys():

                c_w_q = s_vec[term_dic[term_id]["term"]]
                c_w_d = doc_term_count[doc_term_id]

                d_len = doc_length[doc_id]

                d_f_w = term_dic[term_id]["doc_frequency"]


                doc_term_score = c_w_q * c_w_d * (k + 1) * 1.0
                doc_term_score /= (c_w_q + k*(1 - b + b * d_len / average_len))
                doc_term_score *= log((M + 1) * 1.0 / d_f_w)
                score += doc_term_score
        doc_rank[doc_id] = score

    sorted_doc_rank = sorted(doc_rank.items(), key = operator.itemgetter(1),reverse=True)

    helper.log("using %ss to calculate the score of all relevative docs"%(time.time() - start))

    item_count = 0
    for (doc_id, score) in sorted_doc_rank:
        d = doc()
        d.ini_by_id(doc_id)
        top_ten.append(d)
        item_count += 1

        if item_count >= 10:
            break

    result_fragment = []



    for d in top_ten:
        try:
            f = open(d.doc_path)
            fragment_doc = f.read()
            result_fragment.append(fragment_doc)


            f.close()
        except:
            print "can not open %s"%doc.doc_path


    return result_fragment

def build_wiki_entity_list():
    file_name_list = [config.docs_file_name_list_1, config.docs_file_name_list_2]
    entity_file = open(config.wiki_entity_list_file_path,"w")
    entity_file.close()

    entity_file = open(config.wiki_entity_list_file_path,"wa")


    for i in file_name_list:
        f = open(i,"r")
        for line in f.readlines():
            line = line.strip()
            if line[-1] == '-':
                entity_file.write(line[:-1]+"\n")
    entity_file.close()

def insert_wiki_entity_from_list():
    entity_file = open(config.wiki_entity_list_file_path,"r")

    e = entity()

    for line in entity_file.readlines():
        result = e.insert(line.strip())
        if result == 0:
            print line.strip()
    entity_file.close()


