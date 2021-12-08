# this is the file for route and jump
from flask_login import current_user, login_required
from flask import request, redirect, url_for, flash
from flask_login import current_user

from app import app, db

from .model import Group
from .forms import GroupForm


@app.route("/group_submit", methods=["POST"])
@login_required
def group_submit():
    form = GroupForm()

    if form.validate_on_submit():
        group_name = form.group_name.data
        new_group = Group(group_name=group_name)
        db.session.add(new_group)
        new_group.members.append(current_user)
        try:
            db.session.commit()
            message = 'Create a group'
            flash(message, 'success')
            app.logger.info('%s: %s' %(message, current_user.username))
        except Exception as e:
            message = 'Database error'
            flash(message, 'danger')
            app.logger.error('%s: %s' %(message, current_user.username))
            print(e)
            db.session.rollback()
        return redirect(url_for("manage"))

    message = 'Incorrect format'
    flash(message, 'danger')
    return redirect(url_for("create"))
# group_submit an obj with title


@app.route("/join_submit/<int:group_id>")
@login_required
def join_submit(group_id):
    group = Group.query.filter_by(group_id=group_id).first()
    group.members.append(current_user)
    try:
        db.session.commit()
        message = 'Join in a group'
        flash(message, 'success')
        app.logger.info('%s: %s' %(message, current_user.username))
    except Exception as e:
        message = 'Database error'
        flash(message, 'danger')
        app.logger.error('%s: %s' %(message, current_user.username))
        print(e)
        db.session.rollback()

    return redirect(url_for("manage"))
# group_submit an obj with title


@app.route("/quit_submit/<int:group_id>")
@login_required
def quit_submit(group_id):
    group = Group.query.filter_by(group_id=group_id).first()
    if group:
        group.members.remove(current_user)
        db.session.commit()

    if group.members:
        pass
    else:
        db.session.delete(group)
        message = 'A group deleted'
        flash(message, 'warning')
        app.logger.warning('%s: %s' %(message, current_user.username))
        db.session.commit()
        return redirect(url_for("manage"))


    try:
        db.session.commit()
        message = 'Quit a group'
        flash(message, 'warning')
        app.logger.warning('%s: %s' %(message, current_user.username))

    except Exception as e:
        message = 'Database error'
        flash(message, 'danger')
        app.logger.error('%s: %s' %(message, current_user.username))
        print(e)
        db.session.rollback()

    return redirect(url_for("join"))
# group_submit an obj with title

