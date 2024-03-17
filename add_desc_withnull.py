import sqlite3
from bs4 import BeautifulSoup as bs4
import lxml
from  trustmod.vars.env_001 import IDOLSDB_PATH as IDOLSDB_PATH_CONTENTS, FILMSOURCES_PATH as FILMSOURCES_PATH_CONTENTS, USER_AGENT_GOOGLE as USER_AGENT_GOOGLE_CONTENTS


conn2 = sqlite3.connect( IDOLSDB_PATH_CONTENTS)
conn = sqlite3.connect (FILMSOURCES_PATH_CONTENTS)
cursor = conn.cursor()
cr = conn2.cursor()

with open('stuff/nodesc.txt', 'r') as file:
    for line in file:
        film = line.strip()
        cursor.execute("SELECT content FROM filmsources WHERE name = ? and url like '%database%'", (film,))
        soup = bs4(cursor.fetchone ()[0], "lxml")
        desc = soup.h1.text.strip()
        print(film, desc)
#         cr.execute("update films set description = ? where name = ?", (desc, film))
# conn2.commit()



