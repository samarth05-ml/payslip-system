from app import app
from database.models import Employee
from werkzeug.security import check_password_hash

with app.app_context():
    emp = Employee.query.filter_by(email='admin@company.com').first()
    print('Found:', emp)
    print('Hash:', emp.password_hash)
    print('Check:', check_password_hash(emp.password_hash, 'admin123'))