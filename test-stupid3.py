from datetime import datetime
from fuzzywuzzy import fuzz
import sqlite3

from trustmod.vars.env_001 import IDOLSDB_PATH as IDP
from trustmod.classes import Idol_struct
from trustmod.utility import consolidate_idols_withoutconn_idol_struct as consolidate_idols

def compare_idol_v2 (idol1, idol2):
    if idol1.shared_key and idol2.shared_key and idol1.shared_key == idol2.shared_key:
        return 100
    elif idol1.source_id == idol2.source_id:
        return -100
    else:
        return fuzz.ratio(idol1.name, idol2.name)

    
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


        txt = ""

        if counter > new_counter:
            new_counter = counter #maybe-pause
            if len(to_be_matched) > 1:
                if not (to_be_matched[0].shared_key and to_be_matched[1].shared_key and to_be_matched[0].shared_key == to_be_matched[1].shared_key):
                    print (f"socore: {compare_idol_v2(to_be_matched[0], to_be_matched[1] ) }")
                    for i in to_be_matched:
                        txt = txt + f"{i.name} {i.shared_key}: "
                    print(txt)
                    f = input()
                    if f == "a":
                        consolidate_idols(to_be_matched)
                        txt = ""
                        for i in to_be_matched:
                            txt = txt + f"{i.name} {i.shared_key}: "
                        print(txt)
                        input()
        else:
            consolidate_idols(to_be_matched)
            for i in to_be_matched:
                txt = txt + f"{i.name} {i.shared_key}: "
            print(txt)
            #consodilate best

        if idols:
            youpunk(idols, new_counter)







conn = sqlite3.connect(IDP)
cursor = conn.cursor()


# Query to get film names with 3 film sources and all 3 having equal idol_counts > 0
query = """
SELECT films.name, film_sources.idols_count 
FROM films
INNER JOIN film_sources ON films.name = film_sources.film_name
GROUP BY films.name
HAVING COUNT(film_sources.source_link) > 1 
"""
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
        query_idols = """
            SELECT idols.*, idols.rowid
            FROM idols
            INNER JOIN film_idols ON idols.link = film_idols.idol_link
            WHERE film_idols.film_name = ?
            """

            # Execute the query and fetch associated idols
        cursor.execute(query_idols, (film_name,))
        idols = [Idol_struct(idol) for idol in cursor.fetchall() ]

        youpunk (idols, 0 )

