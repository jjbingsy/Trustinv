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
from ..vars.env_001 import IDOLSDB_PATH, FILMSOURCES_PATH, SIMLINK_DIRECTORY, IMAGE_DIRECTORY, MEDIA_DIRECTORIES, USER_AGENT_GOOGLE

def get_content(url, name, store=True, force=False):
    conn = sqlite3.connect(FILMSOURCES_PATH)
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
        response = requests.get(url, headers=USER_AGENT_GOOGLE)
        content = response.text
        #print(name, url)
        if store:
            # Insert the URL, name, and content into the table
            cursor.execute("INSERT or REPLACE INTO filmsources (url, name, content) VALUES (?, ?, ?)", (url, name, content))
            conn.commit()
    conn.close()
    return content


