import random
import array
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from sqlalchemy import insert
from werkzeug.security import generate_password_hash
import datetime

db=SQLAlchemy()
DB_NAME="database.db"


def create_app():
    app=Flask(__name__) # name of the file that ran ?

    app.config['SECRET_KEY']= 'staystrongkarabas' # its going to kinda encrypt or secure cookies and session data. dont share with anybody
    app.config['SQLALCHEMY_DATABASE_URI']=f'sqlite:///{DB_NAME}'

    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note,Teaches
    create_database(app)
    #printff(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


    return app


def printff(app):
    from .models import User, Course, Teaches, Takes,Attendance,Attendance_Batch

    date = f"{datetime.datetime.now().year}-{datetime.datetime.now().month}-{datetime.datetime.now().day}"
    hour = datetime.datetime.now().hour
    minute = datetime.datetime.now().minute
    day = datetime.datetime.now().day
    time = f"{hour}:{minute}"
    attendance = 1
    with app.app_context():
        new_att = Attendance_Batch(
                             course_id=4,
                             student_id=2,
                             enter_date=date,
                             enter_time=time,
                             attendance=attendance)

        db.session.add(new_att)
        db.session.commit()

def insert_attendance(name,course_id,student_id,teacher_id):
    from .models import User, Course, Teaches, Takes, Attendance, Attendance_Batch
    app=create_app()
    print(type(teacher_id))
    date = f"{datetime.datetime.now().year}-{datetime.datetime.now().month}-{datetime.datetime.now().day}"
    hour = datetime.datetime.now().hour
    minute = datetime.datetime.now().minute
    day = datetime.datetime.now().day
    time = f"{hour}:{minute}"
    attendance = 1
    try:
        with app.app_context():
            new_att=Attendance_Batch(
                course_id = course_id,
                student_id=student_id,
                enter_date=date,
                enter_time=time,
                attendance=attendance)
            db.session.add(new_att)
            db.session.commit()
    except:
        pass


def create_database(app):
    if not path.exists('website'+DB_NAME):
        with app.app_context():
            db.create_all()

        print('Created Database!')


