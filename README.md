# Payslip and Leave Management System

## Overview
This project is a backend system built using Flask that manages employees, leave requests, approval workflows, and generates payslips with salary deductions and PDF export functionality.

---

## Features

### Employee Management
- Add employee details
- Store employee information such as name, email, designation, salary, and role

### Leave Management
- Apply for leave
- Role-based approval system:
  - Employee requests are approved by HR
  - HR requests are approved by MD
- View leave status
- View pending leave requests for approvers

### Payroll System
- Generate payslips
- Automatic salary calculation
- Salary deduction based on approved leaves

### PDF Generation
- Generate payslip as a PDF file
- Includes company logo
- Displays structured salary breakdown

---

## Tech Stack
- Python
- Flask
- SQLAlchemy
- SQLite
- ReportLab

---

## Project Structure

payslip-system/
│
├── database/
│   ├── db.py
│   └── models.py
│
├── routes/
│   ├── employee_routes.py
│   ├── leave_routes.py
│   └── payslip_routes.py
│
├── services/
│   ├── payslip_service.py
│   └── pdf_service.py
│
├── utils/
│   └── salary_calculator.py
│
├── assets/
│   └── ymgm-logo.png
│
├── app.py
├── payslip.db
├── requirements.txt
└── README.md

---

## Setup Instructions

### 1. Clone the repository
git clone https://github.com/samarth05-ml/payslip-system.git  

### 2. Create virtual environment
python -m venv venv  

### 3. Activate virtual environment
venv\Scripts\activate   (Windows)

### 4. Install dependencies
pip install -r requirements.txt  

### 5. Run the application
python app.py  

---

## API Endpoints

### Employee
POST /add_employee  
GET /get_employees  

### Leave
POST /apply_leave  
POST /approve_leave  
GET /leave_status/<employee_id>  
GET /pending_leaves/<approver_id>  

### Payslip
POST /generate_payslip  

---

## Key Concepts
- Role-based approval workflow
- Leave tracking and deduction logic
- Modular backend architecture
- RESTful API design

---

## Future Enhancements
- Frontend user interface using React or HTML/CSS
- Machine learning features such as:
  - Leave prediction
  - Salary anomaly detection
  - Employee behavior analysis
- Authentication using JWT

---

## Author
Samarth

---

## Description
This project demonstrates a backend system with real-world business logic, database integration, and document generation.