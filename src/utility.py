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
