from flask import Blueprint, render_template,request, flash,redirect,url_for
from .models import User
from werkzeug.security import generate_password_hash,check_password_hash
from . import db
from flask_login import login_user,login_required,logout_user,current_user

auth=Blueprint('auth',__name__)


@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form.get('email')
        password = request.form.get('password')

        user=User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash('logged in successfully!',category='success')
                login_user(user,remember=True)

                if (user.role == "teacher"):
                    return redirect(url_for('views.teacher_home'))
                elif(user.role=="admin"):
                    return redirect(url_for('views.admin_board'))
                else:
                    return redirect(url_for('views.student_home'))


            else:
                flash('Incorrect password, try again.',category='error')
        else:
            flash('Email does not exist.',category='error')

    return render_template("login.html",user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up',methods=['GET','POST'])
def sign_up():
    if request.method=='POST':
        email=request.form.get('email')
        first_name=request.form.get('firstName')
        password1=request.form.get('password1')
        password2=request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.',category='error')
        elif len(email)<4:
            flash('Email must be greater than for characters.',category='error')
        elif len(first_name)<2:
            flash('First name must be greater than 2 characters.',category='error')
        elif password1!=password2:
            flash('Passwords are not matching.', category='error')
        elif len(password1)<7:
            flash('Passwords must be at least 7 characters.', category='error')
        else:

            role="student"
            new_user=User(email=email,first_name=first_name,password=generate_password_hash(password1,method='sha256'),role=role)
            db.session.add(new_user)
            db.session.commit()
            login_user(current_user, remember=True)
            flash('Account created!',category='success')
            return redirect(url_for('auth.login'))

    return render_template("sign_up.html",user=current_user)