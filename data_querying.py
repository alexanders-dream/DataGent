```python
import streamlit as st
import pandas as pd
from pandasai import Agent

def data_querying_section(data, model, prompt_template):
    st.markdown("### Interactive Data Querying")
    
    agent = Agent(data, config={"llm": model})
    prompt = st.text_input("Enter your data-related question:")
    
    if st.button("Generate"):
        if prompt:
            with st.spinner("Generating response..."):
                modified_prompt = f"Only answer questions related to the provided data. If the question is not about the data, respond with 'Please ask a question related to the data.' Here's the question: {prompt}"
                result = agent.chat(modified_prompt)
                
                # Check if result is an image path
                if isinstance(result, str) and (result.endswith('.png') or result.endswith('.jpg') or result.endswith('.jpeg')):
                    st.image(result)
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
            
            # 2. Generate questions using the LLM directly
            meta_prompt = f"""
            Analyze the following dataset columns and data types:
            Columns: {columns}
            Data Types: {dtypes}
            
            Generate 3 interesting and analytical questions that a expert user might ask to understand this data.
            Return ONLY the questions, one per line, without numbering or bullet points.
            """
            
            try:
                # We use the agent to generate questions about the data itself
                questions_response = agent.chat(meta_prompt)
                
                # Ensure we handle different return types
                if not isinstance(questions_response, str):
                    questions_response = str(questions_response)

                questions = [q.strip() for q in questions_response.split('\n') if q.strip()]
                
                if questions:
                    st.write(f"**Generated Questions:**")
                    for i, question in enumerate(questions):
                        st.markdown(f"**{i+1}. {question}**")
                        with st.spinner(f"Answering: {question}"):
                            answer = agent.chat(question)
                            
                            # Handle image response
                            if isinstance(answer, str) and (answer.endswith('.png') or answer.endswith('.jpg') or answer.endswith('.jpeg')):
                                st.image(answer)
                            # Handle dataframe response
                            elif isinstance(answer, pd.DataFrame):
                                st.dataframe(answer)
                            # Handle text/other response
                            else:
                                st.write(answer)
                            
                            st.divider()
                else:
                     st.error("Could not generate questions. Please try again.")

            except Exception as e:
                st.error(f"An error occurred during automated analysis: {e}")

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