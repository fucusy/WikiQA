#!encoding=utf8
__author__ = 'user'


from config.config import *

def log(text):
    f = open(log_file ,"wa")
    f.write(text + "\n")
    f.close()

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]