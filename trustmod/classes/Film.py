from bs4 import BeautifulSoup as bs4
from .Idol import Idol

class Film:
    def __init__(self, film_name=None, film_link=None,
                 description= None, series_name= None, series_link=None,
                 image_link= None, release_date=None) -> None:
        self.image_link = image_link
        self.description = description
        self.film_name = film_name
        self.film_link = film_link
        self.series_name = series_name
        self.series_link = series_link
        self.release_date = release_date
        self.idols = []


    def add_idol(self, idol):
        if isinstance(idol, Idol):
            self.idols.append(idol)
    
    def prettify(self):
        # Ensure required data is present
        if not self.film_name or not self.film_link or not self.image_link:
            return None
        
        jsoup = bs4('<html><head><title></title></head><body></body></html>', 'lxml')
        mainlink = self.film_link

        # Create the main div tag with class "item"
        body1 = jsoup.new_tag("div")
        body1["class"] = "item"

        # Create and add image, link, and description tags
        image = self.image_link
        div_tag = jsoup.new_tag('div')
        a_tag = jsoup.new_tag('a', href=mainlink)
        a_tag['class'] = "mainlink"
        img_tag = jsoup.new_tag('img', src=image, style='width: 511px; height: 343px; object-fit: cover; margin-right: 10px;')
        desc_tag = jsoup.new_tag('h2')
        desc_tag ['style'] = "width: 511px"
        desc_tag['class'] ="description"
        desc_tag.string = self.description
        a_tag.append(img_tag)
        div_tag.append(a_tag)
        body1.append(div_tag)
        body1.append(desc_tag)

        # Create and add series and idols tags if present
        if self.series_link and self.series_name:
            series_p = jsoup.new_tag('p')
            series_p.string = "Series: "
            series_tag = jsoup.new_tag ('a')
            series_tag.string = self.series_name
            series_tag['href'] = self.series_link
            series_tag['class'] = "series"
            series_p.append (series_tag)
            body1.append(series_p)

        ul_tag = jsoup.new_tag('ul')
        for idol in self.idols:
            li_tag = jsoup.new_tag('li')
            a_tag = jsoup.new_tag('a')
            a_tag['href'] = idol.link
            a_tag['class'] = 'idol'
            a_tag.string = idol.name
            li_tag.append(a_tag)
            ul_tag.append(li_tag)

        # Create and add hidden input tag with metadata
        input_tag = jsoup.new_tag('input')
        input_tag['type'] = 'hidden'
        input_tag['source'] = "deprecated"
        input_tag['title'] = self.film_name
        jsoup.title.string = self.film_name
        input_tag['idol_count'] = len(self.idols)
        body1.append(ul_tag)
        body1.append(input_tag)
        jsoup.body.append(body1)

        return jsoup.prettify()

   
    def _reversedSet(self, page):
        soup = bs4(page, "lxml")
        
        # Ensure required data is present
        image_tag = soup.find("img")
        film_link_tag = soup.find("a", class_="mainlink")
        title_tag = soup.title
        description_tag = soup.find("h2", class_="description")
        
        if not image_tag or not film_link_tag or not title_tag or not description_tag:
            raise ValueError("Corrupt data: Required tags are missing.")
        
        self.image_link = str(image_tag["src"])
        self.film_link = film_link_tag['href']
        self.film_name = str(title_tag.string).strip()
        self.description = description_tag.string.strip()
        
        try:
            series_tag = soup.find("a", class_="series")
            self.series_link = series_tag["href"]
            self.series_name = series_tag.string.strip()
        except:
            self.series_link = None
            self.series_name = None
            
        idols = soup.find_all("a", class_="idol")
        for idol in idols:
            self.idols.append(Idol(idol.string.strip(), idol["href"]))

        for i in self.idols:
            print(i.name, i.link)
