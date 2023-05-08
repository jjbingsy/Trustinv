import sqlite3
from ..vars.env_001 import IDOLSDB_PATH


class Idol:
    def check_link(self):
        if self.link and self.shared_key == 0:
            conn = sqlite3.connect(IDOLSDB_PATH)
            cursor = conn.cursor()
            cursor.execute('''SELECT shared_key FROM idols WHERE idol_link=?''', (self.link,))
            result = cursor.fetchone()
            if result:
                self.shared_key = result[0]
            conn.close()


    def __init__(self, name, link="", image_link=None, image_content=None, shared_key=0) -> None:        
        self.name = name
        self.link = link
        self.image_link = image_link
        self.image_content = image_content
        self.shared_key = shared_key

        # todo: set_key function to set the shared_key value
        # checks if has a valid shared_key value
        # if not, sets the shared_key value
        # if so, does nothing
        # if shared_key is 0, then it will set the shared_key value
    def set_key(self):
        self.check_link()
        if self.shared_key == 0:
            conn = sqlite3.connect(IDOLSDB_PATH)
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO idols (idol_link) VALUES (?)''', (self.link,))
            conn.commit()
            self.shared_key = cursor.lastrowid
            cursor.execute('''UPDATE idols SET shared_key=? WHERE idol_link=?''', (self.shared_key, self.link))
            conn.commit()                
            conn.close()  
        return self.shared_key


    @property
    def skey (self):
        self.check_link()
        return self.shared_key
    
    @skey.setter
    def skey (self, value):
        self.check_link()
        conn = sqlite3.connect(IDOLSDB_PATH)
        cursor = conn.cursor()
        if self.shared_key == 0:
            cursor.execute('''INSERT OR REPLACE INTO IDOLS (idol_link, shared_key) VALUES (?, ?)''', (self.link, value ))                
            self.shared_key = value
        else:
            old_key = self.shared_key
            cursor.execute('''UPDATE idols SET shared_key=? WHERE shared_key=?''', (value, old_key))
        conn.commit()
        conn.close()
        self.shared_key = value


