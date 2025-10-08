# Selenium Demo

A simple, effective Selenium + Pytest demo.
Requires that chrome is installed.

## Features
- Headless Chrome
- Clean Pytest setup
- Simple test example

## Setup
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## Headless Run with Pytest
```bash
pytest -v
```

## Run with head in main
```bash
python test_google_search.py
```