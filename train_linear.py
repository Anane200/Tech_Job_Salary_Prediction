import pickle

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

DATA_PATH = "Data/job_salary_prediction_dataset.csv"
MODEL_PATH = "linear_salary_model.pkl"

df = pd.read_csv(DATA_PATH)

df["experience_squared"] = df["experience_years"] ** 2
df["experience_cubed"] = df["experience_years"] ** 3
df["exp_skills_interaction"] = df["experience_years"] * df["skills_count"]
df["exp_cert_interaction"] = df["experience_years"] * df["certifications"]
df["skills_cert_interaction"] = df["skills_count"] * df["certifications"]
df["skills_per_year"] = df["skills_count"] / (df["experience_years"] + 1)
df["total_qualifications"] = df["skills_count"] + (df["certifications"] * 2)
df["experience_level"] = pd.cut(
    df["experience_years"],
    bins=[-1, 2, 5, 10, 15, 20],
    labels=["Entry", "Junior", "Mid", "Senior", "Expert"],
)

categorical_cols = [
    "job_title",
    "education_level",
    "industry",
    "company_size",
    "location",
    "remote_work",
    "experience_level",
]
df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

X = df_encoded.drop("salary", axis=1)
y = df_encoded["salary"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

pipeline = Pipeline(
    [
        ("scaler", StandardScaler()),
        ("model", LinearRegression()),
    ]
)
pipeline.fit(X_train, y_train)

y_pred = pipeline.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
rmse = mean_squared_error(y_test, y_pred) ** 0.5
r2 = r2_score(y_test, y_pred)
print(f"Linear Regression on hold-out test set:")
print(f"  MAE  = {mae:,.2f}")
print(f"  RMSE = {rmse:,.2f}")
print(f"  R^2  = {r2:.4f}")

with open(MODEL_PATH, "wb") as f:
    pickle.dump(pipeline, f)
print(f"Saved: {MODEL_PATH}")
