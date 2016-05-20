__author__ = 'user'

import os
import re

from db.Page import *
import config
from helper import helper


# TODO LIST
#1. remove attribute noise in the text according rule on wikipedia.
#2. build table to store information used to compute the similarity of query and documents
#3. write program to compute information used to compute the similarity of query and documents





def split_document_to_fragment(document):
    """
    :param document: the text string
    :return: fragment_list, formatted as [{"title":"this is title content","content":"content"},{},{}]
    """


    document = re.sub("\[\[(Category|Wikipedia)\:(.*?)\|(.*?)\]\]","\g<2>,\n",document,flags=re.DOTALL)



    remove_list = ["<ref>.*?</ref>","{\|.*?\|}","<.*?>","{{.*?}}","\[\[File:.*?\]\]"]
    for remove in remove_list:
        document = re.sub(remove,"",document,flags=re.DOTALL)


    replace_list = ["\[\[(.*?)\]\]","'''''(.*?)'''''","'''(.*?)'''","''(.*?)''"]
    for replace in replace_list:
        document = re.sub(replace,"\g<1>",document,flags=re.DOTALL)


    document = re.sub("^\n","",document,flags=re.MULTILINE)
    document = re.sub("^----","",document,flags=re.MULTILINE)

    document = re.sub("^[\*|#](.*?)\n","\g<1>,\n",document,flags=re.MULTILINE)





    lines = document.split("\n")

    title = lines[0]
    sub_title = ""
    fragment_list = []

    fragment_content = ""
    for line in lines[1:]:
        is_split = re.match("==.*?==",line) is not None
        if is_split:
            fragment = {"title":title+"-"+sub_title,"content":fragment_content}
            fragment_list.append(fragment)
            fragment_content = ""
            sub_title = line.strip("=").strip()
        else:
            fragment_content += line



    fragment = {"title":title+"-"+sub_title,"content":fragment_content}
    fragment_list.append(fragment)


    #do some ending work
    for f in fragment_list:
        f["content"] = re.sub("\n","",f["content"])
        f["content"] = re.sub(" ","",f["content"])
    return fragment_list



## init work

def extract_from_db_to_file_system(min_page_len=500):
    """
    :param min_page_len:
    :return:
    """
    folder = "%s/temp" % config.data_base_path
    if not os.path.exists(folder) or not os.path.isdir(folder):
        os.makedirs(folder)
    p = Page()
    counter = 1
    batch_size = 1000
    offset = 0
    limit = batch_size
    batch_result = p.get_pages(offset, limit, min_page_len)
    while len(batch_result) > 0:
        for r in batch_result:
            file_path = "%s/%s.md" % (folder, counter)
            f = open(file_path, "w")
            f.write(r.page_title.encode("utf8"))
            f.write("\n")
            f.write(r.page_content)
            f.close()
            if counter % 100 == 0:
                print("extract %d th page now" % counter)
            counter += 1
        offset += batch_size
        batch_result = p.get_pages(offset, limit, min_page_len)


def save_fragment_list_to_file_system(fragment_list):
    save_path = config.fragment_file_path
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    result = False
    for fragment in fragment_list:
        file_name = fragment["title"]
        content = fragment["content"]
        if content == "":
            continue
        try:
            f = open(save_path+"/"+file_name,"w")
            f.write(content)
            f.close()
            result = True
        except:
            result = False
    return result

def split_documents_test(file_name):
    file_name_list = [file_name]

    file_counter = 0
    for file_name in file_name_list:
        print file_counter
        #ingore hidden file
        if file_name[0] == '.':
            continue
        file_counter += 1

        file_path = config.document_file_path + "/" + file_name
        doc_file  = open(file_path,"r")
        content = doc_file.read()

        fragment_list = split_document_to_fragment(content)

        save_fragment_list_to_file_system(fragment_list)

        log_text = "%d processed file %s"%(file_counter, file_path)
        print log_text
        helper.log(log_text)
        doc_file.close()


def split_documents(start=0):
    file_name_list = os.listdir(config.document_file_path)
    file_counter = 0
    for file_name in file_name_list:
        # ignore hidden file
        if file_name[0] == '.':
            continue
        file_counter += 1
        if file_counter < start:
            print "skip %d" % file_counter
            continue

        file_path = config.document_file_path + "/" + file_name
        doc_file  = open(file_path, "r")
        content = doc_file.read()

        fragment_list = split_document_to_fragment(content)
        save_fragment_list_to_file_system(fragment_list)
        log_text = "%d processed file %s"%(file_counter, file_path)
        if file_counter % 100 == 0:
            print "split  %d th page now" % file_counter
        helper.log(log_text)

