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