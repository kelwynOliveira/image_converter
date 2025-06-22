import io
import re
import unicodedata
import logging

from PIL import Image, UnidentifiedImageError
from fastapi import HTTPException, UploadFile

# Logger
# logger = logging.getLogger("uvicorn")
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger("image_converter")

# Suportted formats
SUPPORTED_FORMATS = {
    "bmp": {"pillow": "BMP", "mime": "image/bmp"},
    "dds": {"pillow": "DDS", "mime": "image/vnd.ms-dds"},
    "eps": {"pillow": "EPS", "mime": "application/postscript"},
    "gif": {"pillow": "GIF", "mime": "image/gif"},
    "ico": {"pillow": "ICO", "mime": "image/vnd.microsoft.icon"},
    "jpg": {"pillow": "JPEG", "mime": "image/jpeg"},
    "jpeg": {"pillow": "JPEG", "mime": "image/jpeg"},
    "jp2": {"pillow": "JPEG2000", "mime": "image/jp2"},
    "jpc": {"pillow": "JPEG2000", "mime": "image/jp2"},
    "png": {"pillow": "PNG", "mime": "image/png"},
    "ppm": {"pillow": "PPM", "mime": "image/x-portable-pixmap"}, 
    "pgm": {"pillow": "PGM", "mime": "image/x-portable-graymap"},
    "pbm": {"pillow": "PBM", "mime": "image/x-portable-bitmap"}, 
    "pcx": {"pillow": "PCX", "mime": "image/x-pcx"},
    "psd": {"pillow": "PSD", "mime": "image/vnd.adobe.photoshop"}, 
    "tiff": {"pillow": "TIFF", "mime": "image/tiff"},
    "tga": {"pillow": "TGA", "mime": "image/x-tga"}, 
    "xbm": {"pillow": "XBM", "mime": "image/x-xbitmap"},
    "xpm": {"pillow": "XPM", "mime": "image/x-xpixmap"},
    "webp": {"pillow": "WEBP", "mime": "image/webp"},
}

# Aux
def get_pillow_format(fmt: str) -> str:
    fmt = fmt.lower()
    data = SUPPORTED_FORMATS.get(fmt)
    if data:
        return data["pillow"]
    return None

def sanitize_filename(filename):
    filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore').decode('ASCII')
    filename = re.sub(r'[^\w\-_\. ]', '_', filename)
    return filename

# Open file - validation
def open_file(file: UploadFile) -> Image.Image:
    try:
        image = Image.open(file.file)
        image.load()
        return image
    except UnidentifiedImageError:
        logger.error(f"Invalid image format: {file.filename}")
        raise HTTPException(status_code=400, detail="Invalid image format or corrupted file.")
    except Exception as e:
        logger.error(f"Error opening the image {file.filename}: {e}")
        raise HTTPException(status_code=400, detail=f"Error opening the image: {e}")


def convert_image(image: Image.Image, output_format: str) -> io.BytesIO:
    output = io.BytesIO()

    output_format_pillow = get_pillow_format(output_format)
    if not output_format_pillow:
        logger.error(f"Output format no supported: {output_format}")
        raise HTTPException(status_code=400, detail=f"Output format not supported: {output_format}")
    
    try:
        image.save(output, format=output_format_pillow)
        output.seek(0)
        return output
    except Exception as e:
        logger.error(f"Error converting to {output_format}: {e}")
        raise HTTPException(status_code=500, detail=f"Error converting: {e}")
