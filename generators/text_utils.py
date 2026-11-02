from bidi.algorithm import get_display
import arabic_reshaper

def fix_hebrew_text(text: str) -> str:
    """תיקון כיווניות (RTL) לתצוגת עברית תקינה ב-PDF"""
    if not isinstance(text, str):
        text = str(text)
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)