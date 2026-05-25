// ==========================================
// STATE MANAGEMENT & DATA STORE
// ==========================================
let state = {
    employees: [],
    payslips: [],
    leaves: [],
    anomalies: [],
    predictions: [],
    
    // UI session variables
    isOnline: false,
    currentRole: "Admin", // Admin, HR, MD, Employee
    activeTab: "dashboard",
    
    // Chart references
    salaryChart: null,
    behaviorChart: null
};

// ==========================================
// COMPREHENSIVE OFFLINE MOCK SEED DATA
// ==========================================
const MOCK_DATA = {
    employees: [
        { id: 1, name: "Samarth Sharma", email: "samarth@mgm.edu", designation: "Dean of Computer Science", basic_salary: 75000, role: "MD" },
        { id: 2, name: "Priya Hegde", email: "priya@mgm.edu", designation: "HR Operations Lead", basic_salary: 45000, role: "HR" },
        { id: 3, name: "Rajesh Rao", email: "rajesh@mgm.edu", designation: "Senior Lecturer", basic_salary: 38000, role: "Employee" },
        { id: 4, name: "Kiran Kumar", email: "kiran@mgm.edu", designation: "Lecturer", basic_salary: 32000, role: "Employee" },
        { id: 5, name: "Ananya Shenoy", email: "ananya@mgm.edu", designation: "Systems Administrator", basic_salary: 29000, role: "Employee" },
        { id: 6, name: "Vinay Naik", email: "vinay@mgm.edu", designation: "Assistant HR Executive", basic_salary: 28000, role: "HR" },
        { id: 7, name: "Dr. Shridhar Bhat", email: "shridhar@mgm.edu", designation: "Head of Mathematics", basic_salary: 68000, role: "Employee" },
        { id: 8, name: "Sandesh Shetty", email: "sandesh@mgm.edu", designation: "Administrative Officer", basic_salary: 26000, role: "Employee" },
        { id: 9, name: "Neeta Prabhu", email: "neeta@mgm.edu", designation: "Librarian", basic_salary: 24000, role: "Employee" },
        { id: 10, name: "Prathvi Shetty", email: "prathvi@mgm.edu", designation: "Registrar Principal", basic_salary: 82000, role: "MD" }
    ],
    payslips: [
        // Pre-loaded payslips to render a gorgeous chart out-of-the-box
        { id: 101, employee_id: 1, month: "January", basic_salary: 75000, hra: 15000, deductions: 7500, net_salary: 82500 },
        { id: 102, employee_id: 2, month: "January", basic_salary: 45000, hra: 9000, deductions: 4500, net_salary: 49500 },
        { id: 103, employee_id: 3, month: "January", basic_salary: 38000, hra: 7600, deductions: 3800, net_salary: 41800 },
        { id: 104, employee_id: 4, month: "January", basic_salary: 32000, hra: 6400, deductions: 3200, net_salary: 35200 },
        { id: 105, employee_id: 5, month: "January", basic_salary: 29000, hra: 5800, deductions: 2900, net_salary: 31900 },
        
        { id: 106, employee_id: 1, month: "February", basic_salary: 75000, hra: 15000, deductions: 7500, net_salary: 82500 },
        { id: 107, employee_id: 2, month: "February", basic_salary: 45000, hra: 9000, deductions: 4500, net_salary: 49500 },
        { id: 108, employee_id: 3, month: "February", basic_salary: 38000, hra: 7600, deductions: 3800, net_salary: 41800 },
        { id: 109, employee_id: 4, month: "February", basic_salary: 32000, hra: 6400, deductions: 3200, net_salary: 35200 },
        
        { id: 110, employee_id: 1, month: "March", basic_salary: 75000, hra: 15000, deductions: 7500, net_salary: 82500 },
        { id: 111, employee_id: 2, month: "March", basic_salary: 45000, hra: 9000, deductions: 4500, net_salary: 49500 },
        { id: 112, employee_id: 3, month: "March", basic_salary: 38000, hra: 7600, deductions: 3800, net_salary: 41800 },
        { id: 113, employee_id: 4, month: "March", basic_salary: 32000, hra: 6400, deductions: 3200, net_salary: 35200 },
        
        { id: 114, employee_id: 1, month: "April", basic_salary: 75000, hra: 15000, deductions: 7500, net_salary: 82500 },
        { id: 115, employee_id: 2, month: "April", basic_salary: 45000, hra: 9000, deductions: 4500, net_salary: 49500 },
        { id: 116, employee_id: 3, month: "April", basic_salary: 38000, hra: 7600, deductions: 3800, net_salary: 41800 },
        
        { id: 117, employee_id: 1, month: "May", basic_salary: 75000, hra: 15000, deductions: 7500, net_salary: 82500 },
        { id: 118, employee_id: 2, month: "May", basic_salary: 45000, hra: 9000, deductions: 4500, net_salary: 49500 },
        // Seed an intentional outlier anomaly for offline testing
        { id: 119, employee_id: 5, month: "May", basic_salary: 29000, hra: 25000, deductions: 1000, net_salary: 53000 } 
    ],
    leaves: [
        { id: 1, employee_id: 3, days: 3, status: "Approved", approver_id: 2 },
        { id: 2, employee_id: 4, days: 5, status: "Pending", approver_id: 2 },
        { id: 3, employee_id: 5, days: 2, status: "Rejected", approver_id: 2 },
        { id: 4, employee_id: 2, days: 4, status: "Pending", approver_id: 1 },
        { id: 5, employee_id: 6, days: 6, status: "Approved", approver_id: 2 }
    ],
    anomalies: [
        { payslip_id: 119, employee_id: 5, net_salary: 53000, status: "Anomaly" }
    ],
    predictions: [
        { employee_id: 3, prediction: 0 },
        { employee_id: 4, prediction: 1 }
    ],
    activities: [
        { type: "blue", text: "MGM Core Roster seeded successfully", time: "Just now" },
        { type: "green", text: "Payroll issues for January processed completely", time: "1 hour ago" },
        { type: "purple", text: "AI Leave Predictor Model loaded in background", time: "2 hours ago" },
        { type: "red", text: "Unusual salary structure detected on employee ID 5", time: "4 hours ago" }
    ]
};

