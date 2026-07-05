# L stands for any mutable object that has an array interface
# Like a standard Python list for example
# For simplicity, L is assumed to be a list of integers, but the algorithm
# applies to any object that also implements the comparison operators: '<',
# '>', '==', '<=', '>='

def radix_sort(L):
    RADIX = 10
    maxLength = False
    tmp , placement = -1, 1

    while not maxLength:
        maxLength = True
        # declare and initialize buckets
        buckets = [list() for i in range( RADIX )]

        # split L between lists
        for  i in L:
            tmp = i / placement
            buckets[tmp % RADIX].append(i)
            if maxLength and tmp > 0:
                maxLength = False

        # empty lists into L array
        a = 0
        for b in range(RADIX):
            buck = buckets[b]
            for i in buck:
                L[a] = i
                a += 1

        # move to next digit
        placement *= RADIX


