import streamlit as st
import pandas as pd

def data_filtering_section(data):
    st.markdown("### Interactive Data Filtering")
    
    columns_to_filter = st.multiselect("Select columns to filter", data.columns)
    filters = {}
    for column in columns_to_filter:
        if data[column].dtype == 'object':
            filters[column] = st.multiselect(f"Filter {column}", data[column].unique())
        else:
            min_val = float(data[column].min())
            max_val = float(data[column].max())
            filters[column] = st.slider(f"Filter {column}", min_val, max_val, (min_val, max_val))

    filtered_data = data.copy()
    for column, filter_val in filters.items():
        if data[column].dtype == 'object':
            filtered_data = filtered_data[filtered_data[column].isin(filter_val)]
        else:
            filtered_data = filtered_data[(filtered_data[column] >= filter_val[0]) & (filtered_data[column] <= filter_val[1])]

    st.write(filtered_data)