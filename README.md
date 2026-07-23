You can demo the app here: [DataGent Demo](https://datagent.streamlit.app)

# DataGent - AI-Powered Data Analysis Assistant

DataGent is an intelligent data analysis application powered by AI models. It provides a user-friendly Streamlit interface for performing various data analysis tasks on CSV and Excel files, including advanced data cleaning, detailed profiling, visualization, natural language querying, and sentiment analysis.

## Features

### 🧹 Advanced Data Cleaning
A comprehensive, wizard-based data cleaning module with 6 dedicated tabs:
- **Missing Values Management**:
    - Column-Specific Strategy: Apply different fill methods (mean, median, mode, forward/backward fill, linear/polynomial interpolation, custom value, drop rows) per column.
    - Global Strategy: Apply a unified method (mean, median, mode, forward/backward fill, drop rows with any/all missing) across the entire dataset.
    - Threshold-Based Dropping: Drop columns or rows exceeding a configurable percentage of missing values.
- **Duplicate Handling**:
    - Detection based on all or specific columns.
    - Options to keep first, last, or remove all duplicates.
- **Outlier Detection & Handling**:
    - Methods: IQR (Interquartile Range) and Z-Score.
    - Interactive visualization of outliers with adjustable boundaries.
    - Handling: Remove, cap at boundaries, or log transform.
- **Data Type Optimization**:
    - **Auto-Optimize**: Automatic memory optimization (downcasting numerics, categorizing low-cardinality objects).
    - **Manual Type Conversion**: Convert specific columns to any supported pandas dtype.
    - **Parse Dates**: Convert string columns to datetime with optional format specification.
    - **Optimize Categories**: Identify and convert object columns to `category` dtype.
- **Data Validation**:
    - Range validation, regex pattern matching, unique value constraints, and cross-column validation.
- **Export & History**:
    - Export cleaned data in CSV, Excel, Parquet, or JSON formats.
    - Generate detailed cleaning reports.
    - Undo functionality to reset to the original dataset.

### 📊 Data Profiling Dashboard
A dedicated, expandable dashboard providing at-a-glance data quality metrics:
- **Quality Report**: Comprehensive metrics including missing %, unique values, memory usage, and quality inference for each column.
- **Missing Values Heatmap**: Visual representation of missing data patterns across the dataset.
- **Distribution Analysis**: Interactive histograms and box plots for numeric columns, frequency analysis for categorical columns.
- **Correlation Analysis**: Interactive correlation matrices with the ability to filter strong correlations by threshold.
- **Column Statistics**: Deep dive into specific column statistics (count, mean, std, min, max, skewness, kurtosis, etc.).

### 🤖 AI-Powered Analysis (Powered by PandasAI & LangChain)
- **Interactive Querying**: Ask natural language questions about your data using local (Ollama) or cloud (Groq) LLMs.
- **Automated Insights**: AI generates 7 analytical questions about your dataset and answers them automatically.
- **Automated Visualizations**: AI suggests 5 relevant and insightful Plotly charts based on your data structure.

### 📈 Data Visualization
- **Interactive Charts** (powered by Plotly):
    - Histograms, Scatter Plots, Bar Plots, Box Plots.
    - Line Plots, Pie Charts, Heatmaps.
    - Geospatial Maps (scatter mapbox).
- **Customization**: Group/color by specific columns for deeper insights.

### 🔎 Interactive Data Filtering
- Dynamic filtering widgets for text (multiselect) and numeric (range sliders) columns.

### 🎭 Sentiment Analysis
- **Text Analysis**: VADER-based sentiment scoring (Positive, Negative, Neutral).
- **Visualizations**: Sentiment distribution bars/pies, Word Clouds for each sentiment category.
- **Time Series**: Track sentiment trends over time (if a date column exists).

## Architecture & Key Technologies

- **Frontend**: Streamlit
- **Data Analysis**: Pandas, PandasAI
- **LLM Orchestration**: LangChain (with Groq and Ollama integrations)
- **Visualizations**: Plotly (primary), Matplotlib, Seaborn
- **Text Processing**: NLTK, WordCloud

## Configuration

### AI Models
DataGent supports two types of AI providers via a unified LangChain wrapper:

1. **Groq (Cloud)**: Fast, high-performance inference.
   - Requires a `GROQ_API_KEY`.
   - Get one at [console.groq.com](https://console.groq.com/keys).
   - Securely manages your API key through session state.
   - Dynamically fetches available models from the configured API endpoint.
   
2. **Ollama (Local)**: Privacy-focused, runs locally.
   - Install Ollama from [ollama.com](https://ollama.com/).
   - Pull a model (e.g., `qwen2.5-coder`):
     ```bash
     ollama pull qwen2.5-coder
     ```
   - Start the server: `ollama serve`

## Project Structure

```
datagent/
├── main.py                  # Main Streamlit application & LLM configuration
├── data_cleaning.py         # Advanced data cleaning module
├── data_profiling.py        # Data profiling dashboard
├── data_visualization.py    # Interactive chart generation
├── data_querying.py         # AI-powered natural language querying
├── advanced_querying.py     # Pandas query string execution
├── data_filtering.py        # Interactive data filtering
├── sentiment_analysis.py    # VADER-based text sentiment analysis
├── ui_components.py         # Reusable UI components & HTML badges
├── utils.py                 # Utility functions
├── requirements.txt         # Python dependencies
├── .env example             # Example environment variables
└── .streamlit/
    └── config.toml          # Streamlit configuration
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/alexanders-dream/DataGent.git
   cd datagent
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   
4. **Run the application**:
   ```bash
   streamlit run main.py
   ```

## Usage

1. **Start the App**: Run `streamlit run main.py`.
2. **Upload Data**: Use the sidebar to upload a CSV or Excel file.
3. **Configure AI**: Select 'Groq' (enter key) or 'Ollama' (ensure local server is running) in the sidebar.
4. **Explore Tabs**:
    - **Data Cleaning**: Fix issues in your dataset step-by-step.
    - **Data Visualization**: Create custom interactive plots.
    - **Data Querying with AI**: Chat with your data or generate auto-insights.
    - **Advanced Querying**: Run pandas query strings.
    - **Interactive Data Filtering**: Slice and dice the data.
    - **Sentiment Analysis**: Analyze text columns.

## Requirements

- Python 3.10+
- Streamlit
- Pandas & PandasAI
- LangChain (Community, Core, Groq, PandasAI wrapper)
- Plotly Express
- NLTK & WordCloud
- python-dotenv
- openpyxl & xlrd (for Excel support)
- scikit-learn, NumPy, SciPy
- st-paywall
- Pillow
- Matplotlib & Seaborn

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.
