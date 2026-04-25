import pandas as pd
from sklearn.cluster import KMeans

from app import app
from database.models import Employee, Leave, Payslip

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

        data.append({
            "employee_id": emp.id,
            "total_leaves": total_leaves,
            "approved_leaves": approved_leaves,
            "avg_salary": avg_salary
        })

    df = pd.DataFrame(data)
    return df


def train_model():

    df = create_dataset()

    print("Dataset:\n", df)

    if df.empty:
        print("No data available ")
        return

    # Features for clustering
    X = df[["total_leaves", "approved_leaves", "avg_salary"]]

    # KMeans model
    model = KMeans(n_clusters=3, random_state=42)
    df["cluster"] = model.fit_predict(X)

    print("\nClustered Data:")
    print(df)

    return df


def label_clusters(df):

    # Simple labeling logic
    labels = {}

    for cluster in df["cluster"].unique():
        subset = df[df["cluster"] == cluster]

        avg_leaves = subset["total_leaves"].mean()

        if avg_leaves > 5:
            labels[cluster] = "Frequent Leave Taker"
        elif avg_leaves > 2:
            labels[cluster] = "High Risk"
        else:
            labels[cluster] = "Normal"

    df["behavior"] = df["cluster"].map(labels)

    print("\nFinal Behavior Classification:")
    print(df[["employee_id", "behavior"]])

    return df


if __name__ == "__main__":
    with app.app_context():
        df = train_model()
        if df is not None:
            df = label_clusters(df)