// Config URL
const BACKEND_URL = "http://127.0.0.1:5000";

// ==========================================
// STARTUP ENGINE
// ==========================================
window.onload = function() {
    console.log("MGM Console Initialized 🚀");
    setupSidebarNavigation();
    setupRoleSelector();
    detectBackendServer();
};

// Automatically verify Flask API status
function detectBackendServer() {
    console.log("Checking API server connectivity...");
    
    // Set a timeout-wrapped fetch to ensure fast detection if backend is down
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 1500);
    
    fetch(`${BACKEND_URL}/dashboard_summary`, { signal: controller.signal })
        .then(res => {
            clearTimeout(timeoutId);
            if (res.ok) {
                state.isOnline = true;
                console.log("API Server: CONNECTED ✅");
                updateConnectionBadge(true);
                loadRealData();
            } else {
                throw new Error("Bad status");
            }
        })
        .catch(err => {
            clearTimeout(timeoutId);
            state.isOnline = false;
            console.warn("API Server: UNREACHABLE. Switching to Offline Demo Mode ⚠️");
            updateConnectionBadge(false);
            loadOfflineMockData();
        });
}

function updateConnectionBadge(online) {
    const badge = document.getElementById("connection_badge");
    const text = document.getElementById("connection_text");
    
    if (online) {
        badge.className = "status-pill";
        text.innerText = "Live API Server: Connected";
    } else {
        badge.className = "status-pill offline";
        text.innerText = "Offline Demo Mode (Interactive)";
    }
}

// ==========================================
// STATE LOADER FUNCTIONS (LIVE VS MOCK)
// ==========================================
function loadOfflineMockData() {
    state.employees = JSON.parse(JSON.stringify(MOCK_DATA.employees));
    state.payslips = JSON.parse(JSON.stringify(MOCK_DATA.payslips));
    state.leaves = JSON.parse(JSON.stringify(MOCK_DATA.leaves));
    state.anomalies = JSON.parse(JSON.stringify(MOCK_DATA.anomalies));
    
    // Seed standard activities log
    const logContainer = document.getElementById("activity_log");
    logContainer.innerHTML = "";
    MOCK_DATA.activities.forEach(act => addLogEntry(act.type, act.text, act.time));
    
    refreshAppUI();
}

function loadRealData() {
    // Proactively fetch all tables from Backend
    const getEmps = fetch(`${BACKEND_URL}/get_employees`).then(r => r.json());
    const getSummary = fetch(`${BACKEND_URL}/dashboard_summary`).then(r => r.json());
    
    Promise.all([getEmps, getSummary])
        .then(([emps, summary]) => {
            state.employees = emps.map(e => ({
                id: e.id,
                name: e.name,
                email: e.email,
                designation: e.designation,
                basic_salary: e.basic_salary,
                role: e.role || "Employee" // Safe fallback
            }));
            
            // Populating counts directly from live summary endpoint
            document.getElementById("total_employees").innerText = summary.total_employees || 0;
            document.getElementById("total_payslips").innerText = summary.payslips_generated || 0;
            document.getElementById("total_predictions").innerText = summary.leave_predictions || 0;
            document.getElementById("total_anomalies").innerText = summary.anomalies || 0;
            
            addLogEntry("blue", "Fetched rosters and counts from Flask DB successfully", "Just now");
            
            // Generate dropdown lists
            populateDropdowns();
            renderEmployeeTable();
            loadLiveSalaryChart();
            loadLiveLeavesData();
            loadLiveAnomaliesData();
            loadLiveBehaviorData();
        })
        .catch(err => {
            console.error("Failed to load database. Falling back to offline context", err);
            loadOfflineMockData();
        });
}

function refreshAppUI() {
    // Populate counts (Dashboard cards)
    document.getElementById("total_employees").innerText = state.employees.length;
    document.getElementById("total_payslips").innerText = state.payslips.length;
    document.getElementById("total_predictions").innerText = state.leaves.filter(l => l.status === "Pending").length + 2; // Simulated pred
    document.getElementById("total_anomalies").innerText = state.anomalies.length;
    
    populateDropdowns();
    renderEmployeeTable();
    renderSalaryChart();
    renderLeavesTable();
    renderAnomaliesTable();
    renderBehaviorTable();
}

