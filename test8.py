from trustmod.vars.env_001 import IDOLSDB_PATH, FILMSOURCES_PATH, SIMLINK_DIRECTORY, IMAGE_DIRECTORY, MEDIA_DIRECTORIES, USER_AGENT_GOOGLE

import os
from pathlib import Path

def main():

    all_files = []
    for directory in MEDIA_DIRECTORIES:
        for root, _, files in os.walk(directory):
            for file in files:
                if Path(file).suffix.lower() in ['.mp4', '.wmv', '.mkv', '.avi']:
                    all_files.append(os.path.join(root, file))

    for root, _, files in os.walk(SIMLINK_DIRECTORY):
        for file in files:
            full_path = os.path.join(root, file)
            if os.path.islink(full_path):
                target = os.readlink(full_path)
                if target in all_files:
                    all_files.remove(target)
                else:
                    print(f"Orphaned symlink: {full_path} -> {target}")

    for file in all_files:
        print(f"File without symlink: {file}")


if __name__ == "__main__":
    videos = set()
    sym_files = set()
    dest = Path(SIMLINK_DIRECTORY)

    for line in MEDIA_DIRECTORIES:
        raw_path = line.strip()
        paths = Path (raw_path)
        for file in paths.iterdir():
            if file.suffix.lower() in ['.mp4', '.wmv', '.mkv', '.avi']:
                videos.add(f"{file.resolve(strict=False)}")
    #print (videos)
    for sym in dest.iterdir():
        if sym.is_symlink():
            src = sym.resolve(strict=False)
            if src.exists():
                sym_files.add (f"{src}")
    #print (sym_files)
    print (videos - sym_files)
    main()
