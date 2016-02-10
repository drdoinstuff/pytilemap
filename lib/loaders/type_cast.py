#import logging
from string import lower

def mylist(ret_value):        
    lst = []
    for x in ret_value.split(","):
        z = x.split(":")
        if len(z) > 3:
            exit("ERROR : list conversion error")
        the_type, value = z[0], z[1]
        lst.append(convert(the_type, value))
    return lst

def mybool(x, cond_true = 'true', cond_false = 'false'):
    if x == cond_true:
        return True
    elif x == cond_false:
        return False
    else:
        exit("ERROR : bool conversion error")
        
def convert(the_type, ret_value):    
    the_type = lower(str(the_type))
    ret_value = lower(str(ret_value))
    
    #'true' == False!?
    #mybool = lambda x: True if x is 'true' else x is False
    
    type_lookup = {
                'int' : int,\
                'float': float,\
                'string' : str, \
                'tuple': mylist, \
                'list': mylist,\
                'bool': mybool
                }
    
    
    if the_type is 'tuple':
        logging.debug('tuples are not supported')
    
    ret_type = type_lookup[the_type]
    return ret_type(ret_value)