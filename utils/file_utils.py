import os, shutil
import time

def clean_dir(dir_to_clean):                        
                
    for filename in os.listdir(dir_to_clean):
            file_path = os.path.join(dir_to_clean, filename)
            try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                            os.unlink(file_path)
                    elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
            except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))

"""
efface un dossier et tout ce qu'il contient
"""
def rmrf(dir_to_clean):
    shutil.rmtree(dir_to_clean)

"""
 delete empty dirs recursively
"""
def delete_empty_folders_recurs(directory):    
    for dirpath, dirnames, filenames in os.walk(directory, topdown=False):
        for dirname in dirnames:
            folder_path = os.path.join(dirpath, dirname)
            if not os.listdir(folder_path):
                try:
                    os.rmdir(folder_path)
                    print(f"Empty folder deleted: {folder_path}")
                except Exception as e:
                    print(e)                                                
                    input("planté ! press any key")
    


def remove_old_files(dir_path, ptime, unit="d"):
    all_files = os.listdir(dir_path)
    now = time.time()
    if unit=="d":        
        ltime = ptime * 86400
    if unit=="h":        
        ltime = ptime * 3600
    if unit=="m":        
        ltime = ptime * 60
    for f in all_files:
        file_path = os.path.join(dir_path, f)
        if not os.path.isfile(file_path):
            continue
        if os.stat(file_path).st_mtime < now - ltime:
            os.remove(file_path)
            print("Deleted ", f)

def str_to_textfile (filename, str_to_write):
    text_file = open(filename, "w")
    text_file.write(str_to_write)
    text_file.close()