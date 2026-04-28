function generatePayslip() {
    let empId = document.getElementById("pay_emp_id").value;
    let month = document.getElementById("month").value;

    fetch("http://127.0.0.1:5000/generate_payslip", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            employee_id: empId,
            month: month
        })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("payslip_result").innerText =
            "Net Salary: " + data.net_salary;
    })
    .catch(() => alert("Error generating payslip"));
}


function predictLeave() {
    let id = document.getElementById("empId").value;

    fetch(`http://127.0.0.1:5000/predict_leave/${id}`)
    .then(res => res.json())
    .then(data => {
        document.getElementById("leave_result").innerText =
            data.prediction === 1
                ? "Will take leave"
                : "Will not take leave";
    })
    .catch(() => alert("Error predicting leave"));
}


function detectAnomaly() {
    fetch("http://127.0.0.1:5000/detect_anomaly")
    .then(res => res.json())
    .then(data => {
        let result = "";
        data.anomalies.forEach(a => {
            result += `Emp ${a.employee_id} → Anomaly\n`;
        });
        document.getElementById("anomaly_result").innerText = result;
    })
    .catch(() => alert("Error detecting anomaly"));
}


function getBehavior() {
    fetch("http://127.0.0.1:5000/employee_behavior")
    .then(res => res.json())
    .then(data => {
        let result = "";
        data.data.forEach(e => {
            result += `Emp ${e.employee_id} → ${e.behavior}\n`;
        });
        document.getElementById("behavior_result").innerText = result;
    })
    .catch(() => alert("Error fetching behavior"));
}