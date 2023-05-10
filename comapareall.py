from fuzzywuzzy import fuzz
from collections import defaultdict

def compare_strings(strings):
    results = []

    for i, string1 in enumerate(strings):
        for j, string2 in enumerate(strings[i + 1:], start=i + 1):
            similarity = fuzz.ratio(string1, string2)
            results.append((string1, string2, similarity))

    sorted_results = sorted(results, key=lambda x: x[2], reverse=True)
    return sorted_results



def compare_idol_v1 (idol1, idol2):
    if idol1[3] and idol2[3] and idol1[3] == idol2[3]:
        return 100
    elif idol1[1] == idol2[1]:
        return -100
    else:
        return fuzz.ratio(idol1, idol2)


def sort_idols(idols, modified_fuzzratio):
    results = []

    for i, idol1 in enumerate(idols):
        for j, idol2 in enumerate(idols[i + 1:], start=i + 1):
            similarity = modified_fuzzratio(idol1, idol2)
            results.append((idol1, idol2, similarity))

    sorted_results = sorted(results, key=lambda x: x[2], reverse=True)
    return sorted_results






def group_best_matches(idols, x):
    sorted_results = sort_idols(idols, compare_idol_v1)
    grouped_results = [] #defaultdict(list)
    first = True
    for idol1, idol2, similarity in sorted_results:
        print (idol1, idol2, similarity)
        if first:
            grouped_results.append([idol1, idol2])
            first = False
            continue # dont need this
        s1 = False
        i1 = -1
        s2 = False
        i2 = -1
        for index, group in enumerate( grouped_results):
            if idol1 in group:
                s1 = True
                i1 = index
            if idol2 in group:
                s2 = True
                i2 = index
        if not s1 and not s2:
            grouped_results.append([idol1, idol2])
        elif s1 and not s2 and len(grouped_results[i1]) < x:
            grouped_results[i1].append(idol2)
        elif s2 and not s1 and len(grouped_results[i2]) < x:
            grouped_results[i2].append(idol1)
    return grouped_results

strings = ['apple', 'aple', 'appel', 'banana', 'bannana', 'oranje', 'orange', 'lll', "bann"]
x = 3



grouped_results = group_best_matches(strings, x)
print(grouped_results)

strings = ['k', 'j', 'l', "ml"]
x = 3

grouped_results = group_best_matches(strings, x)
print(grouped_results)
