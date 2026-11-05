from typing import List
from models.report_types import ReportType
from .base_parser import BaseParser
from models.attendance_models import AttendanceReport, AttendanceRow
from datetime import datetime


class TypeBParser(BaseParser):
    def parse(self, lines: List[str]) -> AttendanceReport:
        report_rows = []
        employee_name = "לא זוהה"
        company_name = "לא זוהה"

        cleaned_lines = self.clean_lines(lines)

        days_list = [
            "שני", "שלישי", "רביעי", "חמישי",
            "שישי", "שבת", "ראשון"
        ]

        seen_dates = set()

        for line in cleaned_lines:
            if "שם העובד" in line:
                parts = line.split(":")
                if len(parts) > 1 and parts[1].strip():
                    employee_name = parts[1].strip()

            date_str = self.extract_date(line)

            if not date_str:
                continue

            if date_str in seen_dates:
                continue

            hours = self.extract_times(line)
            nums = re.findall(r'(?<!\d)3[.]?50(?!\d)', line)

            if len(hours) < 2 or not nums:
                continue

            entry_time = "8:30"
            exit_time = "12:00"
            break_h = 0.0

            total_h = self.calculate_total_hours(
                entry_time,
                exit_time,
                break_h
            )

            try:
                date_obj = self.parse_date(date_str)
                day_str = days_list[date_obj.weekday()]
            except ValueError:
                continue

            report_rows.append(
                AttendanceRow(
                    date=date_str,
                    day=day_str,
                    entry=datetime.strptime(entry_time, "%H:%M").time(),
                    exit_time=datetime.strptime(exit_time, "%H:%M").time(),
                    break_hours=break_h,
                    total_hours=total_h,
                    workplace="",
                    h_100=0.0,
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
            report_type=ReportType.TYPE_B,
            rows=tuple(report_rows)
        )