from datetime import datetime
from fuzzywuzzy import fuzz

from trustmod.vars.env_001 import IMAGE_DIRECTORY, MEDIA_DIRECTORIES, USER_AGENT_GOOGLE, FILMSOURCES_PATH, IDOLSDB_PATH as IDP, IDOLS2DB_PATH
from trustmod.classes import Idol_struct
from pathlib import Path
import sqlite3

# def u (x, y):
#     print (x, y)

# u(*(1,2))


# original_list = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
# new_list = [x for sublist in original_list for x in sublist if x % 2 == 0]
# print(new_list)

# db_path = Path(IDP)
# conn = sqlite3.connect(db_path)
# cur = conn.cursor()
# cur.execute("SELECT *, rowid FROM idols")
# idols = cur.fetchall()
# conn.close()
# for idol in idols:
#     i = Idol_struct(idol)
#     print(i)

def compare_idol_v2 (idol1, idol2):
    if idol1.shared_key and idol2.shared_key and idol1.shared_key == idol2.shared_key:
        return 100
    elif idol1.source_id == idol2.source_id:
        return -100
    else:
        return fuzz.ratio(idol1.name, idol2.name)
    


def best_idols_pair (idols, grouped_idols = []):
    idol, *rest_idols = idols
    if rest_idols:
        best_idols_pair(rest_idols, grouped_idols)
    for i in rest_idols:
        result = compare_idol_v2 (idol, i)
        if result > 0:
            grouped_idols.append((result, idol, i))

def worse_idol_pair (idol, idols, matched):
    for i in idols:
        if i.matched == matched:
            result = compare_idol_v2 (idol, i)
            if result < 0:
                print (f"{result}, {idol.name}, {i.name}")
                return True
    return False

def idol_matching(idols, matched_source, xx=False, recursion = 0):
    if not idols:
        if xx:
            input()
        return

    running_idols = idols.copy()

    for i in running_idols:
        i.matched = -1

    paired_idols = []
    best_idols_pair(running_idols, paired_idols)
    paired_idols.sort(key=lambda x: x[0], reverse=True)
    match_idols(paired_idols, running_idols, index=-1)
    running_idols.sort(key=lambda x: x.matched, reverse=False)

    grouped_idols = []
    for idol in running_idols:
        if len(grouped_idols) == idol.matched:
            new_group = [idol]
            grouped_idols.append(new_group)
        else:
            grouped_idols[idol.matched].append(idol)

    running_idols = []
    for group in grouped_idols:
        txt = ""
        for i in group:
            txt = txt + f"{i.name} {i.source_id}: "
        print(txt)
        if len(group) and len(group) < matched_source:
            for idd in group:
                running_idols.append(idd)

    if running_idols:
        xx = True
        input()

    if recursion > 3:
        input()
    idol_matching(running_idols, matched_source=matched_source, xx=xx, recursion=recursion+1)


def match_idols (group_idols, orig_idols,  index = -1, counter= 0):

    [score, i1, i2], *rest = group_idols

    new_index = index

    # if score < 0:
    #     pass
        # new_index += 1
        # if i1.matched == -1:
        #     i1.matched = new_index
        # if i2.matched == -1:
        #     i2.matched = new_index 
    if i1.matched == -1 and i2.matched == -1:
        new_index += 1
        i1.matched = new_index
        i2.matched = new_index
    elif i1.matched != -1 and i2.matched != -1:
        pass
    else:
        max_index = max(i1.matched, i2.matched)
        lowbar = True
        if i1.matched == max_index and i2.matched == -1:
            lowbar = worse_idol_pair(i2, orig_idols, max_index)
            if lowbar:
                new_index += 1
                i2.matched = new_index
            else:
                i2.matched = max_index
        elif i2.matched == max_index and i1.matched == -1:
            lowbar = worse_idol_pair(i1, orig_idols, max_index)
            if lowbar:
                new_index += 1
                i1.matched = new_index
            else:
                i1.matched = max_index
        else:
            print("ERROR")
            input()
        # i1.matched = new_index
        # i2.matched = new_index
    #print (f"{score}, {i1.link} {i1.matched} -- {i2.link} {i2.matched}")
    if rest:
        match_idols(rest, orig_idols, new_index, counter+1)


    #print (f"{i1.name}, {i1.matched}")
    #print (f"{i2.name}, {i2.matched}")