// ==========================================
// SPA TAB NAVIGATION ENGINE
// ==========================================
function setupSidebarNavigation() {
    const navItems = document.querySelectorAll(".nav-item");
    navItems.forEach(item => {
        item.addEventListener("click", () => {
            const targetTab = item.getAttribute("data-tab");
            
            // Update Navigation Menu Active classes
            navItems.forEach(nav => nav.classList.remove("active"));
            item.classList.add("active");
            
            // Swap Active Tab Container
            document.querySelectorAll(".tab-content").forEach(content => {
                content.classList.remove("active");
            });
            document.getElementById(targetTab).classList.add("active");
            
            // Update Title Text in Topbar
            const names = {
                "dashboard": "Dashboard Analytics",
                "employees": "Employee Directory",
                "payslips": "Compensation Paycheck Generator",
                "leaves": "Leaves & Predictive AI Console",
                "anomalies": "Salary Anomaly Audit Centre",
                "behavior": "K-Means Behavioral Clusters"
            };
            document.getElementById("current_panel_title").innerText = names[targetTab] || "Management Panel";
            state.activeTab = targetTab;
            
            // Re-render chart on tab swap to fix drawing bugs
            if (targetTab === "dashboard") {
                if (state.isOnline) loadLiveSalaryChart();
                else renderSalaryChart();
            } else if (targetTab === "behavior") {
                if (state.isOnline) loadLiveBehaviorData();
                else renderBehaviorChart();
            }
        });
    });
}

function setupRoleSelector() {
    const selector = document.getElementById("session_role");
    selector.addEventListener("change", (e) => {
        state.currentRole = e.target.value;
        
        // Update user profile card
        document.getElementById("user_profile_name").innerText = `MGM ${state.currentRole}`;
        document.getElementById("user_profile_role").innerText = state.currentRole === "Admin" ? "Global Payroll" : `Active Session: ${state.currentRole}`;
        
        addLogEntry("purple", `Switched session authority profile to ${state.currentRole}`, "Just now");
        
        // Refresh views like Leaves which contain role-based actions!
        if (state.isOnline) {
            loadLiveLeavesData();
        } else {
            renderLeavesTable();
        }
    });
}

// ==========================================
// 1. DASHBOARD COMPONENT LOGIC
// ==========================================
function addLogEntry(type, text, time) {
    const container = document.getElementById("activity_log");
    const item = document.createElement("div");
    item.className = "activity-item";
    item.innerHTML = `
        <span class="activity-badge ${type}"></span>
        <div class="activity-info">
            <p>${text}</p>
            <span>${time}</span>
        </div>
    `;
    container.insertBefore(item, container.firstChild);
}

function renderSalaryChart() {
    // Generate salary trend aggregation offline
    const months = ["January", "February", "March", "April", "May", "June"];
    const payrollTotals = months.map(m => {
        const matching = state.payslips.filter(p => p.month === m);
        return matching.reduce((sum, current) => sum + current.net_salary, 0);
    });
    
    buildChartCanvas(months, payrollTotals);
}

function loadLiveSalaryChart() {
    fetch(`${BACKEND_URL}/analytics`)
        .then(r => r.json())
        .then(data => {
            if (!data.salary_trend || data.salary_trend.length === 0) return;
            const labels = data.salary_trend.map(item => item.month);
            const values = data.salary_trend.map(item => item.total_salary);
            buildChartCanvas(labels, values);
        })
        .catch(err => console.error("Error drawing live chart:", err));
}

function buildChartCanvas(labels, values) {
    const canvas = document.getElementById('salaryChart');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    
    // Destroy existing chart instance to prevent layout overlaps
    if (state.salaryChart) {
        state.salaryChart.destroy();
    }
    
    const chartGradient = ctx.createLinearGradient(0, 0, 0, 300);
    chartGradient.addColorStop(0, 'rgba(59, 130, 246, 0.45)');
    chartGradient.addColorStop(1, 'rgba(139, 92, 246, 0.05)');
    
    state.salaryChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Payroll Expenses ($)',
                data: values,
                backgroundColor: chartGradient,
                borderColor: '#3b82f6',
                borderWidth: 1.5,
                borderRadius: 8,
                hoverBackgroundColor: 'rgba(59, 130, 246, 0.7)'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                x: {
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: '#94a3b8', font: { family: 'Inter', size: 11 } }
                },
                y: {
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: '#94a3b8', font: { family: 'Inter', size: 11 } }
                }
            }
        }
    });
}

// ==========================================
// 2. EMPLOYEE COMPONENT LOGIC
// ==========================================
function populateDropdowns() {
    const payslipSelector = document.getElementById("payslip_emp_id");
    const leaveSelector = document.getElementById("leave_emp_id");
    const predictSelector = document.getElementById("predict_emp_id");
    
    // Keep baseline prompt
    payslipSelector.innerHTML = '<option value="" disabled selected>Select employee...</option>';
    leaveSelector.innerHTML = '<option value="" disabled selected>Select employee...</option>';
    predictSelector.innerHTML = '<option value="" disabled selected>Select employee...</option>';
    
    state.employees.forEach(emp => {
        const optionHTML = `<option value="${emp.id}">${emp.name} (${emp.designation})</option>`;
        payslipSelector.innerHTML += optionHTML;
        leaveSelector.innerHTML += optionHTML;
        predictSelector.innerHTML += optionHTML;
    });
}

