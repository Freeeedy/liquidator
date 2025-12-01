# Liquidator

Liquidator is a lightweight Python tool to **sanitize files** by removing metadata, resetting timestamps, and ensuring privacy for documents, images, videos, audio files, eBooks, and design files. It leverages `mat2`, `exiftool`, and `ffmpeg` to clean files while keeping the original content intact.

## Features

- Remove metadata from documents, images, design files, and eBooks.
- Strip metadata from videos and audio files.
- Reset file timestamps to a default date.
- Automatically handles various file types (documents, images, videos, audio, text, eBooks, design files).

## Supported File Types

- **Documents:** doc, docx, dot, dotx, odt, ott, xls, xlsx, ods, csv, tsv, ppt, pptx, odp, pdf, rtf
- **Text/Code Files:** txt, log, md, ini, cfg, conf, json, xml, yaml, yml, toml, py, c, cpp, h, hpp, js, html, css, php, sh, bat, ps1
- **Images:** jpg, jpeg, png, tiff, tif, bmp, gif, webp, heic, heif, raw, cr2, nef, orf, arw
- **Video:** mp4, m4v, mov, avi, mkv, wmv, flv, mpeg, mpg, 3gp, webm
- **Audio:** mp3, wav, flac, m4a, aac, ogg, opus, wma, aif, aiff, amr
- **eBooks:** epub, mobi, azw, fb2, ibooks
- **Design Files:** psd, ai, indd, idml, svg, dwg, dxf, blend, kra, xcf

## Installation

1. Clone the repository:
```
git clone https://github.com/yourusername/liquidator.git
cd liquidator
```
2. Run the install script:
```
chmod +x install.sh
./install.sh
```
3. Run the tool:
```
python3 liquidator.py
```
You will be prompted to enter the path of the file you want to liquidate. The tool will handle it automatically based on its type.