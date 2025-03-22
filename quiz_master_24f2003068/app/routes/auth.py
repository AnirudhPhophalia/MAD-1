from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app import db
from datetime import datetime

anirudh_bp = Blueprint('auth', __name__)

LOG_FILE = "login_attempts.log" # sving the login attempts of each user

def log_login_attempt(email, success):
    with open(LOG_FILE, "a") as file:
        status = "SUCCESS" if success else "FAILED"
        file.write(f"{datetime.now()} - Email: {email} - Status: {status}\n")

@anirudh_bp.route('/')
def index():#main page
    return redirect(url_for('auth.login'))

@anirudh_bp.route('/login', methods=['GET', 'POST'])
def login():#login portalpage
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('user.dashboard'))
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            log_login_attempt(email, True)  # successful login
            next_page = request.args.get('next')
            if user.is_admin:
                return redirect(next_page or url_for('admin.dashboard'))
            return redirect(next_page or url_for('user.dashboard'))
        else:
            log_login_attempt(email, False)  # failed login
            flash('It is wrong password or email')

    return render_template('auth/login.html')

@anirudh_bp.route('/logout')
@login_required
def logout():   #logout page
    logout_user()
    return redirect(url_for('auth.login'))

@anirudh_bp.route('/register', methods=['GET', 'POST'])
def register():#registeration page
    if current_user.is_authenticated:
        return redirect(url_for('user.dashboard'))
    
    if request.method == 'POST':
        try:
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            full_name = request.form['full_name']
            qualification = request.form['qualification']
            date_of_birth = datetime.strptime(request.form['date_of_birth'], '%Y-%m-%d')
            
            if User.query.filter_by(username=username).first():
                flash('Username already exists')
                return redirect(url_for('auth.register'))
            
            if User.query.filter_by(email=email).first():
                flash('Email already exists')
                return redirect(url_for('auth.register'))
            
            user = User(
                username=username,
                email=email,
                full_name=full_name,
                qualification=qualification,
                date_of_birth=date_of_birth,
                is_admin=False
            )
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful. Please log in.')
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash(f'Registration failed: {str(e)}', 'danger')
            return redirect(url_for('auth.register'))
    
    return render_template('auth/register.html')
