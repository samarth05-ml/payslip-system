import pandas as pd
from sklearn.ensemble import IsolationForest

from app import app
from database.models import Payslip

def create_salary_dataset():

    payslips = Payslip.query.all()

    data = []

    for p in payslips:
        data.append({
            "basic_salary": p.basic_salary,
            "hra": p.hra,
            "deductions": p.deductions,
            "net_salary": p.net_salary
        })

    df = pd.DataFrame(data)
    return df


def train_anomaly_model():

    df = create_salary_dataset()

    print("Dataset:\n", df)

    if df.empty:
        print("No data available ")
        return

    # Model
    model = IsolationForest(contamination=0.1)  # 10% anomalies
    model.fit(df)

    # Predict anomalies
    df["anomaly"] = model.predict(df)

    print("\nResults:")
    print(df)

    return model


if __name__ == "__main__":
    with app.app_context():
        model = train_anomaly_model()
        '''
        # Test sample
        sample = pd.DataFrame([{
            "basic_salary": 30000,
            "hra": 6000,
            "deductions": 3000,
            "net_salary": 33000
        }])

        result = model.predict(sample)

        if result[0] == -1:
            print("Anomaly detected ")
        else:
            print("Salary is normal ")'''