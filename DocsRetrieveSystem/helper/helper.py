#!encoding=utf8
__author__ = 'user'

from datetime import datetime

from DocsRetrieveSystem.config.config import *
from AnswerExtraction.helper.helper import is_numeric
from AnswerExtraction.helper.helper import convert_string_to_numeric

def log(text):
    text = text.encode("utf8")
    f = open(log_file ,"a")
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

log(get_datetime())


class ExpressionTree():
    left_tree = None
    right_tree = None
    val = None
    op = None
    index = 0
    operators = ["+","-","*","/",")","("]
    s = ""
    def get_next(self):
        s = self.s
        if self.index < len(s):
            if s[self.index] in self.operators:
                r = s[self.index]
                self.index += 1
                return r
            else:
                next_index = self.index + 1
                while next_index <= len(s) and is_numeric(s[self.index:next_index]):
                    next_index += 1
                r = s[self.index:next_index-1]
                self.index = next_index - 1
                return r
        return ""

    def __init__(self, s):
        self.index = 0
        self.s = s
        next_v = self.get_next()

        if next_v == "(":
            right_par_index = self.s.find(")")
            self.index = right_par_index + 1
            second_next_v = self.get_next()
            if second_next_v != "":
                self.left_tree = ExpressionTree(self.s[1:right_par_index])
                self.op = second_next_v
                self.right_tree = ExpressionTree(self.s[self.index:])
            else:
                self.__init__(self.s[1:right_par_index])
        if is_numeric(next_v):
            second_next_v = self.get_next()
            if second_next_v == "":
                self.val = convert_string_to_numeric(next_v)
            else:

                third_next_v = self.get_next()
                forth_next_v = self.get_next()

                if forth_next_v == "":
                    self.left_tree = ExpressionTree(next_v)
                    self.op = second_next_v
                    self.right_tree = ExpressionTree(third_next_v)
                else:
                    if third_next_v == "(":
                        right_par_index = self.s.find(")")

                    if second_next_v == "*" or second_next_v == "/" or (( second_next_v == "-" or second_next_v == "+") and ( forth_next_v == "-" or forth_next_v == "+" ) ):
                        self.left_tree = ExpressionTree(next_v + second_next_v + third_next_v)
                        self.op = forth_next_v
                        self.right_tree = ExpressionTree(self.s[self.index:])
                    else:
                        self.left_tree = ExpressionTree(next_v)
                        self.op = second_next_v
                        self.right_tree = ExpressionTree(third_next_v + forth_next_v + self.s[self.index:])

    def evaluate(self):
        if self.right_tree is None and self.left_tree is None:
            return self.val
        else:
            if self.op == "+":
                return self.left_tree.evaluate() + self.right_tree.evaluate()
            if self.op == "-":
                return self.left_tree.evaluate() - self.right_tree.evaluate()
            if self.op == "*":
                return self.left_tree.evaluate() * self.right_tree.evaluate()
            if self.op == "/":
                return self.left_tree.evaluate() / self.right_tree.evaluate()

if __name__ == '__main__':
    t = ExpressionTree("1+3*4")
    print t.evaluate()