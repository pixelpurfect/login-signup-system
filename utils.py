import csv
import hashlib
from uuid import uuid4

USER_FILE = 'data/users.csv'
PATIENT_FILE = 'data/patients.csv'

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(email, password):
    with open(USER_FILE, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['email'] == email and row['verified'] == 'True':
                return hash_password(password) == row['password']
    return False

def user_exists(email):
    with open(USER_FILE, newline='') as f:
        reader = csv.DictReader(f)
        return any(row['email'] == email for row in reader)

def add_user(name, email, password, verified=False, verification_code='123456'):
    with open(USER_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([name, email, password, verified, verification_code])

def verify_user(email):
    users = []
    with open(USER_FILE, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['email'] == email:
                row['verified'] = 'True'
            users.append(row)

    with open(USER_FILE, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=users[0].keys())
        writer.writeheader()
        writer.writerows(users)

def add_patient(name, age, condition, caregiver_email):
    with open(PATIENT_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([str(uuid4()), name, age, condition, caregiver_email])

def get_patients_by_user(email):
    patients = []
    with open(PATIENT_FILE, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['caregiver_email'] == email:
                patients.append(row)
    return patients

def get_patient_by_id(patient_id):
    with open(PATIENT_FILE, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['id'] == patient_id:
                return row
    return None

def update_patient(patient_id, name, age, condition):
    patients = []
    with open(PATIENT_FILE, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['id'] == patient_id:
                row['name'] = name
                row['age'] = age
                row['condition'] = condition
            patients.append(row)
    with open(PATIENT_FILE, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=patients[0].keys())
        writer.writeheader()
        writer.writerows(patients)
