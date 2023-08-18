#we gonna create database models here
from . import db #. means importing from the current package
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime,date
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


class Note(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    data=db.Column(db.String(10000))
    date=db.Column(db.DateTime(timezone=True),default=func.now())
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))#user lower case çünkü sql senin User diye yazdığını user olarak tutucak


class User(db.Model,UserMixin):
    id= db.Column(db.Integer,primary_key=True)
    role=db.Column(db.String(50))
    email=db.Column(db.String(150),unique=True)
    password=db.Column(db.String(150))
    first_name=db.Column(db.String(150))
    notes=db.relationship('Note')#ama relationship yaparken classın ismini direkt yazıyosun dont ask why

    # one to many relationship one user has many notes

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    course_id = db.Column(db.Integer, primary_key=True)
    course_title=db.Column(db.String(50))
    weekday_int = db.Column(db.Integer)
    weekday_string = db.Column(db.String(20))
    start_time = db.Column(db.String(150))
    end_time = db.Column(db.String(150))

class Takes(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    student_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    course_id=db.Column(db.Integer,db.ForeignKey('course.course_id'))

class Teaches(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'))

class Attendance(db.Model):
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'),primary_key=True)
    student_id=db.Column(db.Integer, db.ForeignKey('user.id'),primary_key=True)
    enter_date=db.Column(db.String(100),primary_key=True)
    enter_time=db.Column(db.String(150))
    attendance=db.Column(db.Integer,default=0) #0 means absent at first eveyrbody is absent

class Deneme(db.Model):
    id=db.Column(db.Integer, primary_key=True)

class Att(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'), primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    enter_date = db.Column(db.String(100), primary_key=True)
    enter_time = db.Column(db.String(150))
    attendance = db.Column(db.Integer, default=0)  # 0 means absent at first eveyrbody is absent

class Attendance_Batch(db.Model):
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'), primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    enter_date = db.Column(db.String(100), primary_key=True)
    enter_time = db.Column(db.String(150))
    attendance = db.Column(db.Integer, default=0)  # 0 means absent at first eveyrbody is absent