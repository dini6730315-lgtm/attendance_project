import os

TESSERACT_CMD = os.getenv("TESSERACT_CMD", "tesseract")
POPPLER_PATH = os.getenv("POPPLER_PATH") or None
FONTS_DIR = os.getenv("FONTS_DIR")

if not FONTS_DIR:
    raise EnvironmentError("יש להגדיר את משתנה הסביבה FONTS_DIR")

ARIAL_FONT_PATH = os.path.join(FONTS_DIR, "arial.ttf")
ARIAL_BOLD_FONT_PATH = os.path.join(FONTS_DIR, "arialbd.ttf")