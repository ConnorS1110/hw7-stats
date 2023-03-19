import argparse
import random
import functions as fun
from num import NUM

args = None
egs = {}

def eg(key, string, fun):
    """
    Function:
        eg
    Description:
        Creates an example test case and adds it to the dictionary of test cases. Appends the key/value to the actions of the help string
    Input:
        key - key of argument
        string - value of argument as a string
        fun - callback function to use for test case
    Output:
        None
    """
    global egs
    global help
    egs[key] = fun

def getCliArgs():
    """
    Function:
        getCliArgs
    Description:
        Parses out the arguments entered or returns an error if incorrect syntax is used
    Input:
        None
    Output:
        None
    """
    global args
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--bootstrap", type=int, default = 512, required=False)
    parser.add_argument("--conf", type=float, default = 0.05, required=False)
    parser.add_argument("--cliff", type=float, default = 0.4, required=False)
    parser.add_argument("--cohen", type=float, default = 0.35, required=False)
    parser.add_argument("--Fmt", type=str, default = ":6.2f", required=False)
    parser.add_argument("--width", type=int, default = 40, required=False)

    args = parser.parse_args()

def okFunc():
    print(random.seed(1))

def sampleFunc():
    for i in range(10):
        print("", "".join(fun.samples(["a", "b", "c", "d", "e"])))

def numFunc():
    """
    Function:
        numFunc
    Description:
        Callback function to test the NUM class
    Input:
        None
    Output:
        Prints basic statistics of NUM object
    """
    n = NUM([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    print(n.n, n.mu, n.sd)

def gaussFunc():
    t = []
    for i in range(10 ** 4 + 1):
        t.append(fun.gaussian(10, 2))
    n = NUM(t)
    print(n.n, n.mu, n.sd)

def bootFunc():
    a, b = [], []
    for i in range(100):
        a.append(fun.gaussian(10, 1))
    print("","mu","sd","cliffs","boot","both")
    print("","--","--","------","----","----")
    mu = 10.0
    while mu <= 11.0:
        b.clear()
        for i in range(100):
            b.append(fun.gaussian(mu, 1))
        cl = fun.cliffsDelta(a, b)
        bs = fun.bootstrap(a, b)
        print("", mu, 1, cl, bs, cl and bs)
        mu += 0.1

def basicFunc():
        print("\t\ttruee", fun.bootstrap([8, 7, 6, 2, 5, 8, 7, 3], [8, 7, 6, 2, 5, 8, 7, 3]),
                        fun.cliffsDelta([8, 7, 6, 2, 5, 8, 7, 3], [8, 7, 6, 2, 5, 8, 7, 3]))
        print("\t\tfalse", fun.bootstrap([8, 7, 6, 2, 5, 8, 7, 3], [9, 9, 7, 8, 10, 9, 6]),
                        fun.cliffsDelta([8, 7, 6, 2, 5, 8, 7, 3], [9, 9, 7, 8, 10, 9, 6]))
        print("\t\tfalse", fun.bootstrap([0.34, 0.49, 0.51, 0.6, 0.34, 0.49, 0.51, 0.6], [0.6, 0.7, 0.8, 0.9, 0.6, 0.7, 0.8, 0.9]),
                        fun.cliffsDelta([0.34, 0.49, 0.51, 0.6, 0.34, 0.49, 0.51, 0.6], [0.6, 0.7, 0.8, 0.9, 0.6, 0.7, 0.8, 0.9]))