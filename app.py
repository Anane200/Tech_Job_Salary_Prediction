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
