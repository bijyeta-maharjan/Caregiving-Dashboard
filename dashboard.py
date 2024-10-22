# import streamlit as st

# # Set page configuration
# st.set_page_config(page_title="Caregiving Facility Dashboard", layout="wide")

# # Sidebar menu
# st.sidebar.title("PathWell AI")
# st.sidebar.markdown("### Caregiving Facility Dashboard")
# menu = ["Patient Record", "Care Gaps", "Recommendations", "Care Quality"]
# choice = st.sidebar.radio("", menu)

# if choice == "Patient Record":
#     # Title for Patient Record
#     st.title("Patient Record")

#     # Create form layout for patient details
#     col1, col2 = st.columns(2)

#     with col1:
#         patient_name = st.text_input("Patient Name", "John Doe")
#         dob = st.text_input("Date of Birth", "05/15/1950")
#         allergies = st.text_area("Allergies", "Penicillin, Peanuts")
    
#     with col2:
#         mrn = st.text_input("MRN", "1234567")
#         gender = st.text_input("Gender", "Male")
#         primary_physician = st.text_input("Primary Physician", "Dr. Sarah Johnson")

#     # Current Medications section
#     st.subheader("Current Medications")
#     medications = st.text_area(
#         "Medications", 
#         "- Lisinopril 10mg, 1x daily\n- Metformin 500mg, 2x daily\n- Atorvastatin 20mg, 1x daily at bedtime"
#     )

#     # Medical History section
#     st.subheader("Medical History")
#     medical_history = st.text_area(
#         "Medical History", 
#         "- Hypertension (diagnosed 2010)\n- Type 2 Diabetes (diagnosed 2015)\n- Hyperlipidemia (diagnosed 2018)\n- Left hip replacement (2019)"
#     )

#     # Recent Vitals section
#     st.subheader("Recent Vitals")
#     recent_vitals = st.text_area(
#         "Recent Vitals", 
#         "- BP: 138/82 mmHg (06/15/2023)\n- HR: 72 bpm (06/15/2023)\n- Temp: 98.6°F (06/15/2023)\n- Weight: 180 lbs (06/15/2023)"
#     )


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Set up page configuration
st.set_page_config(
    page_title="Caregiving Dashboard",
    page_icon="🏥",
    layout="wide",
)

# Sidebar section: Filters
st.sidebar.header("Filters")
selected_patient = st.sidebar.text_input("Search by Patient MRN")

# Main header
st.title("Caregiving Dashboard 🏥")
st.write("Welcome to the caregiving dashboard. Use the filters on the left to explore patient records, vitals, care gaps, and recommendations.")

# Generate synthetic data
from faker import Faker
import random
import numpy as np

faker = Faker()
Faker.seed(42)
np.random.seed(42)

def random_date(start_date, end_date):
    return faker.date_between_dates(date_start=start_date, date_end=end_date)

# Generate patient data
num_patients = 100
patients_df, vitals_df, care_gaps_df, recommendations_df = None, None, None, None

