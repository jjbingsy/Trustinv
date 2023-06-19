import sqlite3
import random
import subprocess
from pathlib import Path
from icecream import ic
from ..main import checkVideoFiles
import itertools
import threading
from ..classes import MissFilm as Guru

from ..vars.env_001 import IDOLSDB_PATH as IDP,  SIMLINK_DIRECTORY as SDD, IDOLS2DB_PATH as IDB2, MPV_DIRECTORY as MPV, MPV_PLATFORM_OPTIONS as MPO
from ..classes import MissFilm as MissFilm_msl


#https://kivy.org/doc/stable/api-kivy.uix.recycleview.html
#https://kivymd.readthedocs.io/en/0.104.0/components/navigation-drawer/index.html
#https://kivymd.readthedocs.io/en/1.1.1/components/textfield/index.html
class FilmTileLogic:
    series_key = 0
    shared_key = 0
    category_name = ''
    categories = None

    def __init__(self, film_name:str, film_desc:str = '' ) -> None:
        self.film_desc = film_desc

    def load_categories(self, collect):
        cnt = len(collect)
        if cnt  > 0:
            self.shared_key, self.category_name = collect[0]
            ic (self.shared_key, self.category_name)
            if cnt > 1:
                self.categories = itertools.cycle(collect)
                xd, yd = next(self.categories)
                assert xd == self.shared_key
                assert yd == self.category_name
                ic (self.series_key)

    def next_category(self):
        if self.categories:
            self.shared_key, self.category_name = next(self.categories)
            return self.category_name
        else:
            return None




