import streamlit as st
import pandas as pd
from pandasai import Agent
import os
import re

def display_pandasai_result(result):
    """
    Helper function to properly display PandasAI results, 
    including chart images on Streamlit Cloud.
    Returns True if an image was displayed, False otherwise.
    """
    if result is None:
        return False
    
    # If result is already a DataFrame, display it
    if isinstance(result, pd.DataFrame):
        st.dataframe(result)
        return True
    
    # Convert to string for processing
    result_str = str(result).strip().strip("'").strip('"')
    
    # Check if the result looks like an image path
    image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.svg')
    
    # Pattern to find image paths in the result (may be embedded in text)
    image_path_pattern = r'["\']?([^"\'<>\s]*(?:exports[/\\]charts[/\\][^"\'<>\s]+|temp_chart[^"\'<>\s]+)\.(?:png|jpg|jpeg|gif))["\']?'
    
    # First, check if the whole result is an image path
    if result_str.lower().endswith(image_extensions):
        paths_to_try = [
            result_str,  # As-is
            os.path.abspath(result_str),  # Absolute path
            os.path.join(os.getcwd(), result_str),  # Relative to cwd
        ]
        
        for path in paths_to_try:
            if os.path.isfile(path):
                try:
                    st.image(path)
                    return True
                except Exception as e:
                    st.warning(f"Found image but couldn't display: {e}")
                    continue
    
    # Try to find image path embedded in text
    matches = re.findall(image_path_pattern, result_str, re.IGNORECASE)
    for match in matches:
        paths_to_try = [
            match,
            os.path.abspath(match),
            os.path.join(os.getcwd(), match),
            match.replace('\\', '/'),  # Handle Windows paths
            match.replace('/', '\\'),  # Handle Linux paths
        ]
        
        for path in paths_to_try:
            if os.path.isfile(path):
                try:
                    st.image(path)
                    return True
                except Exception:
                    continue
    
    # If no image found but result contains a chart path reference, try direct display
    if 'exports/charts' in result_str or 'temp_chart' in result_str:
        # Extract what looks like a path
        potential_paths = result_str.split()
        for p in potential_paths:
            p = p.strip("'\"")
            if 'chart' in p.lower() and p.lower().endswith(image_extensions):
                if os.path.isfile(p):
                    try:
                        st.image(p)
                        return True
                    except Exception:
                        pass
    
    return False

def data_querying_section(data, model, prompt_template):
    st.markdown("### Interactive Data Querying")
    
    # Get the underlying LLM for text generation tasks (not data queries)
    underlying_llm = model.langchain_llm if hasattr(model, 'langchain_llm') else None
    
    agent = Agent(data, config={
        "llm": model,
        "enable_cache": False,
        "enforce_privacy": False,
        "save_charts": True,
        "save_charts_path": "exports/charts",
        "verbose": False
    })

    prompt = st.text_input("Enter your data-related question:")
    
    if st.button("Generate"):
        if prompt:
            with st.spinner("Generating response..."):
                modified_prompt = f"Only answer questions related to the provided data. If the question is not about the data, respond with 'Please ask a question related to the data.' Here's the question: {prompt}"
                result = agent.chat(modified_prompt)
                
                # Use helper to display result (handles images, DataFrames, and text)
                if not display_pandasai_result(result):
                    # Fallback to simple write if helper didn't display anything
                    st.write(result)

                # Export Results
                if isinstance(result, pd.DataFrame):
                    st.markdown("### Export Results")
                    export_format = st.selectbox("Select export format", ["CSV", "Excel"])
                    if export_format == "CSV":
                        csv = result.to_csv(index=False)
                        st.download_button(
                            label="Download CSV",
                            data=csv,
                            file_name='result.csv',
                            mime='text/csv',
                        )
                    elif export_format == "Excel":
                        excel = result.to_excel(index=False)
                        st.download_button(
                            label="Download Excel",
                            data=excel,
                            file_name='result.xlsx',
                            mime='application/vnd.ms-excel',
                        )

    st.markdown("---")
    st.markdown("### Automated Data Insights")
    if st.button("Generate Automated Insights"):
        with st.spinner("Analyzing data and generating insights..."):
            # 1. Analyze data structure (columns and dtypes)
            columns = data.columns.tolist()
            dtypes = data.dtypes.astype(str).to_dict()
            
            # 2. Generate questions using the LLM directly (not the PandasAI agent)
            # PandasAI agent enforces SQL query execution, but generating questions is a text task
            meta_prompt = f"""Analyze the following dataset columns and data types:
Columns: {columns}
Data Types: {dtypes}

Generate 7 interesting and analytical questions that an expert user might ask to understand this data.
Return ONLY the questions, one per line, without numbering or bullet points."""
            
            try:
                # Use the underlying LLM for text generation (question generation)
                if underlying_llm is not None:
                    # Use LangChain LLM directly for text generation
                    questions_response = underlying_llm.invoke(meta_prompt)
                    # Handle AIMessage or string response
                    if hasattr(questions_response, 'content'):
                        questions_response = questions_response.content
                    else:
                        questions_response = str(questions_response)
                else:
                    # Fallback: try using model directly if it has an invoke method
                    st.warning("Could not access underlying LLM. Using fallback method.")
                    questions_response = str(model.invoke(meta_prompt) if hasattr(model, 'invoke') else "")
                
                questions = [q.strip() for q in questions_response.split('\n') if q.strip()]
                
                if questions:
                    st.write(f"**Generated Questions:**")
                    for i, question in enumerate(questions):
                        st.markdown(f"**{i+1}. {question}**")
                        with st.spinner(f"Answering: {question}"):
                            # Use PandasAI agent for actual data queries
                            answer = agent.chat(question)
                            
                            # Use helper to display result (handles images, DataFrames, and text)
                            if not display_pandasai_result(answer):
                                st.write(answer)
                            
                            st.divider()
                else:
                     st.error("Could not generate questions. Please try again.")

            except Exception as e:
                st.error(f"An error occurred during automated analysis: {e}")