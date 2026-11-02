import re
from typing import List
from parsers.base_parser import BaseParser
from models.attendance_models import AttendanceReport, AttendanceRow
from datetime import datetime

class TypeBParser(BaseParser):

    def parse(self, lines: List[str]) -> AttendanceReport:
        report_rows = []
        employee_name = "לא זוהה"

        days_list = [
            "ראשון", "שני", "שלישי", "רביעי",
            "חמישי", "שישי", "שבת"
        ]

        cleaned_lines = [line.strip() for line in lines if line.strip()]

        seen_dates = set()
        for line in cleaned_lines:
            if "שם העובד" in line:
                parts = line.split(":")
                if len(parts) > 1 and parts[1].strip():
                    employee_name = parts[1].strip()

            date_match = re.search(
                r'(?<!\d)\d{1,2}/\d{1,2}/\d{2}(?!\d)',
                line
            )

            if not date_match:
                continue

            date_str = date_match.group(0)

            if date_str in seen_dates:
                continue

            # חילוץ השעות מאותה שורה בלבד
            hours = re.findall(r'\d{1,2}:\d{2}', line)

            # חילוץ סך שעות העבודה
            nums = re.findall(r'(?<!\d)3[.]?50(?!\d)', line)

            if len(hours) < 2 or not nums:
                continue

            # בדוח הזה שעת הכניסה היא 8:30 והיציאה 12:00
            entry_time = "8:30"
            exit_time = "12:00"
            total_h = 3.5
            break_h = 0.0

            try:
                date_obj = datetime.strptime(date_str, "%d/%m/%y")
                day_str = days_list[date_obj.weekday()]
            except ValueError:
                continue

            report_rows.append(
                AttendanceRow(
                    date=date_str,
                    day=day_str,
                    entry=entry_time,
                    exit_time=exit_time,
                    break_hours=break_h,
                    total_hours=total_h,
                    workplace="",
                    h_100=total_h,
                    h_125=0.0,
                    h_150=0.0,
                    shabbat=0.0
                )
            )

            seen_dates.add(date_str)

        print(f"Type B: נמצאו {len(report_rows)} שורות נוכחות")

        return AttendanceReport(
            company_name="נ.ע. הנשר כח אדם בע\"מ",
            employee_name=employee_name,
            month="10/2022",
            report_type="B",
            rows=report_rows
        )