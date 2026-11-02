import os
TESSERACT_CMD = os.getenv("TESSERACT_CMD", r"C:\Program Files\Tesseract-OCR\tesseract.exe")
POPPLER_PATH = os.getenv("POPPLER_PATH", r"C:\Library\bin")
FONTS_DIR = os.getenv("FONTS_DIR", r"C:\Windows\Fonts")

ARIAL_FONT_PATH = os.path.join(FONTS_DIR, "arial.ttf")
ARIAL_BOLD_FONT_PATH = os.path.join(FONTS_DIR, "arialbd.ttf")