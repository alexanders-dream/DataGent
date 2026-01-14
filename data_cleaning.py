import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
import re
from datetime import datetime

def data_cleaning_section(data):
    """
    Enhanced data cleaning section with advanced features and step-by-step wizard
    """
    st.header("🧹 Data Cleaning")
    
    # Initialize session state for cleaning history
    if 'cleaning_history' not in st.session_state:
        st.session_state.cleaning_history = []
    if 'original_data' not in st.session_state:
        st.session_state.original_data = data.copy()
    if 'cleaned_data' not in st.session_state:
        st.session_state.cleaned_data = data.copy()
    
    # Create tabs for different cleaning operations
    clean_tab1, clean_tab2, clean_tab3, clean_tab4, clean_tab5, clean_tab6 = st.tabs([
        "🔧 Missing Values",
        "🔄 Duplicates",
        "📊 Outliers",
        "🔤 Data Types",
        "✅ Validation",
        "📥 Export & History"
    ])
    
    with clean_tab1:
        handle_missing_values(st.session_state.cleaned_data)
    
    with clean_tab2:
        handle_duplicates(st.session_state.cleaned_data)
    
    with clean_tab3:
        handle_outliers(st.session_state.cleaned_data)
    
    with clean_tab4:
        optimize_data_types(st.session_state.cleaned_data)
    
    with clean_tab5:
        validate_data(st.session_state.cleaned_data)
    
    with clean_tab6:
        export_and_history(st.session_state.cleaned_data, st.session_state.original_data)
    
    return st.session_state.cleaned_data

def handle_missing_values(data):
    """Advanced missing value handling"""
    st.subheader("Missing Values Management")
    
    # Show missing values summary
    missing_summary = data.isnull().sum()
    missing_cols = missing_summary[missing_summary > 0]
    
    if len(missing_cols) == 0:
        st.success("✅ No missing values in the dataset!")
        return
    
    st.warning(f"Found missing values in {len(missing_cols)} columns")
    
    # Display missing values
    with st.expander("📊 View Missing Values Summary", expanded=True):
        missing_df = pd.DataFrame({
            'Column': missing_cols.index,
            'Missing Count': missing_cols.values,
            'Missing %': (missing_cols.values / len(data) * 100).round(2)
        })
        st.dataframe(missing_df, use_container_width=True)
    
    st.markdown("---")
    
    # Strategy selection
    st.subheader("Select Cleaning Strategy")
    
    strategy = st.radio(
        "Choose approach:",
        ["Column-Specific Strategy", "Global Strategy", "Threshold-Based Dropping"],
        help="Column-specific allows different strategies per column, Global applies same strategy to all"
    )
    
    if strategy == "Column-Specific Strategy":
        apply_column_specific_strategy(data, missing_cols)
    elif strategy == "Global Strategy":
        apply_global_strategy(data, missing_cols)
    else:
        apply_threshold_dropping(data)

def apply_column_specific_strategy(data, missing_cols):
    """Apply different strategies to different columns"""
    st.markdown("### Column-Specific Strategy")
    
    selected_col = st.selectbox("Select column to clean", missing_cols.index)
    
    if selected_col:
        col_data = data[selected_col]
        is_numeric = pd.api.types.is_numeric_dtype(col_data)
        
        # Show column info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Data Type", str(col_data.dtype))
        with col2:
            st.metric("Missing Count", col_data.isnull().sum())
        with col3:
            st.metric("Missing %", f"{(col_data.isnull().sum() / len(col_data) * 100):.2f}%")
        
        # Strategy options based on data type
        if is_numeric:
            method = st.selectbox(
                "Fill method",
                ["Mean", "Median", "Mode", "Forward Fill", "Backward Fill", 
                 "Linear Interpolation", "Polynomial Interpolation", "Custom Value", "Drop Rows"]
            )
        else:
            method = st.selectbox(
                "Fill method",
                ["Mode", "Forward Fill", "Backward Fill", "Custom Value", "Drop Rows"]
            )
        
        # Preview before apply
        preview_col1, preview_col2 = st.columns(2)
        
        with preview_col1:
            st.markdown("**Before:**")
            st.dataframe(data[[selected_col]].head(10), use_container_width=True)
        
        with preview_col2:
            st.markdown("**Preview After:**")
            preview_data = data.copy()
            preview_data = apply_fill_method(preview_data, selected_col, method)
            st.dataframe(preview_data[[selected_col]].head(10), use_container_width=True)
        
        # Apply button
        if st.button(f"✅ Apply {method} to {selected_col}", key=f"apply_{selected_col}"):
            data_before = data.copy()
            data = apply_fill_method(data, selected_col, method)
            st.session_state.cleaned_data = data
            log_cleaning_action(f"Applied {method} to column '{selected_col}'")
            st.success(f"✅ Applied {method} to {selected_col}")
            st.rerun()

