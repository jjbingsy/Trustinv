import sqlite3

from trustmod.vars.env_001 import IDOLSDB_PATH, SERIESDB_PATH
from trustmod.classes import GuruFilm as Guru, JavFilm as Jav, MissFilm as Miss, Film


conn = sqlite3.connect(IDOLSDB_PATH)
c = conn.cursor()
c.execute("drop table if exists series")
c.execute("CREATE TABLE  series (link TEXT PRIMARY KEY, name TEXT)")
c.execute("drop table if exists film_series")
c.execute("CREATE TABLE  film_series (film_name TEXT, series_link TEXT, PRIMARY KEY (film_name, series_link))")
conn.commit()
c.execute("select name from films")

films = c.fetchall()
for row in films:
    film = row[0]
    sources = [Guru(name=film), Jav(name=film), Miss(name=film)]
    for source in sources:
        if source.content and source.series_link:
            c.execute("INSERT OR IGNORE INTO series VALUES (?, ?)", (source.series_link, source.series_name))
            c.execute("INSERT OR IGNORE INTO film_series VALUES (?, ?)", (film, source.series_link))
    print (film)
    conn.commit()
conn.close()