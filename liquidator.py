import subprocess
import os
import cv2
import argparse
import uuid
import tempfile
import shutil

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

# Sanity check
if not os.path.isfile(file):
    raise FileNotFoundError(f"{file} not found")

# Split the file extension and remove the dot
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

        # Create a temporary directory to store the converted file
        tmp_dir = tempfile.mkdtemp()

        subprocess.run([
            "libreoffice", "--headless",
            "--convert-to", out_format,
            file, "--outdir",
            tmp_dir], check=True)

        # Get the converted file path
        base_name = os.path.splitext(os.path.basename(file))[0]

        converted_file = os.path.join(tmp_dir, f"{base_name}.{out_format}")

        # Generate a unique filename for the converted file
        uuid_file = f"{uuid.uuid4()}.{out_format}"

        subprocess.run(["mat2", "--inplace", converted_file], check=True)
        subprocess.run(["exiftool", "-PreviewImage=", "-ThumbnailImage=", converted_file], check=True)

        os.rename(converted_file, uuid_file)

        subprocess.run(["touch", "-a", "-m", "-t", "200001010000", uuid_file], check=True)

        os.remove(file)
        shutil.rmtree(tmp_dir)

    elif ext in image_compatabl_with_cv2:
        img = cv2.imread(file)
        if img is None:
            raise ValueError("Failed to load image")

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        face_detect = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

        faces = face_detect.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            # expand the region
            pad = int(0.25 * max(w, h))
            x1 = max(0, x - pad)
            y1 = max(0, y - pad)
            x2 = min(img.shape[1], x + w + pad)
            y2 = min(img.shape[0], y + h + pad)

            roi = img[y1:y2, x1:x2]

            # strong pixelation
            small = cv2.resize(roi, (5 , 5), interpolation=cv2.INTER_LINEAR)
            roi = cv2.resize(small, (x2 - x1, y2 - y1), interpolation=cv2.INTER_NEAREST)

            # optional slight blur to smooth blocks
            roi = cv2.GaussianBlur(roi, (61, 61), 0)

            img[y1:y2, x1:x2] = roi

        print("faces found:", len(faces))
        print(img.shape)
        # Resize the image
        img = cv2.resize(img, None, fx=0.98, fy=0.98)

        if ext == "png":
            ext = "jpg"

        # Generate a unique filename for the new image
        new_file = str(uuid.uuid4()) + f".{ext}"

        # Save the image with appropriate quality settings based on the format
        if ext in ["jpg", "jpeg"]:
            cv2.imwrite(new_file, img, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
        elif ext == "webp":
            cv2.imwrite(new_file, img, [int(cv2.IMWRITE_WEBP_QUALITY), 90])
        else:
            cv2.imwrite(new_file, img)

        # Sanity check
        if not os.path.exists(new_file):
            raise FileNotFoundError(f"Failed to create {new_file}")

        subprocess.run(["mat2", "--inplace", new_file], check=True)
        subprocess.run(["exiftool", "-PreviewImage=", "-ThumbnailImage=", new_file], check=True)

        subprocess.run(["touch", "-a", "-m", "-t", "200001010000", new_file], check=True)

        #os.remove(file)

    elif ext == "pdf":

        new_file = f"{uuid.uuid4()}.pdf"

        subprocess.run([
            "gs",
            "-o", new_file,
            "-sDEVICE=pdfwrite",
            "-dCompatibilityLevel=1.4",
            "-dNOPAUSE",
            "-dBATCH",
            "-dQUIET",
            "-dDetectDuplicateImages=true",
            "-dCompressFonts=true",
            "-dDiscardDocumentStruct=true",
            "-dEmbedAllFonts=true",
            "-dSubsetFonts=true",
            file
        ], check=True)

        subprocess.run(["mat2", "--inplace", new_file], check=True)

        subprocess.run(["touch", "-a", "-m", "-t", "200001010000", new_file], check=True)

        os.remove(file)

    elif ext in video_extensions:
        new_file = f"{uuid.uuid4()}.{ext}"

        subprocess.run([
            "ffmpeg", "-i", file,
            "-map_metadata", "-1",
            "-c:v", "libx264", "-crf", "23",
            "-c:a", "aac",
            new_file
        ], check=True)

        subprocess.run(["exiftool", "-all=", "-overwrite_original", new_file], check=True)
        subprocess.run(["touch", "-a", "-m", "-t", "200001010000", new_file], check=True)

        os.remove(file)

    elif ext in audio_extensions:
        new_file = f"{uuid.uuid4()}.{ext}"

        subprocess.run([
            "ffmpeg", "-i", file,
            "-map_metadata", "-1", "-vn",
            "-c:a", "aac",
            new_file
        ], check=True)

        subprocess.run(["exiftool", "-all=", "-overwrite_original", new_file], check=True)
        subprocess.run(["touch", "-a", "-m", "-t", "200001010000", new_file], check=True)

        os.remove(file)

else:
    if ext in doc_extensions + image_extensions + design_extensions:
        subprocess.run(["mat2", "--inplace", file], check=True)

        # For PDF we only remove metadata but not re-render
        if ext != "pdf":
            subprocess.run(["exiftool", "-all=", "-overwrite_original", file], check=True)
            subprocess.run(["exiftool", "-PreviewImage=", "-ThumbnailImage=", file], check=True)

        subprocess.run(["touch", "-a", "-m", "-t", "200001010000", file], check=True)

    elif ext in text_extensions:
        subprocess.run(["cp", file, f"newfile.{ext}"], check=True)
        subprocess.run(["mv", f"newfile.{ext}", file], check=True)
        subprocess.run(["touch", "-a", "-m", "-t", "200001010000", file], check=True)

    elif ext in video_extensions + audio_extensions:
        subprocess.run([
            "ffmpeg", "-i", file, "-map_metadata", "-1",
            "-c:v", "copy", "-c:a", "copy", f"newfile.{ext}"
        ], check=True)

        subprocess.run(["mv", f"newfile.{ext}", file], check=True)
        subprocess.run(["exiftool", "-all=", "-overwrite_original", file], check=True)
        subprocess.run(["touch", "-a", "-m", "-t", "200001010000", file], check=True)

    elif ext in ebook_extensions:
        subprocess.run(["mat2", "--inplace", file], check=True)
        subprocess.run(["ebook-meta", file, "--delete-metadata"], check=True)
        subprocess.run(["touch", "-a", "-m", "-t", "200001010000", file], check=True)

    else:
        subprocess.run(["cp", file, f"newfile.{ext}"], check=True)
        subprocess.run(["mv", f"newfile.{ext}", file], check=True)
        subprocess.run(["touch", "-a", "-m", "-t", "200001010000", file], check=True)