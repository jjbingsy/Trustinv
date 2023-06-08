# how to import parseTitle from trustmod\uility\string_mainpulation.py
# into test1.py
from icecream import ic
import itertools


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

