#!encoding=utf8
__author__ = 'user'

import operator
import random
import math

import jieba

from DocsRetrieveSystem.db.DBHelper import *
from QuestionAnalysis.config import NLP
from QuestionAnalysis.config import Location
from QuestionAnalysis.process.file import save_to_file


def remove_stop_word(s_list):
    result_list = []
    for s in s_list:
        if s not in NLP.get_stop_word():
            result_list.append(s)

    return result_list

def cut_remove_stop_word(q):
    q_list = jieba.cut(q)
    return remove_stop_word(q_list)

def get_doc_frequency(term_list):
    seg_doc_fre= {}
    e = entity()
    t = term()
    for seg in term_list:
        seg_doc_fre[seg] = 0
        term_id = t.get_term_id(seg)
        if term_id > 0:
            seg_term = term()
            seg_term.ini_by_term_id(term_id)
            seg_doc_fre[seg] = int(seg_term.doc_frequency)
    return seg_doc_fre

def get_key_word_list(q):
    key_word_list = []
    focus = extract_focus(q)
    cut_focus_list = cut_remove_stop_word(q.replace(focus,""))
    seg_frequency = get_doc_frequency(cut_focus_list)
    sorted_x = sorted(seg_frequency.items(), key=operator.itemgetter(1))
    selected = 3

    if len(sorted_x) >= selected:
        min_x = sorted_x[:selected]
    else:
        min_x = sorted_x

    for i in min_x:
        key_word_list.append(i[0])
    return key_word_list


class bayes_classifier():
    __metaclass__ = Singleton
    p_vector_dic = {}
    type_list = []
    word_list = []
    type_question_count = {}
    question_count = 0
    is_trained = False


    def train_process(self, question_type_tran_data = Location.question_type_tran_data):
        # word in type count
        type_word_dic = {}
        type_word_sum = {}
        self.p_vector_dic = {}
        self.type_list = []
        self.word_list = []
        self.type_question_count = {}
        self.question_count = 0

        with open(question_type_tran_data) as f:
            for line in f:
                split_line = line.split()
                if len(split_line) < 2:
                    continue
                self.question_count += 1
                words = cut_remove_stop_word(split_line[1])
                if split_line[0] not in self.type_list:
                    self.type_list.append(split_line[0])

                if not self.type_question_count.has_key(split_line[0]):
                    self.type_question_count[split_line[0]] = 1
                else:
                    self.type_question_count[split_line[0]] += 1

                if not type_word_dic.has_key(split_line[0]):
                    type_word_dic[split_line[0]] = {}

                if not type_word_sum.has_key(split_line[0]):
                    type_word_sum[split_line[0]] = 0

                for word in words:
                    type_word_sum[split_line[0]] += 1
                    if not type_word_dic[split_line[0]].has_key(word):
                        type_word_dic[split_line[0]][word] = 1
                    else:
                        type_word_dic[split_line[0]][word] += 1

                    if word not in self.word_list:
                        self.word_list.append(word)

        p1_vector = {}

        word_type_frequency = {}
        for w in self.word_list:
            word_type_frequency[w] = 0
            for t in self.type_list:
                if type_word_dic.has_key(t) and type_word_dic[t].has_key(w):
                    word_type_frequency[w] += 1

        for t in self.type_list:
            self.p_vector_dic[t] = {}
            type_word_t_sum = 0
            if type_word_sum.has_key(t):
                type_word_t_sum = type_word_sum[t]
            for w in self.word_list:
                word_count = 0
                if type_word_dic.has_key(t) and type_word_dic[t].has_key(w):
                    word_count = type_word_dic[t][w]

                word_type_frequency_w = 0
                if word_type_frequency.has_key(w):
                    word_type_frequency_w = word_type_frequency[w]
                self.p_vector_dic[t][w] = (0.5 + word_count) / (len(self.type_list) + type_word_t_sum) * math.log(len(self.type_list) + 0.1 / word_type_frequency_w + 0.1)

        self.is_trained = True

    def classify(self, q):
        if not self.is_trained:
            self.train_process()
        words = list(jieba.cut(q))
        class_score = {}
        for t in self.type_list:
            class_score[t] = 1
            for w in words:
                if w in self.word_list:
                    class_score[t] *= self.p_vector_dic[t][w]
            class_score[t] *= ( self.type_question_count[t]*1.0 / (self.question_count + 1))
        max_val = 0
        max_type = ""
        for t in class_score.keys():
            if class_score[t] > max_val:
                max_val = class_score[t]
                max_type = t
        return max_type
