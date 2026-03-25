def calculate_salary(basic_salary):

    hra = basic_salary * 0.20
    deductions = basic_salary * 0.10

    net_salary = basic_salary + hra - deductions

    return {
        "hra": hra,
        "deductions": deductions,
        "net_salary": net_salary
    }