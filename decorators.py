from functools import wraps
from flask import redirect, url_for, session, current_app, abort

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        users = current_app.db.select('users', conditions={'id': user_id})
        if not user_id or not users:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def redirect_if_logged_in(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' in session:
            return redirect(url_for('auth.profile'))
        return f(*args, **kwargs)
    return decorated_function

def owner_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        movie_id = kwargs.get('movie_id')
        if not user_id or not movie_id:
            abort(403)
        
        user = current_app.db.select('users', conditions={'id': user_id})[0]
        if movie_id not in user['movie_ids']:
            abort(403)
        
        return f(*args, **kwargs)
    return decorated_function
