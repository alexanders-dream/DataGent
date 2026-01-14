import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO

def data_profiling_dashboard(data):
    """
    Comprehensive data profiling dashboard with quality metrics and visualizations
    """
    st.header("📊 Data Profiling Dashboard")
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Rows", f"{len(data):,}")
    with col2:
        st.metric("Total Columns", len(data.columns))
    with col3:
        missing_pct = (data.isnull().sum().sum() / (len(data) * len(data.columns)) * 100)
        st.metric("Missing Values", f"{missing_pct:.2f}%")
    with col4:
        duplicate_count = data.duplicated().sum()
        st.metric("Duplicate Rows", f"{duplicate_count:,}")
    
    # Create tabs for different profiling sections
    prof_tab1, prof_tab2, prof_tab3, prof_tab4, prof_tab5 = st.tabs([
        "📋 Data Quality Report",
        "🔥 Missing Values Heatmap", 
        "📈 Distribution Analysis",
        "🔗 Correlation Analysis",
        "📊 Column Statistics"
    ])
    
    with prof_tab1:
        show_data_quality_report(data)
    
    with prof_tab2:
        show_missing_values_heatmap(data)
    
    with prof_tab3:
        show_distribution_analysis(data)
    
    with prof_tab4:
        show_correlation_analysis(data)
    
    with prof_tab5:
        show_column_statistics(data)

def show_data_quality_report(data):
    """Generate comprehensive data quality report"""
    st.subheader("Data Quality Report")
    
    # Create quality report dataframe
    quality_report = []
    
    for col in data.columns:
        col_data = data[col]
        
        # Basic stats
        total_count = len(col_data)
        missing_count = col_data.isnull().sum()
        missing_pct = (missing_count / total_count * 100)
        unique_count = col_data.nunique()
        unique_pct = (unique_count / total_count * 100)
        
        # Data type
        dtype = str(col_data.dtype)
        
        # Memory usage
        memory_mb = col_data.memory_usage(deep=True) / 1024 / 1024
        
        # Quality score (simple heuristic)
        quality_score = 100 - missing_pct
        if unique_count == 1:
            quality_score -= 20  # Penalize constant columns
        
        quality_report.append({
            'Column': col,
            'Data Type': dtype,
            'Missing (%)': f"{missing_pct:.2f}%",
            'Missing Count': missing_count,
            'Unique Values': unique_count,
            'Unique (%)': f"{unique_pct:.2f}%",
            'Memory (MB)': f"{memory_mb:.3f}",
            'Quality Score': f"{quality_score:.1f}"
        })
    
    quality_df = pd.DataFrame(quality_report)
    
    # Display with color coding
    st.dataframe(
        quality_df,
        use_container_width=True,
        height=400
    )
    
    # Highlight issues
    st.subheader("⚠️ Potential Issues")
    
    issues = []
    
    # Check for high missing values
    high_missing = quality_df[quality_df['Missing Count'] > 0].sort_values('Missing Count', ascending=False)
    if not high_missing.empty:
        issues.append(f"**{len(high_missing)} columns** have missing values")
    
    # Check for constant columns
    constant_cols = [col for col in data.columns if data[col].nunique() == 1]
    if constant_cols:
        issues.append(f"**{len(constant_cols)} columns** have only one unique value: {', '.join(constant_cols)}")
    
    # Check for high cardinality
    high_cardinality = [col for col in data.columns if data[col].nunique() > len(data) * 0.9]
    if high_cardinality:
        issues.append(f"**{len(high_cardinality)} columns** have very high cardinality (>90% unique)")
    
    # Check for potential ID columns
    potential_ids = [col for col in data.columns if data[col].nunique() == len(data)]
    if potential_ids:
        issues.append(f"**{len(potential_ids)} columns** appear to be ID columns: {', '.join(potential_ids)}")
    
    if issues:
        for issue in issues:
            st.warning(issue)
    else:
        st.success("✅ No major data quality issues detected!")

