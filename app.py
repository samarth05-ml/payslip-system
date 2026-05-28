import os
import hashlib
from flask import Flask, send_from_directory
from config import Config
from database.db import db
from routes.employee_routes import employee_bp
from routes.payslip_routes import payslip_bp
from routes.leave_routes import leave_bp
from routes.ml_routes import ml_bp
from routes.auth_routes import auth_bp          # ← NEW
from flask_cors import CORS
from flask import redirect,session

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.environ.get('SECRET_KEY', 'change-this-in-production')  # ← NEW

CORS(app, supports_credentials=True)           # ← supports_credentials needed for sessions

# Create data directory if it does not exist
os.makedirs(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data'), exist_ok=True)

db.init_app(app)

app.register_blueprint(employee_bp)
app.register_blueprint(payslip_bp)
app.register_blueprint(leave_bp)
app.register_blueprint(ml_bp)
app.register_blueprint(auth_bp)                # ← NEW

with app.app_context():
    db.create_all()


# ── Serve frontend pages ──────────────────────────────────────
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')

@app.route('/login')
def login_page():
    return send_from_directory(FRONTEND_DIR, 'login.html')

@app.route('/employee')
def employee_page():
    return send_from_directory(FRONTEND_DIR, 'employee.html')

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect('/login')
    if session.get('user_role') not in ('Admin', 'HR', 'MD'):
        return redirect('/employee')
    return send_from_directory(FRONTEND_DIR, 'index.html')

@app.route('/frontend/<path:filename>')
def frontend_files(filename):
    return send_from_directory(FRONTEND_DIR, filename)

# ── Seed default admin account ────────────────────────────────
def _seed_admin():
    """Creates a default Admin account on first run if none exists."""
    from database.models import Employee
    if not Employee.query.filter_by(role='Admin').first():
        admin = Employee(
            name          = 'Administrator',
            email         = 'admin@company.com',
            designation   = 'System Admin',
            basic_salary  = 0,
            role          = 'Admin',
            password_hash = hashlib.sha256(b'admin123').hexdigest()
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Default admin created: admin@company.com / admin123")


# Call after function is defined
with app.app_context():
    _seed_admin()


if __name__ == "__main__":
    app.run(debug=True)