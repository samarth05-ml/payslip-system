"""
seed_data.py  —  Run once to generate 5 months of payslip & leave data
                 for every employee already in the database.

Usage (from your project root):
    python seed_data.py

Safe to re-run: skips any month a payslip already exists for that employee.
"""

import sys, os, random
from datetime import datetime, timedelta

# ── Make sure project imports work ──────────────────────────
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import app
from database.db import db
from database.models import Employee, Payslip, Leave
from utils.salary_calculator import calculate_salary

# ── Config ───────────────────────────────────────────────────
MONTHS = ["January", "February", "March", "April", "May"]   # 5 months
YEAR   = 2026

# Leave settings per month (realistic, randomised)
LEAVE_TYPES    = ["casual", "sick", "earned"]
# Probability an employee takes ANY leave in a given month
LEAVE_CHANCE   = 0.45
# Days range when they do take leave
MIN_LEAVE_DAYS = 1
MAX_LEAVE_DAYS = 3

# ── Helpers ──────────────────────────────────────────────────
def month_date_range(month_name, year):
    """Return (first_day, last_day) as datetime objects."""
    first = datetime.strptime(f"1 {month_name} {year}", "%d %B %Y")
    # last day: go to next month, subtract one day
    if first.month == 12:
        last = first.replace(day=31)
    else:
        last = (first.replace(month=first.month + 1)) - timedelta(days=1)
    return first, last

def already_has_payslip(employee_id, month):
    return Payslip.query.filter_by(
        employee_id=employee_id, month=month
    ).first() is not None

# ── Main seed ────────────────────────────────────────────────
def seed():
    with app.app_context():
        employees = Employee.query.all()

        if not employees:
            print("No employees found. Add employees first, then re-run.")
            return

        print(f"Found {len(employees)} employee(s). Seeding {len(MONTHS)} months...\n")

        total_payslips = 0
        total_leaves   = 0

        for emp in employees:
            print(f"  [{emp.id}] {emp.name} ({emp.role}) — ₹{emp.basic_salary:,.0f}/mo")

            # Skip Admin accounts for payslips (salary = 0)
            skip_payslip = (emp.basic_salary == 0)

            for month in MONTHS:
                month_first, month_last = month_date_range(month, YEAR)

                # ── Leave (random, before payslip so deduction is correct) ──
                leave_days_this_month = 0

                if not skip_payslip and random.random() < LEAVE_CHANCE:
                    leave_type = random.choice(LEAVE_TYPES)
                    days       = random.randint(MIN_LEAVE_DAYS, MAX_LEAVE_DAYS)

                    # Pick a random start date that fits inside the month
                    max_start_offset = (month_last - month_first).days - days
                    if max_start_offset >= 0:
                        offset    = random.randint(0, max_start_offset)
                        from_date = month_first + timedelta(days=offset)
                        to_date   = from_date + timedelta(days=days - 1)

                        leave = Leave(
                            employee_id = emp.id,
                            leave_type  = leave_type,
                            from_date   = from_date,
                            to_date     = to_date,
                            days        = days,
                            reason      = f"Auto-seeded {leave_type} leave",
                            status      = "Approved",
                            approver_id = emp.id,   # self for seed purposes
                            submitted_at= from_date
                        )
                        db.session.add(leave)
                        leave_days_this_month = days
                        total_leaves += 1

                # ── Payslip ──
                if skip_payslip:
                    print(f"    {month:10s}  — skipped (salary = 0)")
                    continue

                if already_has_payslip(emp.id, month):
                    print(f"    {month:10s}  — payslip already exists, skipped")
                    continue

                calc        = calculate_salary(emp.basic_salary)
                hra         = calc["hra"]
                deductions  = calc["deductions"]

                # Apply leave deduction (same logic as payslip_service.py)
                per_day        = emp.basic_salary / 30
                leave_deduct   = leave_days_this_month * per_day
                net_salary     = calc["net_salary"] - leave_deduct
                total_deduct   = deductions + leave_deduct

                payslip = Payslip(
                    employee_id  = emp.id,
                    month        = month,
                    basic_salary = emp.basic_salary,
                    hra          = round(hra, 2),
                    deductions   = round(total_deduct, 2),
                    net_salary   = round(net_salary, 2)
                )
                db.session.add(payslip)
                total_payslips += 1

                leave_note = f"({leave_days_this_month}d leave deducted)" if leave_days_this_month else ""
                print(f"    {month:10s}  net ₹{net_salary:>10,.2f}  {leave_note}")

            db.session.commit()
            print()

        print(f"Done! Created {total_payslips} payslip(s) and {total_leaves} leave record(s).")

if __name__ == "__main__":
    random.seed(42)   # remove this line if you want different results each run
    seed()