from flask import render_template, request, redirect, url_for, flash
from app import app, db
from app.models import Employee, User
from app import forms
from flask_login import login_user, logout_user, login_required, current_user
# post functions


def index():
    employees = Employee.query.all()
    return render_template('index.html', employees=employees)


@login_required
def employee_create():
    form = forms.EmployeeForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            fullname = request.form.get('fullname')
            phone = request.form.get('phone')
            short_info = request.form.get('short_info')
            experience = request.form.get('experience')
            preferred_position = request.form.get('preferred_position')
            user = current_user.id
            new_employee = Employee(fullname=fullname, phone=phone, short_info=short_info, experience=experience,
                                    preferred_position=preferred_position, user_id=user)
            db.session.add(new_employee)
            db.session.commit()
            return redirect(url_for('index'))
        if form.errors:
            for errors in form.errors.values():
                for error in errors:
                    flash(error, category='danger')
    return render_template('employee_create.html', form=form)


def employee_detail(employee_id):
    form = forms.EmployeeForm()
    employee = Employee.query.filter_by(id=employee_id).first()
    if employee:
        return render_template('employee_detail.html', employee=employee, form=form)
    else:
        flash('Сотрудник не найден', category='danger')
        return redirect(url_for('index'))


@login_required
def employee_delete(employee_id):
    employee = Employee.query.filter_by(id=employee_id).first()
    if employee:
        if request.method == 'POST':
            db.session.delete(employee)
            db.session.commit()
            flash('Сотрудник успешно удален', category='success')
            return redirect(url_for('index'))
        else:
            form = forms.EmployeeForm()
            return render_template('employee_delete.html', employee=employee, form=form)
    else:
        flash('Сотрудник не найден', category='danger')
        return redirect(url_for('index'))


@login_required
def employee_update(employee_id):
    employee = Employee.query.filter_by(id=employee_id).first()
    if employee:
        form = forms.EmployeeForm(obj=employee)
        if request.method == 'POST':
            if form.validate_on_submit():
                fullname = request.form.get('fullname')
                phone = request.form.get('phone')
                short_info = request.form.get('short_info')
                experience = request.form.get('experience')
                preferred_position = request.form.get('preferred_position')
                employee.fullname = fullname
                employee.phone = phone
                employee.item = short_info
                employee.quantity = experience
                employee.price = preferred_position
                employee.user_id = current_user.id
                db.session.commit()
                flash('Данные успешно изменены', category='success')
                return redirect(url_for('index'))
            if form.errors:
                for errors in form.errors.values():
                    for error in errors:
                        flash(error, category='danger')
        return render_template('employee_update.html', form=form, employee=employee)
    else:
        flash('Сотрудник не найден', category='danger')
        return redirect(url_for('index'))

# user functions


def register():
    form = forms.UserForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User(username=request.form.get('username'), password=request.form.get('password'))
            db.session.add(user)
            db.session.commit()
            flash('Вы успешно зарегестрировались', category='success')
            return redirect(url_for('index'))
        if form.errors:
            for errors in form.errors.values():
                for error in errors:
                    flash(error, category='danger')
    return render_template('register.html', form=form)


def login():
    form = forms.UserForm()
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user and user.check_password(request.form.get('password')):
            login_user(user)
            flash('Вы успешно аутентентифицировались', category='success')
            return redirect(url_for('index'))
        else:
            flash('Неверный логин или пароль', category='danger')
        if form.errors:
            for errors in form.errors.values():
                for error in errors:
                    flash(error, category='danger')
    return render_template('login.html', form=form)


def logout():
    logout_user()
    flash('Вы вышли из учетной записи', category='success')
    return redirect(url_for('index'))
