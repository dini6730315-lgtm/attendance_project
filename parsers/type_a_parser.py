
import re
from typing import List
from datetime import datetime,time
from models.report_types import ReportType
from .base_parser import BaseParser
from models.attendance_models import AttendanceReport, AttendanceRow


class TypeAParser(BaseParser):
    def parse(self, lines: List[str]) -> AttendanceReport:
        report_rows = []
        employee_name = "לא זוהה"
        company_name = "נ.ע. הנשר כח אדם בע\"מ"

        cleaned_lines = self.clean_lines(lines)
        days_list = [
            "שני", "שלישי", "רביעי", "חמישי",
            "שישי", "שבת", "ראשון"
        ]

        seen_dates = set()

        for i, line in enumerate(cleaned_lines):
            if "שם העובד" in line:
                parts = line.split(":")
                if len(parts) > 1 and parts[1].strip():
                    employee_name = parts[1].strip()

            date_str = self.extract_date(line)

            if not date_str:
                continue

            date_parts = re.split(r'[./]', date_str)

            try:
                day_num = int(date_parts[0])
                month_num = int(date_parts[1])
                year_num = int(date_parts[2])

                if year_num < 100:
                    year_num += 2000

                datetime(year_num, month_num, day_num)

            except (ValueError, IndexError):
                continue

            if date_str in seen_dates:
                continue

            # איסוף נתוני השורה הנוכחית והשורות שאחריה
            block_text = line

            hours = self.extract_times(block_text)
            # סך שעות בפורמט כמו 3.50
            if len(hours) < 2:
                continue
            times_in_minutes = []

            for time_str in hours:
                h, m = map(int, time_str.split(":"))
                times_in_minutes.append((h * 60 + m, time_str))

            times_in_minutes.sort()

            entry_time = times_in_minutes[0][1]
            exit_time = times_in_minutes[-1][1]
            entry_time_obj = datetime.strptime(entry_time, "%H:%M").time()
            exit_time_obj = datetime.strptime(exit_time, "%H:%M").time()

            # 3.50 מייצג שלוש וחצי שעות
            entry_h, entry_m = map(int, entry_time.split(":"))
            exit_h, exit_m = map(int, exit_time.split(":"))

            break_h = 0.0

            total_h = self.calculate_total_hours(
                entry_time,
                exit_time,
                break_h
            )

            try:
                date_obj = datetime.strptime(
                    date_str.replace(".", "/"),
                    "%d/%m/%y" if len(date_str.split("/")[-1]) == 2
                    else "%d/%m/%Y"
                )
                day_str = days_list[date_obj.weekday()]
            except ValueError:
                day_str = "לא ידוע"

            report_rows.append(
                AttendanceRow(
                    date=date_str,
                    day=day_str,
                    entry=entry_time_obj,
                    exit_time=exit_time_obj,
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

        return AttendanceReport(
            company_name=company_name,
            employee_name=employee_name,
            month="09/2022",
            report_type=ReportType.TYPE_A,
            rows=tuple(report_rows),
        )
