
def cytest(int n):
    cdef int a = 1
    for _ in range(1,n):
        a = a * _

    print(a)