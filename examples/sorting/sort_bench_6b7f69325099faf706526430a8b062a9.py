import random
import time
#import sys
#sys.path.append("d:/python") # private library (Samy)
#from html_utils import *     # Will try to release it later

def sort_test(sorter):
    for i in range(10):
        L = list(range(0,10))
        random.shuffle(L)
        print("L = ", L)
        sorter(L)
        print("sorted list", L)
        input("Press any key to continue:")


def sort_runtime_graph(sorter, n=10):
    import matplotlib.pyplot as pyplot
    import sys
    Sizes = [100*i for i in range(1,n)]
    Times = list()
    for N in Sizes:
        print("N=", N)
        t = sort_average_time(sorter, N, 16)
        t = round(t,4)
        Times.append(t)

    pyplot.plot(Sizes, Times)
    pyplot.xlabel('List Size')
    pyplot.ylabel('Run Time')
    pyplot.show()
    #header = ('List Size', 'Run Time (seconds)')
    #html_table("d:/dropbox/public/table.html", header, [Sizes, Times])

# Create num_tests lists of size list_size and compute
# average time for doing sort on these lists
def sort_average_time(sorter, list_size, num_tests):
    times = list()
    L = list(range(0, list_size))

    for i in range(num_tests):
        random.shuffle(L)
        t0 = time.time()
        sorter(L)
        t1 = time.time()
        t = t1-t0
        times.append(t)

    return sum(times)/num_tests




