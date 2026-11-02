from abc import ABC, abstractmethod
from typing import List
from models.attendance_models import AttendanceReport


class BaseParser(ABC):

    @abstractmethod
    def parse(self, lines: List[str]) -> AttendanceReport:
        """מתודת פרסור אבסטרטגית הממומשת בכל מחלקה יורשת"""
        pass

    def calculate_total_hours(self, entry: str, exit_time: str, break_hours: float = 0.0) -> float:
        """לוגיקת חישוב שעות משותפת המונעת כפילות קוד"""
        if not entry or not exit_time:
            return 0.0
        try:
            h1, m1 = map(int, entry.split(':'))
            h2, m2 = map(int, exit_time.split(':'))
            total_minutes = (h2 * 60 + m2) - (h1 * 60 + m1)
            net_hours = (total_minutes / 60.0) - break_hours
            return round(max(0.0, net_hours), 2)
        except Exception:
            return 0.0