class q_classifier():
    q = ""
    focus = ""
    focus_index = 0

    class_score = {}
    class_contain_word = {
        "HUM_PERSON": (u"哪位", u"哪一位"),
        "HUM_ORG": (u"机构", u"公司"),
        "LOC_PLANET": (u"行星", u"星球"),
        "LOC_CITY": (u"城市",),
        "LOC_CONTINENT": (u"洲", u"大洲"),
        "LOC_COUNTRY": (u"国家", u"国"),
        "LOC_COUNTY": (u"县",),
        "LOC_STATE": (u"州",),
        "LOC_PROVINCE": (u"省份", u"省"),
        "LOC_TOWN": (u"镇", u"古镇"),
        "LOC_RIVER": (u"河", u"河流"),
        "LOC_LAKE": (u"湖", u"湖泊"),
        "LOC_MOUNTAIN": (u"山", u"山脉"),
        "LOC_OCEAN": (u"洋", u"海洋"),
        "LOC_ISLAND": (u"陆地", u"大陆"),
        "LOC_BASIC": (),
        "NUM_COUNT": (u"个", u"位"),
        "NUM_PRICE": (u"钱", u"奖金", u"金币", u"钞票"),
        "NUM_PERCENT": (u"百分比", u"百分"),
        "NUM_DISTANCE": (u"公里", u"里", u"长", u"长度", u"米", u"厘米", u"毫米"),
        "NUM_WEIGHT": (u"吨", u"公斤", u"斤", u"kg", u"g", u"克", u"公吨"),
        "NUM_DEGREE": (u"度",),
        "NUM_AGE": (u"年纪", u"年龄", u"岁数", u"岁"),
        "NUM_RANGE": (u"范围", ),
        "NUM_SPEED": (u"快", u"速度", u"速",u"米每秒"),
        "NUM_FREQUENCY": (u"频率", ),
        "NUM_SIZE": (u"容量", u"体积"),
        "NUM_AREA": (u"面积", u"多大", u"平方米", u"平方"),
        "NUM_BASIC": (),
        "TIME_YEAR": (u"年", u"年份"),
        "TIME_MONTH": (u"月", u"月份"),
        "TIME_DAY": (u"号", u"日"),
        "TIME_BASIC": (u"时候", u"时间"),
        "OBJ_CURRENCY": (u"货币", u"币"),
        "OBJ_MUSIC": (u"歌", u"音乐", u"名字"),
        "OBJ_MOVIE": (u"电影", u"部"),
        "OBJ_ANIMAL": (u"动物", ),
        "OBJ_COLOR": (u"颜色", u"色", u"色彩"),
        "OBJ_BASIC": ( ),
        "DES_ABB": (u"代表", u"什么", u"简称"),
        "DES_MEANING": (u"指", ),
        "DES_REASON": (u"原因", u"为什么"),
        "DES_BASIC": ()
    }





    def __init__(self,q):
        self.q = q
        self.focus = extract_focus(q)
        self.focus_index = q.find(self.focus)

    @staticmethod
    def get_class_label(p):
        classifier = bayes_classifier()
        return classifier.classify(p)

    def classify(self):
        """
        :return: 分类代码,分类代码，请参考论文
        """

        focus = extract_focus(self.q)

        if self.q.find("哪位") > -1 or self.q.find("哪一位"):
            class_label = "HUM_PERSON"

        for key in self.class_contain_word.keys():
            self.class_score[key] = 0
            for place_word in self.class_contain_word[key]:
                place_word_index = self.q.find(place_word)
                if place_word_index < 0:
                    continue

                if self.focus.find(place_word) > -1:
                    distance = 0
                elif place_word_index >= self.focus_index:
                    distance = place_word_index - self.focus_index - len(self.focus)
                else:
                    distance = - (place_word_index - self.focus_index )

                score = 0.5

                if distance <= 0:
                    score = 0.9
                elif distance <= 3:
                    score = 0.7
                else:
                    score = 0.5

                self.class_score[key] += score



        max_key = self.class_contain_word.keys()[0]
        max_value = 0

        for key in self.class_score.keys():
            if self.class_score[key] > max_value:
                max_value = self.class_score[key]
                max_key = key
        return max_key

