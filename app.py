from flask import Flask, render_template, request, redirect, url_for, session
import csv
import os
from utils import hash_password, check_password, user_exists, add_user, verify_user, add_patient, get_patients_by_user, get_patient_by_id, update_patient
from uuid import uuid4

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Use env variable in real app

DATA_FOLDER = 'data'

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = hash_password(request.form['password'])

        if user_exists(email):
            return 'User already exists.'

        verification_code = str(uuid4())[:6]
        add_user(name, email, password, verified=False, verification_code=verification_code)
        session['email'] = email
        return redirect(url_for('verify_email'))

    return render_template('signup.html')

@app.route('/verify-email', methods=['GET', 'POST'])
def verify_email():
    email = session.get('email')
    if request.method == 'POST':
        if request.form['code'] == '123456':  # Simulated fixed code
            verify_user(email)
            return redirect(url_for('login'))
        else:
            return 'Invalid code.'
    return render_template('verify_email.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if not check_password(email, password):
            return 'Invalid credentials or email not verified.'
        session['email'] = email
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'email' not in session:
        return redirect(url_for('login'))

    patients = get_patients_by_user(session['email'])
    return render_template('dashboard.html', patients=patients)

@app.route('/add-patient', methods=['POST'])
def add_patient_route():
    name = request.form['name']
    age = request.form['age']
    condition = request.form['condition']
    caregiver_email = session['email']
    add_patient(name, age, condition, caregiver_email)
    return redirect(url_for('dashboard'))

@app.route('/patient/<patient_id>', methods=['GET', 'POST'])
def patient_profile(patient_id):
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        condition = request.form['condition']
        update_patient(patient_id, name, age, condition)
        return redirect(url_for('dashboard'))

    patient = get_patient_by_id(patient_id)
    return render_template('patient_profile.html', patient=patient)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    if not os.path.exists('data'):
        os.makedirs('data')
    if not os.path.exists('data/users.csv'):
        with open('data/users.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'email', 'password', 'verified', 'verification_code'])
    if not os.path.exists('data/patients.csv'):
        with open('data/patients.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'name', 'age', 'condition', 'caregiver_email'])
    app.run(debug=True)