def show_missing_values_heatmap(data):
    """Display missing values heatmap"""
    st.subheader("Missing Values Heatmap")
    
    missing_data = data.isnull()
    
    if missing_data.sum().sum() == 0:
        st.success("✅ No missing values in the dataset!")
        return
    
    # Create heatmap using plotly
    fig = go.Figure(data=go.Heatmap(
        z=missing_data.T.values,
        x=missing_data.index,
        y=missing_data.columns,
        colorscale=[[0, '#2ecc71'], [1, '#e74c3c']],
        showscale=True,
        colorbar=dict(title="Missing", tickvals=[0, 1], ticktext=["Present", "Missing"])
    ))
    
    fig.update_layout(
        title="Missing Values Pattern",
        xaxis_title="Row Index",
        yaxis_title="Columns",
        height=max(400, len(data.columns) * 20),
        xaxis=dict(showticklabels=False)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Missing values summary
    st.subheader("Missing Values Summary")
    missing_summary = pd.DataFrame({
        'Column': data.columns,
        'Missing Count': data.isnull().sum().values,
        'Missing Percentage': (data.isnull().sum().values / len(data) * 100).round(2)
    })
    missing_summary = missing_summary[missing_summary['Missing Count'] > 0].sort_values('Missing Count', ascending=False)
    
    if not missing_summary.empty:
        # Bar chart of missing values
        fig_bar = px.bar(
            missing_summary,
            x='Column',
            y='Missing Percentage',
            title='Missing Values by Column (%)',
            labels={'Missing Percentage': 'Missing (%)'},
            color='Missing Percentage',
            color_continuous_scale='Reds'
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        
        st.dataframe(missing_summary, use_container_width=True)

def show_distribution_analysis(data):
    """Show distribution visualizations for all columns"""
    st.subheader("Distribution Analysis")
    
    # Separate numeric and categorical columns
    numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = data.select_dtypes(include=['object', 'category']).columns.tolist()
    
    if numeric_cols:
        st.markdown("### 📊 Numeric Columns")
        
        # Select column to visualize
        selected_num_col = st.selectbox("Select numeric column", numeric_cols, key="dist_num")
        
        if selected_num_col:
            col_data = data[selected_num_col].dropna()
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Histogram
                fig_hist = px.histogram(
                    col_data,
                    nbins=50,
                    title=f"Distribution of {selected_num_col}",
                    labels={selected_num_col: selected_num_col, 'count': 'Frequency'}
                )
                fig_hist.update_traces(marker_color='#3498db')
                st.plotly_chart(fig_hist, use_container_width=True)
            
            with col2:
                # Box plot
                fig_box = px.box(
                    col_data,
                    y=col_data.values,
                    title=f"Box Plot of {selected_num_col}",
                    labels={'y': selected_num_col}
                )
                fig_box.update_traces(marker_color='#e74c3c')
                st.plotly_chart(fig_box, use_container_width=True)
            
            # Statistics
            st.markdown("**Statistics:**")
            stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
            with stats_col1:
                st.metric("Mean", f"{col_data.mean():.2f}")
            with stats_col2:
                st.metric("Median", f"{col_data.median():.2f}")
            with stats_col3:
                st.metric("Std Dev", f"{col_data.std():.2f}")
            with stats_col4:
                st.metric("Range", f"{col_data.max() - col_data.min():.2f}")
    
    if categorical_cols:
        st.markdown("### 📝 Categorical Columns")
        
        selected_cat_col = st.selectbox("Select categorical column", categorical_cols, key="dist_cat")
        
        if selected_cat_col:
            col_data = data[selected_cat_col].dropna()
            value_counts = col_data.value_counts().head(20)
            
            # Bar chart
            fig_bar = px.bar(
                x=value_counts.index,
                y=value_counts.values,
                title=f"Top 20 Values in {selected_cat_col}",
                labels={'x': selected_cat_col, 'y': 'Count'},
                color=value_counts.values,
                color_continuous_scale='Viridis'
            )
            st.plotly_chart(fig_bar, use_container_width=True)
            
            # Statistics
            st.markdown("**Statistics:**")
            stats_col1, stats_col2, stats_col3 = st.columns(3)
            with stats_col1:
                st.metric("Unique Values", col_data.nunique())
            with stats_col2:
                st.metric("Most Common", value_counts.index[0])
            with stats_col3:
                st.metric("Mode Frequency", value_counts.values[0])

def show_correlation_analysis(data):
    """Show correlation matrix for numeric columns"""
    st.subheader("Correlation Analysis")
    
    numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(numeric_cols) < 2:
        st.warning("Need at least 2 numeric columns for correlation analysis")
        return
    
    # Calculate correlation matrix
    corr_matrix = data[numeric_cols].corr()
    
    # Heatmap
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='RdBu',
        zmid=0,
        text=corr_matrix.values.round(2),
        texttemplate='%{text}',
        textfont={"size": 10},
        colorbar=dict(title="Correlation")
    ))
    
    fig.update_layout(
        title="Correlation Matrix",
        height=max(500, len(numeric_cols) * 40),
        xaxis={'side': 'bottom'}
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Find strong correlations
    st.subheader("Strong Correlations")
    threshold = st.slider("Correlation threshold", 0.0, 1.0, 0.7, 0.05)
    
    strong_corr = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            corr_val = corr_matrix.iloc[i, j]
            if abs(corr_val) >= threshold:
                strong_corr.append({
                    'Column 1': corr_matrix.columns[i],
                    'Column 2': corr_matrix.columns[j],
                    'Correlation': f"{corr_val:.3f}"
                })
    
    if strong_corr:
        st.dataframe(pd.DataFrame(strong_corr), use_container_width=True)
    else:
        st.info(f"No correlations found above {threshold:.2f} threshold")

def show_column_statistics(data):
    """Show detailed statistics for each column"""
    st.subheader("Detailed Column Statistics")
    
    selected_col = st.selectbox("Select column for detailed analysis", data.columns)
    
    if selected_col:
        col_data = data[selected_col]
        
        # Basic info
        st.markdown(f"### {selected_col}")
        
        info_col1, info_col2, info_col3, info_col4 = st.columns(4)
        with info_col1:
            st.metric("Data Type", str(col_data.dtype))
        with info_col2:
            st.metric("Non-Null Count", col_data.count())
        with info_col3:
            st.metric("Null Count", col_data.isnull().sum())
        with info_col4:
            st.metric("Unique Values", col_data.nunique())
        
        # Type-specific statistics
        if pd.api.types.is_numeric_dtype(col_data):
            st.markdown("#### Numeric Statistics")
            stats_df = pd.DataFrame({
                'Statistic': ['Count', 'Mean', 'Std', 'Min', '25%', '50%', '75%', 'Max', 'Skewness', 'Kurtosis'],
                'Value': [
                    col_data.count(),
                    col_data.mean(),
                    col_data.std(),
                    col_data.min(),
                    col_data.quantile(0.25),
                    col_data.quantile(0.50),
                    col_data.quantile(0.75),
                    col_data.max(),
                    col_data.skew(),
                    col_data.kurtosis()
                ]
            })
            st.dataframe(stats_df, use_container_width=True)
        else:
            st.markdown("#### Categorical Statistics")
            value_counts = col_data.value_counts().head(10)
            st.dataframe(
                pd.DataFrame({
                    'Value': value_counts.index,
                    'Count': value_counts.values,
                    'Percentage': (value_counts.values / len(col_data) * 100).round(2)
                }),
                use_container_width=True
            )
