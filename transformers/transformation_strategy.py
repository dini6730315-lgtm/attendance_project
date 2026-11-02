# transformers/transformation_strategy.py
from abc import ABC, abstractmethod
import random
from models.attendance_models import AttendanceReport, AttendanceRow


class BaseTransformationStrategy(ABC):
    @abstractmethod
    def transform(self, report: AttendanceReport, seed: int = 42) -> AttendanceReport:
        pass


class StandardTransformationStrategy(BaseTransformationStrategy):
    def transform(self, report: AttendanceReport, seed: int = 42) -> AttendanceReport:
        # שימוש ב-seed להבטחת פלט דטרמיניסטי בהרצות חוזרות
        rng = random.Random(seed)
        new_rows = []

        for row in report.rows:
            # היסט דטרמיניסטי קל בדקות
            shift_minutes = rng.choice([-15, 0, 15, 30])
            entry_h, entry_m = map(int, row.entry.split(':'))
            exit_h, exit_m = map(int, row.exit_time.split(':'))

            original_entry = entry_h * 60 + entry_m
            original_exit = exit_h * 60 + exit_m

            # מניעת מעבר ליום אחר
            if not (
                    0 <= original_entry + shift_minutes < 1440
                    and 0 <= original_exit + shift_minutes < 1440
            ):
                shift_minutes = 0

            # המרת שעת כניסה לדקות מתחילת היום והוספת ההיסט
            entry_h, entry_m = map(int, row.entry.split(':'))
            total_entry_minutes = (entry_h * 60 + entry_m + shift_minutes) % (24 * 60)
            new_entry_h = total_entry_minutes // 60
            new_entry_m = total_entry_minutes % 60
            new_entry = f"{new_entry_h:02d}:{new_entry_m:02d}"

            # המרת שעת יציאה לדקות מתחילת היום והוספת ההיסט
            exit_h, exit_m = map(int, row.exit_time.split(':'))
            total_exit_minutes = (exit_h * 60 + exit_m + shift_minutes) % (24 * 60)
            new_exit_h = total_exit_minutes // 60
            new_exit_m = total_exit_minutes % 60
            new_exit = f"{new_exit_h:02d}:{new_exit_m:02d}"

            # חישוב שעות סה"כ חדש מתוך הזמנים המעודכנים
            entry_decimal = new_entry_h + new_entry_m / 60.0
            exit_decimal = new_exit_h + new_exit_m / 60.0
            dur_hours = exit_decimal - entry_decimal - row.break_hours
            total_h = max(0.0, round(dur_hours, 2))

            new_rows.append(
                AttendanceRow(
                    date=row.date,
                    day=row.day,
                    entry=new_entry,
                    exit_time=new_exit,
                    break_hours=row.break_hours,
                    total_hours=total_h,
                    workplace=row.workplace,
                    h_100=row.h_100,
                    h_125=row.h_125,
                    h_150=row.h_150,
                    shabbat=row.shabbat
                )
            )

        return AttendanceReport(
            company_name=report.company_name,
            employee_name=report.employee_name,
            month=report.month,
            report_type=report.report_type,
            rows=new_rows
        )