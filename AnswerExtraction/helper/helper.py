__author__ = 'user'


import urllib2
from AnswerExtraction.helper.retry_derector import retry
def convert_string_to_numeric(lit):
    'Return value of numeric literal string or ValueError exception'

    # Handle '0'
    if lit == '0': return 0
    # Hex/Binary
    litneg = lit[1:] if lit[0] == '-' else lit
    if litneg[0] == '0':
        if litneg[1] in 'xX':
            return int(lit,16)
        elif litneg[1] in 'bB':
            return int(lit,2)
        else:
            try:
                return int(lit,8)
            except ValueError:
                pass

    # Int/Float/Complex
    try:
        return int(lit)
    except ValueError:
        pass
    try:
        return float(lit)
    except ValueError:
        pass

    try:
        return complex(lit)
    except ValueError:
        return False

def is_numeric(lit):
    return not convert_string_to_numeric(lit) is False


@retry(Exception,tries=6,delay=3,backoff=2)
def urlopen_with_retry(search_request):
    return urllib2.urlopen(search_request)