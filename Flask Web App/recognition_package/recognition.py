import pathlib

import face_recognition
import sys
import cv2
import numpy as np
import math
import datetime
import pickle





class FaceRecognition:
    face_locations = []
    face_encodings = []
    face_names = []
    known_face_encodings = []
    known_face_names = []
    file_path="C:\\Users\\smygmc\\Desktop\\v-desktop\GP1\\Flask Web App\\recognition_package\\encodings_dic.pickle"
    process_current_frame = True

    def __init__(self):
       self.load_current_data()

    def load_current_data(self):
        with open(self.file_path, 'rb') as f:
            all_face_encodings = pickle.load(f)

        # Grab the list of names and the list of encodings
        self.known_face_names= list(all_face_encodings.keys())
        self.known_face_encodings = np.array(list(all_face_encodings.values()))


    def mark_attendance(self, name,course_id,student_id,teacher_id):

        with open('C:\\Users\\smygmc\\Desktop\\v-desktop\\GP1\\Flask Web App\\recognition_package\\attendance.csv', 'r+') as f:
            my_data_list = f.readlines()
            name_list = []
            for line in my_data_list:
                entry = line.split(',')
                name_list.append(entry[0])
            if name not in name_list:
                date=f"{datetime.datetime.now().year}-{datetime.datetime.now().month}-{datetime.datetime.now().day}"
                hour=datetime.datetime.now().hour
                minute=datetime.datetime.now().minute
                day=datetime.datetime.now().day
                time=f"{hour}:{minute}"
                attendance=1
                f.writelines(f'\n{name},{day},{teacher_id},{course_id},{student_id},{date},{time},{attendance}')



    def run_recognition(self):
        cam_url = "http://192.168.1.87:8080/video"
        video_capture = cv2.VideoCapture(0)

        if not video_capture.isOpened():
            sys.exit('Video source not found...')

        while True:
            ret, frame = video_capture.read()
            frame = cv2.resize(frame, (0, 0), fx=0.4, fy=0.4)
            # Only process every other frame of video to save time
            if self.process_current_frame:
                # Resize frame of video to 1/4 size for faster face recognition processing
                #scale_percent=60
                #width=int(frame.shape[1]*scale_percent/100)
                #height=int(frame.shape[0]*scale_percent/100)
                #dim=(width,height)
                #small_frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)  #(width,heigt)
                small_frame=cv2.resize(frame,(0,0),fx=0.25,fy=0.25)
                # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
                #rgb_small_frame = small_frame[:, :, ::-1]
                rgb_small_frame=face_image = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB) #When you use opencv (imread, VideoCapture),
                                                                             # the images are loaded in the BGR color space.


                # Find all the faces and face encodings in the current frame of video
                self.face_locations = face_recognition.face_locations(rgb_small_frame)
                self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations,model="small")

                self.face_names = []
                for face_encoding in self.face_encodings:
                    # See if the face is a match for the known face(s)
                    #matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                    #print(matches)
                    name = "Unknown"
                    #confidence = '???'

                    # Calculate the shortest distance to face
                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                    print(face_distances)
                    best_match_index = np.argmin(face_distances)
                    #print(matches[best_match_index])
                    #if matches[best_match_index]:
                    if face_distances[best_match_index]<=0.5:
                        name = self.known_face_names[best_match_index]
                        self.mark_attendance(name)
                        #confidence = face_confidence(face_distances[best_match_index])

                    self.face_names.append(f'{name}')

            self.process_current_frame = not self.process_current_frame

            # Display the results
            for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Create the frame with the name
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

            # Display the resulting image
            return frame

            # Hit 'q' on the keyboard to quit!
            #if cv2.waitKey(1) == ord('q'):
            #   break

        # Release handle to the webcam
        #video_capture.release()
        #cv2.destroyAllWindows()



