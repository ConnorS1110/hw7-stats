import math
import random
import utility as util
from num import NUM

smallPositive = 1E-32

def erf(x):
    a1 =  0.254829592
    a2 = -0.284496736
    a3 =  1.421413741
    a4 = -1.453152027
    a5 =  1.061405429
    p  =  0.3275911
    sign = 1
    if x < 0:
        sign = -1
    x = abs(x)
    t = 1 / (1 + (p * x))
    y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * math.exp(-x * x)
    return sign * y

def gaussian(mu = 0, sd = 1):
    sq = math.sqrt
    pi = math.pi
    log = math.log
    cos = math.cos
    r = random.random
    return mu + sd * sq(-2 * log(r())) * cos(2 * pi * r())

def samples(t, n = None):
    u = []
    for i in range(n or len(t)):
        u.append(random.choice(t))
    return u

def cliffsDelta(ns1, ns2):
    """
    Function:
        cliffsDelta
    Description:
        Calculates Cliff's delta effect size measure
    Input:
        ns1 - first list of rows
        ns2 - second list of rows
    Output:
        Whether the difference between the 2 lists of rows is great enough to be non-trivial
    """
    n, gt, lt = 0, 0, 0
    if len(ns1) > 128: ns1 = samples(ns1, 128)
    if len(ns2) > 128: ns2 = samples(ns2, 128)
    for x in ns1:
        for y in ns2:
            n += 1
            if x > y: gt += 1
            if x < y: lt += 1
    return abs(lt - gt) / n <= util.args.cliff

def add(i, x):
    i.n += 1
    d = x - i.mu
    i.mu += d / i.n
    i.m2 += d * (x - i.mu)
    i.sd = 0 if i.n < 2 else math.sqrt(i.m2 / (i.n - 1))

def delta(i, other):
    global smallPositive
    e, y, z = smallPositive, i, other
    return abs(y.mu - z.mu) / (math.sqrt(e + y.sd ** 2 / y.n + z.sd ** 2 / z.n))

def bootstrap(y0, z0):
    x, y, z, yhat, zhat = NUM(), NUM(), NUM(), [], []
    for y1 in y0:
        add(x, y1)
        add(y, y1)
    for z1 in z0:
        add(x, z1)
        add(z, z1)
    xmu, ymu, zmu = x.mu, y.mu, z.mu
    for y1 in y0: yhat.append(y1 - ymu + xmu)
    for z1 in z0: zhat.append(z1 - zmu + xmu)
    tobs = delta(y, z)
    n = 0
    for i in range(util.args.bootstrap):
        if (delta(NUM(samples(yhat)), NUM(samples(zhat))) > tobs):
            n += 1
    return n / util.args.bootstrap > util.args.conf

def RX(t, s = None):
    t.sort()
    return {"name": s or "", "rank": 0, "n": len(t), "show": "", "has": t}

def mid(t):
    t = t["has"] if hasattr(t, "has") else t
    n = len(t) // 2
    return len(t) % 2 == 0 and (t[n] + t[n + 1]) / 2 or t[n + 1]

def div(t):
    t = t["has"] if hasattr(t, "has") else t
    return (t[len(t) * 9 // 10] - t[len(t) * 1 // 10]) / 2.56

def merge(rx1, rx2):
    rx3 = RX([], rx1["name"])
    for t in (rx1["has"], rx2["has"]):
        for x in t:
            rx3["has"].append(x)
    rx3["has"].sort()
    rx3["n"] = len(rx3["has"])
    return rx3

def scottKnot(rxs):
    def merges(i, j):
        out = RX([], rxs[i]["name"])
        for k in range(i, j + 1):
            out = merge(out, rxs[j])
        return out
    def same(lo, cut, hi):
        l = merges(lo, cut)
        r = merges(cut + 1, hi)
        return cliffsDelta(l["has"], r["has"]) and bootstrap(l["has"], r["has"])
    def recurse(lo, hi, rank):
        b4 = merges(lo, hi)
        best = 0
        for j in range(lo, hi + 1):
            if j < hi:
                l = merges(lo, j)
                r = merges(j + 1, hi)
                now = (l["n"] * (mid(1) - mid(b4)) ** 2 + r["n"] * (mid(r) - mid(b4)) ** 2) / (l["n"] + r["n"])
                if now > best:
                    if abs(mid(l) - mid(r)) > cohen:
                        cut, best = j, now
        if cut and not same(lo, cut, hi):
            rank = recurse(lo, cut, rank) + 1
            rank  = recurse(cut + 1, hi, rank)
        else:
            for i in range(lo, hi + 1):
                rxs[i]["rank"] = rank
        return rank
    rxs.sort(key=lambda x: mid(x))
    cohen = div(merges(0, len(rxs) - 1)) * util.args.cohen
    recurse(0, len(rxs) - 1, 1)
    return rxs

def tiles(rxs):
    global smallPositive
    huge, minF, maxF, floor = float("inf"), min, max, math.floor
    lo, hi = huge, -huge
    for rx in rxs:
        lo, hi = minF(lo, rx["has"][0]), maxF(hi, rx["has"][-1])
    for rx in rxs:
        t, u = rx["has"], []
        def of(x, most): return max(1, minF(most, x))
        def at(x): return t[of(len(t) * x // 1, len(t) - 1)]
        def pos(x): return floor(of(util.args.width * (x - lo) / (hi - lo + smallPositive) // 1, util.args.width))
        for _ in range(util.args.width): u.append(" ")
        a, b, c, d, e= at(.1), at(.3), at(.5), at(.7), at(.9)
        A, B, C, D, E= pos(a), pos(b), pos(c), pos(d), pos(e)
        for i in range(A, B + 1):
            u[i] = "-"
        for i in range(D, E + 1):
            u[i] = "-"
        u[util.args.width // 2] = "|"
        u[C] = "*"
        rx["show"] = "".join(u) + " { " + util.args.Fmt.format(a) + "}"
        for x in (b, c, d, e):
            rx["show"] += ", " + util.args.Fmt.format(x)
        rx["show"] += " }"
    return rxs
