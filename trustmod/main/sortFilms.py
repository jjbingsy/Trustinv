from pathlib import Path
from dateutil.parser import parse
import sqlite3

from ..vars.env_001 import IDOLSDB_PATH, FILMSOURCES_PATH, SIMLINK_DIRECTORY, IMAGE_DIRECTORY, MEDIA_DIRECTORIES, USER_AGENT_GOOGLE
from ..classes import GuruFilm, JavFilm, MissFilm, Idol



def create_tables(conn):
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS series (
        series_link TEXT PRIMARY KEY,
        name TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS films (
        name TEXT PRIMARY KEY,
        description TEXT,
        series_id INTEGER,
        idols_max_count INTEGER,
        FOREIGN KEY (series_id) REFERENCES series (rowid)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS film_sources (
        source_link TEXT PRIMARY KEY,
        film_name TEXT NOT NULL,
        source_id INTEGER,
        release_date TEXT,
        idols_count INTEGER,
        FOREIGN KEY (film_name) REFERENCES films (name)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS idols (
        link TEXT PRIMARY KEY,
        source_id INTEGER,
        name TEXT,
        shared_key INTEGER,
        FOREIGN KEY (source_id) REFERENCES film_sources (source_id)
    );
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_shared_key ON idols (shared_key);
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS film_idols (
        film_name TEXT,
        idol_link TEXT,
        PRIMARY KEY (film_name, idol_link),
        FOREIGN KEY (film_name) REFERENCES films (name),
        FOREIGN KEY (idol_link) REFERENCES idols (link)
    );
    """)

    conn.commit()

def setTrans():
    conn = sqlite3.connect(IDOLSDB_PATH)
    create_tables(conn)
    conn.close()

def sortFilms():
    setTrans()
    conn = sqlite3.connect(IDOLSDB_PATH)

    cursor = conn.cursor()
    images_dir = Path(IMAGE_DIRECTORY)
    desc = ""
    cntNotStored = 0
    cntTo = 0
    for image in images_dir.iterdir():
        film = image.stem
        try:
            cursor.execute("""
            INSERT INTO films (name)
            VALUES (?);
            """, (film,))
            conn.commit()
        except:
            continue

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
        UPDATE films SET description = ?, idols_max_count = ? where name = ?;
        """, (desc, max_idols_cnt, film))
        conn.commit()
    conn.close()
