import os
from PIL import Image
from pathlib import Path

def convert_to_webp(source, ext, rm_source=False, quality=90):                               
                destination = f"{os.path.splitext(source)[0]}.{ext}"
                image = Image.open(source)  
                # print(destination)
                image.save(destination, format="webp", quality=quality)  
                if rm_source:
                    os.remove(source)
                return destination           
        
""" usage :
if (command == "conv"):
    img_utils.convert_dir_to_webp(f"{self.root_app}{os.path.sep}data{os.path.sep}results", rm_source=True)
    exit()
"""
def convert_dir_to_webp(source_path, rm_source=False):
        paths = Path(f"{source_path}").glob("**/*.png")
        for path in paths:
                destination = os.path.splitext(path)[0]+'.jpg'
                image = Image.open(path)  
                print(destination)
                image.save(destination, format="webp")  
                if rm_source:
                    os.remove(path)