def generate_patient_data():
    global patients_df, vitals_df, care_gaps_df, recommendations_df
    patients = []
    vitals_list = []
    care_gaps_list = []
    recommendations_list = []

    for _ in range(num_patients):
        # Generate patient records
        patient_record = {
            'Patient Name': faker.name(),
            'Date of Birth': faker.date_of_birth(minimum_age=40, maximum_age=90),
            'Gender': random.choice(['Male', 'Female']),
            'MRN': faker.unique.random_number(digits=7),
            'Primary Physician': faker.name()
        }
        patient_mrn = patient_record['MRN']
        patients.append(patient_record)

        # Generate vitals
        bp = np.random.normal(120, 10, 10).round(0).astype(int)
        hr = np.random.normal(72, 10, 10).round(0).astype(int)
        temp = np.random.normal(98.6, 0.7, 10).round(1)
        weight = np.random.normal(180, 20, 10).round(1)
        for i in range(10):
            vitals_list.append({
                'MRN': patient_mrn,
                'BP (mmHg)': f"{bp[i]}/{np.random.normal(80, 5, 1).round(0)[0]}",
                'HR (bpm)': hr[i],
                'Temp (F)': temp[i],
                'Weight (lbs)': weight[i],
                'Date': random_date(datetime(2022, 1, 1), datetime(2023, 12, 31))
            })

        # Generate care gaps
        for _ in range(random.randint(0, 3)):
            care_gaps_list.append({
                'MRN': patient_mrn,
                'Care Gap': random.choice([
                    'Missed blood pressure check',
                    'Skipped medication doses',
                    'Missed diabetes screening',
                    'No follow-up on cholesterol test'
                ]),
                'Gap Date': random_date(datetime(2022, 1, 1), datetime(2023, 12, 31))
            })

        # Generate recommendations
        recommendations_list.append({
            'MRN': patient_mrn,
            'Recommendation': random.choice([
                'Increase Lisinopril dosage for better BP control',
                'Dietary changes recommended to manage diabetes',
                'Consider statins for cholesterol management',
                'Exercise and weight management plan recommended'
            ]),
            'Recommendation Date': datetime.now().strftime("%Y-%m-%d")
        })

    patients_df = pd.DataFrame(patients)
    vitals_df = pd.DataFrame(vitals_list)
    care_gaps_df = pd.DataFrame(care_gaps_list)
    recommendations_df = pd.DataFrame(recommendations_list)

generate_patient_data()

# Filter patient data based on MRN
if selected_patient:
    try:
        selected_patient = int(selected_patient)
        filtered_patients = patients_df[patients_df['MRN'] == selected_patient]
        filtered_vitals = vitals_df[vitals_df['MRN'] == selected_patient]
        filtered_gaps = care_gaps_df[care_gaps_df['MRN'] == selected_patient]
        filtered_recommendations = recommendations_df[recommendations_df['MRN'] == selected_patient]
    except ValueError:
        st.error("Please enter a valid MRN.")
else:
    filtered_patients = patients_df
    filtered_vitals = vitals_df
    filtered_gaps = care_gaps_df
    filtered_recommendations = recommendations_df

# Section: Display Patient Details
st.subheader("Patient Details")
st.write(f"Showing {len(filtered_patients)} patient(s).")
st.dataframe(filtered_patients)

# Section: Vitals Data
st.subheader("Vitals History")
if not filtered_vitals.empty:
    st.dataframe(filtered_vitals)

    # Plot vital signs over time
    st.subheader("Vitals Trends")
    fig, ax = plt.subplots(2, 2, figsize=(12, 8))

    sns.lineplot(x='Date', y='BP (mmHg)', data=filtered_vitals, ax=ax[0, 0])
    ax[0, 0].set_title('Blood Pressure Over Time')

    sns.lineplot(x='Date', y='HR (bpm)', data=filtered_vitals, ax=ax[0, 1])
    ax[0, 1].set_title('Heart Rate Over Time')

    sns.lineplot(x='Date', y='Temp (F)', data=filtered_vitals, ax=ax[1, 0])
    ax[1, 0].set_title('Temperature Over Time')

    sns.lineplot(x='Date', y='Weight (lbs)', data=filtered_vitals, ax=ax[1, 1])
    ax[1, 1].set_title('Weight Over Time')

    st.pyplot(fig)
else:
    st.write("No vitals data available for the selected patient.")

# Section: Care Gaps
st.subheader("Care Gaps")
if not filtered_gaps.empty:
    st.dataframe(filtered_gaps)
else:
    st.write("No care gaps for the selected patient.")

# Section: Care Recommendations
st.subheader("Care Recommendations")
if not filtered_recommendations.empty:
    st.dataframe(filtered_recommendations)
else:
    st.write("No care recommendations for the selected patient.")
