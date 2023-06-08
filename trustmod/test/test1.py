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


my_list = [3, 4, 5, 6, 7, 8, 9, 10]

# Remove the element from its current position
my_list.remove(4)

# Insert the element at the first index
my_list.insert(0, 4)

print(my_list)  # Output: [4, 2, 3, 5]