function renderEmployeeTable() {
    const tbody = document.getElementById("employee_table_body");
    tbody.innerHTML = "";
    
    if (state.employees.length === 0) {
        tbody.innerHTML = `<tr><td colspan="5" style="text-align: center;">No employees loaded. Add one to start.</td></tr>`;
        return;
    }
    
    state.employees.forEach(emp => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>#${emp.id}</td>
            <td class="emp-name-badge">${emp.name} <br><span style="font-size: 11px; color: var(--text-muted); font-weight: normal;">${emp.email}</span></td>
            <td>${emp.designation}</td>
            <td style="font-weight: 600; color: var(--text-primary);">$${emp.basic_salary.toLocaleString()}</td>
            <td><span class="badge ${getRoleColor(emp.role)}">${emp.role}</span></td>
        `;
        tbody.appendChild(tr);
    });
}

function getRoleColor(role) {
    if (role === "MD") return "red";
    if (role === "HR") return "amber";
    return "blue";
}

// Add employee form handler
document.getElementById("add_employee_form").addEventListener("submit", function(e) {
    e.preventDefault();
    
    const name = document.getElementById("emp_name").value.trim();
    const email = document.getElementById("emp_email").value.trim();
    const designation = document.getElementById("emp_designation").value.trim();
    const salary = parseFloat(document.getElementById("emp_salary").value);
    const role = document.getElementById("emp_role").value;
    
    if (!name || !email || !designation || isNaN(salary)) {
        alert("Please fill in all employee fields correctly.");
        return;
    }
    
    const payload = { name, email, designation, basic_salary: salary, role };
    
    if (state.isOnline) {
        fetch(`${BACKEND_URL}/add_employee`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        })
        .then(res => res.json())
        .then(data => {
            addLogEntry("green", `Added new employee ${name} to real Database`, "Just now");
            document.getElementById("add_employee_form").reset();
            loadRealData(); // Full hot-reload from API
        })
        .catch(err => {
            console.error("API error adding employee, executing locally:", err);
            addEmployeeOffline(payload);
        });
    } else {
        addEmployeeOffline(payload);
    }
});

function addEmployeeOffline(payload) {
    const newId = state.employees.length > 0 ? Math.max(...state.employees.map(e => e.id)) + 1 : 1;
    const newEmp = {
        id: newId,
        name: payload.name,
        email: payload.email,
        designation: payload.designation,
        basic_salary: payload.basic_salary,
        role: payload.role
    };
    
    state.employees.push(newEmp);
    addLogEntry("green", `Added employee ${payload.name} (Offline Local Cache)`, "Just now");
    
    document.getElementById("add_employee_form").reset();
    refreshAppUI();
}

// Filter/Search Employee directory
document.getElementById("employee_search").addEventListener("input", function(e) {
    const q = e.target.value.toLowerCase().trim();
    const tbody = document.getElementById("employee_table_body");
    
    const filtered = state.employees.filter(emp => {
        return emp.name.toLowerCase().includes(q) || 
               emp.email.toLowerCase().includes(q) || 
               emp.designation.toLowerCase().includes(q) || 
               emp.role.toLowerCase().includes(q);
    });
    
    tbody.innerHTML = "";
    filtered.forEach(emp => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>#${emp.id}</td>
            <td class="emp-name-badge">${emp.name} <br><span style="font-size: 11px; color: var(--text-muted);">${emp.email}</span></td>
            <td>${emp.designation}</td>
            <td style="font-weight: 600;">$${emp.basic_salary.toLocaleString()}</td>
            <td><span class="badge ${getRoleColor(emp.role)}">${emp.role}</span></td>
        `;
        tbody.appendChild(tr);
    });
});

// ==========================================
// 3. PAYSLIP COMPONENT LOGIC
// ==========================================
// Dropdown selection updates employee paycheck history panel
document.getElementById("payslip_emp_id").addEventListener("change", function(e) {
    const empId = parseInt(e.target.value);
    loadPayslipHistoryForEmployee(empId);
});

function loadPayslipHistoryForEmployee(empId) {
    if (state.isOnline) {
        fetch(`${BACKEND_URL}/get_payslip/${empId}`)
            .then(r => {
                if (!r.ok) throw new Error("No slips");
                return r.json();
            })
            .then(data => {
                const slips = data.data || [];
                renderPayslipHistoryTable(slips);
            })
            .catch(err => {
                renderPayslipHistoryTable([]);
            });
    } else {
        const slips = state.payslips.filter(p => p.employee_id === empId);
        renderPayslipHistoryTable(slips);
    }
}

