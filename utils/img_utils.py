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
        
def convert_png_to_jpg():
        paths = Path(f"{self.root_app}{os.path.sep}data{os.path.sep}results").glob("**/*.png")
        today = datetime.now()
        for path in paths:
                destination = os.path.splitext(path)[0]+'.jpg'
                image = Image.open(path)  
                print(destination)
                image.save(destination, format="webp")  