from flask import Flask
from config import Config
from database.db import db
from routes.employee_routes import employee_bp
from routes.payslip_routes import payslip_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

app.register_blueprint(employee_bp)
app.register_blueprint(payslip_bp)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)