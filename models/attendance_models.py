from dataclasses import dataclass, field
from typing import List

@dataclass(frozen=True)
class AttendanceRow:
    date: str
    day: str
    entry: str
    exit_time: str
    break_hours: float
    total_hours: float
    workplace: str = ""
    h_100: float = 0.0
    h_125: float = 0.0
    h_150: float = 0.0
    shabbat: float = 0.0

@dataclass
class AttendanceReport:
    company_name: str
    employee_name: str
    month: str
    report_type: str
    rows: List[AttendanceRow] = field(default_factory=list)