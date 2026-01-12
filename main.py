import streamlit as st
import pandas as pd
import os
import requests
import requests.exceptions
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
import ui_components

st.set_page_config(
    page_title="DataGent",
    page_icon="images/icon.png"
)

def fetch_available_models(provider, api_endpoint, api_key):
    """Fetch available models from the selected provider's API endpoint"""
    try:
        if provider == "Groq":
            endpoint = f"{api_endpoint.rstrip('/')}/models"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
        else:  # Ollama
            endpoint = f"{api_endpoint.rstrip('/')}/api/tags"
            headers = {"Content-Type": "application/json"}

        response = requests.get(
            endpoint,
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        
        # Handle different response formats
        if provider == "Groq":
            return [model['id'] for model in response.json().get('data', [])]
        else:  # Ollama
            return [model['name'] for model in response.json().get('models', [])]
        
    except requests.exceptions.ConnectionError:
        st.sidebar.error(f"Connection Error: Could not connect to {api_endpoint}. Is the server running?")
        if provider == "Ollama":
             st.sidebar.warning(f"For Ollama, ensure it is running (`ollama serve`). If running in Docker or WSL, you might need to set OLLAMA_HOST=0.0.0.0.")
        return None
    except requests.exceptions.Timeout:
        st.sidebar.error(f"Timeout: Connection to {api_endpoint} timed out.")
        return None
    except requests.exceptions.HTTPError as e:
        st.sidebar.error(f"API Error: {e}")
        return None
    except Exception as e:
        st.sidebar.error(f"Unexpected Error: {str(e)}")
        return None

# Create prompt template
prompt_template = ChatPromptTemplate.from_template(
    "You are a data analysis assistant. Only answer questions related to the uploaded data. "
    "If asked about anything else, respond with: 'I can only answer questions about the uploaded data.' "
)

# Function to restart the session
def restart_session():
    st.session_state.api_key = ""
    st.session_state.clear()
    st.rerun()

# Page title and sidebar title
ICON_LOGO = "images/logo.png"

st.sidebar.image(ICON_LOGO, width=300) 
st.title("DataGent : a Data Analysis AI Agent")
#st.sidebar.title("DataGent AI")

# Combined ProductHunt and Google Form embeds
st.markdown(ui_components.get_social_badges_html(), unsafe_allow_html=True)

#Sidebar extra features
with st.sidebar.expander("Unlock Extra Features", expanded=False):
    st.markdown(ui_components.get_calendly_badge_html(), unsafe_allow_html=True)
    st.markdown(ui_components.get_buymeacoffee_badge_html(), unsafe_allow_html=True)

# File upload function
uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv", "xls", "xlsx"])

# Model Selection Section in Sidebar
st.sidebar.header("AI Model Configuration")

# Initialize session state for models and selected model index
if 'models' not in st.session_state:
    st.session_state.models = []
if 'selected_model_index' not in st.session_state:
    st.session_state.selected_model_index = 0

# Provider Selection
provider = st.sidebar.selectbox(
    "Select AI Provider:",
    options=["Groq", "Ollama"],
    index=0,
    help="Choose between Groq cloud or local Ollama service"
)

# API Configuration
if provider == "Groq":
    default_endpoint = "https://api.groq.com/openai/v1"
else:  # Ollama
    default_endpoint = "http://localhost:11434"

api_endpoint = st.sidebar.text_input(
    "API Endpoint:",
    value=default_endpoint,
    help="Edit the API endpoint if needed"
)

if provider == "Groq":
    if "api_key" not in st.session_state:
        st.session_state.api_key = ""

    st.session_state.api_key = st.sidebar.text_input(
        "Groq API Key:",
        value=st.session_state.api_key,
        type="password",
        help="Required for Groq - securely stored in session",
        placeholder="Enter your Groq API key"
    )
    
    if st.session_state.api_key :
        # Key is securely stored in session state
        pass 
    else:
        st.sidebar.markdown("[Get Groq API Key](https://console.groq.com/keys)")
        st.sidebar.error("GROQ_API_KEY is required for Groq provider")
        provider = "Ollama"
        st.session_state.api_key = ""
else:
    st.session_state.api_key  = ""

# Check if models need to be fetched
if not st.session_state.models or 'selected_model_index' not in st.session_state:
    if api_endpoint:
        if provider == "Groq" and st.session_state.api_key :
            models = fetch_available_models(provider, api_endpoint, st.session_state.api_key )
        else:
            models = fetch_available_models(provider, api_endpoint, st.session_state.api_key )
        if models:
            st.session_state.models = models
        else:
            st.sidebar.error("No models available - check connection and refresh")

# Model Selection with Refresh Button
col1, col2 = st.sidebar.columns([4, 1])
with col1:
    if st.session_state.models:
        selected_model = st.selectbox(
            "Select AI Model:",
            options=st.session_state.models,
            index=st.session_state.selected_model_index,
            on_change=None,
            help="Choose from available AI models"
        )
        st.session_state.selected_model_index = st.session_state.models.index(selected_model)
    else:
        selected_model = None
        st.error("No models available - check connection and refresh")
        st.sidebar.markdown("[Download Ollama](https://ollama.com/)")
with col2:
    st.markdown(ui_components.get_button_css(), unsafe_allow_html=True)
    if st.button("🔄", help="Check available models"):
        if api_endpoint:
            if provider == "Groq" and st.session_state.api_key :
                models = fetch_available_models(provider, api_endpoint, st.session_state.api_key )
            else:
                models = fetch_available_models(provider, api_endpoint, st.session_state.api_key )
            if models:
                st.session_state.models = models
                st.sidebar.success("Models updated successfully!", icon="✅")
            else:
                st.sidebar.error("Failed to fetch models", icon="❗")
        else:
            st.sidebar.warning("Please provide a valid API endpoint", icon="⚠")
    st.markdown("</div>", unsafe_allow_html=True)

# Initialize selected model
if selected_model:
    if provider == "Groq":
        model = ChatGroq(temperature=0, model_name=selected_model, api_key=st.session_state.api_key)
    else:  # Ollama
        model = LocalLLM(api_base=api_endpoint, model=selected_model)
else:
    model = None
    st.sidebar.error("Please select a valid model")

# Show current model info
if model:
    st.sidebar.info(f"Using: {provider} - {selected_model}")

# End session button
if st.sidebar.button("End Session"):
    restart_session()

#Uploaded file logic
if uploaded_file is not None:
    # Read uploaded file
    file_type = uploaded_file.name.split('.')[-1]
    
    if file_type == 'csv':
        # Read the CSV file
        data = pd.read_csv(uploaded_file)
        #st.info("Reading CSV file...")
    elif file_type in ['xls', 'xlsx']:
        # Read the Excel file
        data = pd.read_excel(uploaded_file)
        #st.info(f"Reading Excel file ({file_type.upper()})...")
    else:
        st.error("Unsupported file type. Please upload a CSV or Excel file.")
    
    # Data Preview
    st.subheader("Data Preview")
    st.write(data.head())

    # Create tabs for different sections
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Data Cleaning", "Data Visualization", 
                                          "Data Querying with AI", "Advanced Querying", 
                                          "Interactive Data Filtering", "Sentiment Analysis"])

    with tab1:
        data_cleaning_section(data)

    with tab2:
        data_visualization_section(data)

    with tab3:
        data_querying_section(data, model, prompt_template)

    with tab4:
        advanced_querying_section(data)

    with tab5:
        data_filtering_section(data)
    
    with tab6:
        sentiment_analysis_section(data)

else:
    st.write("Please upload a CSV or Excel file to get started.")