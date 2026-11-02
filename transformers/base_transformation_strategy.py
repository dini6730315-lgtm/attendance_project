
from abc import ABC, abstractmethod
from datetime import datetime, timedelta

from models.attendance_models import AttendanceReport


class BaseTransformationStrategy(ABC):

    @abstractmethod
    def transform(
        self,
        report: AttendanceReport,
        seed: int = 42
    ) -> AttendanceReport:
        pass

    @staticmethod
    def shift_time(time_str: str, shift_minutes: int) -> str:
        time_obj = datetime.strptime(time_str, "%H:%M")
        new_time = time_obj + timedelta(minutes=shift_minutes)
        return new_time.strftime("%H:%M")

    @staticmethod
    def calculate_total(
        entry: str,
        exit_time: str,
        break_hours: float
    ) -> float:

        entry_time = datetime.strptime(entry, "%H:%M")
        exit_obj = datetime.strptime(exit_time, "%H:%M")

        duration = (
            exit_obj.hour * 60 + exit_obj.minute
            - entry_time.hour * 60 - entry_time.minute
        )

        return round(duration / 60 - break_hours, 2)
