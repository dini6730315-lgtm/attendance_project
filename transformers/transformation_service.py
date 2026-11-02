
from models.attendance_models import AttendanceReport

from .type_a_transformation_strategy import TypeATransformationStrategy
from .type_b_transformation_strategy import TypeBTransformationStrategy


class TransformationService:

    def __init__(self, type_b_strategy):

        self.strategies = {
            "A": TypeATransformationStrategy(),
            "TYPE_A": TypeATransformationStrategy(),
            "B": type_b_strategy,
            "TYPE_B": type_b_strategy
        }

    def transform(
        self,
        report: AttendanceReport,
        seed: int = 42
    ) -> AttendanceReport:

        strategy = self.strategies.get(report.report_type.upper())

        if strategy is None:
            raise ValueError(
                f"סוג דו\"ח לא מוכר: {report.report_type}"
            )

        return strategy.transform(report, seed)
