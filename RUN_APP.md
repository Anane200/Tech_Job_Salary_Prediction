# How to Run the Salary Prediction App

## Step 1: Install Dependencies

First, you need to install the required Python packages. Try one of these commands:

### Option 1: Using pip
```bash
pip install -r requirements.txt
```

### Option 2: Using python -m pip
```bash
python -m pip install -r requirements.txt
```

### Option 3: Using py launcher (Windows)
```bash
py -m pip install -r requirements.txt
```

### Option 4: Using python3
```bash
python3 -m pip install -r requirements.txt
```

## Step 2: Run the Streamlit App

Once dependencies are installed, run:

```bash
streamlit run app.py
```

Or if streamlit is not in your PATH:

```bash
python -m streamlit run app.py
```

Or:

```bash
py -m streamlit run app.py
```

## Step 3: Access the App

The app will automatically open in your default browser at:
```
http://localhost:8501
```

If it doesn't open automatically, copy and paste that URL into your browser.

## Troubleshooting

### Python Not Found
If you get "python is not recognized", you may need to:
1. Install Python from https://www.python.org/downloads/
2. Or use `py` instead of `python` on Windows
3. Or add Python to your system PATH

### Streamlit Not Found After Installation
If streamlit is installed but not found, try:
```bash
python -m streamlit run app.py
```

### Port Already in Use
If port 8501 is busy, use a different port:
```bash
streamlit run app.py --server.port 8502
```

## Quick Test

To verify your Python installation:
```bash
python --version
```

To verify pip:
```bash
pip --version
```

## Need Help?

If you continue to have issues:
1. Check that Python 3.8+ is installed
2. Ensure pip is installed and updated
3. Try creating a virtual environment first (see QUICKSTART.md)
