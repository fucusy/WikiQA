#!encoding=utf8
__author__ = 'user'


from QuestionAnalysis.process.question import *
from AnswerExtraction.helper import helper
import jieba.posseg as pseg
from AnswerExtraction.config.config import project

import nltk

class_to_tag = {
        "HUM_PERSON": "nr",
        "HUM_ORG": "nt",
        "LOC_PLANET": "nz",
        "LOC_CITY": "ns",
        "LOC_CONTINENT": "n",
        "LOC_COUNTRY": "n",
        "LOC_COUNTY": "ns",
        "LOC_STATE": "ns",
        "LOC_PROVINCE": "ns",
        "LOC_TOWN": "ns",
        "LOC_RIVER": "ns",
        "LOC_LAKE": "n",
        "LOC_MOUNTAIN": "n",
        "LOC_OCEAN": "n",
        "LOC_ISLAND": "n",
        "LOC_BASIC": "ns",
        "NUM_COUNT": "m",
        "NUM_PRICE": "m",
        "NUM_PERCENT": "m",
        "NUM_DISTANCE": "m",
        "NUM_WEIGHT": "m",
        "NUM_DEGREE": "m",
        "NUM_AGE": "m",
        "NUM_RANGE": "m",
        "NUM_SPEED": "m",
        "NUM_FREQUENCY": "m",
        "NUM_SIZE": "m",
        "NUM_AREA": "m",
        "NUM_BASIC": "m",
        "TIME_YEAR": "m",
        "TIME_MONTH": "m",
        "TIME_DAY": "m",
        "TIME_BASIC": "m",
        "OBJ_CURRENCY": "m",
        "OBJ_MUSIC": "n",
        "OBJ_MOVIE": "n",
        "OBJ_ANIMAL": "n",
        "OBJ_COLOR": "n",
        "OBJ_BASIC": "n",
        "DES_ABB": "nz",
        "DES_MEANING": "n",
        "DES_REASON": "n",
        "DES_BASIC": "n"
    }

tag_to_class = {}
for key in class_to_tag.keys():
    val = class_to_tag[key]
    if tag_to_class.has_key(val):
        tag_to_class[val].append(key)
    else:
        tag_to_class[val] = [key, ]


def answer_type_tagger(passage):
    answer_type_list = []

    f_list = pseg.cut(passage)
    f_dic_list = []
    for w in f_list:
        f_dic_list.append({"word": w.word, "flag": w.flag})


    for word in f_dic_list:
        answer_type_list.append({word["word"]:[]})

    for i in range(len(f_dic_list)):
        word = f_dic_list[i]["word"]
        flag = f_dic_list[i]["flag"]
        # skip if it label is m, but is not numeric

        if flag == "m" and not helper.is_numeric(word):
            continue

        for key in q_classifier.class_contain_word:
            if i + 1 < len(f_dic_list) and f_dic_list[i+1]["word"] in q_classifier.class_contain_word[key]:
                answer_type_list[i][word].append(key)

        if flag.find("nr") > -1:
            answer_type_list[i][word].append("HUM_PERSON")

        for key in tag_to_class.keys():
            if key == "m":
                continue
            if flag.find(key) > -1:
                for tag in tag_to_class[key]:
                    if tag not in answer_type_list[i][word]:
                        answer_type_list[i][word].append(tag)

    return answer_type_list


def select_top_passage(q, fragments):
    """
    :param q: question
    :param fragments: list of fragment( string )
    :return:
    """
    passages = []
    for f in fragments:
        for p in f.split("。"):
            passages.append(p)
    if len(passages) == 0:
        return ""

    q_class = q_classifier.get_class_label(q)

    focus = extract_focus(q)
    q_list = cut_remove_stop_word(q.replace(focus,""))
    count_passages = len(passages)
    score = [0]*count_passages

    for i in range(count_passages):

        tagger = answer_type_tagger(passages[i])
        contain_tag = []
        for t in tagger:
            for tag in t[t.keys()[0]]:
                contain_tag.append(tag)
        if q_class not in contain_tag:
            score[i] = -10000
            continue

        f_list = cut_remove_stop_word(passages[i])
        index_count = 0
        word_position_dic = {}
        #init postion to -1
        for word in q_list:
            word_position_dic[word] = -1

        for f_word in f_list:
            if f_word in q_list and word_position_dic[f_word] == -1:
                word_position_dic[f_word] = index_count
            index_count += 1
        found_count = 0
        term_doc_frequency_sum = 0
        num_list = []
        for word in q_list:
            if word_position_dic[word] != -1:
                num_list.append(word_position_dic[word])
                found_count += 1
                term_doc_frequency_sum = term.get_doc_frequency_by_term(word)
        exchange_count = 0
        for t in range(len(num_list)):
            for j in range(t,len(num_list)):
                if num_list[t] > num_list[j]:
                    exchange_count += 1

        score[i] = found_count*100.0 / (exchange_count+1)
        score[i] = score[i]*1.0/ ( ( term_doc_frequency_sum * 1.0 / (found_count + 1)) + 1 )


    if project.is_debug:
        print "the passage scores are:"
        for i in range(count_passages):
            print "%s:%s"%(score[i],passages[i])


    max_index = 0
    max_value = 0
    for i in range(len(score)):
        if score[i] > max_value:
            max_value = score[i]
            max_index = i

    if project.is_debug:
        print "the candidate passage is %s"%passages[max_index]
    return passages[max_index]

