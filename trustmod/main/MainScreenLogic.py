import sqlite3
import random
import subprocess
from pathlib import Path
import threading
from trustmod.classes import MissFilm as Guru

from trustmod.vars.env_001 import IDOLSDB_PATH as IDP, IMAGE_DIRECTORY as IDD, MEDIA_DIRECTORIES as MDD, SIMLINK_DIRECTORY as SDD, IDOLS2DB_PATH as IDB2


class MainScreenLogic:
    def __init__(self: 'MainScreenLogic'):
        self.mybar = None
        self._collector = None
        self.container = None
        
        # self.conn = sqlite3.connect(IDB2)
        # self.cursor = self.conn.cursor()
        # cn = sqlite3.connect(IDP)
        # cr = cn.cursor()

        # self.cursor.execute('''
        #     CREATE TABLE IF NOT EXISTS idols (
        #     shared_key INTEGER PRIMARY KEY, name TEXT)
        #     ''')
        # self.cursor.execute('''
        #     CREATE TABLE IF NOT EXISTS films (
        #     film TEXT PRIMARY KEY, description TEXT, series_link TEXT, series_name TEXT)
        #     ''')

        # self.cursor.execute('''
        #     CREATE TABLE IF NOT EXISTS idol_films (
        #     shared_key INTEGER, 
        #     film TEXT,
        #     primary key (shared_key, film),
        #     FOREIGN KEY(shared_key) REFERENCES idols(shared_key),
        #     FOREIGN KEY(film) REFERENCES films(film) )
        #     ''')
        # self.conn.commit()




        # q1 = '''
        # select i.shared_key, count(distinct fi.film_name) c from film_idols fi join idols i on fi.idol_link = i.link group by i.shared_key having shared_key not null and c > 1 order by c desc;
        # '''
        # q2 = '''
        # select fi.film_name, count(distinct i.shared_key) c from film_idols fi join idols i on fi.idol_link = i.link group by fi.film_name having c = 1 and i.shared_key = ?;
        # '''

        
        # kk = []
        
        # cr.execute(q1)
        # results = cr.fetchall()
        # for i in results:
        #     shared_key = i[0]
        #     q3 = "select name from idols where shared_key = ?"
        #     cr.execute(q3, (shared_key,))
        #     names = cr.fetchone()                   
        #     name = names[0]
        #     self.cursor.execute("INSERT INTO idols VALUES (?, ?)", (shared_key, name))
        #     self.conn.commit()    
        #     cr.execute(q2, (shared_key,))
            
        #     films = cr.fetchall()
        #     if films:
        #         for film in films:
        #             film_name = film[0]
        #             cr.execute ("select description from films where name = ?", (film_name,))
        #             desc = cr.fetchone()
        #             description = desc[0]
        #             self.cursor.execute("INSERT INTO films(film, description) VALUES (?, ?)", (film_name, description))
        #             #print (film_name, description)
        #             self.cursor.execute("INSERT INTO idol_films VALUES (?, ?)", (shared_key, film_name))
        # cr.execute("select name, description from films")
        # rows1 = cr.fetchall()
        # for row in rows1:
        #     film = row[0]
        #     desc = row[1]                    
        #     self.cursor.execute("INSERT or IGNORE INTO films(film, description) VALUES (?, ?)", (film, desc))
        #     guru = Guru(name=film)
        #     if guru.content:
        #         if guru.series_link:
        #             series_link = guru.series_link
        #             series_name = guru.series_name
        #             self.cursor.execute("UPDATE films SET series_link = ?, series_name = ? WHERE film = ?", (series_link, series_name, film))


        # cn.commit()



        # self.conn.commit()
        # self.conn.close()




        #     # if resul:
        #     #     results2 = resul[random.randint(0, len(resul)-1)]
        #     # # for e in resul:
        #     # #     #kk.append ( e[0] )
        #     # #     results2 = e
        #     #     if results2:
        #     #         #print (results2[0], shared_key)
           
           
        # cn.close()
    


    # @property
    # def collector(self):
    #     """I'm the 'x' property."""
    #     return self._collector

    # @collector.setter    
    def collector(self, value):
        self._collector = value

    def intial_data(self, min_film_count=10, max_film_count=400):
        #self.collector.data = [{'source': 'i'}]
        #self.container.clear_widgets()
        self.collector.data = self.idols(min_film_count=min_film_count, max_film_count=max_film_count ) #[{'text': str(x)} for x in range(50)]    




    def idols(self, min_film_count=10, max_film_count=400):
        cc = sqlite3.connect(IDB2)
        self.cursor = cc.cursor()
        self.cursor.execute(f'''
            SELECT idols.shared_key, idols.name, COUNT(distinct idol_films.film) AS film_count 
            FROM idols
            JOIN idol_films ON idols.shared_key = idol_films.shared_key
            GROUP BY idols.shared_key, idols.name having film_count > {min_film_count} and film_count < {max_film_count}
            ORDER BY film_count DESC
            ''')

        datas = []
        rows = self.cursor.fetchall()
        for shared_key, idol_name, film_count in rows:
            print (shared_key) 



            self.cursor.execute('''
                SELECT films.film, films.description
                FROM films
                JOIN idol_films ON films.film = idol_films.film
                WHERE idol_films.shared_key = ?
                ''', (shared_key,))  # replace `desired_shared_key` with the actual value

            film_rows = self.cursor.fetchall()
            random.shuffle(film_rows)
            #row = random.choice(film_rows)[0]
            film = film_rows[0][0]
            description = film_rows[0][1]

            datas.append ({'source': f'{IDD}/{film}.jpg', 'texti' : film, 'idol_name' : idol_name, 'description' : description, 'shared_key' : shared_key } )
        cc.close()
        return datas




    #def idols_choice(self: 'MainScreenLogic', shared_key: int, idol_name: str):

    def idols_choice(self: 'MainScreenLogic', MyTile):

        shared_key = MyTile.shared_key
        idol_name = MyTile.idol_name

        
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
                datas.append ({'source': f'{IDD}/{film}.jpg', 'texti' : film, 'idol_name' : idol_name, 'description' : description, 'shared_key' : shared_key } )
                random.shuffle(datas)
                self.collector.data = datas
            cn.close()

        else:
            datas = []
            cn = sqlite3.connect(IDB2)
            cr = cn.cursor()
            print (MyTile.series_link)
            cr.execute(f'''
                select f.film, ifs.shared_key, f.series_link, i.name, f.description from films f 
                    join idol_films ifs on f.film = ifs.film 
                    join idols i on ifs.shared_key = i.shared_key
            where f.series_link = '{MyTile.series_link}' ''')
            # cr.execute(f'''
            #     select f.film, ifs.shared_key, f.series_link, f.description from films f 
            #         join idol_films ifs on f.film = ifs.film 
            # where f.series_link = '{MyTile.series_link}' ''')
            for rows in cr.fetchall():
                film = rows[0]
                shared_key = rows[1]
                series_link = rows[2]
                idol_name = rows[3]
                description = rows[4]
                datas.append ({'source': f'{IDD}/{film}.jpg', 'texti' : film, 'description' : description, 'shared_key' : shared_key, "idol_name" : idol_name } )

            self.collector.data = datas
                
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
            SELECT series_link, COUNT(film) as num_films
            FROM films
            GROUP BY series_link having series_link not null and num_films > 1
            ORDER BY num_films desc
        """)
        series_counts = c.fetchall()

        collect = []
        for series_link, count in series_counts:

            print (series_link, count)
            c.execute("""
                SELECT film, description, series_link, series_name
                FROM films
                WHERE series_link = ?
            """, (series_link,))
            film_row = c.fetchall()
            if film_row is not None:
                random.shuffle(film_row)
                film = film_row[0][0]
                description = film_row[0][1]
                series_link = film_row[0][2]
                series_name = film_row[0][3]

                collect.append ({'source': f'{IDD}/{film}.jpg', 
                                'texti' : film, 'description' : description, 
                                'idol_name' : series_name,
                                'series_name' : series_name,
                                'series_link' : series_link, 
                                'shared_key': 0} )

        self.collector.data = collect





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

    