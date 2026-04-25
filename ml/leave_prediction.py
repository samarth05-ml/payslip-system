import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

from app import app
from database.models import Employee, Leave, Payslip
import joblib


def create_dataset():

    employees = Employee.query.all()
    leaves = Leave.query.all()
    payslips = Payslip.query.all()

    data = []

    for emp in employees:
        emp_leaves = [l for l in leaves if l.employee_id == emp.id]
        emp_payslips = [p for p in payslips if p.employee_id == emp.id]

        total_leaves = sum([l.days for l in emp_leaves])
        approved_leaves = sum([l.days for l in emp_leaves if l.status == "Approved"])

        avg_salary = 0
        if emp_payslips:
            avg_salary = sum([p.net_salary for p in emp_payslips]) / len(emp_payslips)

        will_take_leave = 1 if total_leaves > 2 else 0

        data.append({
            "basic_salary": emp.basic_salary,
            "approved_leaves": approved_leaves,
            "avg_salary": avg_salary,
            "target": will_take_leave
        })

    return pd.DataFrame(data)


def train_model():

    df = create_dataset()

    if df.empty:
        print("No data available ❌")
        return None

    X = df[["basic_salary", "approved_leaves", "avg_salary"]]
    y = df["target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    print("Model Accuracy:", accuracy)

    return model


if __name__ == "__main__":
    with app.app_context():
        model = train_model()

        if model is not None:
            joblib.dump(model, "ml/leave_model.pkl")
            print("Model saved successfully ")