#     i1 = paired[0]
#     i2 = paired[1]
#     if i1 not in posted_idols and i2 not in posted_idols:
#         index = len(posted_idols)

#     if rest:
#         match_idols(rest, posted_idols, matched_idols)
    
def youpunk(idols, counter=0):
    for idol in idols:
        other_ids = [i for i in (0, 1, 2) if idol.source_id != i]
        compared_to = ([i for i in idols if i.source_id == other_ids[0]], [i for i in idols if i.source_id == other_ids[1]])
        idol.matched_total = 0
        idol.best_match = []
        for c in compared_to:
            max_score = -101
            best_idol = None
            for i in c:
                next_score = compare_idol_v2(idol, i)
                if max_score < next_score:
                    max_score = next_score
                    best_idol = i
            if best_idol:
                idol.matched_total += max_score
                idol.best_match.append(best_idol)

    idols.sort(key=lambda x: x.matched_total, reverse=True)
    #print (idols[0].source_id)
    if idols:
        to_be_matched = [idols.pop(0)]
        #print (len(idols), idols[0].source_id)
        for idol in to_be_matched[0].best_match:
            to_be_matched.append(idol)
            idols.remove(idol)

                    # print (idol.name, best_idol.name, max_score)
        new_counter = len(to_be_matched)
        print (f"{counter} - {new_counter}")



        if counter > new_counter:
            new_counter = counter #maybe-pause
            input()
        else:
            txt = ""
            for i in to_be_matched:
                txt = txt + f"{i.name} {i.source_id}: "
            print(txt)
            #consodilate best

        if idols:
            youpunk(idols, new_counter)







conn = sqlite3.connect(IDP)
cursor = conn.cursor()

cnt2 = 1

# Query to get film names with 3 film sources and all 3 having equal idol_counts > 0
queryAll = """
SELECT films.name, film_sources.idols_count 
FROM films
INNER JOIN film_sources ON films.name = film_sources.film_name
GROUP BY films.name
"""

query = f"""
SELECT films.name, film_sources.idols_count 
FROM films
INNER JOIN film_sources ON films.name = film_sources.film_name
GROUP BY films.name
HAVING COUNT(film_sources.source_link) > 1 
"""
rest1 ="AND MIN(film_sources.idols_count) > 0 AND MIN(film_sources.idols_count) == MAX(film_sources.idols_count)"
query2 = """
SELECT film_sources.release_date
FROM films
INNER JOIN film_sources ON films.name = film_sources.film_name
WHERE FILMS.name = ?
"""

# Execute the query and fetch film names
cursor.execute(query)
film_names = cursor.fetchall()

# Loop through film names
for film_name_tuple in film_names:
    film_name = film_name_tuple[0]
    #print(f"Film: {film_name}")
    release_dates = cursor.execute(query2, (film_name,)).fetchall()
    max_days = 0
    for d1 in release_dates:
        for d2 in release_dates:
            
                max_days = max(max_days, abs((datetime.strptime(d1[0], "%Y-%m-%dT%H:%M:%S").date() - datetime.strptime(d2[0], "%Y-%m-%dT%H:%M:%S").date()).days))
                #print (d1[0], d2[0])
    if True:
        print (f"{film_name} {max_days}")
####
        query_idols = """
            SELECT idols.*, idols.rowid
            FROM idols
            INNER JOIN film_idols ON idols.link = film_idols.idol_link
            WHERE film_idols.film_name = ?
            """

            # Execute the query and fetch associated idols
        cursor.execute(query_idols, (film_name,))
        idols = []
        idols = [Idol_struct(idol) for idol in cursor.fetchall() ]

        youpunk (idols, 0 )

