
# this is the file for route and jump
from flask_login import current_user, login_required
from flask import request, redirect, url_for, flash
from app import app, db
from datetime import datetime

from .model import Objective, KeyResult
from .forms import ObjectiveForm, KeyResultForm, OKRForm


@app.route("/add", methods=["POST"])
@login_required
def add():
    form = ObjectiveForm()

    if form.validate_on_submit():
        today = datetime.today()
        new_obj = Objective(
            title=form.title.data, 
            date=today,
            owner_id=current_user.id,
            obj_per = 0
        )
        db.session.add(new_obj)
        try:
            db.session.commit()
            message = 'Add objective'
            flash(message, 'success')
            app.logger.info('%s: %s' %(message, current_user.username))
        except Exception as e:
            message = 'Database error'
            flash(message, 'danger')
            app.logger.error('%s: %s' %(message, current_user.username))
            print(e)
            db.session.rollback()
        return redirect(url_for("my_okr"))
    if form.errors:
        message = 'Failed to Add objective'
        flash(message, 'danger')
        app.logger.warning('%s: %s' %(message, current_user.username))
    return redirect(url_for("my_okr"))
# add an obj with title


@app.route("/enrich/<int:obj_id>", methods=["POST"])
@login_required
def enrich(obj_id):
    form = KeyResultForm()

    obj = Objective.query.filter_by(id=obj_id).first()
    if form.validate_on_submit():
        new_kr = KeyResult(
            dcp=form.dcp.data, 
            superior_id=obj_id, 
            now = 0,
            total = 1,
            step = 1,
            kr_per = 0,
            urgency = 'Neturalized',
            note = ''
        )
        db.session.add(new_kr)
        kr_list = KeyResult.query.filter_by(superior_id=obj.id).all()
        ave_per = 0
        for item in kr_list:
            ave_per += item.kr_per
        obj.obj_per = ave_per/float(len(kr_list))
        try:
            db.session.commit()
            message = 'Add Key Result'
            flash(message, 'success')
            app.logger.info('%s: %s' %(message, current_user.username))
        except Exception as e:
            message = 'Database error'
            flash(message, 'danger')
            app.logger.error('%s: %s' %(message, current_user.username))
            print(e)
            db.session.rollback()
        return redirect(url_for("my_okr"))
        
    if form.errors:
        message = 'Failed to add Key Result'
        flash(message, 'danger')
        app.logger.warning('%s: %s' %(message, current_user.username))
    return redirect(url_for("my_okr"))
# add an kr with title


@app.route("/delete_kr/<int:kr_id>")
@login_required
def delete_kr(kr_id):
    kr = KeyResult.query.filter_by(id=kr_id).first()
    obj = Objective.query.filter_by(id=kr.superior_id).first()

    db.session.delete(kr)

    kr_list = KeyResult.query.filter_by(superior_id=obj.id).all()
    ave_per = 0
    for item in kr_list:
        ave_per += item.kr_per
    length = len(kr_list)
    if length != 0:
        obj.obj_per = ave_per/float(len(kr_list))
    else:
        obj.obj_per = 0


    try:
        db.session.commit()
        message = 'Delete Key Result'
        flash(message, 'warning')
        app.logger.warning('%s: %s' %(message, current_user.username))
    except Exception as e:
        message = 'Database error'
        flash(message, 'danger')
        app.logger.error('%s: %s' %(message, current_user.username))
        print(e)
        db.session.rollback()

    return redirect(url_for("my_okr"))
# delete_kr specified obj

@app.route("/delete_obj/<int:obj_id>")
@login_required
def delete_obj(obj_id):
    obj = Objective.query.filter_by(id=obj_id).first()
    for item in obj.keyResults:
        kr = KeyResult.query.filter_by(id=item.id).first()
        db.session.delete(kr)
    db.session.delete(obj)
    try:
        db.session.commit()
        message = 'Delete Objective'
        flash(message, 'warning')
        app.logger.warning('%s: %s' %(message, current_user.username))
    except Exception as e:
        message = 'Database error'
        flash(message, 'danger')
        app.logger.error('%s: %s' %(message, current_user.username))
        print(e)
        db.session.rollback()
    return redirect(url_for("my_okr"))
# delete_obj specified obj


@app.route("/okr_submit/<int:kr_id>", methods=["POST"])
@login_required
def okr_submit(kr_id):
    kr = KeyResult.query.filter_by(id=kr_id).first()
    obj = Objective.query.filter_by(id=kr.superior_id).first()

    okr_form = OKRForm()
    if okr_form.validate_on_submit():

        obj.title = okr_form.title.data
        obj.date = datetime.strptime(
            str(okr_form.date.data),
            '%Y-%m-%d'
        ).date()
        kr.dcp = okr_form.dcp.data
        kr.now = okr_form.now.data
        kr.total = okr_form.total.data
        kr.step = okr_form.step.data
        kr.urgency = okr_form.urgency.data
        kr.note = okr_form.note.data


        kr.kr_per = int(kr.now)/int(kr.total)
        if kr.kr_per >= 1.0:
            kr.kr_per = 1

        kr_list = KeyResult.query.filter_by(superior_id=obj.id).all()
        ave_per = 0
        for item in kr_list:
            ave_per += item.kr_per
        obj.obj_per = ave_per/float(len(kr_list))

        try:
            db.session.commit()
            message = 'Modification submit'
            flash(message, 'success')
            app.logger.info('%s: %s' %(message, current_user.username))
        except Exception as e:
            message = 'Database error'
            flash(message, 'danger')
            app.logger.error('%s: %s' %(message, current_user.username))
            print(e)
            db.session.rollback()
    if okr_form.errors:
        message = 'Failed to submit modification'
        flash(message, 'danger')
        app.logger.warning('%s: %s' %(message, current_user.username))
    return redirect(url_for("my_okr"))
# okr_submit detail modification of obj

