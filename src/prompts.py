"""
Prompts Module for FinWise AI
Defines all prompt templates, chat templates, and JSON schemas
"""
from typing import Dict, Any
from langchain_core.messages import SystemMessage
from langchain_core.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

# JSON Output Schema
FINANCIAL_ANALYSIS_SCHEMA = {
    "financial_summary": "A concise 2-3 sentence summary of the user's financial situation",
    "financial_health_score": "An integer score from 0-100 representing overall financial health",
    "spending_analysis": "List of spending observations and recommendations per category",
    "risk_level": "One of: LOW, MEDIUM, HIGH, EMERGENCY",
    "top_priorities": "List of 3-5 most important financial priorities",
    "budget_recommendations": "List of specific budget improvement recommendations",
    "savings_strategy": "List of savings strategy suggestions",
    "next_month_action_plan": "List of actionable steps for the next month"
}

JSON_SCHEMA_STRING = """
The output must be a valid JSON object with the following exact schema:
{
    "financial_summary": "string - 2-3 sentence summary of financial situation",
    "financial_health_score": "integer - 0-100 score of overall financial health",
    "spending_analysis": [
        {
            "category": "string - expense category name",
            "observation": "string - observation about this category",
            "recommendation": "string - recommendation for this category"
        }
    ],
    "risk_level": "string - one of: LOW, MEDIUM, HIGH, EMERGENCY",
    "top_priorities": ["string", "string"],
    "budget_recommendations": ["string", "string"],
    "savings_strategy": ["string", "string"],
    "next_month_action_plan": ["string", "string"]
}
"""

SYSTEM_MESSAGE_CONTENT = f"""
You are FinWise AI, an educational AI-powered personal financial analysis assistant.

**YOUR ROLE:**
- Provide educational financial insights based on user's income, expenses, and savings
- Analyze spending patterns and identify areas for improvement
- Generate personalized budget recommendations
- Always emphasize that this is for educational purposes only

**SAFETY & COMPLIANCE RULES:**
1. NEVER provide guaranteed investment advice
2. NEVER claim any financial outcome is guaranteed
3. NEVER recommend specific investments, stocks, or financial products
4. ALWAYS state that users should consult a qualified financial professional
5. ALWAYS include the educational disclaimer in your responses
6. DO NOT make predictions about future market conditions
7. DO NOT provide tax, legal, or professional financial advice
8. Frame all suggestions as educational insights, not professional recommendations

**ANALYSIS GUIDELINES:**
- Be honest and direct about financial situations
- Use the preliminary_score as a starting point but refine it based on your analysis
- Consider all financial metrics: savings ratio, expense ratio, remaining income
- Identify high-expense categories that may need attention
- Provide actionable, realistic recommendations
- Prioritize recommendations based on urgency and impact

**OUTPUT REQUIREMENTS:**
- Use the exact JSON schema provided below
- All arrays must have at least 1 item, up to 10 items maximum
- financial_summary: 2-3 sentences max
- Be specific and data-driven in your analysis
- Use clear, simple language

{JSON_SCHEMA_STRING}

**EDUCATIONAL DISCLAIMER TO INCLUDE:**
"This analysis is for educational and informational purposes only. Please consult with a qualified financial professional before making any financial decisions."
"""

HUMAN_TEMPLATE = """
Please analyze my financial situation and provide a detailed assessment.

**My Financial Data:**
- Monthly Income: {currency}{monthly_income}
- Total Expenses: {currency}{total_expenses}
- Remaining Income: {currency}{remaining_income}
- Current Savings: {currency}{current_savings}
- Savings Ratio: {savings_ratio}%
- Expense Ratio: {expense_ratio}%
- Preliminary Score: {preliminary_score}/100

**My Expense Breakdown:**
{expense_breakdown_formatted}

**My Financial Goal:** {financial_goal}

**Questions for Analysis:**
1. What is my overall financial health?
2. How am I doing with my spending in each category?
3. What are my top financial priorities right now?
4. What specific budget improvements can I make?
5. What savings strategies should I consider?
6. What should be my action plan for next month?

**Important:** Please provide your response as valid JSON following the exact schema provided.
"""

