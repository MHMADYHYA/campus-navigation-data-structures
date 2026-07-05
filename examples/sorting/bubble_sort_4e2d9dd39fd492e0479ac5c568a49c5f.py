import random
import time

# L stands for any mutable object that has an array interface
# Like a standard Python list for example
# For simplicity, L is assumed to be a list of integers, but the algorithm
# applies to any object that also implements the comparison operators: '<',
# '>', '==', '<=', '>='

# L is a list of integers that we want to sort
def bubble_sort(L):
    N = len(L)
    while True:
        sorted = True
        for i in range(0,N-1):
            if L[i+1] < L[i]:
                sorted = False
                L[i], L[i+1] = L[i+1], L[i]
        if sorted:
            return

# This is slightly different but simpler version which is also called bubble sort
# L is a list of integers that we want to sort
def bubble_sort2(L):
    N = len(L)
    for i in range(0,N-1):
        for j in range(i+1, N):
            if L[j] < L[i]:
                L[i], L[j] = L[j], L[i]


def bubble_sort_test():
    for i in range(10):
        L = list(range(0,10))
        random.shuffle(L)
        print("L = ", L)
        bubble_sort(L)
        print("Bubble sort:", L)
        input("Press any key to continue:")


def bubble_sort_slow_motion(N=10):
    L = list(range(0,N))
    random.shuffle(L)
    stage = 0
    while True:
        print("STAGE %d: %s"  %  (stage, L))
        stage += 1
        sorted = True
        for i in range(0,N-1):
            if L[i+1] < L[i]:
                sorted = False
                L[i], L[i+1] = L[i+1], L[i]

        if sorted:
            return

def bubble_sort_runtime_graph():
    import matplotlib.pyplot as pyplot
    import sys
    #sys.path.append("d:/python") # private library (Samy)
    #from html_utils import *     # Will try to release it later
    Sizes = [100*i for i in range(1,30)]
    Times = list()
    for N in Sizes:
        print("N=", N)
        t = bubble_sort_average_time(N,3)
        t = round(t,4)
        Times.append(t)

    pyplot.plot(Sizes, Times)
    pyplot.xlabel('List Size')
    pyplot.ylabel('Run Time')
    pyplot.show()
    #header = ('List Size', 'Run Time (seconds)')
    #html_table("d:/dropbox/public/table.html", header, [Sizes, Times])

# Create num_tests lists of size list_size and compute
# average time for doing bubble_sort on these lists
def bubble_sort_average_time(list_size, num_tests):
    times = list()
    L = list(range(0, list_size))

    for i in range(num_tests):
        random.shuffle(L)
        t0 = time.time()
        bubble_sort(L)
        t1 = time.time()
        t = t1-t0
        times.append(t)

    return sum(times)/num_tests

if __name__ == "__main__":
    #bubble_sort_test()
    #bubble_sort_slow_motion(10)
    bubble_sort_runtime_graph()




