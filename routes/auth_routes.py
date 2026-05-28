import hashlib
from flask import Blueprint, request, jsonify, session
from database.db import db
from database.models import Employee

auth_bp = Blueprint('auth', __name__)


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


# ── POST /api/login ──────────────────────────────────────────
@auth_bp.route('/api/login', methods=['POST'])
def login():
    data     = request.get_json() or {}
    email    = data.get('email', '').strip().lower()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({'success': False, 'error': 'Email and password are required'}), 400

    employee = Employee.query.filter(
        db.func.lower(Employee.email) == email
    ).first()

    if not employee or employee.password_hash != hash_password(password):
        return jsonify({'success': False, 'error': 'Invalid email or password'}), 401

    session['user_id']   = employee.id
    session['user_name'] = employee.name
    session['user_role'] = employee.role

    return jsonify({
        'success': True,
        'role':    employee.role,
        'name':    employee.name,
        'user_id': employee.id
    })


# ── POST /api/logout ─────────────────────────────────────────
@auth_bp.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True})


# ── GET /api/me ──────────────────────────────────────────────
@auth_bp.route('/api/me', methods=['GET'])
def me():
    if 'user_id' not in session:
        return jsonify({'logged_in': False}), 401
    return jsonify({
        'logged_in': True,
        'user_id':   session['user_id'],
        'name':      session['user_name'],
        'role':      session['user_role']
    })