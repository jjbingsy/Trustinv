from trustmod.utility import parseTitle
from trustmod.test import test1
from trustmod.main import checkInFilms
from trustmod.main import sortFilms
import platform

from trustmod.classes import GuruFilm, JavFilm, MissFilm, Idol

from trustmod.vars.env_001 import IMAGE_DIRECTORY, MEDIA_DIRECTORIES, USER_AGENT_GOOGLE, FILMSOURCES_PATH, IDOLSDB_PATH, IDOLS2DB_PATH

if __name__ == "__main__":
    # print (parseTitle ("Jesu33s is lordy!"))
    # print("Jesdffu33s is lordy!", IMAGE_DIRECTORY, MEDIA_DIRECTORIES, USER_AGENT_GOOGLE, FILMSOURCES_PATH, IDOLSDB_PATH, IDOLS2DB_PATH)
    # test1("Jesdffu33s is lordy!")
    # guru = GuruFilm(name="SSIS-715")
    # print (guru.description)
    # jav = JavFilm(name="JUL-106")
    # print (jav.description, jav.film_link)
    # miss = MissFilm(name="JUL-106")
    # print (miss.description, miss.film_link)
    checkInFilms()
    sortFilms()
    print (platform.system())