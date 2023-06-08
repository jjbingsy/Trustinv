import sqlite3
import random
import subprocess
from pathlib import Path
from icecream import ic
import itertools
import threading
from trustmod.classes import MissFilm as Guru

from trustmod.vars.env_001 import IDOLSDB_PATH as IDP, IMAGE_DIRECTORY as IDD, MEDIA_DIRECTORIES as MDD, SIMLINK_DIRECTORY as SDD, IDOLS2DB_PATH as IDB2
from trustmod.classes import MissFilm as MissFilm_msl


#https://kivy.org/doc/stable/api-kivy.uix.recycleview.html
class FilmTileLogic:
    idol_shared_key = 0
    series_shared_key = 0
    idols = None

    def __init__(self, film_name:str, series_dominant:bool =True, top_idol:int =0 ) -> None:
        pass




class MainScreenLogic:
    def __init__(self: 'MainScreenLogic'):
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

    # @collector.setter    
    def collector(self, value):
        self._collector = value

    def intial_data(self, min_film_count=10, max_film_count=400):
        self.collector.data = self.solo_idols(min_film_count=min_film_count, max_film_count=max_film_count)


    def intial_data2(self, file_path = './stuff/include1.txt'):
        #self.collector.data = self.solo_idols(min_film_count=min_film_count, max_film_count=max_film_count)
        i = []
        # Check if the file exists
        f = Path(file_path)
        if f.exists():
            # Open the file
            with open(f, 'r') as file:
                # Read each line and strip spaces
                for line in file:
                    line = line.strip()
                    i.append(self.get_film(line))
        else:
            i.append( self.get_film("IPX-551"))
        self.i = i

        self.collector.data =  i


    def get_film(self, film, series_dominant=True) -> dict:
        conn = sqlite3.connect(IDP)
        c = conn.cursor()
        film_data: dict = dict()

        film_data['film_name'] = film
        film_logic = FilmTileLogic(film_name=film)

        c.execute('''select distinct i.shared_key 
            from film_idols fi join idols i on fi.idol_link = i.link 
            where fi.film_name = ?''', (film,))
        idols = c.fetchall()
        conn.close()
        idolsG = [i[0] for i in idols if i[0]]        

        if film in self.film_series:
            film_logic.series_shared_key = self.film_series[film]
            if series_dominant:
                idolsG.insert (0,0)
        idols = None
        if idolsG:
            idols = itertools.cycle(idolsG)
            shared_key = next(idols)
            film_logic.idol_shared_key = shared_key
        if len(idolsG) > 1:
            film_logic.idols = idols
        film_data['tile_logic'] = film_logic        

        return film_data



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
        # c.execute(f'''
        #     select i.shared_key, i.name 
        #     from film_idols fi join idols i on fi.idol_link = i.link 
        #     group by i.shared_key 
        #     having count(distinct fi.film_name) > {min_film_count} 
        #     and count(distinct fi.film_name) < {max_film_count} 
        #     and i.shared_key is not null 
        #     order by count(distinct fi.film_name) desc;
        #     ''')
        rows = self.film_ranges[min_film_count] # c.fetchall()
        datas = []
        for shared_key in rows:
            idol = self.shared_key_name[shared_key]
            c.execute(f'''
                select s.film from solo_cast_films s join films f on film = name where shared_key = {shared_key}''')
            

            films = c.fetchall()
            if films:
                film = random.choice(films)[0]
                idols = [shared_key]
                #print (idols[0][1], description)
                datas.append ({'idols': idols,  'description' : self.film_desc[film], 'film_name' : film, 'label' : f"{film} / {idol}"   } )
        return datas




                #datas.append({'shared_key': shared_key, 'films': films})

            #yield {'shared_key': shared_key[0], 'films': films}





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




    #def idols_choice(self: 'MainScreenLogic', shared_key: int, idol_name: str):

    def idols_choice(self: 'MainScreenLogic', MyTile):

        shared_key = MyTile.shared_key
        print (shared_key)
        idol_name = MyTile.series_name
        if shared_key > 0:
            idol_name = self.shared_key_name[shared_key]

        
        if shared_key > 0:
            cn = sqlite3.connect(IDP)
            cr = cn.cursor()
            cr.execute(f'''
                Select distinct f.film_name from film_idols f join idols i on f.idol_link = i.link where i.shared_key = {shared_key}
                ''')
            datas = []
            for film in cr.fetchall():
                film = film[0]
                cr.execute(f'''select description from films where name = '{film}' ''')
                description = cr.fetchone()[0]
                cr.execute(f'''select distinct i.shared_key from film_idols fi join idols i on i.link = fi.idol_link where fi.film_name = ? ''', (film,))
                idols = []
                for idss in cr.fetchall():
                    
                    if idss[0]:
                        idols.append(idss[0])
                datas.append ({'idols': idols,  'description' : description, 'film_name' : film , 'label' : f"{film} - {self.shared_key_name[idols[0]]}  "} )


                random.shuffle(datas)
                self.collector.data = datas
            cn.close()

        else:
            datas = []
            series_shared_key = int (MyTile.series_shared_key)
            cn = sqlite3.connect(IDB2)
            cr = cn.cursor()

            cr.execute(f'''
                       select name from film_series where shared_key = ?;
            ''', (series_shared_key,))
            i = []
            for rows in cr.fetchall():
                film = rows[0]
                i += self.get_film(film)

            self.collector.data = i
            cn.close()
        


    def playme (self, txt1):
        # print (txt1)
        t = ["C:/Users/bing/Desktop/mpv/mpv.exe", "--fs", "--fs-screen=0", "--loop-playlist" ]
        i = "C:/Users/bing/Desktop/mpv/mpv.exe --fs --fs-screen=0 --loop-playlist" 
        files = Path(SDD).glob ( txt1.lower() + "*")
        #print (files)
        
        for ss2 in files:
            print (ss2)
            t.append(ss2)
            i = i + " " + str(ss2)
            
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
                print (shared_key, count)
                c.execute("""
                    select name from film_series where shared_key = ?;
                """, (shared_key,))
                film_row = c.fetchall()
                if film_row is not None:
                    random.shuffle(film_row)
                    film = film_row[0][0]
                    print (film, shared_key, count)
                    idols = [0]
                    collect.append ({'film_name' : film, 'shared_key' : 0, 'label' : f'{film} -- {self.series_name[shared_key]}',
                                    'idols' : idols, 
                                    'series_shared_key' : shared_key,
                                    'series_name' : self.series_name[shared_key]} )

        self.collector.data = collect


    def getFilmData(self, film, idol=None, check_series=False):
        conn2 = sqlite3.connect(IDP)
        conn = sqlite3.connect(IDB2)
        c = conn.cursor()
        c.execute("select description, series_link, series_name from films where name = ?", (film,))
        description = c.fetchone()[0]
        series_link = c.fetchone()[1]
        series_name = c.fetchone()[2]
        if series_name is None and check_series:
            film = MissFilm_msl(name=film)


        # q1 = '''
        # select i.shared_key, count(distinct fi.film_name) c from film_idols fi join idols i on fi.idol_link = i.link group by i.shared_key having shared_key not null and c > 1 order by c desc;
        # '''
        # q2 = '''
        # select fi.film_name, count(distinct i.shared_key) c from film_idols fi join idols i on fi.idol_link = i.link group by fi.film_name having c = 1 and i.shared_key = ?;
        # '''

        # conn = sqlite3.connect(IDP)
        # kk = []
        # cursor = conn.cursor()
        # cursor.execute(q1)
        # results = cursor.fetchall()
        # for i in results:
        #     shared_key = i[0]
        #     cursor.execute(q2, (shared_key,))
        #     results2 = None
        #     resul = cursor.fetchall()
        #     if resul:
        #         results2 = resul[random.randint(0, len(resul)-1)]
        #     # for e in resul:
        #     #     #kk.append ( e[0] )
        #     #     results2 = e
        #         if results2:
        #             #print (results2[0], shared_key)
        #             q3 = "select name from idols where shared_key = ?"
        #             cursor.execute(q3, (shared_key,))
        #             name = cursor.fetchone()                   
        #             kk.append ( [results2[0], name[0]] )
           
           
        # conn.close()
        # return [{'source': f'{IDD}/{i}.jpg', 'texti' : i, 'act_option': 'idol', 'idol_name' : j } for i, j in kk]

    