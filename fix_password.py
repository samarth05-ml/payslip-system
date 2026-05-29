from app import app
from database.db import db
from database.models import Employee
from werkzeug.security import generate_password_hash

with app.app_context():
    employees = [
        ('samarth@gmail.com', '123456'),
        ('yatiraj@gmail.com', '123456'),
        ('rohit@gmail.com',   '123456'),
        ('shreedar@gmail.com','123456'),
    ]
    
    for email, password in employees:
        emp = Employee.query.filter_by(email=email).first()
        if emp:
            emp.password_hash = generate_password_hash(password)
            print(f' Reset: {email}')
    
    db.session.commit()
    print('Done')