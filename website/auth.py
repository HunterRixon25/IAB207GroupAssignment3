from flask import Blueprint, render_template, redirect, url_for, flash
from .forms import LoginForm, RegisterForm
from flask_login import login_user, login_required, logout_user
from flask_bcrypt import generate_password_hash, check_password_hash
from .models import User
from . import db

authbp = Blueprint('auth', __name__ )

@authbp.route('/register', methods=['GET', 'POST'])
def register():
    register = RegisterForm()
    if (register.validate_on_submit()==True):
            uname = register.user_name.data
            pwd = register.password.data
            email = register.email_id.data
            phone = register.phone.data
            postcode = register.postcode.data
            user = User.query.filter_by(name=uname).first()
            if user:
                flash('Username already exists, please try another')
                return redirect(url_for('auth.register'))
            pwd_hash = generate_password_hash(pwd)
            new_user = User(name=uname, password_hash=pwd_hash, emailid=email, phone=phone, postcode=postcode)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('auth.register'))
    else:
        return render_template('user.html', form=register, heading='Register')

@authbp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    error = None
    if(login_form.validate_on_submit()==True):
        user_name = login_form.user_name.data
        password = login_form.password.data
        user = User.query.filter_by(name=user_name).first()
        if user is None:
            error = 'Incorrect username or password'
        elif not check_password_hash(user.password_hash, password):
            error = 'Incorrect username or password'
        if error is None:
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            flash(error)
    return render_template('user.html', form=login_form, heading='Login')

@authbp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
