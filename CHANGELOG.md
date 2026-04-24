# Changelog

All notable changes to the Job Salary Prediction App project.

## [1.1.0] - 2026-04-24

### Fixed

- Removed bogus `np.exp` transform in the model training loop that
  was producing overflow warnings and nonsensical
  `predictions_original` values (the target was already raw salary).
- Resolved `KeyError` when selecting the best model from the results
  dataframe: `idxmax()` returned a positional index, not a model name.
- Fixed `NameError: y_pred_best is not defined` in the residuals and
  actual-vs-predicted cells by exposing the winning predictions from
  the selection cell.
- App: removed the broken log-inverse transform on predictions so
  predicted salaries are in the correct dollar range.
- App: stop loading an unused StandardScaler artefact that caused the
  app to fail on startup when it was missing.

### Changed

- Salary-prediction target is now clearly documented as raw USD; log
  transformation is only used for the EDA visualization.
- Generated plots are now written to `images/` (previously the repo
  root) so the streamlit Visualizations tab finds them.
- Narrowed bare `except:` blocks in `app.py` to `FileNotFoundError`.

### Added

- Comprehensive performance reporting in the notebook: ASCII metrics
  leaderboard, 5-fold cross-validation on the winner, MAPE + "within
  +/-10%" coverage, and a summary markdown cell.
- Headline model metrics panel in the streamlit sidebar.
- Graceful "run the notebook to regenerate" error when the model
  artefact is missing.

## [1.0.0] - 2024

### Added

#### Infrastructure
- Initialized git repository with proper .gitignore
- Added Python dependencies in requirements.txt
- Set up project structure for production deployment

#### Core Application
- Created Streamlit web application with responsive design
- Implemented custom CSS styling for professional UI
- Added caching mechanisms for optimal performance
- Integrated trained ML model and scaler loading

#### Feature Engineering
- Implemented non-linear experience transformations (squared, cubed)
- Added interaction features (experience × skills, experience × certifications, skills × certifications)
- Created derived features (skills per year, total qualifications)
- Implemented experience level binning (Entry, Junior, Mid, Senior, Expert)
- Built one-hot encoding pipeline matching training process

#### Prediction Interface
- Created interactive input form with 9 key features
- Added real-time salary prediction with log transformation
- Implemented salary breakdown (annual, monthly, hourly)
- Built interactive gauge visualization for salary ranges
- Added salary range estimation (±10%)

#### Data Insights
- Created salary statistics dashboard
- Added dataset overview metrics
- Implemented interactive category-based salary analysis
- Built dynamic bar charts with Plotly

#### Visualizations
- Integrated model performance plots
- Added actual vs predicted scatter plots
- Included residual analysis visualizations
- Displayed feature importance charts
- Showed salary transformation plots

#### Documentation
- Created comprehensive README.md
- Added QUICKSTART.md for easy onboarding
- Included usage examples and troubleshooting guide
- Documented all features and requirements

### Technical Details

#### Technologies Used
- **Frontend**: Streamlit 1.31.0
- **Data Processing**: Pandas 2.1.4, NumPy 1.26.3
- **Visualization**: Plotly 5.18.0
- **ML Framework**: Scikit-learn 1.4.0, XGBoost 2.0.3, LightGBM 4.3.0
- **Model Persistence**: Joblib 1.3.2

#### Model Specifications
- **Training Data**: 250,000 job records
- **Features**: 9 input features + engineered features
- **Target**: Log-transformed salary
- **Preprocessing**: StandardScaler normalization
- **Algorithm**: Gradient Boosting

### Commit History

1. `e67f947` - chore: initialize project with gitignore
2. `7a42378` - build: add project dependencies
3. `245052a` - feat: initialize streamlit app with basic configuration and styling
4. `33296df` - feat: add model and data loading functions with caching
5. `c5a9dd2` - feat: implement feature engineering and input preparation pipeline
6. `70fa3ab` - feat: add interactive prediction interface with input forms and results display
7. `b60e6ac` - feat: add interactive visualizations with plotly and multi-tab interface
8. `c4a3a7a` - docs: add comprehensive project documentation
9. `4631dc2` - chore: add trained model artifacts and dataset
10. `66edc0d` - docs: add quick start guide for easy onboarding

## Future Enhancements

- Add user authentication
- Implement prediction history tracking
- Add export functionality for predictions
- Create API endpoints for programmatic access
- Add more visualization options
- Implement A/B testing for model versions
