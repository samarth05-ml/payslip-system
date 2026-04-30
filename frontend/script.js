// Load dashboard stats
function loadDashboard() {
    fetch("http://127.0.0.1:5000/dashboard_summary")
    .then(res => {
        console.log("Dashboard status:", res.status);
        return res.json();
    })
    .then(data => {
        console.log("DASHBOARD DATA:", data); // 🔥 debug

        if (!data) {
            console.error("No dashboard data");
            return;
        }

        document.getElementById("total_employees").innerText = data.total_employees || 0;
        document.getElementById("total_payslips").innerText = data.payslips_generated || 0;
        document.getElementById("total_predictions").innerText = data.leave_predictions || 0;
        document.getElementById("total_anomalies").innerText = data.anomalies || 0;
    })
    .catch(err => console.error("Dashboard error:", err));
}


// Load chart
function loadChart() {
    fetch("http://127.0.0.1:5000/analytics")
    .then(res => {
        console.log("Analytics status:", res.status);
        return res.json();
    })
    .then(data => {

        console.log("ANALYTICS DATA:", data); // 🔥 debug

        if (!data.salary_trend || data.salary_trend.length === 0) {
            console.error("No chart data");
            return;
        }

        let labels = data.salary_trend.map(item => item.month);
        let values = data.salary_trend.map(item => item.total_salary);

        const canvas = document.getElementById('salaryChart');

        if (!canvas) {
            console.error("Canvas not found");
            return;
        }

        const ctx = canvas.getContext('2d');

        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Salary Trend',
                    data: values,
                    backgroundColor: "rgba(59,130,246,0.6)"
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        labels: { color: "white" }
                    }
                },
                scales: {
                    x: { ticks: { color: "white" } },
                    y: { ticks: { color: "white" } }
                }
            }
        });

    })
    .catch(err => console.error("Chart error:", err));
}


// Run everything on load
window.onload = function() {
    console.log("JS LOADED ✅"); // 🔥 check if script runs

    loadDashboard();
    loadChart();
};