def apply_global_strategy(data, missing_cols):
    """Apply same strategy to all columns with missing values"""
    st.markdown("### Global Strategy")
    
    method = st.selectbox(
        "Select method to apply to all columns",
        ["Mean (numeric only)", "Median (numeric only)", "Mode", 
         "Forward Fill", "Backward Fill", "Drop Rows with Any Missing", 
         "Drop Rows with All Missing"]
    )
    
    # Show impact preview
    st.markdown("**Impact Preview:**")
    
    if "Drop Rows" in method:
        if "Any" in method:
            rows_to_drop = data.isnull().any(axis=1).sum()
        else:
            rows_to_drop = data.isnull().all(axis=1).sum()
        
        st.warning(f"This will remove {rows_to_drop} rows ({(rows_to_drop/len(data)*100):.2f}% of data)")
    else:
        st.info(f"This will fill missing values in {len(missing_cols)} columns")
    
    if st.button("✅ Apply Global Strategy", key="apply_global"):
        data_before = data.copy()
        
        if method == "Mean (numeric only)":
            numeric_cols = data.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                if col in missing_cols.index:
                    data[col].fillna(data[col].mean(), inplace=True)
        
        elif method == "Median (numeric only)":
            numeric_cols = data.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                if col in missing_cols.index:
                    data[col].fillna(data[col].median(), inplace=True)
        
        elif method == "Mode":
            for col in missing_cols.index:
                mode_val = data[col].mode()
                if len(mode_val) > 0:
                    data[col].fillna(mode_val[0], inplace=True)
        
        elif method == "Forward Fill":
            data.fillna(method='ffill', inplace=True)
        
        elif method == "Backward Fill":
            data.fillna(method='bfill', inplace=True)
        
        elif method == "Drop Rows with Any Missing":
            data.dropna(axis=0, how='any', inplace=True)
        
        elif method == "Drop Rows with All Missing":
            data.dropna(axis=0, how='all', inplace=True)
        
        st.session_state.cleaned_data = data
        log_cleaning_action(f"Applied global strategy: {method}")
        st.success(f"✅ Applied {method} globally")
        st.rerun()

def apply_threshold_dropping(data):
    """Drop columns or rows based on missing value threshold"""
    st.markdown("### Threshold-Based Dropping")
    
    drop_type = st.radio("Drop:", ["Columns", "Rows"])
    
    threshold = st.slider(
        f"Drop {drop_type.lower()} with more than X% missing values",
        0, 100, 50, 5,
        help=f"{drop_type} exceeding this threshold will be removed"
    )
    
    if drop_type == "Columns":
        missing_pct = (data.isnull().sum() / len(data) * 100)
        cols_to_drop = missing_pct[missing_pct > threshold].index.tolist()
        
        st.warning(f"Will drop {len(cols_to_drop)} columns: {', '.join(cols_to_drop) if cols_to_drop else 'None'}")
        
        if cols_to_drop and st.button("✅ Drop Columns", key="drop_cols_threshold"):
            data.drop(columns=cols_to_drop, inplace=True)
            st.session_state.cleaned_data = data
            log_cleaning_action(f"Dropped {len(cols_to_drop)} columns with >{threshold}% missing values")
            st.success(f"✅ Dropped {len(cols_to_drop)} columns")
            st.rerun()
    
    else:  # Rows
        missing_pct_rows = (data.isnull().sum(axis=1) / len(data.columns) * 100)
        rows_to_drop = (missing_pct_rows > threshold).sum()
        
        st.warning(f"Will drop {rows_to_drop} rows ({(rows_to_drop/len(data)*100):.2f}% of data)")
        
        if rows_to_drop > 0 and st.button("✅ Drop Rows", key="drop_rows_threshold"):
            data_filtered = data[missing_pct_rows <= threshold]
            st.session_state.cleaned_data = data_filtered
            log_cleaning_action(f"Dropped {rows_to_drop} rows with >{threshold}% missing values")
            st.success(f"✅ Dropped {rows_to_drop} rows")
            st.rerun()

