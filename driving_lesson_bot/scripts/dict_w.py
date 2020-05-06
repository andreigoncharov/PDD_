from _collections import OrderedDict
import random

class Work:
    @staticmethod
    def shuffle_dict(d):
        keys = list(d.keys())
        random.shuffle(keys)
        return OrderedDict([(k, d[k]) for k in keys])