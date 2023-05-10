import sqlite3
from trustmod.utility import group_match_strings
from trustmod.utility import consolidate_idols

from trustmod.vars.env_001 import IMAGE_DIRECTORY, MEDIA_DIRECTORIES, USER_AGENT_GOOGLE, FILMSOURCES_PATH, IDOLSDB_PATH, IDOLS2DB_PATH

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

# Query to get film names with 3 film sources and all 3 having equal idol_counts > 0
query = """
SELECT films.name
FROM films
INNER JOIN film_sources ON films.name = film_sources.film_name
GROUP BY films.name
HAVING COUNT(film_sources.source_link) = 3 AND MIN(film_sources.idols_count) > 0 AND MIN(film_sources.idols_count) = MAX(film_sources.idols_count)
"""

# Execute the query and fetch film names
cursor.execute(query)
film_names = cursor.fetchall()

# Loop through film names
for film_name_tuple in film_names:
    film_name = film_name_tuple[0]
    #print(f"Film: {film_name}")
    
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

    if len(idols) > 3:
        #grouped_idols = group_match_strings(idols, grab_idol_name, 65)    
        grouped_idols = group_match_strings(idols, grab_idol_name, 75, func2=same_shared_key)    
        # Loop through the film's associated idols

        if not equal_length_sublists(grouped_idols):
            combined_idols = combine_short_sublists(grouped_idols)
            
            if equal_length_sublists(combined_idols):
                #print(f"Film: {film_name} is matched")
                for idol in combined_idols:
                    if len(idol) == 3 and False:
                        print(f"{len(idol)} Idol_group: {[  (i[1], i[2]) for i in idol  ]}")
                        consolidate_idols(cursor, idol, conn)
                    else:
                        pass
                        #print(f"{len(idol)} Idol_groupnot stored: {idol}")
            else:
                #print(f"Film: {film_name} is not matched")
                for idol in combined_idols:
                    #print(f"{len(idol)} Idol_group: {idol}")
                    pass
        else:
            for group in grouped_idols:
                #pass
                if group[0][1] + group[1][1] + group[2][1] == 3:
                    print(f"{len(group)} Idol_group: {[  (i[1], i[2]) for i in group  ]}")
                consolidate_idols(cursor, group, conn)
                
    else:
        #pass
        #print (f"Film: {film_name} has {len(idols)} idols")
        consolidate_idols(cursor, idols, conn)

# Close the SQLite connection
conn.close()



# 
# 
'''
SELECT film_name FROM film_idols WHERE idol_link IN (?, ?) GROUP BY film_name HAVING COUNT(idol_link) = 2
'''
# SELECT film_name FROM film_idols WHERE idol_link IN ('https://missav.com/en/actresses/Riho%20Fujimori', 'https://jav.guru/actress/yamamoto-shuri/') GROUP BY film_name HAVING COUNT(idol_link) = 2