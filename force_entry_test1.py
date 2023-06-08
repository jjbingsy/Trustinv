import sqlite3
from pathlib import Path
#from dateutil.parser import parse
import sqlite3

from trustmod.classes import MissFilm, GuruFilm, JavFilm
from trustmod.vars.env_001 import IDOLSDB_PATH as IDP, FILMSOURCES_PATH, SIMLINK_DIRECTORY, IMAGE_DIRECTORY, MEDIA_DIRECTORIES, USER_AGENT_GOOGLE

conn = sqlite3.connect(IDP)
cursor = conn.cursor()

film = "PRED-120"

sources = [ GuruFilm(name=film), MissFilm(name=film), JavFilm(name=film) ]
idols_cnt = [-1, -1, -1]

for index, source in enumerate (sources):
    
    if source.content:
        idols_cnt [index] = len(source.idols)
        desc = source.description
        rdate = source.release_date
        if rdate is None:
            rdate = parse("1900-01-01")

        cursor.execute("""
                INSERT OR IGNORE INTO film_sources (source_link, film_name, source_id, idols_count, release_date)
                VALUES (?, ?, ?, ?, ?);
                """, (source.film_link, film, index, len(source.idols), rdate.isoformat() ))
        conn.commit()



        for idol in source.idols:
            cursor.execute("""
                INSERT OR IGNORE INTO idols (link, source_id, name)
                VALUES (?, ?, ?);
                """, (idol.link, index,  idol.name))
            conn.commit()
            print (film, idol.link)
            cursor.execute("""
            INSERT INTO film_idols (film_name, idol_link)
            VALUES (?, ?);
            """, (film, idol.link))
            conn.commit()
        
            #    input ("Error: " + film + " " + idol.link)




max_idols_cnt = max(idols_cnt)
cursor.execute("""
UPDATE films SET idols_max_count = 1 where name = ?;
""", (film,))








conn.commit()
conn.close()
