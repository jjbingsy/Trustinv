from pathlib import Path
import sqlite3

from ..vars.env_001 import IDOLS2DB_PATH as IDB2_series1
from ..classes import GuruFilm as GuruFilm_series1, JavFilm as JavFilm_series1, MissFilm as MissFilm_series1


def load_film_series(film):
    conn = sqlite3.connect(IDB2_series1)
    c = conn.cursor()
    series= []
    sources = [MissFilm_series1(name=film), GuruFilm_series1(name=film), JavFilm_series1(name=film)]
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
    conn.close()
    