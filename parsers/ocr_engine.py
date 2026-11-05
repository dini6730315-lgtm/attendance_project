from typing import List
from pdf2image import convert_from_path
import pytesseract
import re
import config
import os
pytesseract.pytesseract.tesseract_cmd = config.TESSERACT_CMD


def extract_dates_from_image(image):
    width, height = image.size

    date_column = image.crop((
        int(width * 0.78),
        int(height * 0.10),
        int(width * 0.96),
        int(height * 0.90)
    ))

    date_text = pytesseract.image_to_string(
        date_column,
        lang="eng",
        config="--psm 6"
    )

    return re.findall(
        r'\d{1,2}[./]\d{1,2}[./]\d{2,4}',
        date_text
    )

def extract_summary_from_image(image):
    width, height = image.size

    width, height = image.size

    # חיתוך אזור טבלת הנוכחות
    summary_area = image.crop((
        0,
        int(height * 0.08),
        width,
        int(height * 0.90)
    ))
    crop_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "summary_crop_test.png"    )

    print("גודל התמונה:", image.size)
    print("מצב צבע:", image.mode)
    print("נתיב התמונה:", crop_path)

    summary_area.save(crop_path)
    print("הקובץ נשמר כאן:", crop_path)

    summary_text = pytesseract.image_to_string(
        summary_area,
        lang="heb+eng",
        config="--psm 6"
    )

    print("\n===== SUMMARY OCR =====")
    print(summary_text)
    print("=======================\n")

    return summary_text
def extract_times_with_position(image):
    data = pytesseract.image_to_data(
        image,
        lang="heb",
        config="--psm 6",
        output_type=pytesseract.Output.DICT
    )

    results = []

    for i, word in enumerate(data["text"]):
        match = re.search(r'\b\d{1,2}:\d{2}\b', word)

        if match:
            y_position = data["top"][i]
            results.append((y_position, match.group(0)))

    return sorted(results, key=lambda x: x[0])
def extract_text_from_pdf(pdf_filename: str) -> List[str]:

    try:
        images = convert_from_path(
            pdf_filename,
            poppler_path=config.POPPLER_PATH,
            dpi=300
        )

    except Exception as e:
        print(f"שגיאה בהמרת PDF: {e}")
        return []

    all_lines = []

    for image in images:

        # OCR רגיל על כל העמוד
        full_text = pytesseract.image_to_string(
            image,
            lang="heb",
            config="--psm 4"
        )

        page_lines = full_text.splitlines()

        # זיהוי שורות הנוכחות
        row_indexes = []

        for i, line in enumerate(page_lines):

            times = re.findall(
                r'\b\d{1,2}:\d{2}\b',
                line
            )

            # שורת נוכחות מכילה 3 זמנים:
            # כניסה, יציאה והפסקה
            if len(times) >= 3:
                row_indexes.append(i)

        # חילוץ התאריכים בנפרד
        dates = extract_dates_from_image(image)
        summary_text = extract_summary_from_image(image)
        print(
            f"OCR: נמצאו {len(row_indexes)} שורות "
            f"ו-{len(dates)} תאריכים"
        )

        # חיבור התאריכים לשורות
        if len(row_indexes) == len(dates):

            for index, date in zip(row_indexes, dates):
                page_lines[index] += " " + date

        else:
            print(
                "אזהרה: מספר התאריכים אינו תואם "
                "למספר שורות הנוכחות. לא בוצע שיוך אוטומטי."
            )

        all_lines.extend(summary_text.splitlines())
    return all_lines