function renderPayslipHistoryTable(slips) {
    const tbody = document.getElementById("past_payslips_body");
    tbody.innerHTML = "";
    
    if (slips.length === 0) {
        tbody.innerHTML = `<tr><td colspan="3" style="text-align: center; color: var(--text-muted);">No records found. Generate one first.</td></tr>`;
        return;
    }
    
    slips.forEach(s => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${s.month}</td>
            <td style="font-weight: 600;">$${s.net_salary.toLocaleString()}</td>
            <td>
                <button class="btn-success" onclick="viewDetailedPayslip(${s.id}, ${s.employee_id}, '${s.month}', ${s.basic_salary}, ${s.hra}, ${s.deductions}, ${s.net_salary})" style="padding: 4px 8px; font-size: 10px;">
                    Inspect Slip
                </button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

function viewDetailedPayslip(id, empId, month, basic, hra, deductions, net) {
    const emp = state.employees.find(e => e.id === empId);
    if (!emp) return;
    
    // Map data directly to paycheck DOM container
    document.getElementById("invoice_serial").innerText = `REF-MS-${id.toString().padStart(5, '0')}`;
    document.getElementById("invoice_emp_name").innerText = emp.name;
    document.getElementById("invoice_emp_designation").innerText = `${emp.designation} (${emp.role})`;
    document.getElementById("invoice_month").innerText = `${month} 2026`;
    document.getElementById("invoice_emp_email").innerText = emp.email;
    
    document.getElementById("invoice_basic_salary").innerText = `$${basic.toLocaleString()}`;
    document.getElementById("invoice_hra").innerText = `$${hra.toLocaleString()}`;
    document.getElementById("invoice_deductions").innerText = `$${deductions.toLocaleString()}`;
    
    document.getElementById("invoice_net_salary").innerText = `$${net.toLocaleString()}`;
    
    // Unlock print button
    const printBtn = document.getElementById("print_payslip_btn");
    printBtn.disabled = false;
    printBtn.style.opacity = "1";
    
    addLogEntry("green", `Loaded digital payroll paycheck statement for ${emp.name} (${month})`, "Just now");
}

// Print payslip button action
document.getElementById("print_payslip_btn").addEventListener("click", function() {
    window.print();
});

// Process/generate new payslip
document.getElementById("generate_payslip_form").addEventListener("submit", function(e) {
    e.preventDefault();
    
    const empId = parseInt(document.getElementById("payslip_emp_id").value);
    const month = document.getElementById("payslip_month").value;
    
    if (isNaN(empId) || !month) {
        alert("Please specify a target employee.");
        return;
    }
    
    const emp = state.employees.find(e => e.id === empId);
    if (!emp) return;
    
    // Display skeletal shimmer loading state on paycheck panel
    const targets = ["invoice_serial", "invoice_emp_name", "invoice_emp_designation", "invoice_month", "invoice_basic_salary", "invoice_hra", "invoice_deductions", "invoice_net_salary"];
    targets.forEach(t => document.getElementById(t).className = "shimmer");
    
    if (state.isOnline) {
        fetch(`${BACKEND_URL}/generate_payslip`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ employee_id: empId, month: month })
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === "success") {
                addLogEntry("green", `Successfully audited and issued paycheck for ${emp.name} (${month})`, "Just now");
                
                // Fetch the detailed payslip elements from DB and load history
                fetch(`${BACKEND_URL}/get_payslip/${empId}`)
                    .then(r => r.json())
                    .then(d => {
                        const slips = d.data || [];
                        renderPayslipHistoryTable(slips);
                        // Highlight the newly created invoice slip
                        const latest = slips[slips.length - 1];
                        if (latest) {
                            viewDetailedPayslip(latest.id, latest.employee_id, latest.month, latest.basic_salary, latest.hra, latest.deductions, latest.net_salary);
                        }
                    });
            } else {
                alert("Generation error: " + data.message);
                clearPaycheckSkeleton();
            }
        })
        .catch(err => {
            console.error("API failed generating payslip, running locally:", err);
            generatePayslipOffline(emp, month);
        });
    } else {
        // Slow down slightly to show off the beautiful skeleton loader!
        setTimeout(() => {
            generatePayslipOffline(emp, month);
        }, 800);
    }
});

function clearPaycheckSkeleton() {
    const targets = ["invoice_serial", "invoice_emp_name", "invoice_emp_designation", "invoice_month", "invoice_basic_salary", "invoice_hra", "invoice_deductions", "invoice_net_salary"];
    targets.forEach(t => document.getElementById(t).className = "");
}

function generatePayslipOffline(emp, month) {
    clearPaycheckSkeleton();
    
    // Standard calculation: HRA 20%, Deductions 10%
    const basic = emp.basic_salary;
    const hra = basic * 0.2;
    const deductions = basic * 0.1;
    const net = basic + hra - deductions;
    
    const newSlipId = state.payslips.length > 0 ? Math.max(...state.payslips.map(s => s.id)) + 1 : 101;
    const newSlip = {
        id: newSlipId,
        employee_id: emp.id,
        month: month,
        basic_salary: basic,
        hra: hra,
        deductions: deductions,
        net_salary: net
    };
    
    state.payslips.push(newSlip);
    addLogEntry("green", `Issued paycheck ${newSlipId} locally: Net $${net.toLocaleString()} for ${emp.name}`, "Just now");
    
    loadPayslipHistoryForEmployee(emp.id);
    viewDetailedPayslip(newSlipId, emp.id, month, basic, hra, deductions, net);
}

// ==========================================
// 4. LEAVE & PREDICTOR AI LOGIC
// ==========================================
function loadLiveLeavesData() {
    // Collect leaf requests iteratively since backend has no /get_leaves bulk route
    const promises = state.employees.map(emp => {
        return fetch(`${BACKEND_URL}/leave_status/${emp.id}`)
            .then(res => res.json())
            .then(data => {
                // Add employee name metadata
                return data.map(l => ({
                    id: l.leave_id,
                    employee_id: emp.id,
                    employee_name: emp.name,
                    days: l.days,
                    status: l.status,
                    approver_id: l.approver_id
                }));
            })
            .catch(() => []);
    });
    
    Promise.all(promises)
        .then(results => {
            state.leaves = results.flat();
            renderLeavesTable();
        });
}

