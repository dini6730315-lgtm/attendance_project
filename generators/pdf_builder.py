from fpdf import FPDF
from fpdf.enums import XPos, YPos
import config
from models.attendance_models import AttendanceReport
from .text_utils import fix_hebrew_text

class AttendanceReportPDF(FPDF):
    def __init__(self, report_type: str):
        super().__init__()
        self.report_type = report_type

    def header(self):
        self.set_font("HebrewFont", "B", 13)
        title = fix_hebrew_text(f"Attendance Report - Type {self.report_type}")
        self.cell(0, 8, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        self.ln(3)

def generate_report_pdf(report: AttendanceReport, output_pdf_path: str = "attendance_output.pdf"):
    pdf = AttendanceReportPDF(report.report_type)

    pdf.add_font("HebrewFont", "", config.ARIAL_FONT_PATH)
    pdf.add_font("HebrewFont", "B", config.ARIAL_BOLD_FONT_PATH)

    pdf.add_page()

    # פרטי עובד וכותרת
    pdf.set_font("HebrewFont", "B", 10)
    pdf.cell(0, 6, fix_hebrew_text(f"שם העובד: {report.employee_name}"), new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="R")
    pdf.ln(3)

    # כותרות הטבלה
    headers = ["DATE", "DAY", "LOCATION", "ENTRY", "EXIT", "BREAK", "TOTAL", "100%", "125%", "150%"]
    col_widths = [20, 18, 18, 18, 18, 16, 16, 16, 16, 16]

    pdf.set_font("HebrewFont", "B", 8)
    for i, h in enumerate(headers):
        pdf.cell(col_widths[i], 7, fix_hebrew_text(h), border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align="C")
    pdf.ln()

    # מדפיס את כל השורות מתוך אובייקט הדו"ח
    pdf.set_font("HebrewFont", size=8)
    total_hours = 0.0
    for r in report.rows:
        total_hours += r.total_hours
        row_data = [
            r.date,
            r.day,
            r.workplace,
            r.entry.strftime("%H:%M"),
            r.exit_time.strftime("%H:%M"),
            f"{r.break_hours:.2f}",
            f"{r.total_hours:.2f}",
            f"{r.h_100:.2f}",
            f"{r.h_125:.2f}",
            f"{r.h_150:.2f}"
        ]

        for i, val in enumerate(row_data):
            pdf.cell(col_widths[i], 6, fix_hebrew_text(str(val)), border=1, new_x=XPos.RIGHT, new_y=YPos.TOP, align="C")
        pdf.ln()

    # בלוק סיכום נתונים
    pdf.ln(6)
    pdf.set_font("HebrewFont", "B", 10)
    pdf.cell(0, 6, fix_hebrew_text(":Summary"), new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="L")
    pdf.set_font("HebrewFont", "", 9)
    pdf.cell(0, 5, fix_hebrew_text(f"Total Days: {len(report.rows)}"), new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="L")
    pdf.cell(0, 5, fix_hebrew_text(f"Total Hours: {total_hours:.2f}"), new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="L")
    pdf.cell(0, 5, fix_hebrew_text(f"Hours: {total_hours:.2f} 100%"), new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="L")

    pdf.output(output_pdf_path)
    print(f"הקובץ נוצר בהצלחה: {output_pdf_path}")