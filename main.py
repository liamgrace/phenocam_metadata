import sys, os, shutil
from pathlib import Path
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS

#Convert C6.3 series Phenocam images from sequentially numbered files in the directory to timestamp titled
if __name__ == '__main__':
    input_path = Path(sys.argv[1])
    output_path = input_path / 'converted'
    output_path.mkdir(exist_ok=True)
    with os.scandir(input_path) as dir_entries:
        for entry in dir_entries:
            if entry.name.endswith('.JPG'):
                image = Image.open(input_path / entry.name)
                exif = {
                    TAGS[k]: v
                    for k, v in image._getexif().items()
                    if k in TAGS
                }
                dt = datetime.strptime(exif['DateTime'],'%Y:%m:%d %H:%M:%S').strftime('%Y-%m-%dT%H%M') + '00'
                shutil.copyfile(input_path / entry.name,output_path / (dt + '.JPG'))
                print("Converted {0} to {1}".format(input_path / entry.name, output_path / (dt + '.JPG')))
