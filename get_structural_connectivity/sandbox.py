__author__ = 'Brendan'


import numpy as np

test = [{"source":1,"target":2},
        {"source":3,"target":4},
        {"source":5,"target":6},
        {"source":7,"target":8},
        {"source":9,"target":10},
        {"source":11,"target":12},
        {"source":13,"target":14}]

for idx,row in enumerate(test):
    print 'check row'
    if row['source']==9:
        print idx
        break