def extract_answer(q, fragment):

    candidate_word = []

    p_class = q_classifier.get_class_label(q)
    if project.is_debug:
        print "the answer class label is " + p_class

    f_list = answer_type_tagger(fragment)

    fragment_list = []



    for i in range(len(f_list)):
        word = f_list[i].keys()[0]
        fragment_list.append(word)
        if p_class in f_list[i][word]:
            candidate_word.append(i)

    hold_candidate = ""
    for i in candidate_word:
        hold_candidate += "," + f_list[i].keys()[0]
    if project.is_debug:
        print "candidate answer contain " + hold_candidate

    focus = extract_focus(q)
    focus_index = q.find(focus)
    q_remove_focus = q.replace(focus,"")
    q_remove_focus_list = jieba.cut(q_remove_focus)
    q_remove_focus_list = list(q_remove_focus_list)
    focus_count_index = 0
    count_sum = 0
    for word in q_remove_focus_list:
        count_sum += len(word)
        if count_sum > focus_index:
            break
        else:
            focus_count_index += 1

    word_position_dic = {}

    for w in q_remove_focus_list:
        word_position_dic[w] = -1

    for i in range(len(fragment_list)):

        if fragment_list[i] in q_remove_focus_list and word_position_dic[fragment_list[i]] == -1:
            word_position_dic[fragment_list[i]] = i

    compare_word = []

    word_position_dic_q = {}

    for i in range(len(q_remove_focus_list)):
        word_position_dic_q[q_remove_focus_list[i]] = i

    for word in word_position_dic.keys():
        if word_position_dic[word] != -1:
            compare_word.append(word)

    score = {}
    for word_index in candidate_word:
        score[word_index] = 0

    for word_index in candidate_word:
        for compare in compare_word:
            word_position_dic_q_compare = 0
            if word_position_dic_q.has_key(compare):
                word_position_dic_q_compare = word_position_dic_q[compare]
            if word_index - word_position_dic[compare] == 0:
                division = 1
            else:
                division = (word_index - word_position_dic[compare])
            score[word_index] += (focus_count_index - word_position_dic_q_compare) * 1.0 / division

    max_val = -10000
    max_index = 0

    if project.is_debug:
        print "candidate answer score:"
    for i in score.keys():
        if project.is_debug:
            print "%s:%s"%(str(score[i]), f_list[i].keys()[0])
        if score[i] > max_val:
            max_val = score[i]
            max_index = i
    return fragment_list[max_index]


if __name__ == '__main__':
    q = u"黄牛一词来源于哪里？"
    #print "class label is %s "%q_classifier.get_class_label(q)
    f_list = [u"黃牛是指在合法銷售途徑以外壟斷和銷售限量參與權與商品以圖利的中介人的俗稱。黄牛一词来源于20世纪的上海，是指票贩子们聯群搶購票時常“有如黃牛群之騷動”，故将他们稱为黃牛或黄牛黨。因黃牛行为連帶匿名炒賣圖利的行為严重影響到正當銷售途徑，故在很多地方皆屬違法。現在引申至所有能獲取之特殊方法（或典型的排隊，或囤積限量商品，或像「司法黃牛」般靠著特殊的社會地位或利益關係）有規模的壟斷圖利的商品（不一定是票證，也可以是護照輪候號碼、表格、或有收藏價值之物品如簽名球衣、限量發行之紀念品等等）或服務，而社會上有殷切需求的民眾或願出高價接受就會有黃牛的出現；就算非為圖利而出售，某程度上亦反映著商品流傳的渠道與其商業模式的公正性。以微觀經濟學而言，黃牛黨的行為企圖製造多為限量引起之高需求門票供給的壟斷，使得黃牛黨可操縱轉售門票價格以賺取豐厚利潤；另一方面，買票難度增加（如香港迪士尼樂園需預先訂票）或者本身已是供求失衡的狀態下亦使場外黃牛票有價有市。所以除以行政手法打擊外，外在條件的變化把需求降低或供給增加之下，黃牛縱使再壟斷更多亦不致於能維持成本，更何況是圖利。黃牛黨賣票不一定比原來的票種價格高，如2006年世界盃足球賽開幕式外流之免費贈券則可以普通票價出售圖利。而有黃牛黨出現的地方亦不一定反映實際上的供不應求；在80年代的中國大陸機票因被售票員囤積而製造之短缺現象，借此挾高價錢圖利皆屬黃牛的一種。", ]
    f =  select_top_passage(q, f_list)

    print extract_answer(q,f)

