# this is the file for route and jump
from flask_login import current_user, login_required, logout_user
from flask import render_template, request, redirect, url_for, flash
from app import app, db

from .model import Objective, KeyResult, Group, User
from .forms import ObjectiveForm, KeyResultForm, OKRForm, GroupForm

"""
These are views for main OKR,
which include:
    log out to index page
    main objective interface
    edit page of specified kr
    stream page
    help page
"""


@app.route('/logout')
@login_required
def logout():
    message = 'logged out'
    flash(message, 'success')
    app.logger.warning('%s: %s' %(message, current_user.username))
    logout_user()
    return redirect(url_for('login'))
# log out user

@app.route("/my_okr")
@login_required
def my_okr():
    obj_list = Objective.query.filter_by(owner_id=current_user.id).all()
    obj_form = ObjectiveForm()
    kr_form = KeyResultForm()
    return render_template("my_okr.html", 
        obj_list=obj_list, 
        obj_form=obj_form, 
        kr_form=kr_form, 
        name=current_user.username, 
        email=current_user.email
    )
# display main objective interface

@app.route("/edit/<int:kr_id>")
@login_required
def edit(kr_id):
    kr = KeyResult.query.filter_by(id=kr_id).first()
    obj = Objective.query.filter_by(id=kr.superior_id).first()
    okr_form = OKRForm(
        title=obj.title,
        date = obj.date,
        dcp = kr.dcp,
        now = kr.now,
        total = kr.total,
        step = kr.step,
        urgency=kr.urgency, 
        note=kr.note,
    )

    return render_template("description.html", okr_form=okr_form, kr_id=kr.id)
# jump to edit page of specified kr


@app.route("/stream")
@login_required
def stream():
    obj_list = Objective.query.order_by(Objective.date.desc()).filter_by(owner_id=current_user.id).all()
    return render_template(
        "stream.html", 
        obj_list=obj_list, 
        name=current_user.username,
        email=current_user.email
    )
# jump to stream page




"""
These are views for group,
which include:
    log out to index page
    main objective interface
    edit page of specified kr
    stream page
    help page
"""

@app.route("/join")
@login_required
def join():
    group_list = Group.query.filter_by().all()
    for group in current_user.attendences:
        group_list.remove(group)

    return render_template("join.html", 
        group_list=group_list, 
        name=current_user.username, 
        email=current_user.email
    )
# jump to join page

@app.route("/create")
@login_required
def create():
    group_form = GroupForm()
    return render_template(
        "create.html",
        group_form = group_form,
        name=current_user.username,
        email=current_user.email
    )
# jump to create page

@app.route("/manage")
@login_required
def manage():
    group_list = current_user.attendences
    return render_template("manage.html", 
        group_list=group_list, 
        name=current_user.username, 
        email=current_user.email
    )
# jump to manage page

@app.route("/view_okr/<int:user_id>")
@login_required
def view_okr(user_id):
    obj_list = Objective.query.filter_by(owner_id=user_id).all()
    obj_form = ObjectiveForm()
    kr_form = KeyResultForm()
    user = User.query.filter_by(id=user_id).first()
    user_name = user.username

    message = 'view ' + user_name + '\'s OKR'
    flash(message, 'info')
    app.logger.info('%s: %s' %(message, current_user.username))
    return render_template("view_okr.html", 
        obj_list=obj_list, 
        obj_form=obj_form, 
        kr_form=kr_form, 
        user_name=user_name,
        name=current_user.username, 
        email=current_user.email
    )
# display main objective interface