def extract_focus(q):
    if q[-2:] == u"是？" or q[-2:] == u"为？":
        return q[-1:]
    seg_list = jieba.cut(q)
    seg_list = list(seg_list)

    for i in range(len(seg_list)):
        for word in NLP.get_question_place_word():
            if word == u"是？" or word == u"为？":
                continue
            if seg_list[i] == word:
                return word

    for seg in seg_list:
        for word in NLP.get_question_place_word():
            if word == u"是？" or word == u"为？":
                continue
            if seg.find(word, 0, len(word)) > -1:
                return seg
    return None

def is_q(q):
    return extract_focus(q) is not None


def question_analysis(q):
    seg_list = docs_to_vector(q).keys()

    seg_list_2 = []
    seg_info_dic = {}
    seg_doc_fre = {}
    e = entity()
    t = term()
    max_doc_fre = 10000000
    for seg in seg_list:
        seg_list_2.append(seg)
        seg_info_dic[seg] = ""
        seg_doc_fre[seg] = max_doc_fre
        if e.find(seg) is not None:
            seg_info_dic[seg] += u"wiki_entity,"
        term_id = t.get_term_id(seg)
        if term_id > 0:
            seg_term = term()
            seg_term.ini_by_term_id(term_id)
            seg_info_dic[seg] += u"term,doc_frequency=%s,"%seg_term.doc_frequency
            seg_doc_fre[seg] = seg_term.doc_frequency

    sorted_x = sorted(seg_doc_fre.items(), key=operator.itemgetter(1))
    min_x = sorted_x[:5]

    result = q+"\n"
    for seg in seg_list_2:
        result += seg + "(" + seg_info_dic[seg] + "),"
    for i in min_x:
        result += "\n" + i[0] + ":" + str(i[1])

    return result




def ten_fold_test():
    question_path = Location.question_type_tran_data
    question_set = []
    test_tran_file_name_tep  = "test-tran-data-%d.txt"

    with open(question_path) as f:
        for line in f:
            split_line = line.split()
            q_class = split_line[0]
            q_content = split_line[1]
            if q_class is None:
                continue
            q_dic = {"q_class":q_class,"q_content":q_content}
            question_set.append(q_dic)

    correct_class_sum = 0

    for i in range(10):
        choose_to_tran_number = 397
        candidate_number_list = [k for k in range(0,len(question_set))]
        chosen_number_list = []
        test_number_list = []
        while len(chosen_number_list) < choose_to_tran_number:
            choose = random.randrange(0, len(candidate_number_list))
            candidate_number_list.pop(choose)
            chosen_number_list.append(choose)
        test_number_list = candidate_number_list[:]
        type_tran_data = ""
        for n in chosen_number_list:
            type_tran_data += "%s  %s\n"%(question_set[n]["q_class"],question_set[n]["q_content"])

        file_name = test_tran_file_name_tep%i
        print "the file name is %s"%file_name
        save_to_file(type_tran_data, file_name,replace=True)
        b = bayes_classifier()
        b.train_process(Location.data_path+file_name)

        correct_class = 0
        for test_n in test_number_list:
            q_type = b.classify(question_set[test_n]["q_content"])
            if q_type == question_set[test_n]["q_class"]:
                #print "%s %s"%(q_type, question_set[test_n]["q_content"])
                correct_class += 1

        correct_class_sum += correct_class
        print "correct classify %d question"%correct_class
    print "correct classify %d questions in all"%correct_class_sum


def question_class_analysis():
    question_path = Location.question_type_tran_data
    class_count = {}
    class_count_sum = 0
    q_count_sum = 0

    with open(question_path) as f:
        for line in f:
            split_line = line.split()
            q_class = split_line[0]
            if q_class is None:
                continue

            q_count_sum += 1
            if class_count.has_key(q_class):
                class_count[q_class] += 1
            else:
                class_count[q_class] = 1
                class_count_sum += 1

    sorted_class_count = sorted(class_count.items(), key = operator.itemgetter(1), reverse=True )
    print u"问题类型,问题数量,问题数量百分比"
    for i in sorted_class_count:
        print "%s,%d,%.3f%%"%(i[0],i[1],i[1]*1.0/q_count_sum*100)



    print "%d class"%class_count_sum

if __name__ == '__main__':
    print q_classifier.get_class_label(u"现存所有老虎亚种中最小的亚种是？")