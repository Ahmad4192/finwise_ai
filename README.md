# FinWise AI - AI-Powered Personal Financial Analysis and Smart Budget Assistant

![FinWise AI Logo](https://img.shields.io/badge/FinWise%20AI-LangChain%20%2B%20Streamlit-3b82f6?style=for-the-badge)

**FinWise AI** is an educational AI-powered personal financial analysis and smart budget assistant built with **LangChain** and **Streamlit**. This application helps users understand their spending patterns, identify areas for improvement, and receive personalized financial insights.

> **⚠️ IMPORTANT: This is an educational prototype only. It does NOT provide guaranteed investment advice, execute financial transactions, or connect to real bank accounts. All outputs are for informational purposes only.**

## 📊 Features

### Core Capabilities
- ✅ **Financial Metrics Calculation**: Automatically computes total expenses, remaining income, savings ratio, and expense ratio
- ✅ **AI-Powered Analysis**: LangChain-powered LLM provides structured financial insights
- ✅ **Streaming Output**: Real-time typing effect for recommendations
- ✅ **Dual Caching**: InMemoryCache (RAM) and SQLiteCache (Disk) with toggle switch
- ✅ **Structured JSON Output**: Validated schema with comprehensive financial analysis

### User Interface
- ✅ **Responsive Dashboard**: Clean, modern Streamlit UI with dark theme
- ✅ **Interactive Forms**: Easy input for income, expenses, and financial goals
- ✅ **Visual Metrics**: Color-coded cards, progress bars, and risk badges
- ✅ **Tabbed Navigation**: Organized analysis sections
- ✅ **Expandable Cards**: Detailed insights with smooth expand/collapse

### Technical Implementation
- ✅ **Modular Architecture**: Clean separation of concerns across modules
- ✅ **LangChain Integration**: ChatOpenAI, PromptTemplate, ChatPromptTemplate, LLMChain
- ✅ **Safe JSON Parsing**: Robust error handling for LLM outputs
- ✅ **Environment Management**: Secure API key handling via .env

## 🏗️ Project Structure