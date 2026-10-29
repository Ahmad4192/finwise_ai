"""
Financial Calculator Module for FinWise AI
Performs deterministic financial calculations without AI
"""

from typing import Dict, Any
import math

def calculate_financial_metrics(
    monthly_income: float,
    expenses: Dict[str, float],
    current_savings: float
) -> Dict[str, Any]:
    """
    Calculate all financial metrics from user inputs.

    Args:
        monthly_income: User's monthly income
        expenses: Dictionary of expense categories and amounts
        current_savings: User's current monthly savings

    Returns:
        Dictionary containing all calculated financial metrics
    """
    total_expenses = sum(expenses.values())
    remaining_income = monthly_income - total_expenses

    if monthly_income > 0:
        savings_ratio = (current_savings / monthly_income) * 100
        expense_ratio = (total_expenses / monthly_income) * 100
    else:
        savings_ratio = 0.0
        expense_ratio = 0.0

    preliminary_score = calculate_preliminary_score(
        monthly_income, total_expenses, remaining_income,
        current_savings, savings_ratio, expense_ratio, expenses
    )

    expense_breakdown = {
        category: amount for category, amount in expenses.items() if amount > 0
    }

    return {
        "monthly_income": monthly_income,
        "total_expenses": total_expenses,
        "remaining_income": remaining_income,
        "current_savings": current_savings,
        "savings_ratio": savings_ratio,
        "expense_ratio": expense_ratio,
        "preliminary_score": preliminary_score,
        "expense_breakdown": expense_breakdown
    }

def calculate_preliminary_score(
    monthly_income: float,
    total_expenses: float,
    remaining_income: float,
    current_savings: float,
    savings_ratio: float,
    expense_ratio: float,
    expenses: Dict[str, float]
) -> float:
    """
    Calculate a weighted preliminary financial health score (0-100).
    """
    scores = []
    weights = []

    # Savings Ratio Score (30% weight)
    if monthly_income > 0:
        savings_score = min(savings_ratio / 20 * 100, 100)
    else:
        savings_score = 0
    scores.append(savings_score)
    weights.append(0.30)

    # Remaining Income Score (25% weight)
    if monthly_income > 0:
        if remaining_income >= monthly_income * 0.3:
            remaining_score = 100
        elif remaining_income >= monthly_income * 0.1:
            remaining_score = 75
        elif remaining_income >= 0:
            remaining_score = 50
        else:
            remaining_score = max(0, 50 + (remaining_income / monthly_income) * 50)
    else:
        remaining_score = 0
    scores.append(remaining_score)
    weights.append(0.25)

    # Expense Ratio Score (20% weight)
    if monthly_income > 0:
        if expense_ratio <= 50:
            expense_score = 100
        elif expense_ratio <= 80:
            expense_score = 100 - ((expense_ratio - 50) / 30 * 100)
        else:
            expense_score = max(0, 100 - ((expense_ratio - 50) / 50 * 100))
    else:
        expense_score = 0
    scores.append(expense_score)
    weights.append(0.20)

    # Debt Burden Score (15% weight)
    debt_payments = expenses.get("Loan/Debt Payments", 0)
    if monthly_income > 0:
        debt_ratio = debt_payments / monthly_income
        if debt_ratio <= 0.2:
            debt_score = 100
        elif debt_ratio <= 0.4:
            debt_score = 75
        elif debt_ratio <= 0.6:
            debt_score = 50
        elif debt_ratio <= 0.8:
            debt_score = 25
        else:
            debt_score = 0
    else:
        debt_score = 0
    scores.append(debt_score)
    weights.append(0.15)

    # Income Level Score (10% weight)
    if monthly_income >= 10000:
        income_score = 100
    elif monthly_income >= 5000:
        income_score = 75
    elif monthly_income >= 2000:
        income_score = 50
    else:
        income_score = 25
    scores.append(income_score)
    weights.append(0.10)

    total_weight = sum(weights)
    if total_weight == 0:
        return 50.0

    weighted_score = sum(score * weight for score, weight in zip(scores, weights)) / total_weight
    return round(weighted_score, 2)
def format_currency(value: float, currency: str = "$") -> str:
    """Format a numeric value as currency"""
    return f"{currency}{value:,.2f}"

def format_percentage(value: float) -> str:
    """Format a numeric value as percentage"""
    return f"{value:.1f}%"