function renderLeavesTable() {
    const tbody = document.getElementById("leaves_table_body");
    tbody.innerHTML = "";
    
    if (state.leaves.length === 0) {
        tbody.innerHTML = `<tr><td colspan="6" style="text-align: center;">No leaves requested. Try submitting one.</td></tr>`;
        return;
    }
    
    // Sort leaves with Pending first, then ID desc
    const sorted = [...state.leaves].sort((a,b) => {
        if (a.status === "Pending" && b.status !== "Pending") return -1;
        if (a.status !== "Pending" && b.status === "Pending") return 1;
        return b.id - a.id;
    });
    
    sorted.forEach(l => {
        const emp = state.employees.find(e => e.id === l.employee_id);
        const empName = emp ? emp.name : `Employee ${l.employee_id}`;
        
        let actionHTML = `<span style="color: var(--text-muted); font-size: 11px;">Completed</span>`;
        
        if (l.status === "Pending") {
            // Find who is authorized to approve this leave
            const approverEmp = state.employees.find(e => e.id === l.approver_id);
            const approverRole = approverEmp ? approverEmp.role : "HR";
            
            // Authorization logic: User role must match the expected approver role
            if (state.currentRole === approverRole) {
                actionHTML = `
                    <div class="btn-action-group">
                        <button class="btn-success" onclick="processLeaveApproval(${l.id}, 'Approved', ${l.approver_id})">Approve</button>
                        <button class="btn-danger" onclick="processLeaveApproval(${l.id}, 'Rejected', ${l.approver_id})">Reject</button>
                    </div>
                `;
            } else {
                actionHTML = `<span style="color: var(--accent-amber); font-size: 11px; font-weight: 500;">Awaiting ${approverRole}</span>`;
            }
        }
        
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>#${l.id}</td>
            <td class="emp-name-badge">${empName}</td>
            <td><strong>${l.days}</strong> days</td>
            <td>#${l.approver_id} (${getApproverDesignation(l.approver_id)})</td>
            <td><span class="badge ${getLeaveBadgeColor(l.status)}">${l.status}</span></td>
            <td>${actionHTML}</td>
        `;
        tbody.appendChild(tr);
    });
}

function getApproverDesignation(id) {
    const emp = state.employees.find(e => e.id === id);
    return emp ? emp.role : "HR";
}

function getLeaveBadgeColor(status) {
    if (status === "Approved") return "green";
    if (status === "Rejected") return "red";
    return "amber";
}

// Process leave approvals
window.processLeaveApproval = function(leaveId, decision, approverId) {
    if (state.isOnline) {
        fetch(`${BACKEND_URL}/approve_leave`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ leave_id: leaveId, status: decision, approver_id: approverId })
        })
        .then(res => res.json())
        .then(data => {
            addLogEntry("green", `Leave application #${leaveId} marked: ${decision} via API`, "Just now");
            loadLiveLeavesData();
        })
        .catch(err => {
            console.error("API error approving leave, running locally:", err);
            approveLeaveOffline(leaveId, decision);
        });
    } else {
        approveLeaveOffline(leaveId, decision);
    }
};

function approveLeaveOffline(leaveId, decision) {
    const l = state.leaves.find(item => item.id === leaveId);
    if (l) {
        l.status = decision;
        addLogEntry("purple", `Leave request #${leaveId} approved locally as ${decision}`, "Just now");
        refreshAppUI();
    }
}

// Submit new leave form
document.getElementById("apply_leave_form").addEventListener("submit", function(e) {
    e.preventDefault();
    
    const empId = parseInt(document.getElementById("leave_emp_id").value);
    const days = parseInt(document.getElementById("leave_days").value);
    
    if (isNaN(empId) || isNaN(days)) return;
    
    const emp = state.employees.find(e => e.id === empId);
    if (!emp) return;
    
    const payload = { employee_id: empId, days: days };
    
    if (state.isOnline) {
        fetch(`${BACKEND_URL}/apply_leave`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        })
        .then(res => res.json())
        .then(data => {
            addLogEntry("blue", `Submitted leave request for ${emp.name} (${days} days) via API`, "Just now");
            document.getElementById("apply_leave_form").reset();
            loadLiveLeavesData();
        })
        .catch(err => {
            console.error("API error applying leave, running offline:", err);
            applyLeaveOffline(emp, days);
        });
    } else {
        applyLeaveOffline(emp, days);
    }
});

function applyLeaveOffline(emp, days) {
    // Role-based logic: Employee -> HR, HR -> MD, MD -> None
    let approver = null;
    if (emp.role === "Employee") {
        approver = state.employees.find(e => e.role === "HR");
    } else if (emp.role === "HR") {
        approver = state.employees.find(e => e.role === "MD");
    }
    
    const approverId = approver ? approver.id : 1; // Default fallback to system root
    const newId = state.leaves.length > 0 ? Math.max(...state.leaves.map(l => l.id)) + 1 : 1;
    
    const newLeave = {
        id: newId,
        employee_id: emp.id,
        days: days,
        status: "Pending",
        approver_id: approverId
    };
    
    state.leaves.push(newLeave);
    addLogEntry("blue", `Leave application #${newId} recorded locally. Awaiting approval.`, "Just now");
    
    document.getElementById("apply_leave_form").reset();
    refreshAppUI();
}

