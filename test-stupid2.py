def compare_idol_v2 (idol1, idol2):
    return f"{idol1} : {idol2}"

def best_idols_pair (idols, grouped_idols = []):
    idol, *rest_idols = idols
    if rest_idols:
        best_idols_pair(rest_idols, grouped_idols)
    for i in rest_idols:
        result = compare_idol_v2 (idol, i)
        grouped_idols.append((result, idol, i))

        

i = []
best_idols_pair (["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"], i)
print(i)