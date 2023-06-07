# how to import parseTitle from trustmod\uility\string_mainpulation.py
# into test1.py
from icecream import ic
import itertools

d = [4, 3, 2, 555, 666]
d = []  # Empty list
i = itertools.cycle(d)

try:
    X = next(i)
    print(X)
    print(X)
except StopIteration:
    print("Reached the end of the iterator.")