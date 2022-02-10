import cv2
import numpy as np
import openpibo_face_models

gender_class = ['Male', 'Female']
gendernet = cv2.dnn.readNetFromCaffe(
                openpibo_face_models.filepath("deploy_gender.prototxt"),
                openpibo_face_models.filepath("gender_net.caffemodel")
            )
age_class = ['(0, 2)','(4, 6)','(8, 12)','(15, 20)','(25, 32)','(38, 43)','(48, 53)','(60, 100)']
agenet = cv2.dnn.readNetFromCaffe(
                    openpibo_face_models.filepath("deploy_age.prototxt"),
                    openpibo_face_models.filepath("age_net.caffemodel")
                )
face_detector = cv2.CascadeClassifier(openpibo_face_models.filepath("haarcascade_frontalface_default.xml"))

cap = cv2.VideoCapture(0)
_, img = cap.read()

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_detector.detectMultiScale(gray, 1.1, 5)
face = faces[0]

if not type(img) is np.ndarray:
    raise Exception('"img" must be image data from opencv')

if len(face) != 4:
    raise Exception('"face" must be [x,y,w,h]')

x, y, w, h = face
face_img = img[y:y+h, x:x+w].copy()
blob = cv2.dnn.blobFromImage(face_img, scalefactor=1, size=(227, 227),
    mean=(78.4263377603, 87.7689143744, 114.895847746),
    swapRB=False, crop=False)

# predict gender
gendernet.setInput(blob)
gender_preds = gendernet.forward()
gender = gender_class[gender_preds[0].argmax()]

# predict age
agenet.setInput(blob)
age_preds = agenet.forward()
age = age_class[age_preds[0].argmax()]

print(f'gender is {gender}, age is {age}')