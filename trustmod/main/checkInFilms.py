from pathlib import Path

from ..vars.env_001 import IDOLSDB_PATH, FILMSOURCES_PATH, SIMLINK_DIRECTORY, IMAGE_DIRECTORY, MEDIA_DIRECTORIES, USER_AGENT_GOOGLE
from ..classes import GuruFilm, JavFilm, MissFilm, Idol
from ..utility import parseTitle

def checkInFilms():
    sym_files = set()
    # Read the file and process each line
    dest = Path(SIMLINK_DIRECTORY)
    for line in MEDIA_DIRECTORIES:

        raw_path = line.strip()
        paths = Path (raw_path)
        suffix = "-" + raw_path.replace(':/', '_') 
        for file in paths.iterdir():
            if file.suffix.lower() in ['.mp4', '.wmv', '.mkv', '.avi']:
                newfile = dest / (parseTitle(file.stem) + suffix + file.suffix)
                if not newfile.exists():
                    newfile.symlink_to(file)
                sym_files.add(parseTitle( file.stem).upper())
                        
    # for file in sym_files:
    #     print (file)


    directory = Path( IMAGE_DIRECTORY)

    # List comprehension to process the files in the directory
    processed_files = {parseTitle(file.stem) for file in directory.iterdir() if file.is_file()}

    newfiles = sym_files - processed_files

    # Print the results
    for result in newfiles:
        print (result)
        #print(result)
        shkd2 = GuruFilm(name=result, store=True)
        shkd = MissFilm(name=result, store=True)
        sssd = JavFilm(name=result, store=True)
        print ("result newfiles", result)
        if shkd.content and shkd.get_image_content()[0]:
            image = shkd.image_content
            newfile = directory / (result + '.jpg')
            print (newfile)
            with open(newfile, 'wb') as f:
                f.write(image)
        elif shkd2.content and shkd2.get_image_content()[0]:
            image = shkd2.image_content
            newfile = directory / (result + '.jpg')
            print (newfile)
            with open(newfile, 'wb') as f:
                f.write(image)
        else:
            print (result, 'no image')

