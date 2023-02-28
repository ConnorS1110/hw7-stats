from col import COL
from range import *
import update as update
from query import *
import utility as util
import math
from copy import deepcopy

def bins(cols, rowss):
    out = []
    for col in cols:
        ranges = {}
        for y, rows in rowss.items():
            for row in rows:
                if (isinstance(col, COL)):
                    col = col.col
                x = row[col.at]
                if x != "?":
                    k = int(bin(col, float(x) if x != "?" else x))
                    ranges[k] = ranges[k] if k in ranges else RANGE(col.at, col.txt, float(x) if x != "?" else x)
                    update.extend(ranges[k], float(x), y)
        ranges = {key: value for key, value in sorted(ranges.items(), key=lambda x: x[1].lo)}
        newRanges = {}
        i = 0
        for key in ranges:
            newRanges[i] = ranges[key]
            i += 1
        newRangesList = []
        if hasattr(col, "isSym") and col.isSym:
            for item in newRanges.values():
                newRangesList.append(item)
        out.append(newRangesList if hasattr(col, "isSym") and col.isSym else mergeAny(newRanges))
    return out

def bin(col, x):
    if x=="?" or hasattr(col, "isSym"):
        return x
    tmp = (col.hi - col.lo)/(util.args.bins - 1)
    return 1 if col.hi == col.lo else math.floor(x / tmp + 0.5) * tmp

def mergeAny(ranges0):
    def noGaps(t):
        for j in range(1, len(t)):
            t[j].lo = t[j-1].hi
        t[0].lo = -float("inf")
        t[-1].hi = float("inf")
        return t
    ranges1, j = [], 0
    while j < len(ranges0):
        left, right = ranges0[j], ranges0[j+1] if j + 1 < len(ranges0) else None
        if right:
            y = merge2(left.y, right.y)
            if y:
               j = j+1
               left.hi, left.y = right.hi, y
        ranges1.append(left)
        j += 1
    return noGaps(ranges0) if len(ranges1)==len(ranges0) else mergeAny(ranges1)

def merge2(col1, col2):
    new = merge(col1, col2)
    if div(new) <= (div(col1)*col1.n + div(col2)*col2.n)/new.n:
        return new

def merge(col1, col2):
    new = deepcopy(col1)
    if hasattr(col1, "isSym") and col1.isSym:
        for x, n in col2.has.items():
            add(new, x, n)
    else:
        for n in col2.has:
            add(new, n)
        new.lo = min(col1.lo, col2.lo)
        new.hi = max(col1.hi, col2.hi)
    return new
