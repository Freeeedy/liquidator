import subprocess
import os
import platform
import datetime

# DOCUMENTS
doc_extensions = [
    "doc", "docx", "dot", "dotx", "odt", "ott",
    "xls", "xlsx", "ods", "csv", "tsv",
    "ppt", "pptx", "odp", "pdf", "rtf"
]

# TEXT / CODE FILES
text_extensions = [
    "txt", "log", "md", "ini", "cfg", "conf",
    "json", "xml", "yaml", "yml", "toml",
    "py", "c", "cpp", "h", "hpp", "js", "html", "css",
    "php", "sh", "bat", "ps1"
]

# IMAGES
image_extensions = [
    "jpg", "jpeg", "png", "tiff", "tif",
    "bmp", "gif", "webp", "heic", "heif", "raw", "cr2", "nef", "orf", "arw"
]

# VIDEO 
video_extensions = [
    "mp4", "m4v", "mov", "avi", "mkv", "wmv",
    "flv", "mpeg", "mpg", "3gp", "webm"
]

# AUDIO
audio_extensions = [
    "mp3", "wav", "flac", "m4a", "aac", "ogg", "opus", "wma",
    "aif", "aiff", "amr"
]

# EBOOKS & PUBLISHING
ebook_extensions = [
    "epub", "mobi", "azw", "fb2", "ibooks"
]

# DESIGN
design_extensions = [
    "psd", "ai", "indd", "idml", "svg", "dwg", "dxf", "blend", "kra", "xcf"
]

file = input("what file would you like to liquidate?\n")

ext = os.path.splitext(file)[1]  # gives you ".txt"
ext = ext.replace('.', '')       # remove the dot
if ext in doc_extensions + image_extensions + design_extensions:
    subprocess.run(f'mat2 --inplace "{file}"', shell=True)
    subprocess.run(f'exiftool -all= -overwrite_original "{file}"', shell=True)
    subprocess.run(f'touch -t 200001010000 "{file}"', shell=True)  

elif ext in text_extensions:
    subprocess.run(f'cp "{file}" newfile.{ext}', shell=True)
    subprocess.run(f'mv newfile.{ext} "{file}"', shell=True)
    subprocess.run(f'touch -t 200001010000 "{file}"', shell=True) 
        
elif ext in video_extensions + audio_extensions:
    subprocess.run(f'ffmpeg -i "{file}" -map_metadata -1 -c:v copy -c:a copy newfile.{ext}', shell=True)
    subprocess.run(f'mv newfile.{ext} "{file}"', shell=True)
    subprocess.run(f'exiftool -all= -overwrite_original "{file}"', shell=True)
    subprocess.run(f'touch -t 200001010000 "{file}"', shell=True) 

elif ext in ebook_extensions:
    subprocess.run(f'mat2 --inplace "{file}"', shell=True)
    subprocess.run(f'ebook-meta "{file}" --delete-metadata', shell=True)
    subprocess.run(f'touch -t 200001010000 "{file}"', shell=True)

else:
    subprocess.run(f'cp "{file}" newfile.{ext}', shell=True)
    subprocess.run(f'mv newfile.{ext} "{file}"', shell=True)
    subprocess.run(f'touch -t 200001010000 "{file}"', shell=True)
