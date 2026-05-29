from app import app
from database.db import db
from database.models import Employee
from werkzeug.security import generate_password_hash

with app.app_context():
    emp = Employee.query.filter_by(email='admin@company.com').first()
    emp.password_hash = generate_password_hash('admin123')
    db.session.commit()
    print(' Admin password reset successfully')