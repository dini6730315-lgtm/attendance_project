מערכת זו היא צינור עיבוד (Pipeline) מודולרי, דטרמיניסטי ואובייקט־אוריינטטיבי המיועד לאוטומציה של קליטה, פרסור, אימות אינווריאנטים וגנרוט מחדש של דוחות נוכחות (סוג A וסוג B) מתוך קבצי PDF סרוקים, תוך שמירה מלאה על תקני עברית (RTL).

מבנה הפרויקט
BaseParser – מחלקת בסיס אבסטרקטית המגדירה את ממשק הפרסור ואת הלוגיקה המשותפת (כגון חישוב שעות נטו).

TypeAParser / TypeBParser – מחלקות יורשות המממשות את הפרסור הספציפי לכל סוג דוח.

get_parser_for_report() – פונקציית מפעל (Factory) לבחירה פולימורפית של הפרסר המתאים.

AttendanceReport / AttendanceRow – מודלי נתונים (dataclass) המנתקים לחלוטין בין שלב הקליטה לשלב הגנרוט.

גנרטור PDF מבוסס fpdf2 עם תמיכה מלאה ב־python-bidi ו־arabic-reshaper.

דרישות מערכת והתקנה
Python 3.10+ (מומלץ Python 3.14).

התקנת החבילות הנדרשות באמצעות הטרמינל:

Bash
pip install pandas pytesseract pdf2image fpdf2 python-bidi arabic-reshaper openpyxl
התקנת רכיבים חיצוניים:

Tesseract-OCR: יש לוודא התקנה במחשב (ברירת מחדל בקוד: C:\Program Files\Tesseract-OCR\tesseract.exe) עם חבילת שפה עברית (heb).

Poppler: נדרש עבור pdf2image (ברירת מחדל בקוד: C:\Library\bin).

גופנים: יש לוודא זמינות גופני Arial ו־Arial Bold בתיקיית המערכת (C:\Windows\Fonts).

הפעלת הצינור (Pipeline)
להלן דוגמה להרצת הצינור המלא מקצה לקצה מתוך סביבת פייתון:

Python
from your_module import get_parser_for_report, parse_pdf_to_raw_lines, identify_report_type, generate_report_pdf

# 1. טעינת קובץ המקור וביצוע OCR גולמי
pdf_path = 'n_r_5_n.pdf'
raw_lines = parse_pdf_to_raw_lines(pdf_path)

# 2. בחירת הפרסר המתאים באופן דינמי (ללא תנאי if type)
parser = get_parser_for_report(raw_lines)

# 3. פרסור הנתונים לאובייקט מובנה (AttendanceReport)
report_obj = parser.parse(raw_lines)

# 4. גנרוט קובץ PDF חדש ונקי התואם למקור
generate_report_pdf(report_obj, output_pdf_path="attendance_report_output.pdf")
יומן החלטות ארכיטקטוניות (Decision Log)
מעבר מ־WeasyPrint ל־fpdf2 לגנרוט PDF:

הבעיה: WeasyPrint דרשה ספריות מערכת חיצוניות (כגון Pango/GObject) שעוררו שגיאות סביבה והתקנה מורכבות.

ההחלטה: מעבר לספריית fpdf2 בשילוב python-bidi ו־arabic-reshaper.

הנימוק: מאפשר פתרון נקי, יציב ותלוי־פייתון בלבד, תוך הבטחת הפרדה ארכיטקטונית מושלמת שבה פונקציית הגנרוט מקבלת אך ורק את אובייקט הדו"ח ואינה תלויה כלל בלוגיקת ה־OCR.

יישום ארכיטקטורה אובייקט־אוריינטטיבית (Polymorphism):

ההחלטה: יצירת BaseParser ממנו יורשים TypeAParser ו־TypeBParser, בשילוב פונקציית Factory.

הנימוק: מניעת כפילות קוד (DRY), סילוק תנאי if type מיותרים, והקלה על הרחבת המערכת לתמיכה בסוגי דוחות נוספים בעתיד.

דטרמיניזם ואימות אינווריאנטים:

ההחלטה: שימוש ב־random.seed(42) ובדיקות אימות לחתימות MD5 של אובייקטי הדו"ח בין הרצות עוקבות.

הנימוק: הבטחת תוצאות עקביות, דטרמיניסטיות לחלוטין וחפות מהפתעות בכל הרצה של הצינור.