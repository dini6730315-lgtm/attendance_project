
from abc import ABC, abstractmethod
from datetime import time, datetime, timedelta
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
    def shift_time(time_obj: time, shift: int) -> time:
        base_datetime = datetime.combine(datetime.today(), time_obj)
        shifted_datetime = base_datetime + timedelta(minutes=shift)
        return shifted_datetime.time()

    @staticmethod
    def calculate_total(
            entry: time,
            exit_time: time,
            break_hours: float
    ) -> float:
        duration = (
                exit_time.hour * 60 + exit_time.minute
                - entry.hour * 60 - entry.minute
        )

        return round(duration / 60 - break_hours, 2)