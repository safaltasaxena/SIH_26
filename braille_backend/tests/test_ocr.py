import os
import pytesseract
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

tesseract_path = os.getenv("TESSERACT_PATH")

if tesseract_path:
    pytesseract.pytesseract.tesseract_cmd = tesseract_path

image = Image.open("tests/test.png")

text = pytesseract.image_to_string(image)

print(text)