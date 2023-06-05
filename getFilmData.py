import sqlite3
import random
import subprocess
from pathlib import Path
import threading

from trustmod.vars.env_001 import IDOLSDB_PATH as IDP, IMAGE_DIRECTORY as IDD, MEDIA_DIRECTORIES as MDD, SIMLINK_DIRECTORY as SDD, IDOLS2DB_PATH as IDB2
from trustmod.classes import MissFilm as MissFilm_msl, GuruFilm, JavFilm

# create temp view if not exists solo_cast_films (film, shared_key, idol) as select distinct fi.film_name, i.shared_key, i.name from film_idols fi join idols i on fi.idol_link = i.link group by fi.film_name having count(distinct i.shared_key) = 1;
# select idol, shared_key, count(film) cnt from solo_cast_films group by shared_key having cnt > 4 order by cnt asc;


def getFilmData(self, film, idol=None, check_series=False):
    conn2 = sqlite3.connect(IDP)
    conn = sqlite3.connect(IDB2)
    c = conn.cursor()
    c.execute("select description, series_link, series_name from films where film = ?", (film,))
    y = c.fetchone()
    if y is None:
        return None
    
    print (f"film {film} found in db")
    description = y[0]
    series_link = y[1]
    series_name = y[2]
    if not series_name and check_series:
        pass
    film = MissFilm_msl(name=film)
    if film.content and film.series_link:   
        series_link = film.series_link
        series_name = film.series_name

        print (description, series_link, series_name)
        print ("yeasdsdsdsdsd")
    return True

#select shared_key, name from idols group by shared_key;
#************** side work englishfy description

conn = sqlite3.connect(IDB2)
cnm = sqlite3.connect(":memory:")
conn2 = sqlite3.connect(IDP)
c = conn.cursor()
cr = conn2.cursor()
crm = cnm.cursor()


c.execute('''
    CREATE TABLE IF NOT EXISTS SERIES (
        link TEXT PRIMARY KEY,
        name TEXT,
        shared_key INTEGER
    )
''')


c.execute('''
    CREATE TABLE IF NOT EXISTS film_series (
        name TEXT PRIMARY KEY,
        shared_key INTEGER
    )
''')

# Commit the changes and close the connection
conn.commit()

cr.execute("select distinct name from films")
allfilms = cr.fetchall()
for x in allfilms:
    film = x[0]
    series= []
    sources = [MissFilm_msl(name=film), GuruFilm(name=film), JavFilm(name=film)]
    # for source in sources:
    #     if source.content and source.series_link:
    #         series.append([source.series_link, source.series_name])

    series = [(source.series_link, source.series_name) for source in sources if source.content and source.series_link]
    if series:
         # Insert film into film_series table
        c.execute("INSERT OR IGNORE INTO film_series (name) VALUES (?)", (film,))
        shared_key = c.lastrowid
        if shared_key > 0:
            c.execute("UPDATE film_series SET shared_key = ? WHERE name = ?", (shared_key, film))
            for rows in series:
                c.execute("INSERT OR IGNORE INTO SERIES (link, name, shared_key) VALUES (?, ?, ?)", (rows[0], rows[1], shared_key))
                print (rows[0])
                c.execute("select shared_key from SERIES where link = ?", (rows[0],))
                previous_shared_key = c.fetchone()[0]
                if previous_shared_key != shared_key:
                    c.execute("UPDATE SERIES SET shared_key = ? WHERE shared_key = ?", (shared_key, previous_shared_key))
                    c.execute("UPDATE film_series SET shared_key = ? WHERE shared_key = ?", (shared_key, previous_shared_key))
    conn.commit()

        ## inside this loop I want to insert film, into film_series and update the new film getting the shared_key = to its rowid




# c.execute("select distinct series_link from films")
# for x in c.fetchall():
#     series_link = x[0]
#     c.execute("select distinct film from films where series_link = ?", (series_link,))
#     t = True
    
#     for y in c.fetchall():
#         film = y[0]

#         print (film, series_link)
# select distinct fi.film_name, i.shared_key from film_idols fi join idols i on fi.idol_link = i.link group by fi.film_name having count(distinct i.shared_key) = 1 and i.shared_key = 2033 order by i.shared_key;
# select distinct fi.film_name from film_idols fi join idols i on fi.idol_link = i.link group by fi.film_name having count(distinct i.shared_key) = 1 and i.shared_key = 2033;

conn.close()
conn2.close()
cnm.close()
