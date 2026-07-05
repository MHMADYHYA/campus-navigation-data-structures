import random
import time

# L stands for any mutable object that has an array interface
# Like a standard Python list for example
# For simplicity, L is assumed to be a list of integers, but the algorithm
# applies to any object that also implements the comparison operators: '<',
# '>', '==', '<=', '>='

def selection_sort(L):
    n = len(L)
    for i in range(0, n):
        min = i   # min = index of minimal element in L[i],L[i+1], ..., L[n-1]
        for j in range(i + 1, n):
            if L[j] < L[min]:
                min = j
        L[i], L[min] = L[min], L[i]  # swap



def sort_test(sorter):
    for i in range(10):
        L = list(range(0,10))
        random.shuffle(L)
        print("L = ", L)
        sorter(L)
        print("sorted list", L)
        input("Press any key to continue:")


def selection_sort_slow_motion(n=10):
    L = list(range(0,n))
    random.shuffle(L)
    print(L)
    stage = 0
    for i in range(0, n):
        min = i
        for j in range(i + 1, n):
            if L[j] < L[min]:
                line = "STAGE %d: %s :"  %  (stage, L)
                stage += 1
                input(line)
                min = j
        L[i], L[min] = L[min], L[i]  # swap


#import sys
#sys.path.append("d:/python") # private library (Samy)
#from html_utils import *     # Will try to release it later
def sort_runtime_graph(sorter):
    import matplotlib.pyplot as pyplot
    import sys
    Sizes = [100*i for i in range(1,30)]
    Times = list()
    for N in Sizes:
        print("N=", N)
        t = sort_average_time(sorter, N,16)
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

if __name__ == "__main__":
    #sort_test(selection_sort)
    #selection_sort_slow_motion(10)
    sort_runtime_graph(selection_sort)