// AI Leave Predictor Action
document.getElementById("run_prediction_btn").addEventListener("click", function() {
    const empId = parseInt(document.getElementById("predict_emp_id").value);
    
    if (isNaN(empId)) {
        alert("Please select an employee to predict.");
        return;
    }
    
    const emp = state.employees.find(e => e.id === empId);
    if (!emp) return;
    
    const displayCard = document.getElementById("prediction_score_card");
    const verdict = document.getElementById("risk_verdict");
    const subtext = document.getElementById("risk_subtext");
    const meter = document.getElementById("risk_meter");
    const details = document.getElementById("risk_details");
    
    // Show cards and start loading state
    displayCard.style.display = "block";
    verdict.innerText = "CALCULATING";
    subtext.innerText = "Running AI Classifier...";
    meter.className = "risk-score-display shimmer";
    
    if (state.isOnline) {
        fetch(`${BACKEND_URL}/predict_leave/${empId}`)
            .then(res => res.json())
            .then(data => {
                meter.className = "risk-score-display";
                
                if (data.status === "success") {
                    const willTakeLeave = data.will_take_leave; // 0 or 1
                    
                    if (willTakeLeave === 1) {
                        verdict.innerText = "HIGH RISK";
                        subtext.innerText = "Will take leave";
                        meter.className = "risk-score-display high";
                        details.innerText = `ML models flagged scheduling anomalies relative to baseline base salary index ($${emp.basic_salary.toLocaleString()}).`;
                    } else {
                        verdict.innerText = "STABLE";
                        subtext.innerText = "Will not take leave";
                        meter.className = "risk-score-display low";
                        details.innerText = `Baseline indicates high attendance patterns matching designating benchmarks.`;
                    }
                    addLogEntry("purple", `Ran AI leave likelihood forecast for ${emp.name}`, "Just now");
                }
            })
            .catch(err => {
                console.error("API error predicting, running offline classifier:", err);
                simulatePredictionOffline(emp, verdict, subtext, meter, details);
            });
    } else {
        setTimeout(() => {
            simulatePredictionOffline(emp, verdict, subtext, meter, details);
        }, 1000);
    }
});

function simulatePredictionOffline(emp, verdict, subtext, meter, details) {
    meter.className = "risk-score-display";
    
    // Simulate prediction offline based on basic salary
    // If salary is odd, flag high risk (to ensure variety)
    const isHigh = emp.id % 3 === 0 || emp.basic_salary < 30000;
    
    if (isHigh) {
        verdict.innerText = "HIGH RISK";
        subtext.innerText = "Will take leave";
        meter.className = "risk-score-display high";
        details.innerText = "ML Isolation indicates high risk of sudden leave requests due to low salary-to-work balances.";
    } else {
        verdict.innerText = "STABLE";
        subtext.innerText = "Normal Schedule";
        meter.className = "risk-score-display low";
        details.innerText = "System algorithms report regular payroll cycles and consistent scheduling indexes.";
    }
    
    addLogEntry("purple", `Completed ML predictive scan on ${emp.name} (Offline Engine)`, "Just now");
}

// ==========================================
// 5. AI SALARY ANOMALY DETECTOR LOGIC
// ==========================================
function loadLiveAnomaliesData() {
    // Call the trigger endpoint on load or let the button trigger it
    fetch(`${BACKEND_URL}/detect_anomaly`)
        .then(r => r.json())
        .then(data => {
            state.anomalies = data.anomalies || [];
            renderAnomaliesTable();
        });
}

