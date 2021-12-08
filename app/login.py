from app import app, db, login_manager
from .model import User, Objective, KeyResult
from .forms import LoginForm, RegisterForm, ChangeForm

from flask import Flask, render_template, redirect, url_for, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user


@app.route('/')
def index():
    return render_template('index.html')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated == True:
        message = 'Welcome back! ' + current_user.username + '!'
        flash(message, 'success')
        return redirect(url_for('my_okr'))

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                message = 'Successful login'
                flash(message, 'success')
                app.logger.warning('%s: %s' %(message, current_user.username))
                return redirect(url_for('my_okr'))
            message = 'Incorrect password'
            flash(message, 'danger')
            app.logger.warning('%s: %s' %(message, user.username))
            return redirect(url_for('login'))
        message = 'No existing username'
        flash(message, 'danger')
        return redirect(url_for('login'))
    if form.errors:
        message = 'Incorrect format'
        flash(message, 'danger')
    return render_template('login.html', form=form)

    
# sign up page


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if current_user.is_authenticated == True:
        message = 'Welcome back! ' + current_user.username + '!'
        flash(message, 'success')
        return redirect(url_for('my_okr'))

    if form.validate_on_submit():
        new_username = form.username.data
        new_email = form.email.data

        user_username = User.query.filter_by(username=new_username).first()
        if user_username:
            message = 'Existing username'
            flash(message, 'danger')
            return redirect(url_for('signup'))
        user_email = User.query.filter_by(email=new_email).first()
        if user_email:
            message = 'Existing email'
            flash(message, 'danger')
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(form.password.data, method='sha256') #generate hash 80 chars long
        new_user = User(username=new_username, email=new_email, password=hashed_password)
        db.session.add(new_user)
        try:
            db.session.commit()
            login_user(new_user)
            message = 'Successful registration'
            app.logger.info('%s: %s' %(message, new_username))
            flash(message, 'success')
        except Exception as e:
            message = 'Database error'
            app.logger.error('%s: %s' %(message, new_username))
            flash(message, 'danger')
            print(e)
            db.session.rollback()
        
        return redirect(url_for('my_okr'))
    if form.errors:
        message = 'Incorrect format'
        flash(message, 'danger')
    return render_template('signup.html', form=form)
# sign up page


@app.route('/change', methods=['GET', 'POST'])
def change():
    form = ChangeForm()

    if form.validate_on_submit():
        username = form.username.data
        old_password = form.old_password.data
        new_password = form.new_password.data

        user_username = User.query.filter_by(username=username).first()
        if user_username is None:
            message = 'No existing username'
            flash(message, 'danger')
            return redirect(url_for('change'))
        if check_password_hash(user_username.password, old_password) == False:
            message = 'Incorrect old password'
            flash(message, 'danger')
            app.logger.warning('%s: %s' %(message, username))
            return redirect(url_for('change'))

        hashed_password = generate_password_hash(new_password, method='sha256') #generate hash 80 chars long
        user_username.password = hashed_password
        try:
            db.session.commit()
            message = 'Successful password modification'
            flash(message, 'success')
            app.logger.warning('%s: %s' %(message, username))
        except Exception as e:
            message = 'Database error'
            flash(message, 'danger')
            app.logger.error('%s: %s' %(message, username))
            print(e)
            db.session.rollback()

        return redirect(url_for('login'))

    if form.errors:
        for error in form.errors:
            print(error)
        message = 'Incorrect format'
        flash(message, 'danger')
    return render_template('change.html', form=form)
