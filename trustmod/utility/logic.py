from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def group_match_strings(strings, funcc, threshold=85, func2=None):
    groups = []
    assigned = set()

    for i, string1 in enumerate(strings):
        if i in assigned:
            continue

        group = [string1]
        assigned.add(i)

        for j, string2 in enumerate(strings[i+1:]):
            if i + 1 + j in assigned:
                continue
            score = fuzz.token_set_ratio(funcc (string1), funcc (string2))
            if func2:
                if func2 (string1, string2):
                    score = 100

            if score >= threshold:
                group.append(string2)
                assigned.add(i + 1 + j)

        groups.append(group)

    return groups
