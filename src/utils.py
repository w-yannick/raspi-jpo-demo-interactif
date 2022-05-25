import secrets
import qrcode
import cv2
from PIL import Image

### replace the host name ip by whatever ip the host is using
HOST_NAME = 'xxx.xxx.xxx.xxx'
PORT_NUMBER = 9999
PI_PATH = "public"
EXTENSION = ".jpeg"

def generate_random_string(length=20):
    """Generate a random string of variable length (string is url safe)

    Keyword argument:
    length -- desired length of the string (default 20)
    """
    return secrets.token_urlsafe(length)

def copy_image(path):
    """Internal use only, useless function for application"""
    img = cv2.imread(path)
    cv2.imwrite(f"/home/pi/public/{generate_random_string(20)}.jpg", img)

def generate_QR(filename_no_ext, domain='jpo2019gigl.polymtl.ca', port=PORT_NUMBER):
    """Generate a QR code image for the URL built with server domain and port.

    The image returned is a Pillow image.
    It is currently saved for testing purposes.

    Positional argument:
    filename_no_ext -- image file name (random string), without .jpg extension

    Keyword arguments:
    domain -- server domain (default "jpo2019gigl.polymtl.ca")
    port -- server host (default "9999")
    """
    img = qrcode.make(f"https://{domain}:{port}/{filename_no_ext}")
    img.thumbnail((324, 324), Image.ANTIALIAS)
    img_w, img_h = img.size
    background = Image.new('RGB', (576, 324), (255, 255, 255))
    bg_w, bg_h = background.size
    offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
    background.paste(img, offset)
    return background

