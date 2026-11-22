# Run this script from the LunarLens_ASTRA_Final folder in PowerShell.
if (-not (Test-Path ".\.venv\Scripts\python.exe")) {
    python -m venv .venv
}
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
& .\.venv\Scripts\python.exe -m streamlit run app.py
