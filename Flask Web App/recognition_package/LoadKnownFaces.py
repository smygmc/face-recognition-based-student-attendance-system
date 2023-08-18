import pathlib

import face_recognition
import os
import pickle


class Load:
    encodings_with_names = {}
    file_path="C:\\Users\\smygmc\\Desktop\\v-desktop\GP1\\Flask Web App\\recognition_package\\encodings_dic.pickle"

    def __init__(self):
         self.encode_faces()

    def encode_faces(self):
        for image in os.listdir('faces'):
            face_image = face_recognition.load_image_file(f"faces/{image}")
            name=image.__str__().split('.')[0]
            name=name.lower()
            face_encoding = face_recognition.face_encodings(face_image,num_jitters=10)[0]
            self.encodings_with_names[name]=face_encoding

        with open(self.file_path, 'wb') as f:
            pickle.dump(self.encodings_with_names, f)



Object=Load()

