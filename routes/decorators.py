from functools import wraps
from flask import jsonify, session

ADMIN_ROLES = ('Admin', 'HR', 'MD')


def login_required(f):
    """Block unauthenticated requests."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Unauthorized — please log in'}), 401
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    """Block non-admin (Employee) requests."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Unauthorized — please log in'}), 401
        if session.get('user_role') not in ADMIN_ROLES:
            return jsonify({'error': 'Forbidden — Admin access only'}), 403
        return f(*args, **kwargs)
    return decorated