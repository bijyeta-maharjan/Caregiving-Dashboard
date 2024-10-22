import random
import numpy as np
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta

# Initialize Faker and set seed for reproducibility
faker = Faker()
Faker.seed(42)
np.random.seed(42)

# Parameters
num_patients = 100
num_vitals_records = 200

# Helper function to generate random dates within a range
def random_date(start_date, end_date):
    return faker.date_between_dates(date_start=start_date, date_end=end_date)

# Generate random patient personal details
def generate_patient_record():
    return {
        'Patient Name': faker.name(),
        'Date of Birth': faker.date_of_birth(minimum_age=40, maximum_age=90),
        'Gender': random.choice(['Male', 'Female']),
        'MRN': faker.unique.random_number(digits=7),
        'Primary Physician': faker.name()
    }

# Generate allergies, medications, and medical history
def generate_medical_info():
    allergies = random.sample(['Penicillin', 'Peanuts', 'Sulfa', 'Aspirin'], k=random.randint(0, 2))
    medications = [
        {'drug': 'Lisinopril', 'dosage': '10mg', 'frequency': '1x daily'},
        {'drug': 'Metformin', 'dosage': '500mg', 'frequency': '2x daily'},
        {'drug': 'Atorvastatin', 'dosage': '20mg', 'frequency': '1x daily at bedtime'}
    ]
    medical_history = [
        {'condition': 'Hypertension', 'diagnosed': '2010'},
        {'condition': 'Type 2 Diabetes', 'diagnosed': '2015'},
        {'condition': 'Hyperlipidemia', 'diagnosed': '2018'},
        {'condition': 'Left hip replacement', 'diagnosed': '2019'}
    ]
    return {
        'Allergies': allergies,
        'Current Medications': random.sample(medications, k=random.randint(1, len(medications))),
        'Medical History': random.sample(medical_history, k=random.randint(1, len(medical_history)))
    }

# Generate vitals data (BP, HR, Temp, Weight)
def generate_vitals(patient_mrn):
    bp = np.random.normal(120, 10, num_vitals_records).round(0).astype(int)
    hr = np.random.normal(72, 10, num_vitals_records).round(0).astype(int)
    temp = np.random.normal(98.6, 0.7, num_vitals_records).round(1)
    weight = np.random.normal(180, 20, num_vitals_records).round(1)
    
    vitals = []
    for i in range(num_vitals_records):
        vitals.append({
            'MRN': patient_mrn,
            'BP (mmHg)': f"{bp[i]}/{np.random.normal(80, 5, 1).round(0)[0]}",
            'HR (bpm)': hr[i],
            'Temp (F)': temp[i],
            'Weight (lbs)': weight[i],
            'Date': random_date(datetime(2022, 1, 1), datetime(2023, 12, 31))
        })
    
    return pd.DataFrame(vitals)

# Generate care gaps (missed appointments, overdue tests)
def generate_care_gaps(patient_mrn):
    gaps = []
    for _ in range(random.randint(0, 3)):
        gaps.append({
            'MRN': patient_mrn,
            'Care Gap': random.choice([
                'Missed blood pressure check',
                'Skipped medication doses',
                'Missed diabetes screening',
                'No follow-up on cholesterol test'
            ]),
            'Gap Date': random_date(datetime(2022, 1, 1), datetime(2023, 12, 31))
        })
    return pd.DataFrame(gaps)

# Generate care recommendations based on medical history and vitals
def generate_recommendations(patient_mrn):
    recommendations = []
    recommendations.append({
        'MRN': patient_mrn,
        'Recommendation': random.choice([
            'Increase Lisinopril dosage for better BP control',
            'Dietary changes recommended to manage diabetes',
            'Consider statins for cholesterol management',
            'Exercise and weight management plan recommended'
        ]),
        'Recommendation Date': datetime.now().strftime("%Y-%m-%d")
    })
    return pd.DataFrame(recommendations)

# Generate patient records
def generate_patient_data(num_patients):
    patients = []
    vitals_list = []
    care_gaps_list = []
    recommendations_list = []

    for _ in range(num_patients):
        patient_record = generate_patient_record()
        patient_mrn = patient_record['MRN']
        patients.append(patient_record)

        # Generate associated vitals
        vitals = generate_vitals(patient_mrn)
        vitals_list.append(vitals)

        # Generate care gaps and recommendations
        care_gaps = generate_care_gaps(patient_mrn)
        care_gaps_list.append(care_gaps)

        recommendations = generate_recommendations(patient_mrn)
        recommendations_list.append(recommendations)

    # Combine data into DataFrames
    patients_df = pd.DataFrame(patients)
    vitals_df = pd.concat(vitals_list)
    care_gaps_df = pd.concat(care_gaps_list)
    recommendations_df = pd.concat(recommendations_list)

    return patients_df, vitals_df, care_gaps_df, recommendations_df

# Generate and display synthetic data
patients_df, vitals_df, care_gaps_df, recommendations_df = generate_patient_data(num_patients)

print("Patients Data:")
print(patients_df.head())
print("\nVitals Data:")
print(vitals_df.head())
print("\nCare Gaps:")
print(care_gaps_df.head())
print("\nRecommendations:")
print(recommendations_df.head())
