from models.attendance_models import AttendanceRow, AttendanceReport

def calculate_hours_diff(entry: str, exit_time: str, break_hours: float = 0.0) -> float:
    if not entry or not exit_time:
        return 0.0
    try:
        h1, m1 = map(int, entry.split(":"))
        h2, m2 = map(int, exit_time.split(":"))
        total_minutes = (h2 * 60 + m2) - (h1 * 60 + m1)
        net_hours = (total_minutes / 60.0) - break_hours
        return round(max(0.0, net_hours), 2)
    except Exception:
        return 0.0

def validate_row_invariants(row: AttendanceRow) -> bool:

    try:
        entry_h = row.entry.hour
        entry_m = row.entry.minute
        exit_h = row.exit_time.hour
        exit_m = row.exit_time.minute
        entry_minutes = entry_h * 60 + entry_m
        exit_minutes = exit_h * 60 + exit_m

        if not (0 <= entry_h < 24 and 0 <= entry_m < 60):
            return False

        if not (0 <= exit_h < 24 and 0 <= exit_m < 60):
            return False

        if exit_minutes <= entry_minutes:
            return False

        if row.break_hours < 0:
            return False

        calculated_total = (
            exit_minutes - entry_minutes
        ) / 60 - row.break_hours

        if calculated_total < 0:
            return False

        if abs(calculated_total - row.total_hours) > 0.05:
            return False

        return True

    except (ValueError, TypeError):
        return False

def validate_report_invariants(report: AttendanceReport) -> AttendanceReport:

    valid_rows = []
    invalid_rows = []

    for row in report.rows:
        if validate_row_invariants(row):
            valid_rows.append(row)
        else:
            invalid_rows.append(row)
            print(
                f"שורה נפסלה: תאריך={row.date}, "
                f"כניסה={row.entry}, יציאה={row.exit_time}, "
                f"סה\"כ={row.total_hours}"
            )

    print(f"שורות תקינות: {len(valid_rows)}")
    print(f"שורות לא תקינות: {len(invalid_rows)}")

    if not valid_rows and report.rows:
        raise ValueError(
            "כל שורות הדוח נפסלו בבדיקת התקינות!"
        )

    return AttendanceReport(
        company_name=report.company_name,
        employee_name=report.employee_name,
        month=report.month,
        report_type=report.report_type,
        rows=tuple(valid_rows)
    )

   