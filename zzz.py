import pytesseract

from PIL import Image

obj = pytesseract.image_to_string(Image.open("zzz.png"))


pass