def apply_fill_method(data, column, method):
    """Apply specific fill method to a column"""
    data = data.copy()
    
    if method == "Mean":
        data[column].fillna(data[column].mean(), inplace=True)
    elif method == "Median":
        data[column].fillna(data[column].median(), inplace=True)
    elif method == "Mode":
        mode_val = data[column].mode()
        if len(mode_val) > 0:
            data[column].fillna(mode_val[0], inplace=True)
    elif method == "Forward Fill":
        data[column].fillna(method='ffill', inplace=True)
    elif method == "Backward Fill":
        data[column].fillna(method='bfill', inplace=True)
    elif method == "Linear Interpolation":
        data[column].interpolate(method='linear', inplace=True)
    elif method == "Polynomial Interpolation":
        data[column].interpolate(method='polynomial', order=2, inplace=True)
    elif method == "Drop Rows":
        data.dropna(subset=[column], inplace=True)
    elif method == "Custom Value":
        custom_val = st.text_input(f"Enter custom value for {column}", key=f"custom_{column}")
        if custom_val:
            try:
                data[column].fillna(float(custom_val), inplace=True)
            except ValueError:
                data[column].fillna(custom_val, inplace=True)
    
    return data

def handle_duplicates(data):
    """Duplicate detection and removal"""
    st.subheader("Duplicate Management")
    
    # Check for duplicates
    duplicate_count = data.duplicated().sum()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Rows", len(data))
    with col2:
        st.metric("Duplicate Rows", duplicate_count)
    
    if duplicate_count == 0:
        st.success("✅ No duplicate rows found!")
        return
    
    st.warning(f"Found {duplicate_count} duplicate rows ({(duplicate_count/len(data)*100):.2f}% of data)")
    
    # Duplicate detection criteria
    st.markdown("### Detection Criteria")
    
    criteria = st.radio(
        "Check duplicates based on:",
        ["All Columns", "Specific Columns"],
        help="All columns checks entire row, Specific columns allows custom criteria"
    )
    
    subset_cols = None
    if criteria == "Specific Columns":
        subset_cols = st.multiselect("Select columns to check", data.columns.tolist())
        if subset_cols:
            duplicate_count = data.duplicated(subset=subset_cols).sum()
            st.info(f"Found {duplicate_count} duplicates based on selected columns")
    
    # Preview duplicates
    if st.checkbox("👀 Preview Duplicate Rows", value=False):
        if subset_cols:
            duplicates = data[data.duplicated(subset=subset_cols, keep=False)]
        else:
            duplicates = data[data.duplicated(keep=False)]
        
        st.dataframe(duplicates.head(20), use_container_width=True)
    
    # Removal strategy
    st.markdown("### Removal Strategy")
    
    keep_option = st.selectbox(
        "Which duplicates to keep?",
        ["first", "last", "none"],
        help="first: keep first occurrence, last: keep last occurrence, none: remove all duplicates"
    )
    
    if st.button("🗑️ Remove Duplicates", key="remove_duplicates"):
        initial_count = len(data)
        
        if keep_option == "none":
            if subset_cols:
                data = data[~data.duplicated(subset=subset_cols, keep=False)]
            else:
                data = data[~data.duplicated(keep=False)]
        else:
            if subset_cols:
                data.drop_duplicates(subset=subset_cols, keep=keep_option, inplace=True)
            else:
                data.drop_duplicates(keep=keep_option, inplace=True)
        
        removed_count = initial_count - len(data)
        st.session_state.cleaned_data = data
        log_cleaning_action(f"Removed {removed_count} duplicate rows (keep={keep_option})")
        st.success(f"✅ Removed {removed_count} duplicate rows")
        st.rerun()

