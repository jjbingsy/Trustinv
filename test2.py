import sqlite3
from pathlib import Path
from trustmod.classes import GuruFilm, JavFilm, MissFilm, Idol
from trustmod.utility import parseTitle
from trustmod.vars.env_001 import IMAGE_DIRECTORY, MEDIA_DIRECTORIES, USER_AGENT_GOOGLE, FILMSOURCES_PATH, IDOLSDB_PATH, IDOLS2DB_PATH
from trustmod.main import checkInFilms, sortFilms


if __name__ == "__main__":
    images = Path(IMAGE_DIRECTORY)
    for image in images.iterdir():
        image.stem



