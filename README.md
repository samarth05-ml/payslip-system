# MGM Payslip Analytics & Management Console

A full-stack payroll management system built with Flask and vanilla JavaScript, featuring ML-powered leave forecasting, salary anomaly detection, employee behavioral clustering, and a modern glassmorphism UI.

---

## Features

### Authentication
- Secure session-based login with role-based access (Admin, HR, MD, Employee)
- Passwords hashed using werkzeug scrypt (salted, production-safe)
- Protected routes via server-side session decorators

###  Employee Management
- Add, view, and search employees
- Role assignment (Employee / HR / MD)
- Admin sets initial login password

###  Leave Management
- Employees apply for leave with date range and reason
- Role-based approval workflow:
  - Employee → approved by HR
  - HR → approved by MD
- Month-scoped leave deduction on payslip generation

###  Payroll System
- Generate payslips per employee per month
- Auto salary calculation (Basic + HRA − Deductions)
- Leave days deducted from net salary for the relevant month only

###  PDF Generation
- Professional payslip PDF with company branding
- Colour-coded salary breakdown, net pay highlight, footer
- Download from both employee and admin dashboards

###  AI / ML Features
- **Leave Forecast Engine** — Random Forest model predicts leave likelihood
- **Salary Anomaly Audit** — Isolation Forest flags irregular payslip data
- **Behavioral Clustering** — K-Means groups employees by leave and salary patterns
- **Analytics Dashboard** — Monthly salary trends and leave trend charts

###  UI
- Admin/HR dashboard with aurora gradient background and glass morphism cards
- Employee self-service portal with dark theme
- Responsive layout for desktop and tablet

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Database | SQLAlchemy + SQLite |
| ML | scikit-learn, pandas, joblib |
| PDF | ReportLab |
| Frontend | HTML, CSS, Vanilla JS, Chart.js |
| Auth | Flask Sessions + werkzeug |

---

## Project Structure

```
payslip-system/
│
├── app.py                  # Flask app entry point, seed admin
├── config.py               # App configuration
├── requirements.txt
│
├── database/
│   ├── db.py               # SQLAlchemy instance
│   └── models.py           # Employee, Payslip, Leave, Anomaly, Prediction
│
├── routes/
│   ├── auth_routes.py      # /api/login, /api/logout, /api/me
│   ├── employee_routes.py  # /add_employee, /get_employees
│   ├── leave_routes.py     # /apply_leave, /approve_leave, /my_leaves
│   ├── payslip_routes.py   # /generate_payslip, /my_payslips, /payslip_pdf
│   ├── ml_routes.py        # /predict_leave, /detect_anomalies, /get_analytics
│   └── decorators.py       # login_required, admin_required
│
├── services/
│   ├── payslip_service.py  # Payslip generation logic
│   ├── pdf_service.py      # ReportLab PDF generation
│   └── ml_service.py       # ML model training and inference
│
├── utils/
│   └── salary_calculator.py
│
├── ml/                     # Trained model files (.pkl) — gitignored
│
├── data/                   # SQLite DB and generated PDFs — gitignored
│   ├── payslip.db
│   └── pdfs/
│
└── frontend/
    ├── index.html          # Admin/HR dashboard
    ├── employee.html       # Employee self-service portal
    ├── login.html          # Login page
    ├── script.js           # Admin dashboard JS
    ├── styles.css          # Global styles
    └── assets/             # Icons, logo
```

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/samarth05-ml/payslip-system.git
cd payslip-system
```

### 2. Create and activate virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the application
```bash
python app.py
```

### 5. Open in browser
```
http://127.0.0.1:5000/login
```

### 6. Default admin login
```
Email:  abc  
Password: abc
```

>  Change the admin password immediately after first login in production.

---

## API Endpoints

### Auth
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/login` | Login with email and password |
| POST | `/api/logout` | Clear session |
| GET | `/api/me` | Get current session user |

### Employees
| Method | Endpoint | Description |
|---|---|---|
| POST | `/add_employee` | Register new employee (Admin) |
| GET | `/get_employees` | List all employees (Admin/HR) |

### Leaves
| Method | Endpoint | Description |
|---|---|---|
| POST | `/apply_leave` | Submit leave application |
| POST | `/approve_leave` | Approve or reject leave (Admin/HR) |
| GET | `/my_leaves` | Get current employee's leaves |
| GET | `/pending_leaves` | Get leaves pending approval |

### Payslips
| Method | Endpoint | Description |
|---|---|---|
| POST | `/generate_payslip` | Generate payslip for employee |
| GET | `/my_payslips` | Get current employee's payslips |
| GET | `/payslip_pdf/<id>` | Download payslip as PDF |

### ML / Analytics
| Method | Endpoint | Description |
|---|---|---|
| POST | `/predict_leave` | Run leave forecast for employee |
| POST | `/detect_anomalies` | Run salary anomaly audit |
| GET | `/get_analytics` | Get salary and leave trend data |
| GET | `/get_employee_behavior` | Get K-Means cluster assignments |

---

## Security Notes

- Passwords are hashed using `werkzeug.security.generate_password_hash` (scrypt algorithm)
- All sensitive routes protected by server-side session checks
- `approver_id` for leave approval is taken from session, not client request body
- Secret key should be set via environment variable in production:
  ```bash
  set SECRET_KEY=your-random-secret-key   # Windows
  export SECRET_KEY=your-random-secret-key # Linux/macOS
  ```

---

## Author

**Samarth Prabhu**  
MGM Evening College, Udupi

---

## License

This project is for academic and demonstration purposes.