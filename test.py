from PIL import Image
import pytesseract

path = './images/asdasd.png'

print(pytesseract.image_to_string(Image.open(path)))