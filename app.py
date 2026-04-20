import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load model and scaler
@st.cache_resource
def load_model():
    """Load the trained model and scaler"""
    model = joblib.load('best_salary_model_improved.joblib')
    scaler = joblib.load('scaler_improved.joblib')
    return model, scaler

# Load data for reference
@st.cache_data
def load_data():
    """Load the dataset for reference values"""
    return pd.read_csv('Data/job_salary_prediction_dataset.csv')

def create_features(data):
    """Create engineered features matching the training process"""
    # Non-linear experience effects
    data['experience_squared'] = data['experience_years'] ** 2
    data['experience_cubed'] = data['experience_years'] ** 3
    
    # Interaction features
    data['exp_skills_interaction'] = data['experience_years'] * data['skills_count']
    data['exp_cert_interaction'] = data['experience_years'] * data['certifications']
    data['skills_cert_interaction'] = data['skills_count'] * data['certifications']
    
    # Derived features
    data['skills_per_year'] = data['skills_count'] / (data['experience_years'] + 1)
    data['total_qualifications'] = data['skills_count'] + (data['certifications'] * 2)
    
    # Experience level bins
    data['experience_level'] = pd.cut(data['experience_years'], 
                                      bins=[-1, 2, 5, 10, 15, 20], 
                                      labels=['Entry', 'Junior', 'Mid', 'Senior', 'Expert'])
    
    return data

def prepare_input(job_title, experience_years, education_level, skills_count, 
                  industry, company_size, location, remote_work, certifications, df_reference):
    """Prepare input data for prediction"""
    # Create input dataframe
    input_data = pd.DataFrame({
        'job_title': [job_title],
        'experience_years': [experience_years],
        'education_level': [education_level],
        'skills_count': [skills_count],
        'industry': [industry],
        'company_size': [company_size],
        'location': [location],
        'remote_work': [remote_work],
        'certifications': [certifications]
    })
    
    # Create engineered features
    input_data = create_features(input_data)
    
    # One-hot encoding
    categorical_cols = ['job_title', 'education_level', 'industry', 'company_size', 
                        'location', 'remote_work', 'experience_level']
    input_encoded = pd.get_dummies(input_data, columns=categorical_cols, drop_first=True)
    
    # Get all columns from training data (excluding target)
    df_temp = df_reference.copy()
    df_temp = create_features(df_temp)
    df_temp_encoded = pd.get_dummies(df_temp, columns=categorical_cols, drop_first=True)
    
    # Align columns
    for col in df_temp_encoded.columns:
        if col not in input_encoded.columns and col != 'salary':
            input_encoded[col] = 0
    
    # Ensure same column order
    input_encoded = input_encoded[df_temp_encoded.drop('salary', axis=1).columns]
    
    return input_encoded

# Page configuration
st.set_page_config(
    page_title="Salary Prediction App",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        height: 3em;
        border-radius: 10px;
        font-size: 18px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.title("💰 Job Salary Prediction App")
    st.markdown("### Predict your expected salary based on job characteristics")
    st.markdown("---")
    
    st.info("Application initialized successfully!")

if __name__ == "__main__":
    main()
