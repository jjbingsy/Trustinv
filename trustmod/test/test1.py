# how to import parseTitle from trustmod\uility\string_mainpulation.py
# into test1.py
from icecream import ic
import itertools
import gc
ic.disable()
d = [4, 3, 2, 555, 666]

i = itertools.cycle(d)

ic (next(i))
try:
    ic (next(i))
    ic (next(i))
    ic (next(i))
    ic (next(i))
    ic (next(i))
except StopIteration:
    print("Reached the end of the iterator.")


j = list()
j.append(1)
j.append(2)
ic (j)

oo = None
oo = 0
if not oo:
    ic (oo)
else:
    ic()


my_list = [3, 4, 5, 6, 7, 8, 9, 10]
kk = [-2]
# Remove the element from its current position
my_list.remove(4)

# Insert the element at the first index
my_list.insert(0, 4)

ic(my_list)  # Output: [4, 2, 3, 5]


kk += [21, 32]
if 21 in kk:
    kk.remove(21)
    kk.insert(0, 21)
ic (kk)

ic.enable()
h = [1, 2, 3, 4, 5, 6, 7, 8, 9]
ic (h)
ic(h.pop())
ic(h.pop())
ic(h.pop())

h.append(4234)
h.append(666)
ic (h)
del h[:]
del h[:]
gc.collect()
h.append(15)
ic (h)