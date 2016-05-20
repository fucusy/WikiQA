#!encoding=utf8
__author__ = 'user'

from datetime import datetime
from config import log_file
import os

def log(text):
    text = text
    mode = "a"
    if not os.path.exists(log_file):
        mode = "w"
    f = open(log_file, mode)
    f.write(text + "\n")
    f.close()

def get_datetime():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
