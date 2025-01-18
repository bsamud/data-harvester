# Setup Guide

## Prerequisites
- Python 3.8+
- pip

## Installation
1. Clone repository
2. Install dependencies: `pip install -r requirements.txt`
3. Download spaCy model: `python -m spacy download en_core_web_sm`
4. Copy `.env.example` to `.env` and configure

## Configuration
Edit `appconfig.ini` for application settings.

## Running
```bash
python harvest_main.py
```