def handle_outliers(data):
    """Outlier detection and handling"""
    st.subheader("Outlier Detection & Handling")
    
    numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
    
    if not numeric_cols:
        st.warning("No numeric columns found for outlier detection")
        return
    
    selected_col = st.selectbox("Select column for outlier analysis", numeric_cols)
    
    if selected_col:
        col_data = data[selected_col].dropna()
        
        # Detection method
        method = st.radio(
            "Detection Method:",
            ["IQR (Interquartile Range)", "Z-Score"],
            help="IQR: values beyond 1.5*IQR from quartiles. Z-Score: values beyond threshold standard deviations"
        )
        
        if method == "IQR (Interquartile Range)":
            multiplier = st.slider("IQR Multiplier", 1.0, 3.0, 1.5, 0.1)
            outliers, lower_bound, upper_bound = detect_outliers_iqr(col_data, multiplier)
        else:
            threshold = st.slider("Z-Score Threshold", 1.0, 5.0, 3.0, 0.1)
            outliers, lower_bound, upper_bound = detect_outliers_zscore(col_data, threshold)
        
        # Visualization
        st.markdown("### 📊 Visual Analysis")
        
        fig = go.Figure()
        
        # Box plot
        fig.add_trace(go.Box(
            y=col_data,
            name=selected_col,
            boxmean=True,
            marker_color='#3498db'
        ))
        
        # Add outlier boundaries
        fig.add_hline(y=lower_bound, line_dash="dash", line_color="red", 
                     annotation_text=f"Lower Bound: {lower_bound:.2f}")
        fig.add_hline(y=upper_bound, line_dash="dash", line_color="red",
                     annotation_text=f"Upper Bound: {upper_bound:.2f}")
        
        fig.update_layout(
            title=f"Outlier Detection for {selected_col}",
            yaxis_title=selected_col,
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Outlier summary
        outlier_count = len(outliers)
        st.metric("Outliers Detected", f"{outlier_count} ({(outlier_count/len(col_data)*100):.2f}%)")
        
        if outlier_count > 0:
            # Handling strategy
            st.markdown("### Handling Strategy")
            
            action = st.selectbox(
                "What to do with outliers?",
                ["Remove Outliers", "Cap at Boundaries", "Transform (Log)", "Keep (No Action)"]
            )
            
            # Preview
            preview_data = data.copy()
            if action == "Remove Outliers":
                preview_data = preview_data[~preview_data[selected_col].isin(outliers)]
                st.warning(f"Will remove {outlier_count} rows")
            elif action == "Cap at Boundaries":
                preview_data[selected_col] = preview_data[selected_col].clip(lower_bound, upper_bound)
                st.info(f"Will cap {outlier_count} values at boundaries")
            elif action == "Transform (Log)":
                preview_data[selected_col] = np.log1p(preview_data[selected_col])
                st.info("Will apply log transformation")
            
            if action != "Keep (No Action)" and st.button(f"✅ Apply {action}", key="apply_outlier"):
                st.session_state.cleaned_data = preview_data
                log_cleaning_action(f"Outlier handling: {action} on column '{selected_col}'")
                st.success(f"✅ Applied {action}")
                st.rerun()

def detect_outliers_iqr(data, multiplier=1.5):
    """Detect outliers using IQR method"""
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - multiplier * IQR
    upper_bound = Q3 + multiplier * IQR
    
    outliers = data[(data < lower_bound) | (data > upper_bound)]
    
    return outliers, lower_bound, upper_bound

def detect_outliers_zscore(data, threshold=3):
    """Detect outliers using Z-score method"""
    mean = data.mean()
    std = data.std()
    
    z_scores = np.abs((data - mean) / std)
    outliers = data[z_scores > threshold]
    
    lower_bound = mean - threshold * std
    upper_bound = mean + threshold * std
    
    return outliers, lower_bound, upper_bound

def optimize_data_types(data):
    """Data type optimization and conversion"""
    st.subheader("Data Type Optimization")
    
    # Current data types
    st.markdown("### Current Data Types")
    
    dtype_df = pd.DataFrame({
        'Column': data.columns,
        'Current Type': [str(dtype) for dtype in data.dtypes],
        'Memory (MB)': [data[col].memory_usage(deep=True) / 1024 / 1024 for col in data.columns]
    })
    
    st.dataframe(dtype_df, use_container_width=True)
    
    total_memory = data.memory_usage(deep=True).sum() / 1024 / 1024
    st.metric("Total Memory Usage", f"{total_memory:.2f} MB")
    
    st.markdown("---")
    
    # Optimization options
    st.markdown("### Optimization Options")
    
    option = st.radio(
        "Select operation:",
        ["Auto-Optimize Types", "Manual Type Conversion", "Parse Dates", "Optimize Categories"]
    )
    
    if option == "Auto-Optimize Types":
        auto_optimize_types(data)
    elif option == "Manual Type Conversion":
        manual_type_conversion(data)
    elif option == "Parse Dates":
        parse_dates(data)
    else:
        optimize_categories(data)

def auto_optimize_types(data):
    """Automatically optimize data types"""
    st.markdown("#### Auto-Optimize Data Types")
    
    st.info("This will automatically convert numeric columns to more efficient types and object columns to categories where appropriate")
    
    if st.button("🚀 Auto-Optimize", key="auto_optimize"):
        optimized_data = data.copy()
        changes = []
        
        # Optimize numeric columns
        for col in optimized_data.select_dtypes(include=['int64']).columns:
            col_min = optimized_data[col].min()
            col_max = optimized_data[col].max()
            
            if col_min >= 0:
                if col_max < 255:
                    optimized_data[col] = optimized_data[col].astype('uint8')
                    changes.append(f"{col}: int64 → uint8")
                elif col_max < 65535:
                    optimized_data[col] = optimized_data[col].astype('uint16')
                    changes.append(f"{col}: int64 → uint16")
                elif col_max < 4294967295:
                    optimized_data[col] = optimized_data[col].astype('uint32')
                    changes.append(f"{col}: int64 → uint32")
            else:
                if col_min > -128 and col_max < 127:
                    optimized_data[col] = optimized_data[col].astype('int8')
                    changes.append(f"{col}: int64 → int8")
                elif col_min > -32768 and col_max < 32767:
                    optimized_data[col] = optimized_data[col].astype('int16')
                    changes.append(f"{col}: int64 → int16")
                elif col_min > -2147483648 and col_max < 2147483647:
                    optimized_data[col] = optimized_data[col].astype('int32')
                    changes.append(f"{col}: int64 → int32")
        
        # Optimize float columns
        for col in optimized_data.select_dtypes(include=['float64']).columns:
            optimized_data[col] = optimized_data[col].astype('float32')
            changes.append(f"{col}: float64 → float32")
        
        # Convert low-cardinality object columns to category
        for col in optimized_data.select_dtypes(include=['object']).columns:
            num_unique = optimized_data[col].nunique()
            num_total = len(optimized_data[col])
            if num_unique / num_total < 0.5:  # Less than 50% unique
                optimized_data[col] = optimized_data[col].astype('category')
                changes.append(f"{col}: object → category")
        
        # Calculate memory savings
        original_memory = data.memory_usage(deep=True).sum() / 1024 / 1024
        optimized_memory = optimized_data.memory_usage(deep=True).sum() / 1024 / 1024
        savings = original_memory - optimized_memory
        savings_pct = (savings / original_memory) * 100
        
        st.session_state.cleaned_data = optimized_data
        log_cleaning_action(f"Auto-optimized data types: {len(changes)} changes, saved {savings:.2f} MB")
        
        st.success(f"✅ Optimized! Saved {savings:.2f} MB ({savings_pct:.1f}%)")
        
        with st.expander("View Changes"):
            for change in changes:
                st.text(change)
        
        st.rerun()

def manual_type_conversion(data):
    """Manual type conversion"""
    st.markdown("#### Manual Type Conversion")
    
    selected_col = st.selectbox("Select column", data.columns)
    
    if selected_col:
        current_type = str(data[selected_col].dtype)
        st.info(f"Current type: {current_type}")
        
        new_type = st.selectbox(
            "Convert to:",
            ["int8", "int16", "int32", "int64", "uint8", "uint16", "uint32", "uint64",
             "float32", "float64", "object", "category", "string", "boolean"]
        )
        
        if st.button(f"Convert {selected_col} to {new_type}", key="manual_convert"):
            try:
                data[selected_col] = data[selected_col].astype(new_type)
                st.session_state.cleaned_data = data
                log_cleaning_action(f"Converted column '{selected_col}' from {current_type} to {new_type}")
                st.success(f"✅ Converted {selected_col} to {new_type}")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Conversion failed: {str(e)}")

def parse_dates(data):
    """Parse date columns"""
    st.markdown("#### Parse Date Columns")
    
    object_cols = data.select_dtypes(include=['object']).columns.tolist()
    
    if not object_cols:
        st.warning("No object columns found to parse as dates")
        return
    
    selected_col = st.selectbox("Select column to parse as date", object_cols)
    
    if selected_col:
        # Show sample values
        st.markdown("**Sample values:**")
        st.write(data[selected_col].head(10).tolist())
        
        date_format = st.text_input(
            "Date format (optional)",
            placeholder="e.g., %Y-%m-%d or leave empty for auto-detection",
            help="Use Python strftime format codes"
        )
        
        if st.button(f"Parse {selected_col} as datetime", key="parse_date"):
            try:
                if date_format:
                    data[selected_col] = pd.to_datetime(data[selected_col], format=date_format)
                else:
                    data[selected_col] = pd.to_datetime(data[selected_col], infer_datetime_format=True)
                
                st.session_state.cleaned_data = data
                log_cleaning_action(f"Parsed column '{selected_col}' as datetime")
                st.success(f"✅ Parsed {selected_col} as datetime")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Parsing failed: {str(e)}")

def optimize_categories(data):
    """Optimize categorical columns"""
    st.markdown("#### Optimize Categorical Columns")
    
    object_cols = data.select_dtypes(include=['object']).columns.tolist()
    
    if not object_cols:
        st.warning("No object columns found")
        return
    
    # Show candidates for category conversion
    candidates = []
    for col in object_cols:
        num_unique = data[col].nunique()
        num_total = len(data[col])
        cardinality_ratio = num_unique / num_total
        
        if cardinality_ratio < 0.5:
            current_memory = data[col].memory_usage(deep=True) / 1024
            potential_memory = data[col].astype('category').memory_usage(deep=True) / 1024
            savings = current_memory - potential_memory
            
            candidates.append({
                'Column': col,
                'Unique Values': num_unique,
                'Cardinality %': f"{cardinality_ratio*100:.1f}%",
                'Current Memory (KB)': f"{current_memory:.2f}",
                'Potential Savings (KB)': f"{savings:.2f}"
            })
    
    if candidates:
        st.dataframe(pd.DataFrame(candidates), use_container_width=True)
        
        cols_to_convert = st.multiselect(
            "Select columns to convert to category",
            [c['Column'] for c in candidates]
        )
        
        if cols_to_convert and st.button("Convert to Category", key="convert_category"):
            for col in cols_to_convert:
                data[col] = data[col].astype('category')
            
            st.session_state.cleaned_data = data
            log_cleaning_action(f"Converted {len(cols_to_convert)} columns to category type")
            st.success(f"✅ Converted {len(cols_to_convert)} columns to category")
            st.rerun()
    else:
        st.info("No good candidates for category conversion found")

def validate_data(data):
    """Data validation"""
    st.subheader("Data Validation")
    
    validation_type = st.selectbox(
        "Select validation type:",
        ["Range Validation", "Pattern Matching (Regex)", "Unique Value Constraints", "Cross-Column Validation"]
    )
    
    if validation_type == "Range Validation":
        range_validation(data)
    elif validation_type == "Pattern Matching (Regex)":
        pattern_validation(data)
    elif validation_type == "Unique Value Constraints":
        unique_validation(data)
    else:
        cross_column_validation(data)

def range_validation(data):
    """Validate numeric ranges"""
    st.markdown("#### Range Validation")
    
    numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
    
    if not numeric_cols:
        st.warning("No numeric columns found")
        return
    
    selected_col = st.selectbox("Select column", numeric_cols, key="range_col")
    
    if selected_col:
        col_min = float(data[selected_col].min())
        col_max = float(data[selected_col].max())
        
        st.info(f"Current range: {col_min:.2f} to {col_max:.2f}")
        
        min_val = st.number_input("Minimum allowed value", value=col_min)
        max_val = st.number_input("Maximum allowed value", value=col_max)
        
        # Check violations
        violations = data[(data[selected_col] < min_val) | (data[selected_col] > max_val)]
        
        st.metric("Violations Found", len(violations))
        
        if len(violations) > 0:
            if st.checkbox("Show violations"):
                st.dataframe(violations, use_container_width=True)
            
            action = st.selectbox("Action for violations:", ["Remove Rows", "Clip to Range", "Set to NaN"])
            
            if st.button("Apply Validation", key="apply_range"):
                if action == "Remove Rows":
                    data = data[(data[selected_col] >= min_val) & (data[selected_col] <= max_val)]
                elif action == "Clip to Range":
                    data[selected_col] = data[selected_col].clip(min_val, max_val)
                else:
                    data.loc[(data[selected_col] < min_val) | (data[selected_col] > max_val), selected_col] = np.nan
                
                st.session_state.cleaned_data = data
                log_cleaning_action(f"Range validation on '{selected_col}': {action}")
                st.success(f"✅ Applied {action}")
                st.rerun()

def pattern_validation(data):
    """Validate using regex patterns"""
    st.markdown("#### Pattern Matching (Regex)")
    
    object_cols = data.select_dtypes(include=['object']).columns.tolist()
    
    if not object_cols:
        st.warning("No text columns found")
        return
    
    selected_col = st.selectbox("Select column", object_cols, key="pattern_col")
    
    if selected_col:
        pattern = st.text_input(
            "Enter regex pattern",
            placeholder="e.g., ^[A-Z]{2}\\d{4}$ for format like AB1234",
            help="Use Python regex syntax"
        )
        
        if pattern:
            try:
                matches = data[selected_col].astype(str).str.match(pattern, na=False)
                violations = data[~matches]
                
                st.metric("Violations Found", len(violations))
                
                if len(violations) > 0:
                    if st.checkbox("Show violations"):
                        st.dataframe(violations[[selected_col]], use_container_width=True)
                    
                    if st.button("Remove Invalid Rows", key="apply_pattern"):
                        data = data[matches]
                        st.session_state.cleaned_data = data
                        log_cleaning_action(f"Pattern validation on '{selected_col}': removed {len(violations)} rows")
                        st.success(f"✅ Removed {len(violations)} invalid rows")
                        st.rerun()
                else:
                    st.success("✅ All values match the pattern!")
            
            except Exception as e:
                st.error(f"❌ Invalid regex pattern: {str(e)}")

def unique_validation(data):
    """Validate unique value constraints"""
    st.markdown("#### Unique Value Constraints")
    
    selected_col = st.selectbox("Select column that should be unique", data.columns, key="unique_col")
    
    if selected_col:
        duplicates = data[data.duplicated(subset=[selected_col], keep=False)]
        duplicate_count = len(duplicates)
        
        st.metric("Duplicate Values Found", duplicate_count)
        
        if duplicate_count > 0:
            if st.checkbox("Show duplicates"):
                st.dataframe(duplicates, use_container_width=True)
            
            action = st.selectbox("Action:", ["Keep First", "Keep Last", "Remove All Duplicates"])
            
            if st.button("Apply Constraint", key="apply_unique"):
                if action == "Keep First":
                    data.drop_duplicates(subset=[selected_col], keep='first', inplace=True)
                elif action == "Keep Last":
                    data.drop_duplicates(subset=[selected_col], keep='last', inplace=True)
                else:
                    data = data[~data.duplicated(subset=[selected_col], keep=False)]
                
                st.session_state.cleaned_data = data
                log_cleaning_action(f"Unique constraint on '{selected_col}': {action}")
                st.success(f"✅ Applied {action}")
                st.rerun()
        else:
            st.success("✅ All values are unique!")

def cross_column_validation(data):
    """Cross-column validation"""
    st.markdown("#### Cross-Column Validation")
    
    st.info("Validate relationships between columns (e.g., start_date < end_date)")
    
    numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(numeric_cols) < 2:
        st.warning("Need at least 2 numeric columns for cross-column validation")
        return
    
    col1 = st.selectbox("First column", numeric_cols, key="cross_col1")
    operator = st.selectbox("Operator", ["<", "<=", ">", ">=", "==", "!="])
    col2 = st.selectbox("Second column", numeric_cols, key="cross_col2")
    
    if col1 and col2:
        # Check violations
        if operator == "<":
            violations = data[~(data[col1] < data[col2])]
        elif operator == "<=":
            violations = data[~(data[col1] <= data[col2])]
        elif operator == ">":
            violations = data[~(data[col1] > data[col2])]
        elif operator == ">=":
            violations = data[~(data[col1] >= data[col2])]
        elif operator == "==":
            violations = data[~(data[col1] == data[col2])]
        else:  # !=
            violations = data[~(data[col1] != data[col2])]
        
        st.metric("Violations Found", len(violations))
        
        if len(violations) > 0:
            if st.checkbox("Show violations"):
                st.dataframe(violations[[col1, col2]], use_container_width=True)
            
            if st.button("Remove Violating Rows", key="apply_cross"):
                valid_data = data[~data.index.isin(violations.index)]
                st.session_state.cleaned_data = valid_data
                log_cleaning_action(f"Cross-column validation: {col1} {operator} {col2}, removed {len(violations)} rows")
                st.success(f"✅ Removed {len(violations)} violating rows")
                st.rerun()
        else:
            st.success(f"✅ All rows satisfy: {col1} {operator} {col2}")

def export_and_history(cleaned_data, original_data):
    """Export cleaned data and view cleaning history"""
    st.subheader("Export & History")
    
    # Undo/Redo functionality
    st.markdown("### 🔄 Undo/Redo")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("↩️ Undo (Reset to Original)", key="undo"):
            st.session_state.cleaned_data = original_data.copy()
            st.session_state.cleaning_history = []
            st.success("✅ Reset to original data")
            st.rerun()
    
    with col2:
        st.metric("Cleaning Steps", len(st.session_state.cleaning_history))
    
    with col3:
        original_rows = len(original_data)
        current_rows = len(cleaned_data)
        row_diff = current_rows - original_rows
        st.metric("Row Change", f"{row_diff:+d}")
    
    # Cleaning history log
    st.markdown("### 📋 Cleaning History")
    
    if st.session_state.cleaning_history:
        history_df = pd.DataFrame(st.session_state.cleaning_history)
        st.dataframe(history_df, use_container_width=True)
    else:
        st.info("No cleaning operations performed yet")
    
    st.markdown("---")
    
    # Export section
    st.markdown("### 📥 Export Cleaned Data")
    
    # Summary of changes
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Original Rows", len(original_data))
    with col2:
        st.metric("Cleaned Rows", len(cleaned_data))
    with col3:
        original_memory = original_data.memory_usage(deep=True).sum() / 1024 / 1024
        cleaned_memory = cleaned_data.memory_usage(deep=True).sum() / 1024 / 1024
        st.metric("Memory (MB)", f"{cleaned_memory:.2f}", delta=f"{cleaned_memory - original_memory:.2f}")
    with col4:
        missing_before = original_data.isnull().sum().sum()
        missing_after = cleaned_data.isnull().sum().sum()
        st.metric("Missing Values", missing_after, delta=f"{missing_after - missing_before:+d}")
    
    # Export format selection
    export_format = st.selectbox(
        "Select export format:",
        ["CSV", "Excel (XLSX)", "Parquet", "JSON"]
    )
    
    include_report = st.checkbox("Include cleaning report", value=True)
    
    # Generate download button
    if export_format == "CSV":
        file_data = cleaned_data.to_csv(index=False).encode('utf-8')
        file_name = "cleaned_data.csv"
        mime_type = "text/csv"
    
    elif export_format == "Excel (XLSX)":
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            cleaned_data.to_excel(writer, sheet_name='Cleaned Data', index=False)
            
            if include_report:
                # Add summary sheet
                summary_data = {
                    'Metric': ['Original Rows', 'Cleaned Rows', 'Rows Removed', 'Original Columns', 
                              'Cleaned Columns', 'Missing Values (Before)', 'Missing Values (After)'],
                    'Value': [
                        len(original_data),
                        len(cleaned_data),
                        len(original_data) - len(cleaned_data),
                        len(original_data.columns),
                        len(cleaned_data.columns),
                        original_data.isnull().sum().sum(),
                        cleaned_data.isnull().sum().sum()
                    ]
                }
                pd.DataFrame(summary_data).to_excel(writer, sheet_name='Summary', index=False)
                
                # Add cleaning history
                if st.session_state.cleaning_history:
                    pd.DataFrame(st.session_state.cleaning_history).to_excel(
                        writer, sheet_name='Cleaning History', index=False
                    )
        
        file_data = buffer.getvalue()
        file_name = "cleaned_data.xlsx"
        mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    
    elif export_format == "Parquet":
        buffer = BytesIO()
        cleaned_data.to_parquet(buffer, index=False)
        file_data = buffer.getvalue()
        file_name = "cleaned_data.parquet"
        mime_type = "application/octet-stream"
    
    else:  # JSON
        file_data = cleaned_data.to_json(orient='records', indent=2).encode('utf-8')
        file_name = "cleaned_data.json"
        mime_type = "application/json"
    
    st.download_button(
        label=f"📥 Download {export_format}",
        data=file_data,
        file_name=file_name,
        mime=mime_type,
        use_container_width=True
    )
    
    # Generate cleaning report separately
    if include_report and export_format != "Excel (XLSX)":
        report = generate_cleaning_report(original_data, cleaned_data)
        st.download_button(
            label="📄 Download Cleaning Report (TXT)",
            data=report,
            file_name="cleaning_report.txt",
            mime="text/plain",
            use_container_width=True
        )

def generate_cleaning_report(original_data, cleaned_data):
    """Generate a text cleaning report"""
    report = []
    report.append("=" * 60)
    report.append("DATA CLEANING REPORT")
    report.append("=" * 60)
    report.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    report.append("\n--- SUMMARY ---")
    report.append(f"Original Rows: {len(original_data):,}")
    report.append(f"Cleaned Rows: {len(cleaned_data):,}")
    report.append(f"Rows Removed: {len(original_data) - len(cleaned_data):,}")
    report.append(f"Original Columns: {len(original_data.columns)}")
    report.append(f"Cleaned Columns: {len(cleaned_data.columns)}")
    
    report.append("\n--- MISSING VALUES ---")
    report.append(f"Before: {original_data.isnull().sum().sum():,}")
    report.append(f"After: {cleaned_data.isnull().sum().sum():,}")
    
    report.append("\n--- MEMORY USAGE ---")
    original_memory = original_data.memory_usage(deep=True).sum() / 1024 / 1024
    cleaned_memory = cleaned_data.memory_usage(deep=True).sum() / 1024 / 1024
    report.append(f"Before: {original_memory:.2f} MB")
    report.append(f"After: {cleaned_memory:.2f} MB")
    report.append(f"Savings: {original_memory - cleaned_memory:.2f} MB")
    
    if st.session_state.cleaning_history:
        report.append("\n--- CLEANING OPERATIONS ---")
        for i, action in enumerate(st.session_state.cleaning_history, 1):
            report.append(f"{i}. [{action['Timestamp']}] {action['Action']}")
    
    report.append("\n" + "=" * 60)
    
    return "\n".join(report)

def log_cleaning_action(action):
    """Log a cleaning action to history"""
    st.session_state.cleaning_history.append({
        'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'Action': action
    })