#create database
create database wiki_search charset = utf8;
use wiki_search;
#create tables
create table wiki_term(
  `term_id` int NOT NULL AUTO_INCREMENT COMMENT '中文词汇的ID',
    `term` VARCHAR(100) NOT NULL  COMMENT '中文词汇的内容',
    `doc_frequency` int NOT NULL DEFAULT 0,
    PRIMARY KEY(`term_id`),
    UNIQUE(`term`)
)ENGINE=MyISAM CHARSET=utf8 COLLATE utf8_bin;

create table wiki_doc(
  `doc_id` int not null auto_increment,
  `doc_len` int not null DEFAULT 0,
  `doc_path` varchar(200) not null comment '文档所在的路径',
  PRIMARY KEY (`doc_id`)
) ENGINE=MyISAM CHARSET=utf8 COLLATE utf8_bin;

create table wiki_doc_term(
  `doc_id` int not null,
  `term_id` int not null,
  `count` int not null,
  PRIMARY KEY(`doc_id`,`term_id`)
)ENGINE=MyISAM CHARSET=utf8 COLLATE utf8_bin;


ALTER TABLE wiki_doc CONVERT TO CHARACTER SET utf8 COLLATE utf8_bin;


create table wiki_data(
  `data_id` int not null auto_increment,
  `data_name` varchar(50) not null,
  `value` varchar(50) not null,
  `last_update` datetime,
  PRIMARY KEY (`data_id`),
  UNIQUE KEY (`data_name`)
)ENGINE=MyISAM CHARSET=utf8 COLLATE utf8_bin;

CREATE INDEX d_t_term_index ON wiki_doc_term (`term_id`);




CREATE TABLE wiki_entity(
  `entity_id` int not null auto_increment,
  `entity_name` VARCHAR(100) not null,
  `term_id` int null,
  PRIMARY KEY (`entity_id`),
  UNIQUE KEY (`entity_name`)
)ENGINE=MyISAM CHARSET=utf8 COLLATE utf8_bin;
#2015-05-11 add `column`
ALTER TABLE `wiki_entity` ADD COLUMN `entity_type` VARCHAR(50) NULL ;