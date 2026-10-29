"""
FinWise AI - Main Streamlit Application
AI-Powered Personal Financial Analysis and Smart Budget Assistant
"""

import streamlit as st
from typing import Dict, List, Any, Optional
from streamlit.components.v1 import html
import pandas as pd
import json
import os
import sys

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.config import (
    APP_TITLE, APP_SUBTITLE, APP_DESCRIPTION,
    EDUCATIONAL_DISCLAIMER, CURRENCY_OPTIONS, FINANCIAL_GOAL_OPTIONS,
    EXPENSE_CATEGORIES, DEFAULT_EXPENSES, FINANCIAL_HEALTH_BANDS,
    RISK_LEVELS, CACHE_OPTIONS, MODEL_OPTIONS, TEMPERATURE_OPTIONS,
    get_currency_symbol, get_health_score_band, get_risk_level_info
)

from src.financial_calculator import (
    calculate_financial_metrics, calculate_preliminary_score
)

from src.prompts import (
    FINANCIAL_CHAT_TEMPLATE, NARRATIVE_CHAT_TEMPLATE,
    create_human_message_inputs, create_narrative_inputs,
    format_expense_breakdown
)

from src.chains import (
    get_llm,
    create_financial_analysis_chain,
    stream_recommendations,
    parse_json_safely,
    validate_json_schema,
    run_full_analysis,
)

from src.cache_manager import (
    FinWiseCacheManager,
    create_cached_llm,
    configure_cache_for_llm,
)

from src.utils import (
    safe_json_parse,
    validate_financial_json,
    format_financial_number,
    get_risk_level_color,
    get_health_score_color,
    format_list_items,
)

# ============================================================================
# Custom CSS
# ============================================================================

