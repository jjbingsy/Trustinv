from pathlib import Path
from trustmod.vars.env_001 import IDOLSDB_PATH, IDOLS2DB_PATH
import sqlite3
import webbrowser
from trustmod.classes import GuruFilm, JavFilm, MissFilm, Idol
query = """select DISTINCT fi.film_name from idols i join film_idols fi on i.link = fi.idol_link where shared_key is null;"""
queryIdols = """select I.name, i.shared_key, i.link from idols i join film_idols fi on i.link = fi.idol_link where fi.film_name = ?;"""
queryfilmLink = """select source_link from film_sources where film_name = ?;"""


conn = sqlite3.connect(IDOLSDB_PATH)

cursor = conn.cursor()
cursor.execute(query)
results = cursor.fetchall()
for fil in results:
    film = fil[0]
    print(film)
    idols = cursor.execute(queryIdols, (film,)).fetchall()
    for idol in idols:
        print(film, idol[0], idol[1], idol[2])
    i = input("pause: ")
    if i == "o":
        cursor.execute (queryfilmLink, (film,))
        film_link = cursor.fetchall()
        for link in film_link:
            webbrowser.open(link[0])
        i = input("pause: ")



conn.close()
