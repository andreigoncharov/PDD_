class User:
    def __init__(self, tel_id, username, context):
        self.tel_id = tel_id
        self.username = username
        self.context = context

'''import random
from _collections import OrderedDict

l= {1:'right', 2: 'wrong 2', 3: 'wrong 3', 4: 'wrong 4'}

def shuffle_dict(d):
    keys = list(d.keys())
    random.shuffle(keys)
    print(keys)
    e = []
    e= list(d.keys())
    i= e.index(3)
    print(i)
    return OrderedDict([(k, d[k]) for k in keys])

print(shuffle_dict(l))
#print(l)'''
