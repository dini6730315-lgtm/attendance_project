from dataclasses import dataclass
from datetime import time
from typing import Tuple
from models.report_types import ReportType
@dataclass(frozen=True)
class AttendanceRow:
    date: str
    day: str
    entry: time
    exit_time: time
    break_hours: float
    total_hours: float
    workplace: str = ""
    h_100: float = 0.0
    h_125: float = 0.0
    h_150: float = 0.0
    shabbat: float = 0.0


@dataclass(frozen=True)
class AttendanceReport:
    company_name: str
    employee_name: str
    month: str
    report_type: ReportType
    rows: Tuple[AttendanceRow, ...] = ()