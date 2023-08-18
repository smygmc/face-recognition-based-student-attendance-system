from datetime import datetime
from sqlalchemy import insert
from flask import Blueprint,render_template,request,flash,jsonify,Response,redirect,url_for, current_app as app
from flask_login import login_required,current_user
from .models import Note,User,Attendance, Teaches, Takes, Course,Attendance_Batch
from . import db
import json
from recognition_package import recognition
import cv2
import face_recognition
from werkzeug.security import generate_password_hash
import numpy as np
import datetime
from . import insert_attendance






views=Blueprint('views',__name__)


@views.route('/teacher-home',methods=['GET','POST'])
@login_required
def teacher_home():

    courses = db.session.query(Course.course_title).join(Teaches).filter(Teaches.teacher_id==current_user.id)
    if request.method=='GET':
        courses = db.session.query(Course.course_title).join(Teaches).filter(Teaches.teacher_id==current_user.id)
        return render_template("teacher_home.html", user=current_user,courses=courses)

    if request.method=='POST':
        note=request.form.get('note')

        if len(note)<1:
            flash('Note is too short',category='error')
        else:
            new_note=Note(data=note,user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!',category='success')
            return render_template("teacher_home.html",user=current_user,courses=courses)

    return render_template("teacher_home.html",user=current_user,courses=courses)

@views.route('/')
def home():
    print("views.home")
    if current_user.is_authenticated:
        if current_user.role=="teacher":
            return teacher_home()
        elif current_user.role=="student":
            return student_home()
        elif current_user.role=="admin":
            return admin_board()
        else:
            return render_template("role_not_assigned_home.html", user=current_user)
    else:
        return render_template("home.html",user=current_user)


@views.route('/student-home')
@login_required
def student_home():
    #courses = db.session.query(Course.course_title).join(Takes).filter(Takes.student_id == current_user.id)
    courses = db.session.query(Course.course_title,Course.weekday_string,Course.start_time,Course.end_time).join(Takes).filter(Takes.student_id == current_user.id)

    if request.method == 'GET':
        #courses = db.session.query(Course.course_title).join(Takes).filter(Takes.student_id == current_user.id)
        courses = db.session.query(Course.course_title,Course.weekday_string, Course.start_time, Course.end_time).join(Takes).filter(
            Takes.student_id == current_user.id)

        return render_template("student_home.html", user=current_user, courses=courses)
    return render_template("student_home.html",user=current_user,courses=courses)


@views.route('/admin-board',methods=['GET','POST'])
@login_required
def admin_board():
    print("views.admin-board")
    attendance_all=Attendance_Batch.query.order_by(Attendance_Batch.course_id).all()

    users=db.session.execute(db.select(User).order_by(User.first_name)).scalars()
    if request.method=='GET':
        attendance_all =Attendance_Batch.query.order_by(Attendance_Batch.course_id).all()

        users = db.session.execute(db.select(User).order_by(User.first_name)).scalars()
        return render_template("admin_manager.html", user=current_user, users=users,attendance_all=attendance_all)

    if request.method=='POST':
        email=request.form.get('email')
        first_name=request.form.get('firstName')
        password1=request.form.get('password1')
        role=request.form.get('role')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.',category='error')
        elif len(email)<4:
            flash('Email must be greater than for characters.',category='error')
        elif len(first_name)<2:
            flash('First name must be greater than 2 characters.',category='error')
        elif len(password1)<7:
            flash('Passwords must be at least 7 characters.', category='error')
        elif role !='teacher' and role !='student':
            flash("Role must be either 'teacher' or 'student'.", category='error')
        else:
            new_user = User(email=email,first_name=first_name,password=generate_password_hash(password1,method='sha256'),role=role)
            db.session.add(new_user)
            db.session.commit()
            flash('User created!',category='success')
            return redirect(url_for('views.admin_board'))


    return render_template("admin_manager.html",user=current_user,users=users,attendance_all=attendance_all)

@views.route('/admin-board/users',methods=['GET','POST'])
@login_required
def users():


    users = db.session.execute(db.select(User).order_by(User.first_name)).scalars()
    if request.method == 'GET':
        users = db.session.execute(db.select(User).order_by(User.first_name)).scalars()
        return render_template("users.html", user=current_user, users=users)

    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        role = request.form.get('role')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than for characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 2 characters.', category='error')
        elif len(password1) < 7:
            flash('Passwords must be at least 7 characters.', category='error')
        elif role != 'teacher' and role != 'student':
            flash("Role must be either 'teacher' or 'student'.", category='error')
        else:
            new_user = User(email=email, first_name=first_name,
                            password=generate_password_hash(password1, method='sha256'), role=role)
            db.session.add(new_user)
            db.session.commit()
            flash('User created!', category='success')
            return redirect(url_for('views.users'))

@views.route('/admin-board/courses',methods=['GET'])
@login_required
def courses():
    courses = db.session.execute(db.select(Course).order_by(Course.course_id)).scalars()
    if request.method == 'GET':
        return render_template("courses.html", user=current_user, courses=courses)

@views.route('/delete-note',methods=['POST'])
@login_required
def delete_note():
    note=json.loads(request.data)
    noteId=note['noteId']
    note=Note.query.get(noteId)
    if note:
        if note.user_id==current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/delete-user',methods=['POST'])
@login_required
def delete_user():
    user=json.loads(request.data)
    userId=user['userId']
    user=User.query.get(userId)

    db.session.delete(user)
    db.session.commit()

    return jsonify({})

@views.route('/admin-attendance')
@login_required
def admin_attendance():
    attendance_all = Attendance_Batch.query.order_by(Attendance_Batch.course_id).all()
    courses =db.session.execute(db.select(Course).filter(Course.course_id==Attendance_Batch.course_id).order_by(Course.course_id)).scalars()
    users=db.session.query(User.first_name).join(Attendance_Batch).filter(Attendance_Batch.student_id == User.id).all()
    if request.method=='GET':
        attendance_all =Attendance_Batch.query.order_by(Attendance_Batch.course_id).all()
        courses = db.session.query(Course.course_title).join(Attendance_Batch).filter(Attendance_Batch.course_id == Course.course_id).all()
        users = db.session.query(User.first_name).join(Attendance_Batch).filter(Attendance_Batch.student_id == User.id).all()
        return render_template("admin_attendance.html", user=current_user, users=users,attendance_all=attendance_all,courses=courses,zip=zip)





url = "http://192.168.1.4:8080/video"
camera = cv2.VideoCapture(url)
fr = recognition.FaceRecognition()
names=fr.known_face_names
ids=[25,22,23,19,18,16,20,14,17,15,13,21]
names_ids={}
for name,id in zip(names,ids):
    names_ids[name]=id


def helper_get_course():
    today=datetime.datetime.now().weekday() #bugün haftanın hangi günü
    hour=datetime.datetime.now().hour
    course = db.session.query(Course).filter(hour>=Course.start_time).filter(hour<Course.end_time).all()
    if(len(course)==0):
        return [False]
    else:
        students = db.session.query(User).join(Takes).filter(Takes.course_id == course[0].course_id).all()
        teacher = db.session.query(Teaches).filter(Teaches.course_id == course[0].course_id).all()
        return [course[0],students,teacher[0]]


COURSE_ID=0
TEACHER_ID=0





def generate_frames():
    while True:
        ret, frame = camera.read()
        frame = cv2.resize(frame, (0, 0), fx=0.4, fy=0.4)
        # Only process every other frame of video to save time
        if fr.process_current_frame:
            # Resize frame of video to 1/4 size for faster face recognition processing
            # scale_percent=60
            # width=int(frame.shape[1]*scale_percent/100)
            # height=int(frame.shape[0]*scale_percent/100)
            # dim=(width,height)
            # small_frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)  #(width,heigt)
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            # rgb_small_frame = small_frame[:, :, ::-1]
            rgb_small_frame = face_image = cv2.cvtColor(small_frame,
                                                        cv2.COLOR_BGR2RGB)  # When you use opencv (imread, VideoCapture),
            # the images are loaded in the BGR color space.

            # Find all the faces and face encodings in the current frame of video
            fr.face_locations = face_recognition.face_locations(rgb_small_frame)
            fr.face_encodings = face_recognition.face_encodings(rgb_small_frame,fr.face_locations, model="small")

            fr.face_names = []
            for face_encoding in fr.face_encodings:
                # See if the face is a match for the known face(s)
                # matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                # print(matches)
                name = "Unknown"
                # confidence = '???'

                # Calculate the shortest distance to face
                face_distances = face_recognition.face_distance(fr.known_face_encodings, face_encoding)

                best_match_index = np.argmin(face_distances)
                # print(matches[best_match_index])
                # if matches[best_match_index]:
                if face_distances[best_match_index] <= 0.5:
                    name = fr.known_face_names[best_match_index]
                    fr.mark_attendance(name,COURSE_ID,names_ids[name],TEACHER_ID)
                    insert_attendance(name,COURSE_ID,names_ids[name],TEACHER_ID)

                    #confidence = face_confidence(face_distances[best_match_index])

                fr.face_names.append(f'{name}')

        fr.process_current_frame = not fr.process_current_frame

        # Display the results
        for (top, right, bottom, left), name in zip(fr.face_locations, fr.face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Create the frame with the name
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
@views.route('/attendance-teacher',methods=['GET','POST'])
def attendace_teacher():
    pass

@views.route('/index')
def index():
    _x_=helper_get_course()
    if len(_x_)==1:
        return render_template('no_lecture.html')
    else:
        course_title=_x_[0].course_title
        global COURSE_ID
        COURSE_ID=_x_[0].course_id
        global TEACHER_ID
        TEACHER_ID=_x_[2].teacher_id
        students=_x_[1]
        return render_template('index.html',course_title=course_title,students=students)


@views.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

