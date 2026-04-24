import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image

@st.cache_resource
def load_model():
    return joblib.load('best_salary_model_improved.joblib')

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
    
    # Ensure same column order and select only feature columns (exclude salary)
    feature_cols = [c for c in df_temp_encoded.columns if c != 'salary']
    input_encoded = input_encoded[feature_cols]
    
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
    # Load model and data
    model = load_model()
    df = load_data()
    
    st.title("💰 Job Salary Prediction App")
    st.markdown("### Predict your expected salary based on job characteristics")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("📊 About")
        st.info(
            "This app uses machine learning to predict job salaries based on various factors "
            "including experience, education, skills, and more."
        )
        
        st.header("📈 Model Performance")
        try:
            img = Image.open('images/model_comparison_improved.png')
            st.image(img, use_container_width=True)
        except:
            st.warning("Model comparison image not found")
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["🔮 Prediction", "📊 Data Insights", "📈 Visualizations"])
    
    with tab1:
        st.header("Enter Job Details")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            job_title = st.selectbox(
                "Job Title",
                options=sorted(df['job_title'].unique()),
                help="Select the job title"
            )
            
            experience_years = st.slider(
                "Years of Experience",
                min_value=0,
                max_value=20,
                value=5,
                help="Total years of professional experience"
            )
            
            education_level = st.selectbox(
                "Education Level",
                options=sorted(df['education_level'].unique()),
                help="Highest education level achieved"
            )
        
        with col2:
            skills_count = st.slider(
                "Number of Skills",
                min_value=1,
                max_value=19,
                value=10,
                help="Total number of professional skills"
            )
            
            industry = st.selectbox(
                "Industry",
                options=sorted(df['industry'].unique()),
                help="Industry sector"
            )
            
            company_size = st.selectbox(
                "Company Size",
                options=sorted(df['company_size'].unique()),
                help="Size of the company"
            )
        
        with col3:
            location = st.selectbox(
                "Location",
                options=sorted(df['location'].unique()),
                help="Work location"
            )
            
            remote_work = st.selectbox(
                "Remote Work",
                options=sorted(df['remote_work'].unique()),
                help="Remote work arrangement"
            )
            
            certifications = st.slider(
                "Number of Certifications",
                min_value=0,
                max_value=5,
                value=2,
                help="Total number of professional certifications"
            )
        
        st.markdown("---")
        
        if st.button("🎯 Predict Salary"):
            with st.spinner("Calculating prediction..."):
                input_data = prepare_input(
                    job_title, experience_years, education_level, skills_count,
                    industry, company_size, location, remote_work, certifications, df
                )

                # The trained model regresses directly on raw salary, so the
                # prediction is already in dollars — no exp() transform needed.
                predicted_salary = float(model.predict(input_data)[0])
                
                # Display results
                st.success("✅ Prediction Complete!")
                
                result_col1, result_col2, result_col3 = st.columns(3)
                
                with result_col1:
                    st.metric(
                        label="Predicted Annual Salary",
                        value=f"${predicted_salary:,.0f}",
                        delta=None
                    )
                
                with result_col2:
                    monthly_salary = predicted_salary / 12
                    st.metric(
                        label="Monthly Salary",
                        value=f"${monthly_salary:,.0f}",
                        delta=None
                    )
                
                with result_col3:
                    hourly_rate = predicted_salary / (52 * 40)
                    st.metric(
                        label="Hourly Rate",
                        value=f"${hourly_rate:,.2f}",
                        delta=None
                    )
                
                # Salary gauge visualization
                st.markdown("### 📊 Salary Range Estimate")
                lower_bound = predicted_salary * 0.9
                upper_bound = predicted_salary * 1.1
                
                fig = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=predicted_salary,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Predicted Salary", 'font': {'size': 24}},
                    delta={'reference': df['salary'].median(), 'increasing': {'color': "green"}},
                    gauge={
                        'axis': {'range': [None, df['salary'].max()]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, lower_bound], 'color': "lightgray"},
                            {'range': [lower_bound, upper_bound], 'color': "lightgreen"},
                            {'range': [upper_bound, df['salary'].max()], 'color': "lightgray"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': df['salary'].median()
                        }
                    }
                ))
                
                st.plotly_chart(fig, use_container_width=True)
                st.info(f"💡 Estimated salary range: ${lower_bound:,.0f} - ${upper_bound:,.0f}")
    
    with tab2:
        st.header("Dataset Insights")
        
        insight_col1, insight_col2 = st.columns(2)
        
        with insight_col1:
            st.subheader("📈 Salary Statistics")
            stats_df = pd.DataFrame({
                'Metric': ['Mean', 'Median', 'Min', 'Max', 'Std Dev'],
                'Value': [
                    f"${df['salary'].mean():,.0f}",
                    f"${df['salary'].median():,.0f}",
                    f"${df['salary'].min():,.0f}",
                    f"${df['salary'].max():,.0f}",
                    f"${df['salary'].std():,.0f}"
                ]
            })
            st.dataframe(stats_df, use_container_width=True, hide_index=True)
        
        with insight_col2:
            st.subheader("🎯 Dataset Overview")
            overview_df = pd.DataFrame({
                'Attribute': ['Total Records', 'Features', 'Job Titles', 'Industries', 'Locations'],
                'Count': [
                    len(df),
                    len(df.columns) - 1,
                    df['job_title'].nunique(),
                    df['industry'].nunique(),
                    df['location'].nunique()
                ]
            })
            st.dataframe(overview_df, use_container_width=True, hide_index=True)
        
        st.subheader("📊 Salary Distribution by Category")
        
        category = st.selectbox(
            "Select Category",
            options=['job_title', 'education_level', 'industry', 'company_size', 'location', 'remote_work']
        )
        
        avg_salary = df.groupby(category)['salary'].mean().sort_values(ascending=False)
        
        fig = px.bar(
            x=avg_salary.values,
            y=avg_salary.index,
            orientation='h',
            labels={'x': 'Average Salary ($)', 'y': category.replace('_', ' ').title()},
            title=f'Average Salary by {category.replace("_", " ").title()}'
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.header("Model Visualizations")
        
        viz_col1, viz_col2 = st.columns(2)
        
        with viz_col1:
            try:
                st.subheader("🎯 Actual vs Predicted")
                img = Image.open('images/actual_vs_predicted_improved.png')
                st.image(img, use_container_width=True)
            except:
                st.warning("Actual vs Predicted image not found")
            
            try:
                st.subheader("📊 Residuals Plot")
                img = Image.open('images/residuals_improved.png')
                st.image(img, use_container_width=True)
            except:
                st.warning("Residuals image not found")
        
        with viz_col2:
            try:
                st.subheader("⭐ Feature Importance")
                img = Image.open('images/feature_importance.png')
                st.image(img, use_container_width=True)
            except:
                st.warning("Feature importance image not found")
            
            try:
                st.subheader("📈 Salary Transformation")
                img = Image.open('images/salary_transformation.png')
                st.image(img, use_container_width=True)
            except:
                st.warning("Salary transformation image not found")

if __name__ == "__main__":
    main()
