import sqlite3
import random
import subprocess
from pathlib import Path
import threading

from trustmod.vars.env_001 import IDOLSDB_PATH as IDP, IMAGE_DIRECTORY as IDD, MEDIA_DIRECTORIES as MDD, SIMLINK_DIRECTORY as SDD, IDOLS2DB_PATH as IDB2
from trustmod.classes import MissFilm as MissFilm_msl, GuruFilm, JavFilm

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


#************** side work englishfy description

conn = sqlite3.connect(IDB2)
c = conn.cursor()

c.execute("select distinct series_link from films")
for x in c.fetchall():
    series_link = x[0]
    c.execute("select distinct film from films where series_link = ?", (series_link,))
    t = True
    
    for y in c.fetchall():
        film = y[0]

        print (film, series_link)
