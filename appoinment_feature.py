import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect(':memory:') #creates temp
cursor = conn.cursor() #sql commands

cursor.execute(''' 
    CREATE TABLE Appointments(
               ID INTEGER PRIMARY KEY AUTOINCREMENT,
               PatientName TEXT NOT NULL,
               DoctorName TEXT NOT NULL,
               AppointmentDate DATE NOT NULL,
               AppointmentTime TEXT NOT NULL)
''')
conn.commit()


def create_appt(patient_name, doctor_name, date, time):
    try:
        time = datetime.strptime(time, '%H:%M').time()
    except ValueError:
        return 'Use 24 hour format.'
    
    if time < datetime.strptime('8:00', '%H:%M').time() or time > datetime.strptime('20:00', '%H:%M').time():
        return 'NY Health Clinic is only open 8AM - 8PM.'
    
    cursor.execute('SELECT * FROM Appointments WHERE DoctorName=? AND AppointmentDate=? AND AppointmentTime=?',
                   (doctor_name, date, time.strftime('%H:%M')))
    
    if cursor.fetchone():
        return 'Sorry that time is unavailable please select a different time.'
    
    cursor.execute('INSERT INTO Appointments (PatientName, DoctorName, AppointmentDate, AppointmentTime) VALUES (?,?,?,?)',
                   (patient_name, doctor_name, date, time.strftime('%H:%M')))
    conn.commit()

    return f"Appointment booked for {patient_name} with {doctor_name} at {time.strftime('%H:%M')} on {date}."

patient_name = input('Enter your name: \n')
doctor_name = input('The name of your doctor: \n')
date = input('Enter the appointment date (YYYY-MM-DD): \n')
time = input('Enter the time of the appointment (HH:MM): \n')
test_result = create_appt(patient_name, doctor_name, date, time)
print(test_result)

