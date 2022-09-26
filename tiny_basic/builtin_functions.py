import random


def fn_rnd(args):
    range_begin = 0 if 2 != len(args) else args[0]
    range_end = args[0] if 1 == len(args) else args[1]
    return random.randrange(range_begin, range_end)


def fn_mid(args):
    src = args[0]
    index_from = args[1]
    if 2 < len(args):
        index_to = index_from + args[2]
        return src[index_from:index_to]
    else:
        return src[index_from]