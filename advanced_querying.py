import streamlit as st
import pandas as pd

def advanced_querying_section(data):
    st.markdown("### Advanced Querying")
    
    query = st.text_area("Enter your SQL-like query:")
    if st.button("Run Query"):
        try:
            result = data.query(query)
            st.write(result)
        except Exception as e:
            st.error(f"Error: {e}")