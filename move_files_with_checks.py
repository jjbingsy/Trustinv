from pathlib import Path
import shutil
import math

from trustmod.vars.env_001 import SIMLINK_DIRECTORY as SDD, DESTIN_FILES as DF


#DESTIN_FILES = "E:/destin_temp"
DESTIN_FILES = Path(DF)
SIMLINK_DIRECTORY = Path(SDD)


print(f"SIMLINK_DIRECTORY: {DESTIN_FILES} {SIMLINK_DIRECTORY}")

def move_file_with_check(src_path: Path, dst_path: Path) -> bool:
    # Create destination directory if not exist
    dst_path.parent.mkdir(parents=True, exist_ok=True)

    # Check if file already exists at destination
    if dst_path.is_file():
        base = dst_path.stem
        ext = dst_path.suffix
        counter = 1
        while dst_path.is_file():
            # Generate new path with counter suffix
            dst_path = dst_path.with_name(f'{base}_{counter}{ext}')
            counter += 1

    # Copy file to destination
    shutil.copy2(src_path, dst_path)

    # Verify the files are the same
    if src_path.stat().st_size == dst_path.stat().st_size:
        # If files are the same, delete original file
        src_path.unlink()
        print(f'Moved: {src_path} --> {dst_path}')
        return True
    else:
        print(f'Failed to move: {src_path} --> {dst_path}')
        return False



def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 5)
    return f'{s} {size_name[i]}'


def process_files(prefix_to_move):
    for simlink in SIMLINK_DIRECTORY.iterdir():
        if simlink.is_symlink() and simlink.name.startswith(prefix_to_move):
            src = simlink.resolve(strict=False)  # get the source file of the simlink
            dst = DESTIN_FILES / src.name
            src_size = src.stat().st_size
            print(f"{simlink} moving {src} {convert_size(src_size) } {src_size} to {dst}")
            # if move_file_with_check(src, dst):
            #     simlink.unlink()
            #     if dst.is_file():
            #         print(f"Created {dst}")




process_files("ADN-348")
