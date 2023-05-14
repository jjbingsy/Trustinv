import sqlite3
import requests
from pathlib import Path

from trustmod.classes import GuruFilm, JavFilm, MissFilm, Idol
from trustmod.vars.env_001 import IMAGE_DIRECTORY, MEDIA_DIRECTORIES, USER_AGENT_GOOGLE, FILMSOURCES_PATH, IDOLSDB_PATH, IDOLS2DB_PATH

images = Path(IMAGE_DIRECTORY)

def update_content(db_path, url, new_content):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    update_sql = """
        UPDATE filmsources 
        SET content = ? 
        WHERE url = ?
    """
    
    cursor.execute(update_sql, (new_content, url))
    conn.commit()
    conn.close()



# jav = JavFilm(name="MEYD-421", force=True)

# for i in jav.idols:
#     print(i.name, i.link)

for i in images.iterdir():
    filmo = i.stem
    film_name = i.stem + "-2"
    if ("MIDV-" in film_name):
        miss = MissFilm(name=film_name)
        jav = JavFilm(name=film_name)
        if miss.content:
            misso = MissFilm(name=filmo)
            print (filmo, misso.film_link)
            update_content(FILMSOURCES_PATH, misso.film_link, miss.content)
            print (film_name, miss.film_link)
            for idol in miss.idols:
                print(idol.name, idol.link)
        if jav.content:
            javo = JavFilm(name=filmo)
            print (filmo, javo.film_link)
            update_content(FILMSOURCES_PATH, javo.film_link, jav.content)
            print (film_name, jav.film_link)
            for idol in jav.idols:
                print(idol.name, idol.link)
            #print (fil , miss.description, miss.film_link)


