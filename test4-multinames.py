import sqlite3
from trustmod.vars.env_001 import IDOLSDB_PATH as IDP, IMAGE_DIRECTORY as IDD, MEDIA_DIRECTORIES as MDD, SIMLINK_DIRECTORY as SDD, IDOLS2DB_PATH as IDB2
from trustmod.classes import MissFilm , GuruFilm, JavFilm

conn = sqlite3.connect(IDB2)
cnn = sqlite3.connect(IDP)

c = cnn.cursor() # idp
cr = conn.cursor() # idb2

cr.execute('''
    select name, shared_key from film_series; 
''')
for film, shared_key in cr.fetchall():
    print (film, shared_key)
    c.execute('''update films set series_id = ? where name = ?''', (shared_key, film))
cnn.commit()

miss = MissFilm(name="JUQ-049")
series_tochange = miss.series_link
cr.execute('''select rowid from film_series where name = ?''', ("JUQ-049",))
new_shared_key = cr.fetchone()[0]

c.execute('''select name from films where series_id = ?''', (1125,))
for film_t in c.fetchall():
    film = film_t[0]
    miss = MissFilm(name=film)
    if miss.content and miss.series_link == series_tochange:
        print (film)
        cr.execute('''update film_series set shared_key = ? where name = ?''', (new_shared_key, film))
        
cr.execute('''update series set shared_key = ? where link = ?''', (new_shared_key, series_tochange))
conn.commit()

conn.close()
cnn.close()

# ihad toupdate series set shared_key = 951 where link = 'https://jav.guru/series/on-the-7th-day-after-being-raped-by-my-husbands-boss-i-lost-my-mind/';
'''
update film_series set shared_key = 951 where name = 'JUX-790';
update film_series set shared_key = 951 where name = 'JUX-942';
update film_series set shared_key = 951 where name = 'JUX-728';
delete from film_series where name = 'JUL-254';
'''