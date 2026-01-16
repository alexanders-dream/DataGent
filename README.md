## Demo

You can demo the app here: [DataGent Demo](https://datagent.streamlit.app)

# DataGent - AI-Powered Data Analysis Assistant

DataGent is an intelligent data analysis application powered by AI models. It provides a user-friendly interface for performing various data analysis tasks on CSV and Excel files, including advanced data cleaning, detailed profiling, visualization, natural language querying, and sentiment analysis.

## Features

### 🧹 Advanced Data Cleaning
- **Missing Values Management**: 
    - Detailed summary of missing data.
    - Strategies: Global fill (mean/median/mode), column-specific methods, forward/backward fill, linear/polynomial interpolation, and threshold-based dropping.
- **Duplicate Handling**: 
    - Detection based on all or specific columns.
    - Options to keep first, last, or remove all duplicates.
- **Outlier Detection & Handling**:
    - Methods: IQR (Interquartile Range) and Z-Score.
    - Interactive visualization of outliers.
    - Handling: Remove, cap at boundaries, log transform, or ignore.
- **Data Type Optimization**:
    - Automatic memory optimization (downcasting numerics, categorizing objects).
    - Manual type conversion and date parsing.
- **Data Validation**:
    - Range validation, regex pattern matching, unique value constraints, and cross-column validation.

### 📊 Data Profiling Dashboard
- **Quality Report**: Comprehensive metrics including missing %, unique values, memory usage, and quality inference.
- **Visual Analysis**: Missing values heatmap, distribution plots (histograms/box plots), and correlation matrices.
- **Detailed Statistics**: Deep dive into specific column statistics (skewness, kurtosis, etc.).

### 🤖 AI-Powered Analysis
- **Interactive Querying**: Ask natural language questions about your data using local (Ollama) or cloud (Groq) LLMs.
- **Automated Insights**: AI generates and answers analytical questions about your dataset automatically.
- **Automated Visualizations**: AI suggests and generates relevant Plotly charts based on your data structure.

### 📈 Data Visualization
- **Interactive Charts**:
    - Histograms, Scatter Plots, Bar Plots, Box Plots.
    - Line Plots, Pie Charts, Heatmaps.
    - Geospatial Maps (scatter mapbox).
- **Customization**: Group/color by specific columns for deeper insights.

### 🔎 Interactive Filtering
- Dynamic filtering widgets for text (multiselect) and numeric (range sliders) columns.

### 🎭 Sentiment Analysis
- **Text Analysis**: VADER-based sentiment scoring (Positive, Negative, Neutral).
- **Visualizations**: Sentiment distribution bars/pies, Word Clouds for each sentiment category.
- **Time Series**: Track sentiment trends over time (if date column exists).

## Configuration

### AI Models
DataGent supports two types of AI models:

1. **Groq (Cloud)**: Fast, high-performance inference.
   - Requires a `GROQ_API_KEY`.
   - Get one at [console.groq.com](https://console.groq.com/keys).
   
2. **LocalLLM (Ollama)**: Privacy-focused, runs locally.
   - Install Ollama from [ollama.com](https://ollama.com/).
   - Pull a model (e.g., `qwen2.5-coder`):
     ```bash
     ollama pull qwen2.5-coder
     ```
   - Start the server: `ollama serve`

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
    - **Data Visualization**: create custom plots.
    - **Data Querying with AI**: Chat with your data or generate auto-insights.
    - **Advanced Querying**: Run pandas query strings.
    - **Interactive Data Filtering**: Slice and dice the data.
    - **Sentiment Analysis**: Analyze text columns.

## Requirements

- Python 3.10+
- Streamlit
- Pandas & PandasAI
- LangChain (Community & Groq)
- Plotly Express
- NLTK & WordCloud
- python-dotenv

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.
