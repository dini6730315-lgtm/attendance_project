
import random

from models.attendance_models import AttendanceReport, AttendanceRow
from .base_transformation_strategy import BaseTransformationStrategy


class TypeBTransformationStrategy(BaseTransformationStrategy):

    def __init__(
        self,
        regular_hours_limit: float,
        first_overtime_limit: float
    ):
        self.regular_hours_limit = regular_hours_limit
        self.first_overtime_limit = first_overtime_limit

    def calculate_overtime(self, total_hours: float):

        h_100 = min(total_hours, self.regular_hours_limit)

        remaining = max(
            0,
            total_hours - self.regular_hours_limit
        )

        h_125 = min(
            remaining,
            self.first_overtime_limit
        )

        h_150 = max(
            0,
            remaining - self.first_overtime_limit
        )

        return h_100, h_125, h_150

    def transform(
        self,
        report: AttendanceReport,
        seed: int = 42
    ) -> AttendanceReport:

        rng = random.Random(seed)
        new_rows = []

        for row in report.rows:

            shift = rng.choice([-15, 0, 15, 30])

            new_entry = self.shift_time(row.entry, shift)
            new_exit = self.shift_time(row.exit_time, shift)

            # בשלב זה ההפסקה נשארת ללא שינוי
            new_break = row.break_hours

            total_h = self.calculate_total(
                new_entry,
                new_exit,
                new_break
            )

            h_100, h_125, h_150 = self.calculate_overtime(total_h)

            new_rows.append(
                AttendanceRow(
                    date=row.date,
                    day=row.day,
                    entry=new_entry,
                    exit_time=new_exit,
                    break_hours=new_break,
                    total_hours=total_h,
                    workplace=row.workplace,
                    h_100=h_100,
                    h_125=h_125,
                    h_150=h_150,
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