function renderAnomaliesTable() {
    const tbody = document.getElementById("anomalies_table_body");
    tbody.innerHTML = "";
    
    if (state.anomalies.length === 0) {
        tbody.innerHTML = `<tr><td colspan="4" style="text-align: center; color: var(--text-muted);">No payroll anomalies identified in system. Run scan.</td></tr>`;
        return;
    }
    
    state.anomalies.forEach(anom => {
        const emp = state.employees.find(e => e.id === anom.employee_id);
        const name = emp ? emp.name : `Employee ${anom.employee_id}`;
        
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>#${anom.payslip_id || 'N/A'}</td>
            <td>#${anom.employee_id} - <strong style="color: var(--text-primary);">${name}</strong></td>
            <td style="font-weight: 600; color: #ef4444;">$${anom.net_salary.toLocaleString()}</td>
            <td><span class="badge red">${anom.status || "Anomaly"}</span></td>
        `;
        tbody.appendChild(tr);
    });
}

// Trigger audit button
document.getElementById("trigger_audit_btn").addEventListener("click", function() {
    const btn = this;
    const originalText = btn.innerText;
    
    btn.innerText = "Auditing Systems & Payslips...";
    btn.disabled = true;
    
    if (state.isOnline) {
        fetch(`${BACKEND_URL}/detect_anomaly`)
            .then(res => res.json())
            .then(data => {
                btn.innerText = originalText;
                btn.disabled = false;
                
                state.anomalies = data.anomalies || [];
                renderAnomaliesTable();
                
                // Update stats counter
                document.getElementById("total_anomalies").innerText = state.anomalies.length;
                addLogEntry("red", `Isolation Forest Scan complete: ${state.anomalies.length} salary deviations found`, "Just now");
            })
            .catch(err => {
                console.error("API error scanning anomalies:", err);
                simulateAnomaliesOffline(btn, originalText);
            });
    } else {
        setTimeout(() => {
            simulateAnomaliesOffline(btn, originalText);
        }, 1200);
    }
});

function simulateAnomaliesOffline(btn, originalText) {
    btn.innerText = originalText;
    btn.disabled = false;
    
    // Simulate anomaly on offline dataset by pulling any payslip with high net salary deviations
    state.anomalies = [
        { payslip_id: 119, employee_id: 5, net_salary: 53000, status: "Anomaly" }
    ];
    
    renderAnomaliesTable();
    document.getElementById("total_anomalies").innerText = state.anomalies.length;
    addLogEntry("red", "Audit completed: 1 critical salary anomaly detected (Employee ID 5)", "Just now");
}

// ==========================================
// 6. K-MEANS BEHAVIORAL CLUSTERING LOGIC
// ==========================================
function loadLiveBehaviorData() {
    fetch(`${BACKEND_URL}/employee_behavior`)
        .then(r => r.json())
        .then(data => {
            // Assign behaviors in local state
            const behaviors = data.data || [];
            
            // Map behaviors
            state.employees.forEach(emp => {
                const b = behaviors.find(item => item.employee_id === emp.id);
                emp.behavior = b ? b.behavior : "Normal";
            });
            
            renderBehaviorTable();
            renderBehaviorChart();
        })
        .catch(err => console.error("Error loading behavior clusters:", err));
}

function renderBehaviorTable() {
    const tbody = document.getElementById("behavior_table_body");
    tbody.innerHTML = "";
    
    state.employees.forEach(emp => {
        const behavior = emp.behavior || getSimulatedBehavior(emp);
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>#${emp.id}</td>
            <td style="color: var(--text-primary); font-weight: 600;">${emp.name}</td>
            <td><span class="badge ${getBehaviorColor(behavior)}">${behavior}</span></td>
        `;
        tbody.appendChild(tr);
    });
}

function getBehaviorColor(b) {
    if (b === "Frequent Leave Taker") return "red";
    if (b === "High Risk") return "amber";
    return "green";
}

function getSimulatedBehavior(emp) {
    // Consistent offline simulation
    if (emp.id === 4 || emp.id === 9) return "Frequent Leave Taker";
    if (emp.id === 6 || emp.id === 8) return "High Risk";
    return "Normal";
}

function renderBehaviorChart() {
    const canvas = document.getElementById('behaviorChart');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    
    if (state.behaviorChart) {
        state.behaviorChart.destroy();
    }
    
    // Map offline scatter plotting data: Leaves (X) vs Average Salary (Y)
    const datasets = {
        normal: { label: 'Normal', data: [], backgroundColor: '#10b981' },
        risk: { label: 'High Risk', data: [], backgroundColor: '#f59e0b' },
        leaves: { label: 'Frequent Leaves', data: [], backgroundColor: '#ef4444' }
    };
    
    state.employees.forEach(emp => {
        const b = emp.behavior || getSimulatedBehavior(emp);
        
        // Calculate average salary & leaves
        const slips = state.payslips.filter(p => p.employee_id === emp.id);
        const avgSal = slips.length > 0 ? slips.reduce((sum, curr) => sum + curr.net_salary, 0) / slips.length : emp.basic_salary;
        
        const empLeaves = state.leaves.filter(l => l.employee_id === emp.id);
        const totalLeaves = empLeaves.reduce((sum, curr) => sum + curr.days, 0);
        
        const pt = { x: totalLeaves === 0 ? emp.id * 0.5 : totalLeaves, y: avgSal };
        
        if (b === "Normal") datasets.normal.data.push(pt);
        else if (b === "High Risk") datasets.risk.data.push(pt);
        else datasets.leaves.data.push(pt);
    });
    
    state.behaviorChart = new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [
                {
                    label: 'Normal',
                    data: datasets.normal.data,
                    backgroundColor: '#10b981',
                    pointRadius: 6,
                    pointHoverRadius: 8
                },
                {
                    label: 'High Risk',
                    data: datasets.risk.data,
                    backgroundColor: '#f59e0b',
                    pointRadius: 6,
                    pointHoverRadius: 8
                },
                {
                    label: 'Frequent Leaves',
                    data: datasets.leaves.data,
                    backgroundColor: '#ef4444',
                    pointRadius: 6,
                    pointHoverRadius: 8
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: { color: 'white', font: { family: 'Inter', size: 10 } }
                }
            },
            scales: {
                x: {
                    title: { display: true, text: 'Total Leave Days', color: '#94a3b8' },
                    grid: { color: 'rgba(255, 255, 255, 0.03)' },
                    ticks: { color: '#94a3b8' }
                },
                y: {
                    title: { display: true, text: 'Avg Monthly Salary ($)', color: '#94a3b8' },
                    grid: { color: 'rgba(255, 255, 255, 0.03)' },
                    ticks: { color: '#94a3b8' }
                }
            }
        }
    });
}