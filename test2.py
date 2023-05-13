import sqlite3
from pathlib import Path
from trustmod.classes import JavFilm
#from trustmod.utility import parseTitle
from trustmod.vars.env_001 import IMAGE_DIRECTORY, MEDIA_DIRECTORIES, USER_AGENT_GOOGLE, FILMSOURCES_PATH, IDOLSDB_PATH, IDOLS2DB_PATH
#from trustmod.main import checkInFilms, sortFilms
#from trustmod.utility import process_lists
#from trustmod.utility import consolidate_idols_withoutconn 
#from trustmod.main import sortSpecificFilm



def my_process (list):
    for x in list:
        x[1] = x[1] + 1

def my_display (lst):
    #return lst
    return [(x[1], x[2], x[3]) for x in lst]


if __name__ == "__main__":
    #images = Path(IMAGE_DIRECTORY)
#    for image in images.iterdir():
#        print (image.stem)
#    print (None == 33)

    query_idols = """
        SELECT idols.*, idols.rowid
        FROM idols
        INNER JOIN film_idols ON idols.link = film_idols.idol_link
        WHERE film_idols.film_name = ?
        """

    conn = sqlite3.connect(IDOLSDB_PATH)
    cursor = conn.cursor()
    cursor.execute(query_idols, ("SSNI-580",))
    idols = cursor.fetchall()
    conn.close()

    #x = [idols]
    y = [list(a) for a in idols]
    print (idols)
    print (y)
    r = [y]#print (y)
    print (r)
    #sortSpecificFilm("DLDSS-100")
    #i = GuruFilm(name="MEYD-421")

    print (2)
    

    
