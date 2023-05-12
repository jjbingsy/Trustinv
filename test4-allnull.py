import sqlite3
from fuzzywuzzy import fuzz
from datetime import datetime

from trustmod.utility import group_match_strings
from trustmod.utility import consolidate_idols
from trustmod.utility import consolidate_idols_withoutconn
from trustmod.utility import process_lists


from trustmod.vars.env_001 import IMAGE_DIRECTORY, MEDIA_DIRECTORIES, USER_AGENT_GOOGLE, FILMSOURCES_PATH, IDOLSDB_PATH, IDOLS2DB_PATH

# THINGS TO DO
# SELECT a.name, b.link, a.link, b.shared_key FROM idols a JOIN idols b ON a.name = b.name AND a.shared_key IS NULL and b.shared_key is not null;
# SELECT a.name, b.link, a.link, b.shared_key FROM idols a JOIN idols b ON a.name = b.name AND a.shared_key <> b.shared_key;
# SELECT NAME, count (name) cnt from idols group by name having shared_key is null and cnt > 1;
# SELECT NAME, count (name) cnt from idols group by name having shared_key is null and cnt = 1;
# SELECT NAME cnt from idols group by name having shared_key is null and cnt = 1
# select fi.film_name, i.link, i.name, i.shared_key from film_idols fi join idols i on fi.idol_link = i.link where i.link in (SELECT link cnt from idols group by name having shared_key is null and cnt > 1);

def my_display (lst):
    #return lst
    return [(x[1], x[2], x[3]) for x in lst]


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

def isolate_idols(x, group):
    if x[1]:
        for idol in group:
            if idol[1] and idol[1] == x[1]:
                return False
    return True



def group_best_matches(idols, x):
    sorted_results = sort_idols(idols, compare_idol_v1)
    grouped_results = [] #defaultdict(list)
    first = True
    for idol1, idol2, similarity in sorted_results:
        #print (idol1, idol2, similarity)
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
            if  idol1[1] != idol2[1]:
                grouped_results.append([idol1, idol2])
            else:
                grouped_results.append([idol1])
                grouped_results.append([idol2])
        elif s1 and not s2 and len(grouped_results[i1]) < x:
            if  isolate_idols(idol2,  grouped_results[i1]):
                grouped_results[i1].append(idol2)
            # else:
            #     grouped_results.append([idol2])
        elif s2 and not s1 and len(grouped_results[i2]) < x:
            if  isolate_idols(idol1,  grouped_results[i2]):
                grouped_results[i2].append(idol1)
            # else:
            #     grouped_results.append([idol1])
    return grouped_results




def combine_short_sublists(list_of_lists):
    if not list_of_lists:
        return []

    # Find the length of the largest sublist
    max_length = max(len(sublist) for sublist in list_of_lists)

    # Initialize an empty list to store the new sublists
    combined_sublists = []

    # Iterate through the list_of_lists
    for sublist in list_of_lists:
        # If the current sublist is shorter than the largest sublist
        if len(sublist) < max_length:
            # Check if there's a previous sublist in the combined_sublists that can be extended
            for previous_sublist in combined_sublists:
                if len(previous_sublist) + len(sublist) == max_length:
                    previous_sublist.extend(sublist)
                    break
            else:  # If no suitable previous sublist was found, add the current sublist as is
                combined_sublists.append(sublist)
        else:
            combined_sublists.append(sublist)

    return combined_sublists

def same_shared_key(s, t):
    return s[3] and t[3] and s[3] == t[3]

def grab_idol_name(idol):
    return idol[2]

def equal_length_sublists(list_of_lists):
    if not list_of_lists:
        return True

    length = len(list_of_lists[0])
    for sublist in list_of_lists[1:]:
        if len(sublist) != length:
            return False

    return True


# Establish a connection with your SQLite database
conn = sqlite3.connect(IDOLSDB_PATH)
cursor = conn.cursor()

cnt2 = 3

# Query to get film names with 3 film sources and all 3 having equal idol_counts > 0
queryAll = """
select distinct fi.film_name, i.name from film_idols fi join idols i on fi.idol_link = i.link where i.shared_key is null;
"""

query = f"""
SELECT films.name, film_sources.idols_count 
FROM films
INNER JOIN film_sources ON films.name = film_sources.film_name
GROUP BY films.name
HAVING COUNT(film_sources.source_link) = {cnt2} AND MIN(film_sources.idols_count) > 0 AND MIN(film_sources.idols_count) == MAX(film_sources.idols_count)
"""
query2 = """
SELECT film_sources.release_date
FROM films
INNER JOIN film_sources ON films.name = film_sources.film_name
WHERE FILMS.name = ?
"""

# Execute the query and fetch film names
cursor.execute(queryAll)
film_names = cursor.fetchall()

