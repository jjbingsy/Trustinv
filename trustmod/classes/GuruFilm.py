from .Film import Film
from .Idol import Idol
from ..vars.env_001 import FILMSOURCES_PATH
import sqlite3
import requests
import time
from bs4 import BeautifulSoup as bs4
from ..utility import parseTitle
from ..utility import get_content
from dateutil.parser import parse



class GuruFilm(Film):
    """A class for storing information about a film from jav.guru
    
    Attributes:
        series_name (str): The name of the series the film belongs to.
        series_link (str): The link to the series the film belongs to.
        image_link (str): The link to the film's image.
        description (str): The description of the film.
        film_link (str): The link to the film's page.
        film_name (str): The name of the film.
        idols (list): A list of Idol objects that are in the film.
    """

    def get_image_content(self, store=True):
        self.image_content = None
        self.image_type = None
        conn = sqlite3.connect(FILMSOURCES_PATH)
        cursor = conn.cursor()
        if not self.image_link:
            conn.close()
            return None, None
        # Check if the URL exists in the table
        cursor.execute("SELECT content, type FROM images WHERE url = ?", (self.image_link,))
        result = cursor.fetchone()

        if result:
            self.image_content = result[0]
            self.image_type = result[1]
        else:
            headers1 = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
            # Request the content from the URL
            time.sleep(2)
            response = requests.get(self.image_link, headers=headers1)
            self.image_content = response.content
            self.image_type = response.headers['Content-Type']
            if store:
                # Insert the URL, name, and content into the table
                cursor.execute("INSERT or replace INTO images (url, name, content, type) VALUES (?, ?, ?, ?)", (self.image_link, self.film_name, self.image_content, self.image_type))
                conn.commit()

        conn.close()
        return self.image_content, self.image_type



    def _reversedSet(self, page):
        return super()._reversedSet(page)

    def __initializeFilm(self, page):
        rdate = None
        series_name = None
        series_link = None

        soup = bs4(page, "lxml")
        series = soup.find("div", class_="infoleft").select('a[href*="jav.guru/series/"]')

        for i in series:
            series_name = i.string.strip()
            series_link = i["href"]

        header1 = soup.find('link', rel='canonical')
        if not header1:
            raise ValueError("Corrupt data: No canonical link found.")

        film_link = header1['href']
        description = soup.title.string
        iimage = None
        img = soup.find('div', class_="large-screenimg")
        if not img or not img.img:
            raise ValueError("Corrupt data: No image source found.")
        name = parseTitle(description)
        iimage = img.img['src']

        t = soup.find('div', class_="infoleft")
        e = t.find_all('li')
        for dates in e:
            if "Release Date" in dates.text:
                rdate = parse(dates.text, fuzzy=True)


        super().__init__(series_name=series_name, series_link=series_link, image_link=iimage, description=description, film_link=film_link, film_name=name, release_date=rdate)
        idols = soup.find("div", class_="infoleft").select('a[href*="jav.guru/actress/"]')

        for i in idols:
            self.idols.append(Idol(i.string.strip(), i['href']))

    def __init__(self, page=None, file=None, name=None, fixed_text=None, store=True, force=False):
        self.idols = []
        self.content = None
        #self.image_link = None already in Film
        self.image_type = None
        self.image_content = None
        #self.film_name = None already in Film
        #self.film_link = None already in Film


        if page:
            self.__initializeFilm(page)
            self.content = page
        elif file:
            with open(file, "r", encoding="UTF-8") as f:
                self.content = f.read()
                self.__initializeFilm(self.content)
        elif name:
            href = f"https://jav.guru/?s={name}"
            qcontent = get_content(href, name, store=store, force=force)      
            if qcontent:      
                soup = bs4(qcontent, 'lxml')
                films = soup.find_all("h2")
                #self.description = None
                if films[0].a:
                    href2 = films[0].a["href"]
                    self.content = get_content(href2, name, store=store, force=force)            
                    #store all new to proper store of site pick-up htmls
                    self.__initializeFilm(self.content)
                else:
                    self.content = None
                    self.film_name = None
                    self.film_link = None
            else:
                print ("No content")
                self.content = None
                self.film_name = None
                self.film_link = None



        elif fixed_text:
            super().__init__()
            self._reversedSet(fixed_text)


