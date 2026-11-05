# Attendance Report Generator
## מחולל וריאציות לדוחות נוכחות

### 1. תיאור הפרויקט

הפרויקט הוא מערכת Python לעיבוד וליצירה מחדש של דוחות נוכחות מסוג A ו־Type B מתוך קובצי PDF סרוקים.

המערכת מבצעת תהליך עיבוד (Pipeline) הכולל:
1. חילוץ טקסט מקובץ PDF באמצעות OCR.
2. זיהוי סוג הדוח.
3. פענוח הנתונים למבנה נתונים אחיד.
4. בדיקת תקינות הנתונים (Invariants).
5. שינוי נתוני הדוח באמצעות אסטרטגיה מתאימה.
6. יצירת קובץ PDF חדש.

המערכת בנויה בצורה מודולרית ואובייקט־אוריינטטיבית, תוך הפרדה בין שלבי העיבוד השונים.

---

### 2. מבנה הפרויקט

```text
attendance_project/
│
├── main.py
├── config.py
│
├── models/
│   └── attendance_models.py
│
├── parsers/
│   ├── base_parser.py
│   ├── type_a_parser.py
│   ├── type_b_parser.py
│   ├── parser_factory.py
│   └── ocr_engine.py
│
├── transformers/
│   ├── invariants.py
│   ├── base_transformation_strategy.py
│   ├── type_a_transformation_strategy.py
│   ├── type_b_transformation_strategy.py
│   └── transformation_service.py
│
├── generators/
│   ├── ...
│
└── tests/
    └── ...
```

---

### 3. ארכיטקטורת המערכת

#### Domain – מודלי הנתונים

הקובץ `models/attendance_models.py` מכיל את מודלי הנתונים המרכזיים:

- `AttendanceRow` – מייצג שורת נוכחות בודדת.
- `AttendanceReport` – מייצג דוח נוכחות שלם.

המודלים מנותקים מתהליך חילוץ הנתונים ומאופן יצירת קובץ הפלט.

`AttendanceRow` מוגדרת כ־frozen dataclass, כדי למנוע שינוי ישיר של שדות השורה לאחר יצירתה.

#### Parsing – חילוץ ופענוח

אחראי על קריאת קובצי ה־PDF והפיכת המידע הגולמי לנתונים מובנים.

- `ocr_engine.py` – מבצע המרת PDF לתמונה וחילוץ טקסט באמצעות Tesseract OCR.
- `BaseParser` – מחלקת בסיס המגדירה את ממשק הפענוח.
- `TypeAParser` – מפענח דוחות מסוג A.
- `TypeBParser` – מפענח דוחות מסוג B.
- `get_parser_for_report()` – פונקציית Factory המזהה את סוג הדוח ומחזירה את ה־Parser המתאים.

#### Transformation – שינוי הנתונים

אחראי על יצירת וריאציה חדשה של הדוח.

- `BaseTransformationStrategy` – מגדירה את ממשק אסטרטגיות השינוי.
- `TypeATransformationStrategy` – אסטרטגיית שינוי לדוחות מסוג A.
- `TypeBTransformationStrategy` – אסטרטגיית שינוי לדוחות מסוג B.
- `TransformationService` – בוחרת ומפעילה את אסטרטגיית השינוי בהתאם לסוג הדוח.
- `invariants.py` – מכיל פונקציות לבדיקת תקינות הנתונים ולחישוב שעות עבודה.

#### Generation – יצירת הדוח

אחראי על הפקת קובץ PDF חדש מתוך אובייקט `AttendanceReport`.

הגנרטור מקבל את אובייקט הדוח ואינו תלוי במימוש של שלב ה־Parsing או ב־OCR.

הפקת ה־PDF מתבצעת באמצעות `fpdf2`, עם תמיכה בעיבוד טקסט בעברית באמצעות `python-bidi` ו־`arabic-reshaper`.

---

### 4. דרישות מערכת

- Python 3.10 ומעלה.
- Tesseract OCR.
- Poppler.
- גופני Arial ו־Arial Bold.

#### התקנת ספריות Python

יש להריץ בטרמינל:

```bash
pip install pdf2image pytesseract fpdf2 python-bidi arabic-reshaper
```

אם הפרויקט משתמש גם בספריות נוספות, יש להתקינן בהתאם לייבואים בקוד.

#### התקנת רכיבים חיצוניים

**Tesseract OCR**

יש להתקין את Tesseract ולוודא שחבילת השפה העברית (`heb`) מותקנת.

**Poppler**

נדרש לצורך המרת קובצי PDF לתמונות באמצעות `pdf2image`.

**גופנים**

יש לוודא שקובצי Arial ו־Arial Bold זמינים במחשב.

---

### 5. הגדרת נתיבים ומשתני סביבה

הנתיבים לרכיבים החיצוניים מנוהלים בקובץ `config.py`.

הקובץ משתמש ב־`os.getenv` כדי לאפשר הגדרת נתיבים באמצעות משתני סביבה, במקום לפזר אותם בקבצי הפרויקט.

המשתנים הנתמכים:

| משתנה | תפקיד |
|---|---|
| `TESSERACT_CMD` | נתיב לקובץ ההפעלה של Tesseract |
| `POPPLER