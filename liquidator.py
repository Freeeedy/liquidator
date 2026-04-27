import subprocess
import os
import cv2
import argparse
import uuid
import tempfile

# DOCUMENTS
doc_extensions = [
    "doc", "docx", "dot", "dotx", "odt", "ott",
    "xls", "xlsx", "ods", "csv", "tsv",
    "ppt", "pptx", "odp", "pdf", "rtf"
]

doc_for_re_rerendering = ["doc", "docx", "xls", "xlsx", "ppt", "pptx"]

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

image_compatabl_with_cv2 = [
    "jpg", "jpeg", "png", "bmp", "tiff", "tif", "webp"
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

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", required=True, help="the file you want to liquidate")
parser.add_argument("-p", "--paranoid", action="store_true", help="Enable paranoid mode")

args = parser.parse_args()

file = args.file

if not os.path.isfile(file):
    raise FileNotFoundError(f"{file} not found")

ext = os.path.splitext(file)[1]
ext = ext.replace('.', '')

if args.paranoid:
    print(f"Processing {file} with extension {ext} in paranoid mode...")

    if ext in doc_for_re_rerendering:

        if ext in ["doc", "docx"]:
            out_format = "docx"

        elif ext in ["xls", "xlsx"]:
            out_format = "xlsx"

        elif ext in ["ppt", "pptx"]:
            out_format = "pptx"

        tmp_dir = tempfile.mkdtemp()

        subprocess.run([
            "libreoffice",
            "--headless",
            "--convert-to",
            out_format,
            file,
            "--outdir",
            tmp_dir
        ], check=True)

        base_name = os.path.splitext(os.path.basename(file))[0]
        converted_file = os.path.join(tmp_dir, f"{base_name}.{out_format}")

        uuid_file = f"{uuid.uuid4()}.{out_format}"

        subprocess.run(["mat2", "--inplace", converted_file], check=True)

        os.rename(converted_file, uuid_file)

        os.remove(file)

    if ext in image_compatabl_with_cv2:
        img = cv2.imread(file)
        if img is None:
            raise ValueError("Failed to load image")

        img = cv2.resize(img, None, fx=0.98, fy=0.98)

        if ext == "png":
            ext = "jpg"

        new_file = str(uuid.uuid4()) + f".{ext}"

        # encode
        if ext in ["jpg", "jpeg"]:
            cv2.imwrite(new_file, img, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
        elif ext == "webp":
            cv2.imwrite(new_file, img, [int(cv2.IMWRITE_WEBP_QUALITY), 90])
        else:
            cv2.imwrite(new_file, img)

        if not os.path.exists(new_file):
            raise FileNotFoundError(f"Failed to create {new_file}")

        subprocess.run(["mat2", "--inplace", new_file], check=True)

        os.remove(file)
else:
    if ext in doc_extensions + image_extensions + design_extensions:
        subprocess.run(["mat2", "--inplace", file], check=True)

        if ext != "pdf":
            subprocess.run(["exiftool", "-all=", "-overwrite_original", file], check=True)

        subprocess.run(["touch", "-t", "200001010000", file], check=True)

    elif ext in text_extensions:
        subprocess.run(["cp", file, f"newfile.{ext}"], check=True)
        subprocess.run(["mv", f"newfile.{ext}", file], check=True)
        subprocess.run(["touch", "-t", "200001010000", file], check=True)

    elif ext in video_extensions + audio_extensions:
        subprocess.run([
            "ffmpeg", "-i", file, "-map_metadata", "-1",
            "-c:v", "copy", "-c:a", "copy", f"newfile.{ext}"
        ], check=True)

        subprocess.run(["mv", f"newfile.{ext}", file], check=True)
        subprocess.run(["exiftool", "-all=", "-overwrite_original", file], check=True)
        subprocess.run(["touch", "-t", "200001010000", file], check=True)

    elif ext in ebook_extensions:
        subprocess.run(["mat2", "--inplace", file], check=True)
        subprocess.run(["ebook-meta", file, "--delete-metadata"], check=True)
        subprocess.run(["touch", "-t", "200001010000", file], check=True)

    else:
        subprocess.run(["cp", file, f"newfile.{ext}"], check=True)
        subprocess.run(["mv", f"newfile.{ext}", file], check=True)
        subprocess.run(["touch", "-t", "200001010000", file], check=True)