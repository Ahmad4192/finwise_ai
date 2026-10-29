"""
Utilities Module for FinWise AI
Helper functions for JSON parsing, validation, and general utilities
"""

import json
import re
from typing import Dict, Any, Optional, List
import hashlib

def safe_json_parse(
    json_string: str,
    max_retries: int = 3,
    verbose: bool = False
) -> Optional[Dict[str, Any]]:
    if not json_string or not isinstance(json_string, str):
        return None

    for attempt in range(max_retries):
        try:
            cleaned = json_string.strip()
            cleaned = re.sub(r'^```(json)?\s*', '', cleaned, flags=re.IGNORECASE)
            cleaned = re.sub(r'\s*```\s*$', '', cleaned, flags=re.IGNORECASE)
            cleaned = cleaned.strip()
            try:
                return json.loads(cleaned)
            except json.JSONDecodeError:
                pass

            cleaned = re.sub(r',\s*([}\])', r'\1', cleaned)
            cleaned = re.sub(r'([{,])', r'\1\"', cleaned)
            cleaned = re.sub(r'"([a-zA-Z_][a-zA-Z0-9_]*)"\s*:', r'\"\1\":', cleaned)
            return json.loads(cleaned)
        except json.JSONDecodeError:
            if attempt == max_retries - 1:
                return None
            continue
        except Exception:
            return None
    return None

def validate_financial_json(
    data: Dict[str, Any],
    strict: bool = True
) -> tuple:
    errors = []
    if not isinstance(data, dict):
        errors.append("Root element must be a dictionary")
        return False, errors

    required_fields = [
        "financial_summary", "financial_health_score", "spending_analysis",
        "risk_level", "top_priorities", "budget_recommendations",
        "savings_strategy", "next_month_action_plan"
    ]

    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: {field}")

    if "financial_health_score" in data:
        score = data["financial_health_score"]
        if not isinstance(score, (int, float)):
            errors.append("financial_health_score must be a number")
        elif isinstance(score, float):
            if score.is_integer():
                data["financial_health_score"] = int(score)
            else:
                errors.append("financial_health_score must be an integer")
        elif score < 0 or score > 100:
            errors.append("financial_health_score must be between 0 and 100")

    if "risk_level" in data:
        valid_risk_levels = ["LOW", "MEDIUM", "HIGH", "EMERGENCY"]
        risk_level = data["risk_level"].upper()
        if risk_level not in valid_risk_levels:
            errors.append(f"risk_level must be one of: {', '.join(valid_risk_levels)}")
        else:
            data["risk_level"] = risk_level

    if strict and errors:
        return False, errors

    critical_errors = [e for e in errors if "missing" in e.lower() or "must be" in e.lower()]
    if critical_errors:
        return False, critical_errors

    return len(errors) == 0, errors

def extract_json_from_text(text: str) -> Optional[str]:
    if not text:
        return None
    json_match = re.search(r'```(json)?\s*({.*?})\s*```', text, re.DOTALL | re.IGNORECASE)
    if json_match:
        return json_match.group(2)
    json_match = re.search(r'\{.*\}', text, re.DOTALL)
    if json_match:
        return json_match.group(0)
    return None

def generate_unique_id(data: Dict[str, Any]) -> str:
    data_str = json.dumps(data, sort_keys=True, default=str)
    return hashlib.md5(data_str.encode('utf-8')).hexdigest()

def format_financial_number(value: float, currency: str = "$") -> str:
    return f"{currency}{value:,.2f}"

def format_percentage(value: float) -> str:
    return f"{value:.1f}%"

def truncate_text(text: str, max_length: int = 100, ellipsis: str = "...") -> str:
    if not text:
        return ""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(ellipsis)] + ellipsis

def get_risk_level_color(risk_level: str) -> str:
    colors = {
        "LOW": "#28a745",
        "MEDIUM": "#ffc107",
        "HIGH": "#fd7e14",
        "EMERGENCY": "#dc3545"
    }
    return colors.get(risk_level.upper(), "#6c757d")

def get_health_score_color(score: float) -> str:
    if score >= 80:
        return "#28a745"
    elif score >= 60:
        return "#007bff"
    elif score >= 40:
        return "#ffc107"
    else:
        return "#dc3545"

def format_list_items(items: List[str], max_items: int = 5) -> List[str]:
    if not items:
        return ["No items"]
    if len(items) <= max_items:
        return items
    return items[:max_items] + [f"... and {len(items) - max_items} more"]