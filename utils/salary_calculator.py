def calculate_salary(
    basic_salary,
    leave_days=0,
    ot_hours=0,
    bonus=0,
    expenses=0
):

    hra = basic_salary * 0.20

    pf = basic_salary * 0.12

    daily_salary = basic_salary / 30

    leave_deduction = daily_salary * leave_days

    hourly_rate = basic_salary / (30 * 8)

    ot_amount = ot_hours * hourly_rate * 1.5

    net_salary = (
        basic_salary
        + hra
        + ot_amount
        + bonus
        + expenses
        - pf
        - leave_deduction
    )

    return {
        "hra": hra,
        "pf": pf,
        "leave_deduction": leave_deduction,
        "ot_amount": ot_amount,
        "bonus": bonus,
        "expenses": expenses,
        "net_salary": net_salary
    }