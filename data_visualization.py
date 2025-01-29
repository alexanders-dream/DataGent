import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import io

def data_visualization_section(data):
    st.markdown("### Data Visualization")
    
    
    plot_type = st.selectbox(
        "Select plot type",
        ["Histogram", "Scatter Plot", "Bar Plot", "Box Plot", "Line Plot", 
         "Pie Chart", "Heatmap", "Map (Geospatial)"]
    )
    
    if plot_type == "Histogram":
        column = st.selectbox("Select column for histogram", data.columns)
        plt.figure(figsize=(10, 6))
        sns.histplot(data[column], kde=True)
        st.pyplot(plt)

        if st.button("Download Histogram as PNG"):
            buf = io.BytesIO()
            plt.savefig(buf, format="png")
            buf.seek(0)
            st.download_button(
                label="Download Histogram",
                data=buf,
                file_name="histogram.png",
                mime="image/png",
            )

    elif plot_type == "Scatter Plot":
        x_axis = st.selectbox("Select X-axis", data.columns)
        y_axis = st.selectbox("Select Y-axis", data.columns)
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=data[x_axis], y=data[y_axis])
        st.pyplot(plt)
        if st.button("Download Scatter Plot as PNG"):
            buf = io.BytesIO()
            plt.savefig(buf, format="png")
            buf.seek(0)
            st.download_button(
                label="Download Scatter Plot",
                data=buf,
                file_name="scatter_plot.png",
                mime="image/png",
            )

    elif plot_type == "Bar Plot":
        x_axis = st.selectbox("Select X-axis", data.columns)
        y_axis = st.selectbox("Select Y-axis", data.columns)
        plt.figure(figsize=(10, 6))
        sns.barplot(x=data[x_axis], y=data[y_axis])
        st.pyplot(plt)
        if st.button("Download Bar Plot as PNG"):
            buf = io.BytesIO()
            plt.savefig(buf, format="png")
            buf.seek(0)
            st.download_button(
                label="Download Bar Plot",
                data=buf,
                file_name="bar_plot.png",
                mime="image/png",
            )

    elif plot_type == "Box Plot":
        column = st.selectbox("Select column for box plot", data.columns)
        plt.figure(figsize=(10, 6))
        sns.boxplot(x=data[column])
        st.pyplot(plt)
        if st.button("Download Box Plot as PNG"):
            buf = io.BytesIO()
            plt.savefig(buf, format="png")
            buf.seek(0)
            st.download_button(
                label="Download Box Plot",
                data=buf,
                file_name="box_plot.png",
                mime="image/png",
            )

    elif plot_type == "Line Plot":
        x_axis = st.selectbox("Select X-axis", data.columns)
        y_axis = st.selectbox("Select Y-axis", data.columns)
        fig = px.line(data, x=x_axis, y=y_axis, title="Line Plot")
        st.plotly_chart(fig)
        if st.button("Download Line Plot as PNG"):
            buf = io.BytesIO()
            fig.write_image(buf, format="png")
            buf.seek(0)
            st.download_button(
                label="Download Line Plot",
                data=buf,
                file_name="line_plot.png",
                mime="image/png",
            )

    elif plot_type == "Pie Chart":
        column = st.selectbox("Select column for pie chart", data.columns)
        fig = px.pie(data, names=column, title="Pie Chart")
        st.plotly_chart(fig)
        if st.button("Download Pie Chart as PNG"):
            buf = io.BytesIO()
            fig.write_image(buf, format="png")
            buf.seek(0)
            st.download_button(
                label="Download Pie Chart",
                data=buf,
                file_name="pie_chart.png",
                mime="image/png",
            )

    elif plot_type == "Heatmap":
        numeric_data = data.select_dtypes(include=['float64', 'int64'])
        if not numeric_data.empty:
            plt.figure(figsize=(10, 6))
            sns.heatmap(numeric_data.corr(), annot=True, cmap="coolwarm")
            st.pyplot(plt)
            if st.button("Download Heatmap as PNG"):
                buf = io.BytesIO()
                plt.savefig(buf, format="png")
                buf.seek(0)
                st.download_button(
                    label="Download Heatmap",
                    data=buf,
                    file_name="heatmap.png",
                    mime="image/png",
                )
        else:
            st.warning("No numeric columns found for heatmap.")

    elif plot_type == "Map (Geospatial)":
        if st.checkbox("Show geospatial map (requires latitude and longitude columns)"):
            if "latitude" in data.columns and "longitude" in data.columns:
                fig = px.scatter_mapbox(data, lat="latitude", lon="longitude", zoom=3)
                fig.update_layout(mapbox_style="open-street-map")
                st.plotly_chart(fig)
                if st.button("Download Map as PNG"):
                    buf = io.BytesIO()
                    fig.write_image(buf, format="png")
                    buf.seek(0)
                    st.download_button(
                        label="Download Map",
                        data=buf,
                        file_name="map.png",
                        mime="image/png",
                    )
            else:
                st.warning("Latitude and Longitude columns are required for geospatial maps.")