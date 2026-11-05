
import random

from models.attendance_models import AttendanceReport, AttendanceRow
from .base_transformation_strategy import BaseTransformationStrategy


class TypeATransformationStrategy(BaseTransformationStrategy):

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

            total_h = self.calculate_total(
                new_entry,
                new_exit,
                row.break_hours
            )

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
            rows=tuple(new_rows)        )
