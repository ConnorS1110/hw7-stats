import utility as util
from cluster import *
import query as query

def sway(data):
    """
    Function:
        sway
    Description:
        Finds the best half of the data by recursion
    Input:
        data - data to sway
    Output:
        Swayed data
    """
    def worker(rows, worse, above = None):
        if len(rows) <= len(data.rows) ** util.args.min:
            return rows, many(worse, util.args.rest*len(rows))
        else:
            l , r, A, B,_ = half(data, rows, None, above)
            if query.better(data, B, A):
                l, r, A, B = r, l, B, A
            for row in r:
                worse.append(row)
            return worker(l, worse, A)
    best, rest = worker(data.rows, [])
    return data.clone(data, best), data.clone(data, rest)