def inject_custom_css():
    """Inject custom CSS for a refined dark theme and professional styling"""
    custom_css = """
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f1f5f9;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    .st-emotion-cache-6qob1r {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        border-right: 1px solid #334155;
    }
    .finwise-card {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 24px;
        margin: 16px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    .finwise-card:hover {
        border-color: #475569;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.4);
    }
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stSelectbox>div>div>select,
    .stButton>button {
        transition: all 0.3s ease;
    }
    .stTextInput>div>div>input:focus,
    .stNumberInput>div>div>input:focus,
    .stSelectbox>div>div>select:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.3) !important;
    }
    .stButton>button {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 16px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(59, 130, 246, 0.3);
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(59, 130, 246, 0.4);
    }
    .stButton>button:active {
        transform: translateY(0);
        box-shadow: 0 2px 4px rgba(59, 130, 246, 0.3);
    }
    .stButton>button.secondary {
        background: transparent;
        border: 2px solid #3b82f6;
        color: #3b82f6;
    }
    .stButton>button.secondary:hover {
        background: rgba(59, 130, 246, 0.1);
        border-color: #2563eb;
        color: #2563eb;
    }
    .stMetric {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px;
        color: #f1f5f9;
    }
    .risk-badge {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 14px;
        margin: 4px;
    }
    .risk-low {
        background: rgba(40, 167, 69, 0.2);
        border: 1px solid #28a745;
        color: #28a745;
    }
    .risk-medium {
        background: rgba(255, 193, 7, 0.2);
        border: 1px solid #ffc107;
        color: #ffc107;
    }
    .risk-high {
        background: rgba(253, 126, 20, 0.2);
        border: 1px solid #fd7e14;
        color: #fd7e14;
    }
    .risk-emergency {
        background: rgba(220, 53, 69, 0.2);
        border: 1px solid #dc3545;
        color: #dc3545;
    }
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #3b82f6 0%, #1d4ed8 100%);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid #334155;
        border-radius: 8px 8px 0 0;
        padding: 12px 24px;
        color: #94a3b8;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(59, 130, 246, 0.2);
        border-color: #3b82f6;
        color: #3b82f6;
    }
    .stExpander > div {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid #334155;
        border-radius: 8px;
        margin-bottom: 8px;
    }
    .stForm > div {
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 24px;
    }
    .stAlert {
        border-radius: 8px;
        border-left: 4px solid;
    }
    .finwise-title {
        color: #f1f5f9;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 16px;
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .finwise-subtitle {
        color: #94a3b8;
        font-size: 1.2rem;
        font-weight: 400;
        margin-bottom: 32px;
    }
    .disclaimer-box {
        background: rgba(245, 158, 11, 0.1);
        border: 1px solid #f59e0b;
        border-radius: 8px;
        padding: 16px;
        margin: 24px 0;
        font-size: 14px;
        color: #fbbf24;
    }
    @media (max-width: 768px) {
        .finwise-title { font-size: 2rem; }
        .finwise-card { padding: 16px; margin: 8px 0; }
        .stButton>button { padding: 10px 20px; font-size: 14px; }
    }
    ::-webkit-scrollbar { width: 10px; height: 10px; }
    ::-webkit-scrollbar-track { background: #1e293b; }
    ::-webkit-scrollbar-thumb { background: #334155; border-radius: 5px; }
    ::-webkit-scrollbar-thumb:hover { background: #475569; }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

# ============================================================================
# Session State Management
# ============================================================================

def initialize_session_state():
    """Initialize all session state variables"""
    if 'financial_data' not in st.session_state:
        st.session_state.financial_data = None
    if 'analysis_result' not in st.session_state:
        st.session_state.analysis_result = None
    if 'cache_manager' not in st.session_state:
        st.session_state.cache_manager = None
    if 'llm' not in st.session_state:
        st.session_state.llm = None
    if 'show_analysis' not in st.session_state:
        st.session_state.show_analysis = False
    if 'streaming_complete' not in st.session_state:
        st.session_state.streaming_complete = False
    if 'selected_cache' not in st.session_state:
        st.session_state.selected_cache = CACHE_OPTIONS[0]
    if 'selected_model' not in st.session_state:
        st.session_state.selected_model = MODEL_OPTIONS[0]
    if 'selected_temperature' not in st.session_state:
        st.session_state.selected_temperature = "Balanced"
    if 'expenses' not in st.session_state:
        st.session_state.expenses = DEFAULT_EXPENSES.copy()

# ============================================================================
# Sidebar Components
# ============================================================================

def render_sidebar():
    """Render the application sidebar with settings and information"""
    with st.sidebar:
        st.markdown("""
        <div style='text-align: center; padding: 24px;'>
            <h1 style='color: #3b82f6; font-size: 2rem; font-weight: 800;'>FinWise AI</h1>
            <p style='color: #94a3b8; font-size: 0.9rem;'>AI-Powered Financial Analysis</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        with st.expander("⚠️ **Educational Disclaimer**", expanded=False):
            st.markdown(EDUCATIONAL_DISCLAIMER)

        st.markdown("---")
        st.markdown("### 🤖 Model Settings")

        model_idx = st.selectbox(
            "OpenAI Model",
            options=MODEL_OPTIONS,
            index=MODEL_OPTIONS.index(st.session_state.selected_model) if st.session_state.selected_model in MODEL_OPTIONS else 0,
            key="model_select"
        )
        st.session_state.selected_model = model_idx

        temp_option = st.selectbox(
            "Creativity Level",
            options=list(TEMPERATURE_OPTIONS.keys()),
            index=list(TEMPERATURE_OPTIONS.keys()).index(st.session_state.selected_temperature) if st.session_state.selected_temperature in TEMPERATURE_OPTIONS else 1,
            key="temp_select"
        )
        st.session_state.selected_temperature = temp_option

        st.markdown("---")
        st.markdown("### 💾 Cache Settings")

        cache_option = st.selectbox(
            "Cache Type",
            options=CACHE_OPTIONS,
            index=CACHE_OPTIONS.index(st.session_state.selected_cache) if st.session_state.selected_cache in CACHE_OPTIONS else 0,
            key="cache_select"
        )
        st.session_state.selected_cache = cache_option

        if st.session_state.cache_manager:
            cache_info = st.session_state.cache_manager.get_cache_info()
            st.markdown(f"**Current:** {cache_info['cache_type']}")

        st.markdown("---")

        if st.button("🔄 Reset Session", use_container_width=True):
            reset_session()

        st.markdown("---")

        st.markdown("""
        <div style='text-align: center; padding: 16px; color: #64748b;'>
            <p style='font-size: 0.8rem;'>FinTech AI Assignment</p>
            <p style='font-size: 0.7rem;'>LangChain + Streamlit</p>
        </div>
        """, unsafe_allow_html=True)

def reset_session():
    """Reset all session state"""
    st.session_state.financial_data = None
    st.session_state.analysis_result = None
    st.session_state.show_analysis = False
    st.session_state.streaming_complete = False
    st.session_state.expenses = DEFAULT_EXPENSES.copy()
    cache_type = "InMemoryCache" if "InMemoryCache" in st.session_state.selected_cache else "SQLiteCache"
    st.session_state.cache_manager = FinWiseCacheManager(cache_type=cache_type)
    st.session_state.llm = None
    st.rerun()

