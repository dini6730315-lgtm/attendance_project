from datetime import time
from models.attendance_models import AttendanceRow, AttendanceReport
from models.report_types import ReportType
from transformers.transformation_strategy import StandardTransformationStrategy


def test_transformation():
    row = AttendanceRow(
        date="01/09/2022",
        day="חמישי",
        entry=time(8, 30),
        exit_time=time(12, 0),
        break_hours=0,
        total_hours=3.5
    )

    report = AttendanceReport(
        company_name="חברה",
        employee_name="ישראל",
        month="09/2022",
        report_type=ReportType.TYPE_A,
        rows=(row,)
    )

    strategy = StandardTransformationStrategy()
    result = strategy.transform(report, seed=42)

    assert result is not None
    assert len(result.rows) == 1
    assert result.rows[0].entry < result.rows[0].exit_time
    