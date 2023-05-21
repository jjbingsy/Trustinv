from bs4 import BeautifulSoup as bs4
from .string_mainpulation import parseTitle
from pathlib import Path
import requests
import time
import re
import sqlite3
import requests
from pathlib import Path
from PIL import Image
from datetime import datetime
from dateutil.parser import parse

from ..vars.env_001 import IDOLSDB_PATH as IDOLSDB_PATH_CONTENTS, FILMSOURCES_PATH as FILMSOURCES_PATH_CONTENTS, USER_AGENT_GOOGLE as USER_AGENT_GOOGLE_CONTENTS
# from ..vars.env_001 import IDOLSDB_PATH, FILMSOURCES_PATH, SIMLINK_DIRECTORY, IMAGE_DIRECTORY, MEDIA_DIRECTORIES, USER_AGENT_GOOGLE
# from ..vars.env_001 import IDOLSDB_PATH, FILMSOURCES_PATH, SIMLINK_DIRECTORY, IMAGE_DIRECTORY, MEDIA_DIRECTORIES, USER_AGENT_GOOGLE

def get_content(url, name, store=True, force=False):
    conn = sqlite3.connect(FILMSOURCES_PATH_CONTENTS)
    cursor = conn.cursor()

    # Check if the URL exists in the table
    result = None
    if not force:
        cursor.execute("SELECT content FROM filmsources WHERE url = ?", (url,))
        result = cursor.fetchone()
    content = None

    if result:
        content = result[0]
    else:
        # Request the content from the URL
        time.sleep(2)
        response = requests.get(url, headers=USER_AGENT_GOOGLE_CONTENTS)
        content = response.text
        #print(name, url)
        if store:
            # Insert the URL, name, and content into the table
            cursor.execute("INSERT or REPLACE INTO filmsources (url, name, content) VALUES (?, ?, ?)", (url, name, content))
            conn.commit()
    conn.close()
    return content

def consolidate_idols(cursor, idols, conn):
    new_key = idols[0][4]
    for idol in idols:
        if idol[3] and idol[3] != new_key:
            cursor.execute("""update idols set shared_key = ? where shared_key = ?""", (new_key, idol[3]))
        cursor.execute("""update idols set shared_key = ? where link = ?""", (new_key, idol[0]))
    conn.commit()

def consolidate_idols_withoutconn(idols):
    conn = sqlite3.connect(IDOLSDB_PATH_CONTENTS)
    cursor = conn.cursor()

    new_key = idols[0][4]
    for idol in idols:
        if idol[3] and idol[3] != new_key:
            cursor.execute("""update idols set shared_key = ? where shared_key = ?""", (new_key, idol[3]))
        cursor.execute("""update idols set shared_key = ? where link = ?""", (new_key, idol[0]))
    for idol in idols:
        idol[3] = new_key
    conn.commit()
    conn.close()

def my_display (lst):
    #return lst
    return [(x[1], x[2], x[3]) for x in lst]

