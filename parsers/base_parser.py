
from abc import ABC, abstractmethod
from typing import List
from models.attendance_models import AttendanceReport
import re
from datetime import datetime


class BaseParser(ABC):

    @abstractmethod
    def parse(self, lines: List[str]) -> AttendanceReport:
        """מתודת פרסור אבסטרקטית הממומשת בכל מחלקה יורשת"""
        pass

    def clean_lines(self, lines: List[str]) -> List[str]:
        return [line.strip() for line in lines if line.strip()]

    def extract_date(self, line: str):
        match = re.search(
            r'(?<!\d)\d{1,2}[./]\d{1,2}[./]\d{2,4}(?!\d)',
            line
        )
        return match.group(0) if match else None

    def extract_times(self, line: str) -> List[str]:
        return re.findall(r'\d{1,2}:\d{2}', line)

    def parse_date(self, date_str: str) -> datetime:
        for fmt in ("%d/%m/%Y", "%d/%m/%y",
                    "%d.%m.%Y", "%d.%m.%y"):
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        raise ValueError(f"תאריך לא תקין: {date_str}")

    def calculate_total_hours(
        self,
        entry: str,
        exit_time: str,
        break_hours: float = 0.0
    ) -> float:
        if not entry or not exit_time:
            return 0.0
        try:
            h1, m1 = map(int, entry.split(':'))
            h2, m2 = map(int, exit_time.split(':'))
            total_minutes = (h2 * 60 + m2) - (h1 * 60 + m1)
            net_hours = (total_minutes / 60.0) - break_hours
            return round(max(0.0, net_hours), 2)
        except (ValueError, TypeError):
            return 0.0
