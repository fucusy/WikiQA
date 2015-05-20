SELECT term_id,term,doc_frequency
FROM wiki_term where doc_frequency = 0
INTO OUTFILE '/Volumes/Apple HD/Documents/scu.computer.scienct.2015.graduate.project/data/mysql/term_doc_0.csv' FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n';



 SELECT  term_id, doc_id, `count` from wiki_doc_term where term_id IN
(select term_id FROM wiki_term where doc_frequency = 0)
INTO OUTFILE '/Volumes/Apple HD/Documents/scu.computer.scienct.2015.graduate.project/data/mysql/term_doc_relation_0.csv' FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n';

DELETE FROM wiki_doc_term
WHERE term_id IN
(select term_id FROM wiki_term where doc_frequency = 0);

DELETE FROM wiki_term
WHERE doc_frequency = 0;


/* get stop word */
SELECT term FROM wiki_term order by doc_frequency desc limit 300
INTO OUTFILE '/Volumes/Apple HD/Documents/scu.computer.scienct.2015.graduate.project/data/mysql/stopword_300.txt'
FIELDS TERMINATED BY ','
ENCLOSED BY ''
LINES TERMINATED BY '\n';

/* remove data about stopword in wiki_doc_term */

DELETE FROM wiki_doc_term WHERE term_id IN
(SELECT term_id FROM wiki_term order by doc_frequency desc limit 300);
DELETE FROM wiki_doc_term WHERE term_id IN
(SELECT term_id FROM wiki_term where  doc_frequency >= 41091);