# Loop through film names
for film_name_tuple in film_names:
    film_name = film_name_tuple[0]
    print(f"Film: {film_name} idol missing {film_name_tuple[1]}")
    release_dates = cursor.execute(query2, (film_name,)).fetchall()
    max_days = 0
    for d1 in release_dates:
        for d2 in release_dates:
            
                max_days = max(max_days, abs((datetime.strptime(d1[0], "%Y-%m-%dT%H:%M:%S").date() - datetime.strptime(d2[0], "%Y-%m-%dT%H:%M:%S").date()).days))
    print (f"{release_dates}")
    print (f"{film_name} {max_days}")
    query_idols = """
        SELECT idols.*, idols.rowid
        FROM idols
        INNER JOIN film_idols ON idols.link = film_idols.idol_link
        WHERE film_idols.film_name = ?
        """

        # Execute the query and fetch associated idols
    cursor.execute(query_idols, (film_name,))
    idols = cursor.fetchall()
    y = [list(a) for a in idols]
    groups = group_best_matches ( y, cnt2)
    
    if len(groups) > 1:
        for i, group in enumerate( groups):
            # if all have the same shared key pop it out
            truth = True
            for g in group:
                for h in group:
                    truth = truth and same_shared_key(g, h)
            if truth:
                groups.pop(i)
    process_lists(groups, consolidate_idols_withoutconn, my_display)
                


    if False:
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
        idols = cursor.fetchall()
        y = [list(a) for a in idols]
        groups = group_best_matches ( y, cnt2)
        for i, group in enumerate( groups):
            # if all have the same shared key pop it out
            truth = True
            for g in group:
                for h in group:
                    truth = truth and same_shared_key(g, h)
            if truth:
                groups.pop(i)
        if max_days <= 30:
            for group in groups:
                #print ([  (i[1], i[2]) for i in group  ])
                if len(group) == cnt2:
                    consolidate_idols(cursor, group, conn)
                else:
                    print (f"{film_name} Not enough matches {group}")
                    process_lists([group], consolidate_idols_withoutconn, my_display)
                    #consolidate_idols(cursor, group, conn)

        else:

            # FOR GREATER THAN 30 DAYS
            if groups:
                process_lists(groups, consolidate_idols_withoutconn, my_display)

####

# SELECT DISTINCT film_name FROM film_idols JOIN idols ON film_idols.idol_link = idols.link WHERE idols.shared_key = 71;

if False:

    # Query to get associated idols for the film
    query_idols = """
    SELECT idols.*, idols.rowid
    FROM idols
    INNER JOIN film_idols ON idols.link = film_idols.idol_link
    WHERE film_idols.film_name = ?
    """

    # Execute the query and fetch associated idols
    cursor.execute(query_idols, (film_name,))
    idols = cursor.fetchall()
    
    groups = group_best_matches ( idols, 2)
    for group in groups:
        #print ([  (i[1], i[2]) for i in group  ])
        if len(group) == 2:
            consolidate_idols(cursor, group, conn)
        else:
            print (f"{film_name} Not enough matches {group}")
            #consolidate_idols(cursor, group, conn)




    # if len(idols) > 3:
    #     #grouped_idols = group_match_strings(idols, grab_idol_name, 65)    
    #     grouped_idols = group_match_strings(idols, grab_idol_name, 75, func2=same_shared_key)    
    #     # Loop through the film's associated idols
    # SELECT DISTINCT f.name AS film_name, i.shared_key FROM films f JOIN film_idols fi ON f.name = fi.film_name JOIN idols i ON fi.idol_link = i.link;
    #     if not equal_length_sublists(grouped_idols):
    #         combined_idols = combine_short_sublists(grouped_idols)
            
    #         if equal_length_sublists(combined_idols):
    #             print(f"Film: {film_name} is matched")
    #             for idol in combined_idols:
    #                 if len(idol) == 3 and False:
    #                     print(f"{len(idol)} Idol_group: {[  (i[1], i[2]) for i in idol  ]}")
    #                     consolidate_idols(cursor, idol, conn)
    #                 else:
    #                     pass
    #                     #print(f"{len(idol)} Idol_groupnot stored: {idol}")
    #         else:
    #             #print(f"Film: {film_name} is not matched")
    #             for idol in combined_idols:
    #                 #print(f"{len(idol)} Idol_group: {idol}")
    #                 pass
    #     else:
    #         for group in grouped_idols:
    #             #pass
    #             if group[0][1] + group[1][1] + group[2][1] == 3:
    #                 print(f"{len(group)} Idol_group: {[  (i[1], i[2]) for i in group  ]}")
    #             consolidate_idols(cursor, group, conn)
                
    # else:
    #     #pass
    #     #print (f"Film: {film_name} has {len(idols)} idols")
    #     consolidate_idols(cursor, idols, conn)

# Close the SQLite connection
conn.close()



# 
# 
'''
SELECT film_name FROM film_idols WHERE idol_link IN (?, ?) GROUP BY film_name HAVING COUNT(idol_link) = 2
'''
# SELECT film_name FROM film_idols WHERE idol_link IN ('https://missav.com/en/actresses/Riho%20Fujimori', 'https://jav.guru/actress/yamamoto-shuri/') GROUP BY film_name HAVING COUNT(idol_link) = 2