import pickle
import cv2
import os
import cvzone
import face_recognition
import numpy as np
import firebase_admin
from firebase_admin import credentials, db, storage
from datetime import datetime


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://asn-attendance-real-time-default-rtdb.firebaseio.com/",
    'storageBucket': "asn-attendance-real-time.firebasestorage.app"
})

bucket = storage.bucket()

cap = cv2.VideoCapture(1)
cap.set(3,640)
cap.set(4,480)

imgBG = cv2.imread("./Resources/background.png")

#Importing the mode ui image to the list
modePathFolder = "./Resources/Modes"
modePathList = os.listdir(modePathFolder)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(modePathFolder, path)))


# Loading encoding file
file = open('EncodeFile.p', 'rb')
encodeListKnownIds = pickle.load(file)
file.close()
encodeListKnown, studentIdList = encodeListKnownIds
#print(studentIdList)

modeType = 0
counter = 0
id = -1
imgStudent = []

while True:
    success, img = cap.read()
    img = cv2.resize(img, (640,480))
    imgS = cv2.resize(img,(0,0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBG[162:162+480, 55:55+640] = img
    imgBG[44:44+633, 808:808+414] = imgModeList[modeType]

    # if connection.ConnectError:
    #     print("Connection Error")
    #     modeType = 4


    if faceCurFrame:

        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:

                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55+x1, 162+y1, x2-x1, y2-y1
                imgBG = cvzone.cornerRect(imgBG,bbox=bbox, rt=0)
                id = studentIdList[matchIndex]

                if counter == 0:
                    cvzone.putTextRect(imgBG, "Loading", (275, 400))
                    cv2.imshow("ASN Attendance", imgBG)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1

            if counter != 0:

                if counter == 1:
                    #Gathering Data
                    studentInfo = db.reference(f'Students/{id}').get()
                    print(studentInfo)

                    #Getting Image From database storage
                    blob = bucket.get_blob(f'Resources/Images/{id}_1.png')
                    array = np.frombuffer(blob.download_as_string(), np.uint8)
                    imgStudent = cv2.imdecode(array, cv2.IMREAD_COLOR)

                    #Updating the data for attendance
                    datetimeObject = datetime.strptime(studentInfo['last_attendance_time'], "%Y-%m-%d %H:%M:%S")
                    secondsElapsed = (datetime.now()-datetimeObject).total_seconds()
                    print(secondsElapsed)
                    if secondsElapsed > 30:
                        ref = db.reference(f'Students/{id}')
                        studentInfo['total_attendance'] += 1
                        ref.child('total_attendance').set(studentInfo['total_attendance'])
                        ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    else:
                        modeType = 3
                        counter = 0
                        imgBG[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                if modeType != 3:

                    if 10<counter<20:
                        modeType = 2

                    imgBG[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                    if counter <= 10:

                        cv2.putText(imgBG, str(studentInfo['total_attendance']), (861, 125), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1)
                        cv2.putText(imgBG, str(studentInfo['major']), (1006, 550), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                        cv2.putText(imgBG, str(id), (1006, 493), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                        cv2.putText(imgBG, str(studentInfo['GPA']), (910, 625), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 100, 100), 1)
                        cv2.putText(imgBG, str(studentInfo['year']), (1025, 625), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 100, 100), 1)
                        cv2.putText(imgBG, str(studentInfo['starting_year']), (1125, 625), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 100, 100), 1)

                        (w,h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_SIMPLEX, 1, 1)
                        offset = (414-w)//2
                        cv2.putText(imgBG, str(studentInfo['name']), (808+offset, 445), cv2.FONT_HERSHEY_SIMPLEX, 1, (55, 55, 55), 1)

                        imgBG[175:175+216, 909:909+216] = imgStudent

                    counter += 1

                    if counter >= 20:
                        counter = 0
                        modeType = 0
                        studentInfo = []
                        imgStudent = []
                        imgBG[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
    else:
        modeType = 0
        counter = 0



    cv2.imshow("ASN Attendance", imgBG)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break