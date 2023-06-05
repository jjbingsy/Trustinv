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

class JavFilm (Film):

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
        self.content = None
        self.image_link = None
        soup = bs4(page, "lxml")
        series_name = None
        series_link = None
        desc = None
        film_link = None
        name = None

        image_source = soup.find('tr', class_='moviecovertb')
        if image_source:
            image_link = image_source.find('img')['src']
            name = soup.h1.text
            film_link = f"https://www.javdatabase.com/movies/{name.lower()}/"
            description = soup.find('td', text='Translated Title:')
            #print ("XXX", description.text)
            try:
                desc = description.next_sibling.text.strip()
            except:
                pass
            try:
                desc = description.next_sibling.next_sibling.text.strip()
            except:
                pass
            seriesTitle = soup.find('td', text='Series: ')
            #stitle = seriesTitle.next_sibling.text.strip()
            #print ("STITLE", stitle)
            try:
                if seriesTitle.next_sibling.text.strip() != "":
                    series_name = seriesTitle.next_sibling.text.strip()
                    series_link = seriesTitle.next_sibling.a['href']
            except:
                pass
            try:
                if seriesTitle.next_sibling.next_sibling.text.strip() != "":
                    series_name = seriesTitle.next_sibling.next_sibling.text.strip()
                    series_link = seriesTitle.next_sibling.next_sibling.a['href']
            except:
                pass

            self.content = page
            releaseDateTitle = soup.find('td', text='Release Date:')
            releaseDate1 = releaseDateTitle.next_sibling.text
            try:
                releaseDate1 = releaseDateTitle.next_sibling.next_sibling.text
            except:
                pass
            rdate = parse(releaseDate1, fuzzy=True)



            super().__init__(image_link=image_link, film_name=name, description=desc, series_name=series_name, series_link=series_link, film_link=film_link, release_date=rdate)
            idols = soup.find_all('div', class_='idol-thumb')


            for idol in idols:
                idolsp = idol.previous_sibling
                #print(idolsp.a.text, idolsp.a['href'])
                # Extract the idol name
                idol_name = idolsp.find('a').text
                #print (idol_name)
            
                # Extract the idol link
                idol_link = idol.find('a')['href']
            
                # Extract the idol image URL
                idol_image = idol.find('img')['src']
                self.add_idol(Idol(idol_name, link=idol_link, image_link=idol_image))
        else:
            super().__init__()



        if False:
            image_link = image_source[0]['data-poster']
            series_raw = soup.find('a', {'href': re.compile("https://missav.com/en/series")}, class_="text-nord13 font-medium")
            try:
                series_link = series_raw['href']
                series_name = series_raw.text
            except:
                series_name = None
                series_link = None
            description = soup.find('h1')
            if not description:
                raise ValueError("Corrupt data: No h1 found.")
            #name = parseTitle(description.string)
            name = parseTitle(description.string)
            film_link = f"https://missav.com/en/{name.lower()}"

            desc = (description.string.replace(name, "")).strip()
            self.content = page
            

            # Idols must be added after the init has been called because the empty list is initialized on self.idols.
            idols = soup.find_all('a', {'href': re.compile(f"https://missav.com/en/actresses/")}, class_="text-nord13 font-medium")
            for idol in idols:
                self.add_idol(Idol(idol.string, link=idol["href"]))

    def checkSource(self, name, store=True, force=False):
        href = f"https://www.javdatabase.com/movies/{name.lower()}/"
        page = get_content(href, parseTitle(name.upper()), store=store, force=force)
        soup = bs4(page, "lxml")
        return soup.find('tr', class_='moviecovertb'), soup, page


    def __init__(self, name=None, store=True, force=False):
        self.content = None
        self.idols = []
        #self.image_link = None already in Film
        self.series_link = None
        self.series_name = None
        self.image_type = None
        self.image_content = None
        #self.film_name = None already in Film
        #self.film_link = None already in Film
        self.content = None
        self.film_name = None
        self.film_link = None
        page = None
        image_source = None
        soup = None
        if "MIDV-" in name:
            alt_name = name + "-2"
            image_source, soup, page = self.checkSource(alt_name, store=store, force=force)
        if not image_source:
            image_source, soup, page = self.checkSource(name, store=store, force=force)
        rdate = None
        self.content = None
        self.image_link = None
        series_name = None
        series_link = None
        desc = None
        film_link = None
        name = None
        if image_source:
            image_link = image_source.find('img')['src']
            name = soup.h1.text
            film_link = f"https://www.javdatabase.com/movies/{name.lower()}/"
            description = soup.find('td', text='Translated Title:')
            #print ("XXX", description.text)
            try:
                desc = description.next_sibling.text.strip()
            except:
                pass
            try:
                desc = description.next_sibling.next_sibling.text.strip()
            except:
                pass
            seriesTitle = soup.find('td', text='Series: ')
            #stitle = seriesTitle.next_sibling.text.strip()
            #print ("STITLE", stitle)
            try:
                if seriesTitle.next_sibling.text.strip() != "":
                    series_name = seriesTitle.next_sibling.text.strip()
                    series_link = seriesTitle.next_sibling.a['href']
            except:
                pass
            try:
                if seriesTitle.next_sibling.next_sibling.text.strip() != "":
                    series_name = seriesTitle.next_sibling.next_sibling.text.strip()
                    series_link = seriesTitle.next_sibling.next_sibling.a['href']
            except:
                pass

            self.content = page
            releaseDateTitle = soup.find('td', text='Release Date:')
            releaseDate1 = releaseDateTitle.next_sibling.text
            try:
                releaseDate1 = releaseDateTitle.next_sibling.next_sibling.text
            except:
                pass
            rdate = parse(releaseDate1, fuzzy=True)



            super().__init__(image_link=image_link, film_name=name, description=desc, series_name=series_name, series_link=series_link, film_link=film_link, release_date=rdate)
            idols = soup.find_all('div', class_='idol-thumb')


            for idol in idols:
                idolsp = idol.previous_sibling
                #print(idolsp.a.text, idolsp.a['href'])
                # Extract the idol name
                idol_name = idolsp.find('a').text
                #print (idol_name)
            
                # Extract the idol link
                idol_link = idol.find('a')['href']
            
                # Extract the idol image URL
                idol_image = idol.find('img')['src']
                self.add_idol(Idol(idol_name, link=idol_link, image_link=idol_image))






    def ___orig_init__(self, name=None, fixed_text=None, page=None, file=None, store=True, force=False):
        self.content = None
        self.idols = []
        #self.image_link = None already in Film
        self.series_link = None
        self.series_name = None
        self.image_type = None
        self.image_content = None
        #self.film_name = None already in Film
        #self.film_link = None already in Film

        if page:
            self.__initializeFilm(page)
        elif file:
            with open(file, "r", encoding="UTF-8") as f:
                self.__initializeFilm(f.read())
        elif name:
            self.content = None
            self.film_name = None
            self.film_link = None
            href = f"https://www.javdatabase.com/movies/{name.lower()}/"
            qcontent = get_content(href, parseTitle(name.upper()), store=store, force=force)
            self.__initializeFilm(qcontent)
            
        elif fixed_text:
            super().__init__()
            self._reversedSet(fixed_text)