NARRATIVE_TEMPLATE = """
Based on the following financial analysis, provide a comprehensive written recommendation:

**Financial Overview:**
- Monthly Income: {currency}{monthly_income}
- Total Expenses: {currency}{total_expenses}
- Remaining Income: {currency}{remaining_income}
- Savings Ratio: {savings_ratio}%
- Financial Health Score: {financial_health_score}/100
- Risk Level: {risk_level}

**Key Findings:**
{top_findings}

Please write a detailed, educational recommendation (3-5 paragraphs) that covers:
1. Overall financial health assessment
2. Strengths in current financial management
3. Areas that need improvement
4. Specific, actionable recommendations
5. Encouragement and motivation

Remember: This is for educational purposes only. Always advise consulting a financial professional.
Write in a friendly, professional tone using complete sentences.
"""

# Plain text prompt template
FINANCIAL_PROMPT_TEMPLATE = PromptTemplate(
    input_variables=[
        "monthly_income", "total_expenses", "remaining_income",
        "current_savings", "savings_ratio", "expense_ratio",
        "preliminary_score", "expense_breakdown_formatted", "financial_goal", "currency"
    ],
    template=HUMAN_TEMPLATE
)

# Chat prompt template using tuples or MessagePromptTemplates
FINANCIAL_CHAT_TEMPLATE = ChatPromptTemplate.from_messages([
    SystemMessage(content=SYSTEM_MESSAGE_CONTENT),
    ("human", HUMAN_TEMPLATE)
])

NARRATIVE_CHAT_TEMPLATE = ChatPromptTemplate.from_messages([
    ("system", """
You are FinWise AI, an educational financial analysis assistant.
Provide detailed, educational financial recommendations based on the analysis.
Always remind users this is for educational purposes only.
Write in a professional, friendly tone.
"""),
    ("human", NARRATIVE_TEMPLATE)
])

def format_expense_breakdown(expense_breakdown: Dict[str, float], currency: str = "$") -> str:
    if not expense_breakdown:
        return "No expenses recorded"

    lines = []
    total = sum(expense_breakdown.values())
    for category, amount in expense_breakdown.items():
        if amount > 0:
            percentage = (amount / total) * 100 if total > 0 else 0
            lines.append(f"  - {category}: {currency}{amount:,.2f} ({percentage:.1f}%)")

    return "\n".join(lines)

def create_human_message_inputs(
    monthly_income: float,
    total_expenses: float,
    remaining_income: float,
    current_savings: float,
    savings_ratio: float,
    expense_ratio: float,
    preliminary_score: float,
    expense_breakdown: Dict[str, float],
    financial_goal: str,
    currency: str = "$"
) -> Dict[str, Any]:
    return {
        "monthly_income": f"{monthly_income:,.2f}",
        "total_expenses": f"{total_expenses:,.2f}",
        "remaining_income": f"{remaining_income:,.2f}",
        "current_savings": f"{current_savings:,.2f}",
        "savings_ratio": f"{savings_ratio:.1f}",
        "expense_ratio": f"{expense_ratio:.1f}",
        "preliminary_score": f"{preliminary_score:.1f}",
        "expense_breakdown_formatted": format_expense_breakdown(expense_breakdown, currency),
        "financial_goal": financial_goal,
        "currency": currency
    }

def create_narrative_inputs(
    monthly_income: float,
    total_expenses: float,
    remaining_income: float,
    savings_ratio: float,
    financial_health_score: float,
    risk_level: str,
    top_findings: str,
    currency: str = "$"
) -> Dict[str, Any]:
    return {
        "monthly_income": f"{monthly_income:,.2f}",
        "total_expenses": f"{total_expenses:,.2f}",
        "remaining_income": f"{remaining_income:,.2f}",
        "savings_ratio": f"{savings_ratio:.1f}",
        "financial_health_score": int(financial_health_score),
        "risk_level": risk_level,
        "top_findings": top_findings,
        "currency": currency
    }