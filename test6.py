from pathlib import Path
from trustmod.vars.env_001 import IDOLSDB_PATH, IDOLS2DB_PATH
import sqlite3
import webbrowser
from trustmod.classes import GuruFilm, JavFilm, MissFilm, Idol
query = """select DISTINCT fi.film_name from idols i join film_idols fi on i.link = fi.idol_link where shared_key is null;"""
queryIdols = """select I.name, i.shared_key, i.link from idols i join film_idols fi on i.link = fi.idol_link where fi.film_name = ?;"""
queryfilmLink = """select source_link from film_sources where film_name = ?;"""

q1 = '''
select i.shared_key, count(distinct fi.film_name) c from film_idols fi join idols i on fi.idol_link = i.link group by i.shared_key having shared_key not null and c > 1 order by c desc;
'''
q2 = '''
select fi.film_name, count(distinct i.shared_key) c from film_idols fi join idols i on fi.idol_link = i.link group by fi.film_name having c = 1 and i.shared_key = ?;
'''

def getSharedKey():
    conn = sqlite3.connect(IDOLSDB_PATH)

    cursor = conn.cursor()
    cursor.execute(q1)
    results = cursor.fetchall()
    for i in results:
        shared_key = i[0]
        cursor.execute(q2, (shared_key,))
        results2 = cursor.fetchone()
        if results2:
            print (results2[0], shared_key)
        else:
            print (shared_key)
            input("pause: ")
    conn.close()


# for fil in results:
#     film = fil[0]
#     print(film)
#     idols = cursor.execute(queryIdols, (film,)).fetchall()
#     for idol in idols:
#         print(film, idol[0], idol[1], idol[2])
#     i = input("pause: ")
#     if i == "o":
#         cursor.execute (queryfilmLink, (film,))
#         film_link = cursor.fetchall()
#         for link in film_link:
#             webbrowser.open(link[0])
#         i = input("pause: ")
