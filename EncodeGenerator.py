import cv2
import os
import face_recognition
import pickle
import firebase_admin
from click import format_filename
from firebase_admin import credentials, db, storage


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://asn-attendance-real-time-default-rtdb.firebaseio.com/",
    'storageBucket': "asn-attendance-real-time.firebasestorage.app"
})


#Importing the students images
folderPath = "Resources/Images"
PathList = os.listdir(folderPath)
imgList = []
studentIdList = []

for path in PathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    #print(os.path.splitext(path)[0])
    studentIdList.append(os.path.splitext(path)[0].split("_")[0])

    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)

print(studentIdList)


def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)
        if encode:
            encodeList.append(encode[0])

    return encodeList


print("Encoding Started.....")
encodeListKnown = findEncodings(imgList)
encodeListKnownIds = [encodeListKnown, studentIdList]
print("Encoding Completed")

file = open("EncodeFile.p", 'wb')
pickle.dump(encodeListKnownIds, file)
file.close()
print("File Saved!")
