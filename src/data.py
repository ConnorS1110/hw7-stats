import math
import utility as util
from collections.abc import Iterable
from utility import *
import update

class DATA:

    def __init__(self):
        self.rows = []
        self.cols = None

    def read(self, sFile):
        data = DATA()
        callback = lambda t: update.row(data, t)
        util.readCSV(sFile, callback)
        return data

    def clone(self, data, ts = None):
        """
        Function:
            clone
        Description:
            Creates a clone of the DATA object and returns it
        Input:
            self - current DATA instance
            data - data to be cloned
        Output:
            data - Clone of DATA object
        """
        data1 = update.row(DATA(), data.cols.names)
        for t in (ts or []):
            update.row(data1, t)
        return data1
