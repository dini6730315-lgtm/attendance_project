from typing import List
from .base_parser import BaseParser
from .type_a_parser import TypeAParser
from .type_b_parser import TypeBParser
import re

def get_parser_for_report(lines: List[str]) -> BaseParser:

    combined_text = " ".join(lines)


    # מנרמלים את הטקסט כדי להתגבר על רווחים מיותרים ב-OCR
    normalized_text = re.sub(r'\s+', '', combined_text)
    normalized_text = normalized_text.replace('"', '')
    print("===== NORMALIZED TEXT =====")
    print(normalized_text)
    print("===========================")
    score_a = 0
    score_b = 0

    # מאפיינים של Type A
    if "סהכימיעבודהלחודש" in normalized_text:
        score_a += 3

    if "שעות100%" in normalized_text:
        score_a += 2

    if "שבת150%" in normalized_text:
        score_a += 5

    # מאפיינים של Type B
    if "125%" in normalized_text:
        score_b += 2

    if "150%" in normalized_text:
        score_b += 2

    if "מקוםעבודה" in normalized_text:
        score_b += 2



    print(f"Type A={score_a}, Type B={score_b}")

    if score_a == score_b:
        raise ValueError(
            f"לא ניתן לזהות בוודאות את סוג הדו\"ח. "
            f"Type A={score_a}, Type B={score_b}"
        )

    if score_b > score_a:
        return TypeBParser()

    return TypeAParser()