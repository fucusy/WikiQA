# Design and implementation of answer Robot Based Wikipedia data

## pre-requirement

* you know basic python 2.7 
* you know basic sql syntax
* you know chinese



## environments


* python 2.7
* python 2.7 library: 
    * jieba==0.38
    * MySQL-python==1.2.5
    * xmldict==0.4.1
* mysql Ver 14.14 or higher and lower, test on version 14.14
* test on mac os, it may be support linux and windows.


## data

* wikipedia data: 维基百科为对维基百科中的内容有使用兴趣的人提供了完整内容的电子档案。
这里选择的是,20141009 版本的镜像。我们只需要,维基百科内容中的文字信息,以及最新一版本的数据情况
,而不需要维基百科内容的历史 修改记录,因此我们选择下载页面中的, zhwiki-20141009-pages-articles-multistream.xml 其容量大小为 4.9G
,其压缩版下载网址在[这里](http://download.wikipedia.com/zhwiki/
/20141009/zhwiki-20141009-pages-articles-multistream.xml.bz2), 如果下载不到这个版本的数据，你也可以选择其它时间的比如[20160501](https://dumps.wikimedia.org/zhwiki/20160501/)
的[zhwiki-20160501-pages-articles-multistream.xml.bz2](https://dumps.wikimedia.org/zhwiki/20160501/zhwiki-20160501-pages-articles-multistream.xml.bz2)
。


* question set data: 问题集的获取:这里使用的问题集来自万小军语义计算与知识挖掘课程[5] 中的中文智能问答系统的问题集, 其中包括100个有答案的问题，位于在data/question_with_answer_100.xml，和10000个没有答案的问题,位于data/question_without_answer_10000.xml。


## how to run

1. get raw data from wikipedia, see more from previous data section, by the way you can check the [raw data format](https://www.mediawiki.org/wiki/Help:Formatting)
2. unzip the raw data,get a big xml file, then convert the xml to sql scripts using by the method describe [here](https://meta.wikimedia.org/wiki/Data_dumps/Tools_for_importing)
recommend to use [mwdum.py](https://github.com/nutztherookie/mwdum.py),
 it will cost you almost 30 minutes.create the wikipedia database using the sql script ExportMysqlDataToFile/sql/wikipedia_create_table.sql,  know more about the wikipedia database table structure from [here](https://www.mediawiki.org/wiki/Manual:Database_layout) 
, then run the sql scripts which generated from xml. it will cost you almost 30 minutes
  
3. clean data and get useful data into file system using ExportMysqlDataToFile module
4. build retrieve system using DocsRetrieveSystem module
5. this system is ready to answer question, run the script in AnswerExtraction, AnswerExtraction/process/answer.py


## module description
every module is a Pycharm project, you need run it in Pycharm if you do not know exactly how python module works

### ExportMysqlDataToFile

#### how to run

* update ExportMysqlDataToFile/config.py file, 
1. update DB connect info


    class DB:
        host = "127.0.0.1"
        username = "root"
        password = ""
        database = "wikipedia"

2. update `project_base_path` where the ExportMysqlDataToFile module located and `data_base_path` where you want the files export to from mysql database

3. delete log.txt files

4. change directory to ExportMysqlDataToFile, then extract to file system by running main.py `python main.py extract_to_file_system` by command,
after almost 5 minutes, you can check the `data_base_path` directory, there is a `temp` directory contain the wiki page content.

then you need to split the page to fragments by running `python main.py split_to_fragment`, you can stop the script anytime, the progress will stored in the log.txt file, next 
time when you run `python main.py split_to_fragment` again, it will continue from previous progress.
it will cost you nearly 1 hour, then you will see `fragment` directory in your `data_base_path`

5. then you can delete the `temp` folder in your  `data_base_path` path, you also can remove the `wikipedia` database

6. done

### DocsRetrieveSystem

#### how to run
1. run sql script at DocsRetrieveSystem/db/create_table.sql to create tables for docs retrieve system, make sure database `wiki_search` do not exists before,
after running, you will see a empty database named `wiki_search`
2. make sure the database is empty, by running sql:

        truncate table wiki_doc_term;
        truncate table wiki_term;
        truncate table wiki_doc;

3.  change directory to DocsRetrieveSystem, to do index by running `python main.py`,  15:22 ~  

### AnswerExtraction




### QuestionAnalysis

## result 

data/question_with_answer_100.xml中的100 个问题中,有 33 个问题,在文档检索系统的工作下成功的把含有答案的文档检索出来,候选句选择程序,从 33 个包含正确答案的文档列表中, 成功抽取出 11 个包含正确答案的候选句子,成功率为 33.3%(11/33 = 33.3%)。 最终的答案抽取程序,从候选句中抽取出最终的正确答案,成功抽取出的结 果,有 5 个与标准答案相符合,抽取的成功率为,45.5%(5/11 = 45.5%)。

final answer accuracy: 5% 


almost 200k pages, 720k fragments

## more detail you need to check the docs/related_paper.pdf, by the way it's Chinese


## reference

1. Sproat, R. and Emerson, T. The First International Chinese Word Segmentation Bakeoff[A]. In: Proceedings of the Second SIGHAN Workshop on Chinese Language Processing[C]. Sapporo , Japan: July 11-12 , 2003 ,133-143.
2. 黄昌宁,赵海. 中文分词十年回顾[J]. 中文信息学报,2007,03:8-19.
3. 结巴中文分词[EB/OL]https://github.com/fxsjy/jieba,2015.05.09/2015.05.09
4. The Integration of Lexical Knowledge and External Resources for Question Answering
5. Web Data Mining 2014 Fall – PKU » 互联网数据挖掘[EB/OL]http://www.icst.pku.edu.cn/lcwm/course/WebDataMining2014/
6. 黄翼彪. 开源中文分词器的比较研究[D].郑州大学,2013.
7. Help:Formatting – MediaWiki[EB/OL]http://www.mediawiki.org/wiki/Help:Formatting,2015.04.12/2015.05.03
8. Manual:Database layout[EB/OL]http://www.mediawiki.org/wiki/Manual:Database_layout,2015.03.12/2015.05.09
9. Data dumps/xml2sql[EB/OL]http://meta.wikimedia.org/wiki/Data_dumps/xml2sql, 2013.3.5/2015.05.09
10. Robertson, Stephen, and Hugo Zaragoza. The probabilistic relevance framework: BM25 and beyond. [M] Now Publishers Inc, 2009
11. Singhal, Amit, Chris Buckley, and Mandar Mitra. "Pivoted document length normalization." [C] Proceedings of the 19th annual international ACM SIGIR conference on Research and development in information retrieval. ACM, 1996.
12. 维基百科:数据库下载[EB/OL]http://zh.wikipedia.org/wiki/Wikipedia:数据库下载, 2014.10.15/2015.05.09
13. 下载页面[EB/OL] http://download.wikipedia.com/zhwiki/20141009/zhwiki-20141009-pages-articles-multistream.xml.bz2,2015.05.09/2015.05.09
14. 张宇,刘挺,文勖. 基于改进贝叶斯模型的问题分类[J]. 中文信息学报,2005,02:100-105.
15. https://github.com/nutztherookie/mwdum.py.git/

 