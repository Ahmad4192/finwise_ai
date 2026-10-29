"""
Chains Module for FinWise AI
Implements ChatOpenAI, LLMChain, and streaming functionality
"""

from typing import Dict, Any, Optional, List, Generator, Union
from langchain_classic.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import json
import re

from src.config import OPENAI_API_KEY, OPENAI_MODEL
from src.prompts import (
    FINANCIAL_CHAT_TEMPLATE,
    NARRATIVE_CHAT_TEMPLATE,
    create_human_message_inputs,
    create_narrative_inputs
)

def get_llm(
    model_name: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None
) -> ChatOpenAI:
    if not model_name:
        model_name = OPENAI_MODEL

    llm = ChatOpenAI(
        api_key=OPENAI_API_KEY,
        model=model_name,
        temperature=temperature,
        max_tokens=max_tokens or 4000,
        response_format={"type": "json_object"}
    )
    return llm

def create_financial_analysis_chain(
    llm: Optional[ChatOpenAI] = None,
    temperature: float = 0.3
) -> LLMChain:
    if llm is None:
        llm = get_llm(temperature=temperature)

    chain = LLMChain(
        llm=llm,
        prompt=FINANCIAL_CHAT_TEMPLATE,
        output_key="financial_analysis",
        verbose=False
    )
    return chain

def create_narrative_chain(
    llm: Optional[ChatOpenAI] = None,
    temperature: float = 0.7
) -> LLMChain:
    if llm is None:
        llm = get_llm(model_name=OPENAI_MODEL, temperature=temperature)

    chain = LLMChain(
        llm=llm,
        prompt=NARRATIVE_CHAT_TEMPLATE,
        output_key="narrative",
        verbose=False
    )
    return chain

def stream_recommendations(
    llm: ChatOpenAI,
    inputs: Dict[str, Any]
) -> Generator[str, None, None]:
    messages = NARRATIVE_CHAT_TEMPLATE.format_messages(**inputs)
    for chunk in llm.stream(messages):
        if chunk.content:
            yield chunk.content

def stream_financial_analysis(
    llm: ChatOpenAI,
    inputs: Dict[str, Any]
) -> Generator[str, None, None]:
    messages = FINANCIAL_CHAT_TEMPLATE.format_messages(**inputs)
    for chunk in llm.stream(messages):
        if chunk.content:
            yield chunk.content

def parse_json_safely(
    json_string: str,
    max_retries: int = 3
) -> Optional[Dict[str, Any]]:
    for attempt in range(max_retries):
        try:
            cleaned = json_string.strip()
            if '```json' in cleaned:
                cleaned = re.sub(r'^.*```json', '', cleaned, flags=re.DOTALL)
                cleaned = re.sub(r'```.*$', '', cleaned, flags=re.DOTALL)
                cleaned = cleaned.strip()
            if '```' in cleaned:
                cleaned = re.sub(r'^.*```', '', cleaned, flags=re.DOTALL)
                cleaned = re.sub(r'```.*$', '', cleaned, flags=re.DOTALL)
                cleaned = cleaned.strip()
            cleaned = re.sub(r',\s*}', '}', cleaned)
            cleaned = re.sub(r',\s*\]', ']', cleaned)
            return json.loads(cleaned)
        except json.JSONDecodeError:
            if attempt == max_retries - 1:
                return None
            continue
    return None

def validate_json_schema(data: Dict[str, Any]) -> bool:
    required_keys = [
        "financial_summary",
        "financial_health_score",
        "spending_analysis",
        "risk_level",
        "top_priorities",
        "budget_recommendations",
        "savings_strategy",
        "next_month_action_plan"
    ]

    for key in required_keys:
        if key not in data:
            return False

    if not isinstance(data.get("financial_summary"), str):
        return False

    if not isinstance(data.get("financial_health_score"), int):
        try:
            data["financial_health_score"] = int(data["financial_health_score"])
        except (ValueError, TypeError):
            return False

    if not isinstance(data.get("spending_analysis"), list):
        return False

    if not isinstance(data.get("risk_level"), str):
        return False

    valid_risk_levels = ["LOW", "MEDIUM", "HIGH", "EMERGENCY"]
    if data.get("risk_level").upper() not in valid_risk_levels:
        return False

    for item in data.get("spending_analysis", []):
        if not isinstance(item, dict):
            return False
        if "category" not in item or "observation" not in item or "recommendation" not in item:
            return False

    return True

def run_full_analysis(
    inputs: Dict[str, Any],
    temperature: float = 0.3
) -> Optional[Dict[str, Any]]:
    llm = get_llm(temperature=temperature)
    chain = create_financial_analysis_chain(llm, temperature)

    try:
        result = chain.invoke(inputs)
        analysis_text = result.get("financial_analysis", "")
        if not analysis_text:
            return None

        parsed = parse_json_safely(analysis_text)
        if parsed is None:
            return None

        if not validate_json_schema(parsed):
            return parsed

        return parsed
    except Exception:
        return None