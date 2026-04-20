# 💰 Job Salary Prediction App

A machine learning-powered Streamlit application that predicts job salaries based on various factors including experience, education, skills, industry, and more.

## Features

- **Interactive Prediction**: Enter job details and get instant salary predictions
- **Visual Analytics**: Explore salary distributions across different categories
- **Model Insights**: View model performance metrics and feature importance
- **Responsive Design**: Clean, modern UI with intuitive navigation

## Installation

1. Clone or download this repository

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit app:
```bash
streamlit run app.py
```

The app will open in your default web browser at `http://localhost:8501`

## App Structure

### 🔮 Prediction Tab
- Enter job characteristics (title, experience, education, etc.)
- Get predicted annual, monthly, and hourly salary
- View salary range estimates with visual gauge

### 📊 Data Insights Tab
- Explore dataset statistics
- View salary distributions by category
- Interactive visualizations

### 📈 Visualizations Tab
- Model performance plots
- Feature importance analysis
- Residual plots
- Salary transformation visualizations

## Input Features

The model uses the following features for prediction:

- **Job Title**: Role/position
- **Experience Years**: 0-20 years
- **Education Level**: High School, Diploma, Bachelor, Master, PhD
- **Skills Count**: Number of professional skills (1-19)
- **Industry**: Business sector
- **Company Size**: Small, Medium, Large, Enterprise
- **Location**: Geographic location
- **Remote Work**: Yes, No, Hybrid
- **Certifications**: Number of professional certifications (0-5)

## Model Details

The app uses an advanced machine learning model trained on 250,000 job records with:

- **Feature Engineering**: Non-linear transformations, interaction features, derived metrics
- **Preprocessing**: StandardScaler for feature normalization
- **Target Transformation**: Log transformation for better prediction accuracy
- **Algorithm**: Gradient Boosting (LightGBM/XGBoost)

## Files

- `app.py`: Main Streamlit application
- `best_salary_model_improved.joblib`: Trained ML model
- `scaler_improved.joblib`: Feature scaler
- `Data/job_salary_prediction_dataset.csv`: Training dataset
- `images/`: Model visualization plots
- `requirements.txt`: Python dependencies
- `notebook.ipynb`: Model training notebook

## Requirements

- Python 3.8+
- Streamlit
- Pandas
- NumPy
- Scikit-learn
- Plotly
- Joblib
- Pillow

## Tips

- Adjust the input parameters to see how different factors affect salary predictions
- Explore the Data Insights tab to understand salary trends
- Check the Visualizations tab to see model performance metrics

## License

This project is open source and available for educational purposes.
