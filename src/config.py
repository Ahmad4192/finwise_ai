"""
Configuration module for FinWise AI
Handles environment variables, form options, and application settings
"""

import os
from dotenv import load_dotenv
from typing import List, Dict, Any

# Load environment variables from .env file
load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# Application Settings
APP_TITLE = "FinWise AI"
APP_SUBTITLE = "AI-Powered Personal Financial Analysis and Smart Budget Assistant"
APP_DESCRIPTION = "Educational financial analysis tool - for informational purposes only"

# Educational Disclaimer
EDUCATIONAL_DISCLAIMER = """
**IMPORTANT - EDUCATIONAL USE ONLY**

This application is an educational prototype. It does NOT provide guaranteed investment advice,
execute financial transactions, connect to real bank accounts, or claim that any financial outcome is guaranteed.

All outputs are for informational purposes only. Please consult with a qualified financial professional
before making any financial decisions.

FinWise AI is not responsible for any financial losses or decisions made based on this tool.
"""

# Currency Options
CURRENCY_OPTIONS = [
    "USD - US Dollar",
    "EUR - Euro",
    "GBP - British Pound",
    "JPY - Japanese Yen",
    "CAD - Canadian Dollar",
    "AUD - Australian Dollar",
    "SGD - Singapore Dollar",
    "HKD - Hong Kong Dollar",
    "INR - Indian Rupee",
    "CNY - Chinese Yuan"
]

# Financial Goal Options
FINANCIAL_GOAL_OPTIONS = [
    "Save money",
    "Build emergency fund",
    "Pay off debt",
    "Save for vacation",
    "Start a business",
    "Improve budgeting",
    "Invest for future",
    "Buy a home",
    "Retirement planning",
    "Other"
]

# Expense Categories
EXPENSE_CATEGORIES = [
    "Housing/Rent",
    "Food & Groceries",
    "Transportation",
    "Utilities",
    "Education",
    "Healthcare",
    "Entertainment",
    "Loan/Debt Payments",
    "Insurance",
    "Other"
]

# Default Expense Values
DEFAULT_EXPENSES = {
    "Housing/Rent": 0.0,
    "Food & Groceries": 0.0,
    "Transportation": 0.0,
    "Utilities": 0.0,
    "Education": 0.0,
    "Healthcare": 0.0,
    "Entertainment": 0.0,
    "Loan/Debt Payments": 0.0,
    "Insurance": 0.0,
    "Other": 0.0
}

# Financial Health Score Bands
FINANCIAL_HEALTH_BANDS = {
    "STRONG": {"min": 80, "max": 100, "color": "green", "label": "Strong"},
    "HEALTHY": {"min": 60, "max": 79, "color": "blue", "label": "Generally Healthy"},
    "NEEDS_IMPROVEMENT": {"min": 40, "max": 59, "color": "orange", "label": "Needs Improvement"},
    "HIGH_ATTENTION": {"min": 0, "max": 39, "color": "red", "label": "High Attention Required"}
}

# Risk Level Configuration
RISK_LEVELS = {
    "LOW": {"color": "#28a745", "label": "Low Risk", "icon": "✅"},
    "MEDIUM": {"color": "#ffc107", "label": "Medium Risk", "icon": "⚠️"},
    "HIGH": {"color": "#fd7e14", "label": "High Risk", "icon": "🔴"},
    "EMERGENCY": {"color": "#dc3545", "label": "Emergency", "icon": "🚨"}
}

# Cache Configuration
CACHE_OPTIONS = [
    "InMemoryCache (RAM - Fastest, session only)",
    "SQLiteCache (Disk - Persistent across sessions)"
]

# Model Configuration Options
MODEL_OPTIONS = [
    "gpt-4o-mini",
    "gpt-4o",
    "gpt-3.5-turbo",
    "gpt-4"
]

# Temperature Settings
TEMPERATURE_OPTIONS = {
    "Conservative": 0.3,
    "Balanced": 0.7,
    "Creative": 1.0
}

def get_currency_symbol(currency: str) -> str:
    currency_map = {
        "USD - US Dollar": "$",
        "EUR - Euro": "€",
        "GBP - British Pound": "£",
        "JPY - Japanese Yen": "¥",
        "CAD - Canadian Dollar": "CA$",
        "AUD - Australian Dollar": "A$",
        "SGD - Singapore Dollar": "S$",
        "HKD - Hong Kong Dollar": "HK$",
        "INR - Indian Rupee": "₹",
        "CNY - Chinese Yuan": "¥"
    }
    return currency_map.get(currency, "$")

def get_health_score_band(score: float) -> Dict[str, Any]:
    for band_name, band_info in FINANCIAL_HEALTH_BANDS.items():
        if band_info["min"] <= score <= band_info["max"]:
            return band_info
    return FINANCIAL_HEALTH_BANDS["HIGH_ATTENTION"]

def get_risk_level_info(risk_level: str) -> Dict[str, Any]:
    return RISK_LEVELS.get(risk_level.upper(), RISK_LEVELS["MEDIUM"])