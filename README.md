# Face Recognition Attendance System

Real-time face recognition attendance system built using Python, OpenCV, and Firebase Realtime Database.
The system detects and recognizes faces through a webcam feed and automatically marks attendance.

---

## Features

* Real-time face detection and recognition
* Firebase Realtime Database integration
* Automatic attendance marking
* Live webcam recognition
* Student/User information management
* Face encoding storage
* Attendance timestamps and tracking

---

## Tech Stack

* Python
* OpenCV
* Firebase
* NumPy
* face_recognition
* cvzone
* Pickle

---

## Project Structure

```bash id="5kq4rn"
FaceAttendanceSystem/
│
├── main.py
├── EncodeGenerator.py
├── AddDataToDatabase.py
├── EncodeFile.p
├── serviceAccountKey.json
├── Images/
└── Resources/
```

---

## Installation

Clone the repository:

```bash id="f2pdqi"
git clone https://github.com/yourusername/face-attendance-system.git
cd face-attendance-system
```

Install dependencies:

```bash id="e0jnj9"
pip install -r requirements.txt
```

---

## Firebase Setup

1. Create a Firebase project
2. Enable Realtime Database
3. Generate Firebase Admin SDK private key
4. Rename the key file to:

```bash id="9wd5k6"
serviceAccountKey.json
```

5. Place it inside the project folder

---

## Running the Project

Generate face encodings:

```bash id="rkm6wa"
python EncodeGenerator.py
```

Upload data to Firebase:

```bash id="jlwmyl"
python AddDataToDatabase.py
```

Start the attendance system:

```bash id="4i6rd6"
python main.py
```

---

## How It Works

1. Faces are encoded and stored from reference images
2. Webcam captures live video feed
3. Detected faces are compared with stored encodings
4. If a match is found:

   * User data is fetched from Firebase
   * Attendance is marked automatically
   * Timestamp and attendance count are updated

---

## Demo Representation


---

## Future Improvements

* Better UI
* Multiple camera support
* Excel/CSV export
* Web dashboard
* Anti-spoofing system
* Cloud deployment

---

## Credits

Built while learning from tutorials by Murtaza's Workshop with additional Firebase realtime database integration and custom modifications.

---

## Author

Ahsin Memon

GitHub: https://github.com/ahsinmemon

LinkedIn: https://www.linkedin.com/in/ahsin-m/