class MainScreenLogic:

    def add_and_refresh(self):
        checkVideoFiles()
        self.initial_clear()
        print('refreshed')

    def add_new_videos(self):
        thread = threading.Thread(target=self.add_and_refresh)
        thread.start()

        #        checkVideoFiles()

    def get_film(self, film, series_dominant=False, idol_dominant=0) -> dict:

        idolsG = list()
        film_logic = None
        film_data: dict = dict()
        film_data['film_name'] = film
        if film not in self.film_desc:
            return dict()
        
        if film in self.films:
            film_logic, idolsG = self.films[film]
        else:
            conn = sqlite3.connect(IDP)
            c = conn.cursor()
            film_logic = FilmTileLogic(film_name=film, film_desc = self.film_desc[film]  )

            c.execute('''select distinct i.shared_key 
                from film_idols fi join idols i on fi.idol_link = i.link 
                where fi.film_name = ?''', (film,))
            idols = c.fetchall()
            conn.close()
            idolsG = [i[0] for i in idols if i[0]]   
            self.films[film] = (film_logic, idolsG)





        series = []
        if idol_dominant > 0 and idol_dominant in idolsG:
            idolsG.remove(idol_dominant)
            idolsG.insert(0, idol_dominant)

        if film in self.film_series:
            series_key = self.film_series[film]
            film_logic.series_key = series_key
            if series_dominant:
                series.append((-series_key, self.series_name[series_key])  )
        series += [(i, self.shared_key_name[i]) for i in idolsG]
        #u = series += idolsG
        film_logic.load_categories(series)
        film_data['tile_logic'] = film_logic
        return film_data

    def load_page (self, page):
        if self.current:
            self.previous.append(self.current)
        self.current = page
        self.collector.data = page
        del self.forward[:]

    def load_previous(self):
        if self.previous:
            self.forward.append(self.current)
            self.current = self.previous.pop()
            self.collector.data = self.current
    
    def load_forward(self):
        if self.forward:
            self.previous.append(self.current)
            self.current = self.forward.pop()
            self.collector.data = self.current

    def initial_clear(self):
        self.films = dict()
        self.previous = list()
        self.forward = list()
        self.current = None
        self.mybar = None
        self._collector = None
        self.container = None
        conn = sqlite3.connect(IDB2)
        c = conn.cursor()
        cn = sqlite3.connect(IDP)
        cr = cn.cursor()
    
        range_tup = [(10, 400), (5,11), (3, 6), (2, 4), (1, 3), (0, 2) ]




        self.film_ranges = dict()
        for min_film_count, max_film_count in range_tup:     
            cr.execute(f'''
                select i.shared_key
                from film_idols fi join idols i on fi.idol_link = i.link 
                group by i.shared_key 
                having count(distinct fi.film_name) > {min_film_count} 
                and count(distinct fi.film_name) < {max_film_count} 
                and i.shared_key is not null 
                order by count(distinct fi.film_name) desc;
                ''')
            rows = cr.fetchall()
            idols = [shared_key[0] for shared_key in rows]
            self.film_ranges[min_film_count] = idols



        query = '''
        select shared_key, name from (select * from series where link not like "%miss%") group by shared_key;
        
        '''
        c.execute(query)
        self.series_name = {tup[0]: tup[1] for tup in c.fetchall()}
        # self.cursor = self.conn.cursor()
        cr.execute('select shared_key, name from idols group by shared_key;') #XX
        results = cr.fetchall()
        self.shared_key_name = {tup[0]: tup[1] for tup in results}
        #print (self.shared_key_name)
        cr.execute('select name, description from films;')
        self.film_desc = {tup[0]: tup[1] for tup in cr.fetchall()}

        c.execute('select name, shared_key from film_series;')
        self.film_series = {tup[0]: tup[1] for tup in c.fetchall()}

        cr.close()
        conn.close()


    def __init__(self: 'MainScreenLogic'):
        self.initial_clear()
    # @collector.setter    
    def collector(self, value):
        self._collector = value

    def intial_data(self, min_film_count=10, max_film_count=400):
        self.load_page( self.solo_idols(min_film_count=min_film_count, max_film_count=max_film_count))


    def intial_data2(self, file_path = './stuff/include1.txt'):
        #self.collector.data = self.solo_idols(min_film_count=min_film_count, max_film_count=max_film_count)
        i = []
        # Check if the file exists
        f = Path(file_path)
        if f.exists():
            print (f"my file_p[ath] is {file_path}")
            # Open the file
            with open(f, 'r') as file:
                # Read each line and strip spaces
                for line in file:
                    line = line.strip()
                    new_film = self.get_film(line, series_dominant=False)
                    if new_film:
                        i.append(new_film)
        else:
            i.append( self.get_film("IPX-551", series_dominant=True))
        self.load_page( i)



    def solo_idols(self, min_film_count=10, max_film_count=400):
        conn = sqlite3.connect(IDP)
        c = conn.cursor()
        c.execute(f'''
            create temp view if not exists 
            solo_cast_films (film, shared_key, idol) as 
            select distinct fi.film_name, i.shared_key, i.name 
            from film_idols fi join idols i 
            on fi.idol_link = i.link 
            group by fi.film_name 
            having count(distinct i.shared_key) = 1; 
            ''')
        conn.commit()
        rows = self.film_ranges[min_film_count]
        datas = []
        for shared_key in rows:
            c.execute(f'''
                select s.film from solo_cast_films s join films f on film = name where shared_key = {shared_key}''')
            ic(shared_key)
            films = c.fetchall()
            if films:
                film = random.choice(films)[0]
                datas.append (self.get_film(film))
        return datas







    def idols(self, min_film_count=10, max_film_count=400):
        cc = sqlite3.connect(IDP)
        cr = cc.cursor()
        cr.execute(f'''
            select i.shared_key, i.name, count(distinct fi.film_name) cnt 
                from idols i 
                    join film_idols fi 
                        on fi.idol_link = i.link 
                    group by i.shared_key 
                    having cnt > {min_film_count} and cnt < {max_film_count} and i.shared_key is not null
                    order by cnt desc ;            
            ''')

        datas = []
        rows = cr.fetchall()
        for shared_key, idol_name, film_count in rows:

            cr.execute('''
                select film_name, shared_key, count(*) cnt 
                    from (select distinct fi.film_name, i.shared_key from idols i 
                            join film_idols fi on fi.idol_link = i.link order by fi.film_name) 
                    group by film_name 
                    having cnt = 1 and shared_key = ?;                
                ''', (shared_key,))  # replace `desired_shared_key` with the actual value

            film_rows = cr.fetchall()
            random.shuffle(film_rows)
            #row = random.choice(film_rows)[0]
            if film_rows:
                film = film_rows[0][0]
                #cr.execute('select description from films where name = ?', (film,))
                description = self.film_desc[film]
                #print (film, description)
                idols = [shared_key]
                datas.append ({'idols': idols,  'description' : description, 'film_name' : film, 'label' : f'{film} --' } )
            else:
                print (f'no film for {idol_name} {shared_key}')
                

        cc.close()
        return datas




    def idols_choice(self: 'MainScreenLogic', MyTile):

        shared_key = MyTile.shared_key
        if shared_key > 0:
            #            idol_name = self.shared_key_name[shared_key]
            cn = sqlite3.connect(IDP)
            cr = cn.cursor()
            cr.execute(f'''
                Select distinct f.film_name from film_idols f join idols i on f.idol_link = i.link where i.shared_key = {shared_key}
                ''')
            films_raw = cr.fetchall()
            films = [i for i, in films_raw]
            random.shuffle(films)
            to_process = [self.get_film(film, idol_dominant=shared_key) for film in films]
            self.load_page( to_process)
        elif shared_key < 0:
            series_key = abs(shared_key)
            self.load_series(series_key)

        
    def load_series(self, series_key):
        cn = sqlite3.connect(IDB2)
        cr = cn.cursor()
        cr.execute(f'''
            select name from film_series where shared_key = ?;
        ''', (series_key,))
        ii = cr.fetchall()
        my_list = [i[0] for i in ii ] 
        random.shuffle(my_list)
        self.mybar.title = self.series_name[series_key]
        self.load_page([ self.get_film(rows, series_dominant=True) for rows in my_list])
        cn.close()
        

    def playme (self, txt1):
        print (txt1)
        # print (txt1) on windows 
        '''
        MPV_DIRECTORY = "C:/Users/bing/Desktop/mpv/mpv.exe"
        MPV_PLATFORM_OPTIONS = "--fs-screen=0"
        
        '''

        t = [MPV, "--fs", MPO, "--loop-playlist" ]
        files = Path(SDD).glob ( txt1.upper() + "*")
        for ss2 in files:
            t.append(ss2)

        subprocess.run(t)

    def playme2 (self, film_name):              
        thread = threading.Thread(target=self.playme, args=(film_name,))
        thread.start()

    def get_random_films_in_series(self):
        conn = sqlite3.connect(IDB2)
        c = conn.cursor()

        # Query to get the number of films in each series
        c.execute("""
        select shared_key, count(name) cnt from film_series group by shared_key having cnt > 1 order by cnt desc;
        """)
        series_counts = c.fetchall()
        collect = []
        for shared_key, count in series_counts:
            #shared_key = int(shared_key_raw
            if shared_key in self.series_name:
                c.execute("""
                    select name from film_series where shared_key = ?;
                """, (shared_key,))
                film_row = c.fetchall()
                if film_row:
                    film = random.choice(film_row)
                    collect.append (self.get_film(film[0], series_dominant=True))
        
        self.mybar.title = f'Random Films in Series'
        self.load_page(collect)
        conn.close()