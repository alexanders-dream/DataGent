import streamlit as st
import pandas as pd
from pandasai import Agent
import os

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
                
                # Check if result is an image path
                if isinstance(result, str):
                    clean_result = result.strip().strip("'").strip('"')
                    if os.path.isfile(clean_result) and (clean_result.lower().endswith(('.png', '.jpg', '.jpeg'))):
                        st.image(clean_result)
                    else:
                        st.write(result)
                else:
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
                            
                            # Handle answer
                            answered = False
                            if isinstance(answer, str):
                                clean_answer = answer.strip().strip("'").strip('"')
                                if os.path.isfile(clean_answer) and (clean_answer.lower().endswith(('.png', '.jpg', '.jpeg'))):
                                    st.image(clean_answer)
                                    answered = True
                            
                            if not answered:
                                if isinstance(answer, pd.DataFrame):
                                    st.dataframe(answer)
                                else:
                                    st.write(answer)
                            
                            st.divider()
                else:
                     st.error("Could not generate questions. Please try again.")

            except Exception as e:
                st.error(f"An error occurred during automated analysis: {e}")