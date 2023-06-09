from pathlib import Path
import sqlite3
from icecream import ic

from trustmod.vars.env_001 import IDOLSDB_PATH as IDP, IMAGE_DIRECTORY as IDD, MEDIA_DIRECTORIES as MDD, SIMLINK_DIRECTORY as SDD, IDOLS2DB_PATH as IDB2
file_path = './stuff/include12.txt'

# Check if the file exists
f = Path(file_path)
if f.exists():
    # Open the file
    ic.disable()
    ic.enable()
    with open(f, 'r') as file:
        # Read each line and strip spaces
        for line in file:
            line = line.strip()
            # Process the line
            # For example, print the line
            ic(line)
else:
    ic(f"The file '{file_path}' does not exist.")

'''
EMSK-006
NATR-687
BDA-071
BDA-073
BDA-080
BDA-082
BDA-150
KEED-077
MIAA-858
DVEH-008
SAME-056
SPZ-1133
NSFS-139
JUL-106
MIRD-202
MIRD-197
IPZ-950
IPX-551
MIAA-380
JUQ-017
MEYD-482
JUY-609
VEC-543
VEC-535
ADN-467
JUL-254
FSDSS-615
STARS-839
IPX-811
ADN-286
HOMA-119
JUQ-240
BMW-283
MIAA-862
SHKD-966
MIDV-002
MIDV-375
MIDV-236
MIDV-010
MIDV-023
IPX-993
MIAA-860

'''

conn = sqlite3.connect(IDP)
c = conn.cursor()
range_tup = [(10, 400), (5,11), (3, 6), (2, 4), (1, 3), (0, 2) ]

film_ranges = {}
for min_film_count, max_film_count in range_tup:     
    c.execute(f'''
        select i.shared_key
        from film_idols fi join idols i on fi.idol_link = i.link 
        group by i.shared_key 
        having count(distinct fi.film_name) > {min_film_count} 
        and count(distinct fi.film_name) < {max_film_count} 
        and i.shared_key is not null 
        order by count(distinct fi.film_name) desc;
        ''')
    rows = c.fetchall()
    films = [film[0] for film in rows]
    film_ranges[min_film_count] = films
ic(film_ranges[0])
ic(film_ranges[1])
ic(film_ranges[2])
ic(film_ranges[3])
ic(film_ranges[5])
ic(film_ranges[10])


from trustmod.main import MainScreenLogic, FilmTileLogic

i = MainScreenLogic()
# ic (i.get_film("MIRD-197", series_dominant=True, idol_dominant=45))


# for key, val in i.film_series.items():
#     ic (key, val)

# conn = sqlite3.connect(IDP)
# cn = conn.cursor()

i.load_series( 1529)
