#!encoding=utf8
__author__ = 'user'
import process
import config
import sys

if len(sys.argv) > 1 and sys.argv[1] == "split_to_fragment":
    process.split_documents(config.last_split_process_id)
elif len(sys.argv) > 1 and sys.argv[1] == "extract_to_file_system":
    process.extract_from_db_to_file_system()
else:
    print("usage: python main.py extract_to_file_system")
    print("or:python main.py split_to_fragment")