# ============================================================================
# Main Form Components
# ============================================================================

def render_input_form():
    """Render the financial input form"""
    st.markdown("<div class='finwise-card'>", unsafe_allow_html=True)
    st.markdown("## 📊 Financial Information")

    with st.form(key="financial_form", clear_on_submit=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            monthly_income = st.number_input(
                "Monthly Income",
                min_value=0.0,
                value=5000.0,
                step=100.0,
                format="%.2f"
            )
        with col2:
            currency = st.selectbox(
                "Currency",
                options=CURRENCY_OPTIONS,
                index=0
            )

        st.markdown("---")
        current_savings = st.number_input(
            "Current Monthly Savings",
            min_value=0.0,
            value=500.0,
            step=50.0,
            format="%.2f"
        )

        st.markdown("---")
        financial_goal = st.selectbox(
            "Financial Goal",
            options=FINANCIAL_GOAL_OPTIONS,
            index=0
        )

        st.markdown("---")
        st.markdown("### 💰 Expense Categories")
        col1, col2 = st.columns(2)
        expense_inputs = []

        for i, category in enumerate(EXPENSE_CATEGORIES):
            parent_col = col1 if i % 2 == 0 else col2
            with parent_col:
                expense_value = st.number_input(
                    category,
                    min_value=0.0,
                    value=st.session_state.expenses.get(category, 0.0),
                    step=10.0,
                    format="%.2f",
                    key=f"expense_{category}"
                )
                expense_inputs.append((category, expense_value))

        new_expenses = {}
        for category, value in expense_inputs:
            new_expenses[category] = value
            st.session_state.expenses[category] = value

        st.markdown("---")
        submit_col1, submit_col2, submit_col3 = st.columns([1, 2, 1])
        with submit_col2:
            submit_button = st.form_submit_button(
                "🔍 Analyze My Finances",
                use_container_width=True,
                type="primary"
            )

    st.markdown("</div>", unsafe_allow_html=True)

    if submit_button:
        process_form_submission(
            monthly_income=monthly_income,
            expenses=new_expenses,
            current_savings=current_savings,
            financial_goal=financial_goal,
            currency=get_currency_symbol(currency)
        )

def process_form_submission(
    monthly_income: float,
    expenses: Dict[str, float],
    current_savings: float,
    financial_goal: str,
    currency: str
):
    """Process form submission and calculate metrics"""
    financial_metrics = calculate_financial_metrics(
        monthly_income=monthly_income,
        expenses=expenses,
        current_savings=current_savings
    )

    st.session_state.financial_data = {
        "monthly_income": monthly_income,
        "expenses": expenses,
        "current_savings": current_savings,
        "financial_goal": financial_goal,
        "currency": currency,
        **financial_metrics
    }

    st.session_state.show_analysis = True
    st.session_state.streaming_complete = False
    st.session_state.analysis_result = None

    if not st.session_state.cache_manager:
        cache_type = "InMemoryCache" if "InMemoryCache" in st.session_state.selected_cache else "SQLiteCache"
        st.session_state.cache_manager = FinWiseCacheManager(cache_type=cache_type)

    temperature = TEMPERATURE_OPTIONS.get(st.session_state.selected_temperature, 0.7)
    st.session_state.llm = create_cached_llm(
        model_name=st.session_state.selected_model,
        temperature=temperature,
        cache_type="InMemoryCache" if "InMemoryCache" in st.session_state.selected_cache else "SQLiteCache"
    )
    st.rerun()

# ============================================================================
# Financial Overview Components
# ============================================================================

def render_financial_overview():
    """Render the financial overview section"""
    if not st.session_state.financial_data:
        return

    data = st.session_state.financial_data
    currency = data.get("currency", "$")

    st.markdown("<div class='finwise-card'>", unsafe_allow_html=True)
    st.markdown("## 📈 Financial Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Monthly Income",
            value=format_financial_number(data["monthly_income"], currency),
            delta=None
        )

    with col2:
        st.metric(
            "Total Expenses",
            value=format_financial_number(data["total_expenses"], currency),
            delta=f"{data['expense_ratio']:.1f}% of income",
            delta_color="normal"
        )

    with col3:
        remaining = data["remaining_income"]
        remaining_color = "green" if remaining >= 0 else "red"
        remaining_text = format_financial_number(abs(remaining), currency)
        if remaining < 0:
            remaining_text = f"-{remaining_text}"

        st.metric(
            "Remaining",
            value=remaining_text,
            delta=None,
            delta_color=remaining_color
        )

    with col4:
        st.metric(
            "Current Savings",
            value=format_financial_number(data["current_savings"], currency),
            delta=f"{data['savings_ratio']:.1f}% of income",
            delta_color="green"
        )

    st.markdown("---")
    col1, col2, col3 = st.columns([2, 3, 1])

    with col1:
        score = data["preliminary_score"]
        band = get_health_score_band(score)
        st.metric(
            "Preliminary Score",
            value=f"{score:.1f}/100",
            delta=band["label"],
            delta_color="normal"
        )

    with col2:
        st.progress(score / 100.0)

    with col3:
        st.markdown(f"**{band['label']}**")

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
# AI Analysis Components
# ============================================================================

def render_ai_analysis():
    """Render the AI analysis section"""
    if not st.session_state.financial_data:
        return

    data = st.session_state.financial_data

    if st.session_state.analysis_result is None and st.session_state.show_analysis:
        run_ai_analysis()

    if st.session_state.analysis_result:
        render_analysis_results()
    elif st.session_state.show_analysis:
        with st.spinner("🤖 Analyzing your financial data..."):
            st.write("Please wait while we analyze your finances...")

def run_ai_analysis():
    """Run the AI analysis on financial data"""
    if not st.session_state.financial_data or not st.session_state.llm:
        return

    data = st.session_state.financial_data

    inputs = create_human_message_inputs(
        monthly_income=data["monthly_income"],
        total_expenses=data["total_expenses"],
        remaining_income=data["remaining_income"],
        current_savings=data["current_savings"],
        savings_ratio=data["savings_ratio"],
        expense_ratio=data["expense_ratio"],
        preliminary_score=data["preliminary_score"],
        expense_breakdown=data["expense_breakdown"],
        financial_goal=data["financial_goal"],
        currency=data.get("currency", "$")
    )

    try:
        result = run_full_analysis(
            inputs=inputs,
            temperature=TEMPERATURE_OPTIONS.get(st.session_state.selected_temperature, 0.7)
        )
        if result:
            st.session_state.analysis_result = result
            st.session_state.streaming_complete = False
            st.rerun()
    except Exception as e:
        st.error(f"Error running analysis: {str(e)}")

def render_analysis_results():
    """Render the AI analysis results"""
    if not st.session_state.analysis_result:
        return

    result = st.session_state.analysis_result
    data = st.session_state.financial_data

    st.markdown("<div class='finwise-card'>", unsafe_allow_html=True)
    st.markdown("## 🤖 AI Financial Analysis")

    st.markdown("""
    <div class='disclaimer-box'>
        <strong>⚠️ Educational Use Only:</strong> This analysis is for informational purposes only.
        Please consult with a qualified financial professional before making any financial decisions.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📝 Financial Summary")
    st.info(result.get("financial_summary", "No summary available"))

    st.markdown("---")
    col1, col2 = st.columns([3, 1])

    with col1:
        health_score = result.get("financial_health_score", 0)
        band = get_health_score_band(health_score)
        st.metric(
            "AI Financial Health Score",
            value=f"{health_score}/100",
            delta=band["label"],
            delta_color="normal"
        )

    with col2:
        risk_level = result.get("risk_level", "MEDIUM").upper()
        risk_info = get_risk_level_info(risk_level)
        risk_class = f"risk-{risk_level.lower()}"
        st.markdown(f"""
        <div class='risk-badge {risk_class}'>
            {risk_info['icon']} {risk_info['label']}
        </div>
        """, unsafe_allow_html=True)

    st.progress(health_score / 100.0)
    st.markdown("---")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Spending Analysis",
        "🎯 Top Priorities",
        "💡 Budget Recommendations",
        "🏦 Savings Strategy",
        "📅 Next Month Plan"
    ])

    with tab1:
        render_spending_analysis(result.get("spending_analysis", []))
    with tab2:
        render_priorities(result.get("top_priorities", []))
    with tab3:
        render_recommendations(result.get("budget_recommendations", []))
    with tab4:
        render_savings_strategy(result.get("savings_strategy", []))
    with tab5:
        render_action_plan(result.get("next_month_action_plan", []))

    st.markdown("</div>", unsafe_allow_html=True)
    render_streaming_recommendations()

def render_spending_analysis(spending_analysis: List[Dict[str, str]]):
    """Render spending analysis section"""
    if not spending_analysis:
        st.info("No spending analysis available")
        return
    for analysis in spending_analysis:
        with st.expander(f"💰 {analysis.get('category', 'Unknown Category')}", expanded=True):
            st.markdown(f"**Observation:** {analysis.get('observation', 'No observation')}")
            st.markdown(f"**Recommendation:** {analysis.get('recommendation', 'No recommendation')}")

def render_priorities(priorities: List[str]):
    """Render top priorities section"""
    if not priorities:
        st.info("No priorities identified")
        return
    for i, priority in enumerate(priorities, 1):
        st.markdown(f"**{i}. {priority}**")
        if i < len(priorities):
            st.markdown("---")

def render_recommendations(recommendations: List[str]):
    """Render budget recommendations section"""
    if not recommendations:
        st.info("No recommendations available")
        return
    for i, recommendation in enumerate(recommendations, 1):
        st.markdown(f"**{i}. {recommendation}**")
        if i < len(recommendations):
            st.markdown("---")

def render_savings_strategy(strategy: List[str]):
    """Render savings strategy section"""
    if not strategy:
        st.info("No savings strategy available")
        return
    for i, item in enumerate(strategy, 1):
        st.markdown(f"**{i}. {item}**")
        if i < len(strategy):
            st.markdown("---")

def render_action_plan(plan: List[str]):
    """Render action plan section"""
    if not plan:
        st.info("No action plan available")
        return
    for i, action in enumerate(plan, 1):
        st.markdown(f"**{i}. {action}**")
        if i < len(plan):
            st.markdown("---")

def render_streaming_recommendations():
    """Render the streaming recommendations section"""
    if not st.session_state.financial_data or not st.session_state.llm:
        return

    st.markdown("<div class='finwise-card'>", unsafe_allow_html=True)
    st.markdown("## 📝 Personalized Recommendations")

    data = st.session_state.financial_data
    top_findings = []
    if st.session_state.analysis_result:
        result = st.session_state.analysis_result
        if result.get("top_priorities"):
            top_findings.append(f"Top priorities: {', '.join(result['top_priorities'][:3])}")
        if result.get("risk_level"):
            top_findings.append(f"Risk level: {result['risk_level']}")
        if result.get("financial_health_score"):
            top_findings.append(f"Health score: {result['financial_health_score']}/100")

    if not top_findings:
        top_findings.append("Comprehensive financial analysis completed")

    narrative_inputs = create_narrative_inputs(
        monthly_income=data["monthly_income"],
        total_expenses=data["total_expenses"],
        remaining_income=data["remaining_income"],
        savings_ratio=data["savings_ratio"],
        financial_health_score=data.get("preliminary_score", 50),
        risk_level=data.get("risk_level", "MEDIUM"),
        top_findings="; ".join(top_findings),
        currency=data.get("currency", "$")
    )

    if st.button("🎯 Generate Personalized Recommendations", use_container_width=True):
        st.session_state.streaming_complete = False
        st.rerun()

    if not st.session_state.streaming_complete:
        st.markdown("""
        <div style='min-height: 200px; padding: 16px; background: rgba(30, 41, 59, 0.3);
                    border-radius: 8px; border: 1px dashed #475569;'>
        """, unsafe_allow_html=True)

        full_response = ""
        for chunk in stream_recommendations(st.session_state.llm, narrative_inputs):
            full_response += chunk
            st.write(chunk)

        st.session_state.streaming_complete = True

        st.markdown("""
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Click the button above to generate personalized recommendations with live streaming.")

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
# Main Application
# ============================================================================

def main():
    """Main application entry point"""
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon="💰",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    inject_custom_css()
    initialize_session_state()
    render_sidebar()

    with st.container():
        st.markdown(f"<h1 class='finwise-title'>{APP_TITLE}</h1>", unsafe_allow_html=True)
        st.markdown(f"<p class='finwise-subtitle'>{APP_SUBTITLE}</p>", unsafe_allow_html=True)

        with st.expander("⚠️ **Important Educational Disclaimer - Please Read**", expanded=False):
            st.markdown(EDUCATIONAL_DISCLAIMER)

        st.markdown("---")
        render_input_form()

        if st.session_state.show_analysis and st.session_state.financial_data:
            st.markdown("---")
            render_financial_overview()
            st.markdown("---")
            render_ai_analysis()

    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 24px; color: #64748b;'>
        <p>FinWise AI - AI-Powered Personal Financial Analysis | Educational Prototype</p>
        <p style='font-size: 0.8rem;'>Built with LangChain + Streamlit | For educational purposes only</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()