import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://asn-attendance-real-time-default-rtdb.firebaseio.com/"
})

ref = db.reference('Students')

data = {
    "12938":
    {
        "name": "Ahsin Memon",
        "major": "Computer Science",
        "starting_year": "2026",
        "total_attendance": 100,
        "GPA": 3.8,
        "year": 3,
        "last_attendance_time": "2026-06-25 00:24:43"
    },

    "23847":
    {
        "name": "Jake Gyllenhaal",
        "major": "Computer Engineering",
        "starting_year": "2014",
        "total_attendance": 128,
        "GPA": 2.9,
        "year": 4,
        "last_attendance_time": "2025-04-12 00:14:34"
    },

    "74631":
        {
            "name": "Robert Downey Jr",
            "major": "Artificial Intelligence",
            "starting_year": "2012",
            "total_attendance": 118,
            "GPA": 4.0,
            "year": 4,
            "last_attendance_time": "2022-08-28 00:11:55"
        }
}

for key, value in data.items():
    ref.child(key).set(value)