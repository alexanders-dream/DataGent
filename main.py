import streamlit as st
import pandas as pd
import os
from langchain_groq.chat_models import ChatGroq
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from data_cleaning import data_cleaning_section
from data_visualization import data_visualization_section
from data_querying import data_querying_section
from advanced_querying import advanced_querying_section
from data_filtering import data_filtering_section
from sentiment_analysis import sentiment_analysis_section
from pandasai import Agent
from pandasai.llm.local_llm import LocalLLM

# Create prompt template
DATA_ANALYSIS_PROMPT = ChatPromptTemplate.from_template(
    "You are a data analysis assistant. Only answer questions related to the uploaded data. "
    "If asked about anything else, respond with: 'I can only answer questions about the uploaded data.' "
)
# Function to restart the session
def restart_session():
    st.session_state.clear()
    st.rerun()

# Page title and sidebar title
st.title("DataGent : a Data Analysis AI Agent")
st.sidebar.title("DataGent AI")

# File upload function
uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

#Model
st.sidebar.title("AI Model Configuration")
model_choice = st.sidebar.radio(
    "Choose AI Model",
    options=["Groq (Cloud)", "Ollama/LocalLLM"],
    index=0 if os.getenv("GROQ_API_KEY") else 1
)

# Initialize selected model
if model_choice == "ChatGroq (Cloud)":
    if not os.getenv("GROQ_API_KEY"):
        st.sidebar.error("GROQ_API_KEY not found in .env file")
        model = LocalLLM(api_base="http://localhost:11434/v1", model="qwen2.5-coder")
    else:
        model = ChatGroq(temperature=0, model_name="gemma2-9b-it")
else:
    model = LocalLLM(api_base="http://localhost:11434/v1", model="qwen2.5-coder")

# Show current model info
st.sidebar.info(f"Using: {model_choice}")

# Setup for local AI model of choice
# model = LocalLLM(api_base="http://localhost:11434/v1", model="qwen2.5-coder")

#End session button
if st.sidebar.button("End Session"):
    restart_session()

if uploaded_file is not None:
    # Read uploaded file
    data = pd.read_csv(uploaded_file)
    
    # Data Preview
    st.subheader("Data Preview")
    st.write(data.head())

    # Create tabs for different sections
    tab1, tab2, tab3, tab4, tab5, tab6= st.tabs(["Data Cleaning", "Data Visualization", 
                                          "Data Querying with AI", "Advanced Querying", 
                                          "Interactive Data Filtering", "Sentiment Analysis"])

    with tab1:
        data_cleaning_section(data)

    with tab2:
        data_visualization_section(data)

    with tab3:
        data_querying_section(data, model, DATA_ANALYSIS_PROMPT)

    with tab4:
        advanced_querying_section(data)

    with tab5:
        data_filtering_section(data)
    
    with tab6:
        sentiment_analysis_section(data)


else:
    st.write("Please upload a CSV file to get started.")