from range import *
import update as update
from query import *
import utility as util
import list as LIST
import math
from copy import deepcopy
from rule import RULE

def bins(cols, rowss):
    def with1Col(col):
        n, ranges = withAllRows(col)
        ranges = sorted(map(lambda x: x, ranges.values()), key = lambda x: x.lo)
        if hasattr(col, "isSym") and col.isSym:
            return ranges
        else:
            return merges(ranges, n // util.args.bins, util.args.d * div(col))

    def withAllRows(col):
        n, ranges = 0, {}

        def xy(x, y):
            nonlocal n, ranges
            if x != "?":
                n += 1
                k = bin(col, x)
                if k not in ranges:
                    ranges[k] = RANGE(col.col.at, col.col.txt, x)
                extend(ranges[k], x, y)

        for y, rows in rowss.items():
            for row in rows:
                xy(row[col.col.at], y)
        return n, ranges

    return list(map(with1Col, cols))


def bin(col, x):
    if x=="?" or hasattr(col, "isSym"):
        return x
    tmp = (col.col.hi - col.col.lo)/(util.args.bins - 1)
    return 1 if col.col.hi == col.col.lo else math.floor(float(x) / tmp + 0.5) * tmp

def merges(ranges0, nSmall, nFar):
    def noGaps(t):
        for j in range(1, len(t)):
            t[j].lo = t[j-1].hi
        t[0].lo  = -float('inf')
        t[-1].hi = float('inf')
        return t

    def try2Merge(left, right, j):
        y = merged(left.y, right.y, nSmall, nFar)
        if y:
            j += 1  # next round, skip over right.
            left.hi, left.y = right.hi, y
        return j, left

    ranges1 = []
    j = 0
    while j < len(ranges0):
        here = ranges0[j]
        if j < len(ranges0) - 1:
            j, here = try2Merge(here, ranges0[j+1], j)
        j += 1
        ranges1.append(here)

    return noGaps(ranges0) if len(ranges0) == len(ranges1) else merges(ranges1, nSmall, nFar)

def merged(col1, col2, nSmall=None, nFar=None):
    new = merge(col1, col2)
    if nSmall and col1.n < nSmall or col2.n < nSmall:
        return new
    if nFar and not (hasattr(col1, "isSym") and col1.isSym) and abs(mid(col1) - mid(col2)) < nFar:
        return new
    if div(new) <= (div(col1)*col1.n + div(col2)*col2.n) / new.n:
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

def xpln(data, best, rest):
    def v(has):
        return value(has, len(best.rows), len(rest.rows), "best")

    def score(ranges):
        rule = RULE(ranges, maxSizes)
        if rule:
            print(showRule(rule))
            bestr = selects(rule, best.rows)
            restr = selects(rule, rest.rows)
            if len(bestr) + len(restr) > 0:
                return v({"best": len(bestr), "rest": len(restr)}), rule

    tmp, maxSizes = [], {}
    for ranges in bins(data.cols.x, {"best": best.rows, "rest": rest.rows}):
        maxSizes[ranges[0].txt] = len(ranges)
        print("")
        for range in ranges:
            print(range.txt, range.lo, range.hi)
            tmp.append({"range": range, "max": len(ranges), "val": v(range.y.has)})

    rule, most = firstN(sorted(tmp, key=lambda x: x["val"], reverse=True), score)
    return rule, most

def firstN(sortedRanges, scoreFun):
    print("")
    first = sortedRanges[0].val
    def useful(range):
        if range.val > 0.05 and range.val > first / 10:
            return range

    sortedRanges = list(filter(lambda x: x is not None, map(useful, sortedRanges)))
    most, out = -1, None

    for n in range(len(sortedRanges)):
        tmp, rule = scoreFun(list(map(lambda x: x.range, sortedRanges[:n])))

        if tmp and tmp > most:
            out, most = rule, tmp

    return out, most

def showRule(rule):
    def pretty(range):
        return range['lo'] if range['lo'] == range['hi'] else [range['lo'], range['hi']]

    def merges(attr, ranges):
        return list(map(pretty, merge(sorted(ranges, key=lambda r: r['lo'])))), attr

    def merge(t0):
        t, j = [], 0
        while j < len(t0):
            left, right = t0[j], t0[j+1] if j+1 < len(t0) else None
            if right and left['hi'] == right['lo']:
                left['hi'] = right['hi']
                j += 1
            t.append({'lo': left['lo'], 'hi': left['hi']})
            j += 1
        return t if len(t0) == len(t) else merge(t)

    return LIST.kap(rule, merges)

def selects(rule, rows):
    def disjunction(ranges, row):
        for range in ranges:
            lo, hi, at = range['lo'], range['hi'], range['at']
            x = row[at]
            if x == "?":
                return True
            if lo == hi and lo == x:
                return True
            if lo <= x and x < hi:
                return True
        return False

    def conjunction(row):
        for ranges in rule:
            if not disjunction(ranges, row):
                return False
        return True

    return [r for r in rows if conjunction(r)]
