# Liquidator

Liquidator is a lightweight Python (Linux-only) tool to **sanitize files by removing metadata, resetting timestamps, and re-encoding content for privacy purposes**. It supports documents, images, videos, audio, eBooks, and design files using tools like `mat2`, `exiftool`, `ffmpeg`, `libreoffice`, `ghostscript`, and `mediapipe`.

---

## Features

- Remove metadata from files using multiple sanitization layers
- Reset file timestamps to a fixed historical value
- Re-encode media to strip hidden data
- Optional **Paranoid Mode** for deeper file rewriting and obfuscation
- **Face detection and automatic pixelation (privacy protection)**
- Supports documents, images, videos, audio, eBooks, and design files
- Automatic handling based on file type

---

## Modes

### Normal Mode (default)

A lightweight sanitization mode that:
- Removes metadata using `mat2`
- Clears EXIF data with `exiftool`
- Resets timestamps
- Keeps file structure mostly intact
- Minimal modification to content

Best for:
- Quick metadata cleanup
- Non-sensitive use cases
- Preserving original file fidelity

---

### Paranoid Mode (`-p` / `--paranoid`)

Paranoid mode performs **deep sanitization and file rewriting**, including re-encoding and regeneration of files to reduce forensic recoverability.

Enable it:

```bash
python3 liquidator.py -f file.ext -p
```

---

## What Paranoid Mode does

### Documents (doc, docx, xls, xlsx, ppt, pptx)
- Re-rendered via LibreOffice headless conversion
- Stored temporarily
- Metadata removed (`mat2`, `exiftool`)
- Renamed using UUID
- Timestamp reset
- Original file deleted

### Images
- **Face detection using MediaPipe**
- **Automatic face pixelation with optional blur smoothing**
- Bounding box expansion to avoid partial face leaks
- Resized to 98% to break exact binary similarity
- Re-encoded via OpenCV
- Optional format normalization (e.g. PNG → JPG)
- Metadata stripped
- UUID filename
- Original optionally removed

### PDF
- Rewritten using Ghostscript
- Fonts embedded, structure rebuilt
- Metadata removed
- Timestamp reset
- Original deleted

### Video
- Re-encoded (H.264 + AAC)
- Metadata stripped
- EXIF removed
- Timestamp reset
- Original deleted

### Audio
- Re-encoded (AAC)
- Metadata removed
- Timestamp reset
- Original deleted

---


## Supported File Types

### Documents
doc, docx, dot, dotx, odt, ott,  
xls, xlsx, ods, csv, tsv,  
ppt, pptx, odp, pdf, rtf  

### Text / Code
txt, log, md, ini, cfg, conf,  
json, xml, yaml, yml, toml,  
py, c, cpp, h, hpp, js, html, css,  
php, sh, bat, ps1  

### Images
jpg, jpeg, png, tiff, tif,  
bmp, gif, webp, heic, heif,  
raw, cr2, nef, orf, arw  

### Video
mp4, m4v, mov, avi, mkv, wmv,  
flv, mpeg, mpg, 3gp, webm  

### Audio
mp3, wav, flac, m4a, aac, ogg,  
opus, wma, aif, aiff, amr  

### eBooks
epub, mobi, azw, fb2, ibooks  

### Design Files
psd, ai, indd, idml, svg, dwg,  
dxf, blend, kra, xcf  

---

## Installation

```
git clone https://github.com/yourusername/liquidator.git
cd liquidator
chmod +x install.sh
./install.sh
```

---

## Usage

Normal mode:
```
python3 liquidator.py -f file.ext
```

Paranoid mode:
```
python3 liquidator.py -f file.ext -p
```

---

## Requirements

- Python 3
- mat2
- exiftool
- ffmpeg
- libreoffice
- ghostscript
- mediapipe
- opencv-python

---

## Notes

- Paranoid mode is destructive (original files removed)
- Prioritizes privacy over fidelity
- Face pixelation only applies to supported image formats (OpenCV-compatible)
- Linux only
