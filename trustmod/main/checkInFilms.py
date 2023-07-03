import io
from pathlib import Path
import platform
from icecream import ic
import numpy as np_numpy
from PIL import Image as Im_PIL


from ..vars.env_001 import IDOLSDB_PATH, FILMSOURCES_PATH, SIMLINK_DIRECTORY, IMAGE_DIRECTORY, MEDIA_DIRECTORIES, USER_AGENT_GOOGLE
from ..classes import GuruFilm, JavFilm, MissFilm, Idol
from ..utility import parseTitle
from .initiate_individual_film_series import load_film_series as load_series
from .idol_shared_key_entry import add_idol_shared_key_from as load_idol_shared_key
from .sortFilms import sortFilm



class EntyFilms:
    def __init__(self, film):
        self.image = None
        self.film = film
        self.film_sources = []
        source = GuruFilm (name=film)
        if source.content:
            self.film_sources.append(source)
            if source.get_image_content():
                self.image = source.image_content
        source = MissFilm (name=film)
        if source.content:
            self.film_sources.append(source)
            if not self.image and source.get_image_content():
                    self.image = source.image_content
            #else:
            elif not self.image:
                random_color = np_numpy.random.randint(0, 256, 3, dtype=np_numpy.uint8)
                #     # Create a 512x512 array filled with the random RGB value
                random_array = np_numpy.full((539, 800, 3), random_color, dtype=np_numpy.uint8)
                #     # Create an image from the array
                #self.image = Im_PIL.fromarray(random_array)
                image_data = io.BytesIO()
                Im_PIL.fromarray(random_array).save(image_data, 'JPEG') # im.save(image_data, format='JPEG')
                self.image = image_data.getvalue()
                ic(f"image for {self.film} is wrong")
        source = JavFilm (name=film)
        if source.content:
            self.film_sources.append(source)

    def isValidFilm(self):
        if self.film_sources:
            return True
        else:
            return False
    def storeFilm(self):
        pass
    def storeImage(self, force=False):
        image_path = Path (IMAGE_DIRECTORY) / f"{self.film}.jpg"
        if image_path.exists():
            if force:
                with open(image_path, 'wb') as f:
                    f.write(self.image)
        else:
            with open(image_path, 'wb') as f:
                f.write(self.image)
        return image_path
        
    
    def isFilmStored(self):
        pass


def counter_suffix(x):
    if x:
        return f"_{x}"
    else:
        return ""
def symlink_toe(path):
    counter = 0
    midfix = (f"{path.parent}").replace(":", "").replace("/", "").replace ("\\", "")

    newfile = f"{parseTitle(path.stem)}_{midfix}{counter_suffix(counter)}{path.suffix}"
    i = Path(SIMLINK_DIRECTORY) / newfile
    while i.exists():
        counter += 1
        newfile = f"{parseTitle(path.stem)}_{midfix}{counter_suffix(counter)}{path.suffix}"
        i = Path(SIMLINK_DIRECTORY) / newfile
    i.symlink_to(path)
    ic (f"symlinked {path} to {i}")
    #print (f"symlinked {path} to {i}")
    return parseTitle(path.stem)



def checkVideoFiles():
    bookmarked = set()
    bookmarked_path = Path ("stuff/added_films.txt")
    # with open(bookmarked_path, 'r') as f:
    #     for line in f:
    #         if line.strip():
    #             bookmarked.add(line.strip())
    videos = set()
    sym_files = set()
    dest = Path(SIMLINK_DIRECTORY)

    for line in MEDIA_DIRECTORIES:
        raw_path = line.strip()
        paths = Path (raw_path)
        for file in paths.iterdir():
            if file.suffix.lower() in ['.mp4', '.wmv', '.mkv', '.avi']:
                videos.add(f"{file.resolve(strict=False)}")
                #p (file.parent) is its directory


    for sym in dest.iterdir():
        if sym.is_symlink():
            src = sym.resolve(strict=False)
            if src.exists():
                sym_files.add (f"{src}")
            else:
                sym.unlink()
                ic (f"deleted broken link {sym} from {src}")

    no_sym = videos - sym_files
    print (f"no_sym: {len(no_sym)}")
    for file in no_sym:
        counter = 0
        #print (file)
        video = Path(file)
        film = symlink_toe(video)
        ic (film)
        film = EntyFilms(film)
        if film.isValidFilm():
            bookmarked.add(film.film)
            ic(film.storeImage())
            sortFilm(film.film, film.film_sources)
            load_idol_shared_key(film.film)
            load_series(film.film)
    with open(bookmarked_path, 'a') as f:
        for line in bookmarked:
            print (line, file=f )
            #f.write(f"{line}\n") 

    


# def checkInFilms():
#     sym_files = set()
#     # Read the file and process each line
#     dest = Path(SIMLINK_DIRECTORY)
#     for line in MEDIA_DIRECTORIES:

#         raw_path = line.strip()
#         paths = Path (raw_path)
#         suffixrep = ":/"
#         if platform.system() == "Linux":
#             suffixrep = "/"
#         suffix = "-" + raw_path.replace(suffixrep, '_') 
#         for file in paths.iterdir():
#             if file.suffix.lower() in ['.mp4', '.wmv', '.mkv', '.avi']:
#                 newfile = dest / (parseTitle(file.stem) + suffix + file.suffix)
#                 if not newfile.exists():
#                     print (file)
#                     newfile.symlink_to(file)
#                     print ("good", newfile)
#                 else:
#                     nn = ""
#                     cnt = 0
#                     while True:
#                         cnt += 1
#                         new_filename = parseTitle(file.stem) + suffix + f"_{cnt}{file.suffix}"
#                         nn = dest / new_filename
#                         if not nn.exists():
#                             break
#                     nn.symlink_to(file)
#                     print ("badto good", nn)         
#                 sym_files.add(parseTitle( file.stem).upper())
        
                        
#     # for file in sym_files:
#     #     print (file)


#     directory = Path( IMAGE_DIRECTORY)

#     # List comprehension to process the files in the directory
#     processed_files = {parseTitle(file.stem) for file in directory.iterdir() if file.is_file()}

#     newfiles = sym_files - processed_files

#     # Print the results
#     for result in newfiles:
#         print (result)
#         #print(result)
#         shkd2 = GuruFilm(name=result, store=True)
#         shkd = MissFilm(name=result, store=True)
#         sssd = JavFilm(name=result, store=True)
#         print ("result newfiles", result)
#         if shkd.content and shkd.get_image_content()[0]:
#             image = shkd.image_content
#             newfile = directory / (result + '.jpg')
#             print (newfile)
#             with open(newfile, 'wb') as f:
#                 f.write(image)
#         elif shkd2.content and shkd2.get_image_content()[0]:
#             image = shkd2.image_content
#             newfile = directory / (result + '.jpg')
#             print (newfile)
#             with open(newfile, 'wb') as f:
#                 f.write(image)
#         else:
#             print (result, 'no image')

