import streamlit as st
import pandas as pd
import plotly.express as px

def data_visualization_section(data):
    st.markdown("### Data Visualization")
    
    plot_type = st.selectbox(
        "Select plot type",
        ["Histogram", "Scatter Plot", "Bar Plot", "Box Plot", "Line Plot", 
         "Pie Chart", "Heatmap", "Map (Geospatial)"]
    )
    
    # Common helper to add "Color by" option
    color_col = None
    if plot_type in ["Histogram", "Scatter Plot", "Bar Plot", "Box Plot", "Line Plot"]:
        col1, col2 = st.columns([1, 1])
        with col1:
             st.info("💡 Tip: You can interact with the plots (zoom, pan) and download them using the camera icon in the toolbar on the exact top right of the chart.")
        with col2:
            if st.checkbox("Group/Color by another column?", key="color_checkbox"):
                color_col = st.selectbox("Select column for coloring", data.columns, key="color_select")

    if plot_type == "Histogram":
        column = st.selectbox("Select column for histogram", data.columns)
        try:
            fig = px.histogram(data, x=column, color=color_col, title=f"Histogram of {column}")
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error creating histogram: {e}")

    elif plot_type == "Scatter Plot":
        c1, c2 = st.columns(2)
        with c1:
            x_axis = st.selectbox("Select X-axis", data.columns)
        with c2:
            y_axis = st.selectbox("Select Y-axis", data.columns)
            
        try:
            fig = px.scatter(data, x=x_axis, y=y_axis, color=color_col, title=f"Scatter Plot: {x_axis} vs {y_axis}")
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error creating scatter plot: {e}")

    elif plot_type == "Bar Plot":
        c1, c2 = st.columns(2)
        with c1:
            x_axis = st.selectbox("Select X-axis", data.columns)
        with c2:
            y_axis = st.selectbox("Select Y-axis", data.columns)
            
        try:
            fig = px.bar(data, x=x_axis, y=y_axis, color=color_col, title=f"Bar Plot: {x_axis} vs {y_axis}")
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error creating bar plot: {e}")

    elif plot_type == "Box Plot":
        column = st.selectbox("Select column for box plot", data.columns)
        try:
            # Box plot can be vertical or horizontal. 
            # If color is provided, it groups by color.
            # We can also add a y-axis if the user wants to break it down.
            fig = px.box(data, y=column, color=color_col, title=f"Box Plot of {column}")
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error creating box plot: {e}")

    elif plot_type == "Line Plot":
        c1, c2 = st.columns(2)
        with c1:
            x_axis = st.selectbox("Select X-axis", data.columns)
        with c2:
            y_axis = st.selectbox("Select Y-axis", data.columns)
            
        try:
            fig = px.line(data, x=x_axis, y=y_axis, color=color_col, title=f"Line Plot: {x_axis} vs {y_axis}")
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error creating line plot: {e}")

    elif plot_type == "Pie Chart":
        column = st.selectbox("Select column for pie chart", data.columns)
        try:
            fig = px.pie(data, names=column, title=f"Pie Chart of {column}")
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error creating pie chart: {e}")

    elif plot_type == "Heatmap":
        numeric_data = data.select_dtypes(include=['float64', 'int64'])
        if not numeric_data.empty:
            try:
                corr_matrix = numeric_data.corr()
                fig = px.imshow(corr_matrix, text_auto=True, aspect="auto", title="Correlation Heatmap")
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Error creating heatmap: {e}")
        else:
            st.warning("No numeric columns found for heatmap.")

    elif plot_type == "Map (Geospatial)":
        st.markdown("#### Map Configuration")
        c1, c2 = st.columns(2)
        
        # Try to auto-detect lat/lon columns
        possible_lat = [col for col in data.columns if "lat" in col.lower()]
        possible_lon = [col for col in data.columns if "lon" in col.lower() or "lng" in col.lower()]
        
        default_lat_index = data.columns.get_loc(possible_lat[0]) if possible_lat else 0
        default_lon_index = data.columns.get_loc(possible_lon[0]) if possible_lon else 0

        with c1:
            lat_col = st.selectbox("Select Latitude Column", data.columns, index=default_lat_index)
        with c2:
            lon_col = st.selectbox("Select Longitude Column", data.columns, index=default_lon_index)

        if st.checkbox("Show Map"):
            try:
                fig = px.scatter_mapbox(data, lat=lat_col, lon=lon_col, zoom=3)
                fig.update_layout(mapbox_style="open-street-map")
                fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Error creating map: {e}")