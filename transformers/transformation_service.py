
from models.attendance_models import AttendanceReport
from models.report_types import ReportType
from .type_a_transformation_strategy import TypeATransformationStrategy
from .type_b_transformation_strategy import TypeBTransformationStrategy


class TransformationService:
    def __init__(self):
        self.strategies = {
            ReportType.TYPE_A: TypeATransformationStrategy(),
            ReportType.TYPE_B: TypeBTransformationStrategy(
                regular_hours_limit=8,
                first_overtime_limit=2
            )
        }

    def transform(self, report: AttendanceReport, seed: int = 42) -> AttendanceReport:
        strategy = self.strategies.get(report.report_type)
        if strategy is None:
            raise ValueError(f"סוג דו\"ח לא מוכר: {report.report_type}")

        return strategy.transform(report, seed)