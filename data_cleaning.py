import streamlit as st
import pandas as pd

def data_cleaning_section(data):
          
    st.subheader("Data Cleaning Options")
    
    # Missing values section
    if st.checkbox("Show missing values"):
        st.write("Missing Values Summary:")
        st.write(data.isnull().sum())
    
    # Column selection for targeted cleaning
    selected_columns = st.multiselect("Select columns to clean", data.columns)
    
    # Drop options
    if st.checkbox("Drop columns with missing values"):
        if selected_columns:
            data = data.drop(columns=selected_columns)
            st.write(f"Dropped selected columns: {selected_columns}")
        else:
            data = data.dropna(axis=1)
            st.write("Columns with missing values dropped.")
    
    if st.checkbox("Drop rows with missing values"):
        data = data.dropna(axis=0)
        st.write("Rows with missing values dropped.")
    
    # Fill options
    fill_method = st.selectbox(
        "Choose fill method",
        ["Mean", "Median", "Mode", "Custom Value"],
        index=0
    )
    
    if st.checkbox(f"Fill missing values with {fill_method.lower()}"):
        if fill_method == "Mean":
            data = data.fillna(data.mean(numeric_only=True))
        elif fill_method == "Median":
            data = data.fillna(data.median(numeric_only=True))
        elif fill_method == "Mode":
            data = data.fillna(data.mode().iloc[0])
        else:
            custom_value = st.text_input("Enter custom value")
            if custom_value:
                try:
                    data = data.fillna(float(custom_value))
                except ValueError:
                    data = data.fillna(custom_value)
        st.write(f"Missing values filled with {fill_method.lower()}.")
    
    # Show cleaned data preview
    if st.checkbox("Show cleaned data preview"):
        st.write(data.head())
    
    # Save option
    if st.button("Save cleaned data"):
        data.to_csv("cleaned_data.csv", index=False)
        st.success("Data saved as cleaned_data.csv")
    
    return data